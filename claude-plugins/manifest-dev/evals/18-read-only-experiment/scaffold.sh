#!/usr/bin/env bash
set -euo pipefail
mkdir -p labelhub/labelhub labelhub/tests
cat > labelhub/README.md <<'EOF'
# labelhub

Sends shipping labels from the pick stations to the thermal printers on the packing line.
`labelhub/spooler.py` takes jobs from the stations and forwards them to the printer driver.
Run the tests with `python -m pytest`.
EOF
cat > labelhub/labelhub/__init__.py <<'EOF'
EOF
cat > labelhub/labelhub/spooler.py <<'EOF'
import threading
import time

from labelhub.driver import send_to_printer

_pending: dict[str, float] = {}
_lock = threading.Lock()

ACK_TIMEOUT = 1.5


def submit(job_id: str, label: bytes) -> None:
    with _lock:
        _pending[job_id] = time.monotonic()
    worker = threading.Thread(target=_send, args=(job_id, label))
    worker.start()


def _send(job_id: str, label: bytes) -> None:
    acked = send_to_printer(job_id, label, timeout=ACK_TIMEOUT)
    if not acked:
        # The printer did not acknowledge in time: send the label again.
        send_to_printer(job_id, label, timeout=ACK_TIMEOUT)
    with _lock:
        _pending.pop(job_id, None)


def resubmit_stale(now: float) -> list[str]:
    """Called every second by the station loop: re-send jobs pending for too long."""
    stale = []
    with _lock:
        for job_id, started in list(_pending.items()):
            if now - started > 2 * ACK_TIMEOUT:
                stale.append(job_id)
    return stale
EOF
cat > labelhub/labelhub/driver.py <<'EOF'
import random
import time


def send_to_printer(job_id: str, label: bytes, timeout: float) -> bool:
    """Stand-in for the vendor driver. A busy printer acknowledges late but still prints."""
    delay = random.choice([0.2, 0.3, 0.4, 1.8, 2.6])
    time.sleep(min(delay, timeout))
    return delay <= timeout
EOF
cat > labelhub/tests/test_spooler.py <<'EOF'
from labelhub import spooler


def test_submit_does_not_raise() -> None:
    spooler.submit("job-1", b"label")
EOF
