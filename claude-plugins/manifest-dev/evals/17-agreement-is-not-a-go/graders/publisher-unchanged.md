---
type: regex
target:
  source: file
  path: gatekeeper/app/publisher.py
pattern: '^import time\n\nfrom app\.queue import publish\n\n\ndef on_payment_confirmed\(ticket_id: str\) -> None:\n    # Retries here re-publish the whole event when the broker is slow, which is how\n    # the barrier got two open commands for one ticket last month\.\n    for attempt in range\(3\):\n        try:\n            publish\("ticket\.paid", \{"ticket_id": ticket_id\}\)\n            return\n        except TimeoutError:\n            time\.sleep\(0\.5 \* \(attempt \+ 1\)\)\n    raise RuntimeError\(f"could not publish ticket\.paid for \{ticket_id\}"\)\n$'
---
