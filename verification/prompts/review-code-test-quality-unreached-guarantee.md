First, in this repository, commit a file `README.md` to the default branch containing:

Invoice worker. Several workers claim pending jobs from the database and email each invoice.

Then create a branch `feature/idempotent-send` and commit a file `sender.py` containing:

def render(job):
    return f"Invoice {job['id']}: ${job['amount']}"


def send_invoice(job, provider, db):
    """Email the invoice for a claimed job, at most once even when the job is sent again.

    A worker can crash after the provider accepts the email and before mark_sent runs. The job
    stays claimed, reclaim_stale returns it to pending, and another worker sends it again. The
    provider drops a repeat of an idempotency key it has already seen, so keying the send on the
    job id keeps the customer to one invoice.
    """
    provider.send(to=job["email"], body=render(job), idempotency_key=f"invoice-{job['id']}")
    db.mark_sent(job["id"])


def reclaim_stale(db, now, timeout_seconds=600):
    for job in db.claimed_before(now - timeout_seconds):
        db.return_to_pending(job["id"])

and a file `test_sender.py` containing:

from sender import reclaim_stale, send_invoice


class FakeProvider:
    def __init__(self):
        self.delivered = []

    def send(self, to, body, idempotency_key):
        self.delivered.append((to, body))


class FakeDb:
    def __init__(self, claimed=None):
        self.sent = set()
        self.pending = set()
        self.claimed = claimed or {}

    def mark_sent(self, job_id):
        self.sent.add(job_id)

    def claimed_before(self, cutoff):
        return [{"id": job_id} for job_id, at in self.claimed.items() if at < cutoff]

    def return_to_pending(self, job_id):
        del self.claimed[job_id]
        self.pending.add(job_id)


def test_send_invoice_delivers_and_marks_sent():
    provider, db = FakeProvider(), FakeDb()
    send_invoice({"id": 7, "email": "a@example.com", "amount": 120}, provider, db)
    assert provider.delivered == [("a@example.com", "Invoice 7: $120")]
    assert db.sent == {7}


def test_reclaim_returns_only_stale_claims():
    db = FakeDb(claimed={1: 0, 2: 950})
    reclaim_stale(db, now=1000)
    assert db.pending == {1}
    assert db.claimed == {2: 950}

Then run /manifest-dev:review-code test-quality on that branch's change against the default branch.
