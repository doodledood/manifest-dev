#!/usr/bin/env bash
set -euo pipefail
mkdir -p gatekeeper/app gatekeeper/tests
cat > gatekeeper/README.md <<'EOF'
# gatekeeper

Opens the barrier at the parking garage exit once a ticket is paid. The payment terminal
publishes `ticket.paid` to the queue; `app/consumer.py` reads it and calls the barrier
controller over HTTP.
EOF
cat > gatekeeper/app/publisher.py <<'EOF'
import time

from app.queue import publish


def on_payment_confirmed(ticket_id: str) -> None:
    # Retries here re-publish the whole event when the broker is slow, which is how
    # the barrier got two open commands for one ticket last month.
    for attempt in range(3):
        try:
            publish("ticket.paid", {"ticket_id": ticket_id})
            return
        except TimeoutError:
            time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"could not publish ticket.paid for {ticket_id}")
EOF
cat > gatekeeper/app/consumer.py <<'EOF'
from app.barrier import open_barrier


def handle(event: dict) -> None:
    open_barrier(event["ticket_id"])
EOF
cat > gatekeeper/app/barrier.py <<'EOF'
import httpx

BARRIER_URL = "http://barrier.local/open"


def open_barrier(ticket_id: str) -> None:
    httpx.post(BARRIER_URL, json={"ticket_id": ticket_id}, timeout=2.0).raise_for_status()
EOF
cat > gatekeeper/app/queue.py <<'EOF'
def publish(topic: str, payload: dict) -> None:
    raise NotImplementedError("wired to the broker in production")
EOF
cat > gatekeeper/tests/test_consumer.py <<'EOF'
def test_placeholder() -> None:
    assert True
EOF
