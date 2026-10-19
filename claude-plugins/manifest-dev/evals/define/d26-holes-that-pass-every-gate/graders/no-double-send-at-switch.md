---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The design replaces one invoice worker with several. The old worker takes a pending job, emails
the invoice, and marks the job `sent`, with no claim and no idempotency key. The new workers claim
jobs and send with the provider's idempotency key set to the job id, so the provider drops a
repeat of a key it has seen.

Trace this path against the spec's gates — every acceptance criterion, invariant, or other check
that must pass before the work counts as done:

1. During the switch, the old worker takes job J and sends the invoice.
2. The old worker is stopped — a deploy, a kill, a crash — before it marks J `sent`.
3. A new worker finds J pending, claims it, and sends it with key = J's id, which the provider has
   never seen, since the old worker sent no key.
4. The customer gets the same invoice twice.

PASS if at least one gate would fail an implementation or rollout that lets this happen: for
example, a gate on how the switch is done (the old worker drained or stopped cleanly before the
new ones start, or jobs the old code may have sent checked before any resend), or a gate that
each invoice is delivered at most once across the switch itself. FAIL if every gate lets it
through, even when the spec names this path, notes it as a risk, or records it as accepted: an
entry that only accepts the path closes nothing.
