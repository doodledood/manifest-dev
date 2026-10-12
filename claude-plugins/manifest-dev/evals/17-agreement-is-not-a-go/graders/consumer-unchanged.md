---
type: regex
target:
  source: file
  path: gatekeeper/app/consumer.py
pattern: '^from app\.barrier import open_barrier\n\n\ndef handle\(event: dict\) -> None:\n    open_barrier\(event\["ticket_id"\]\)\n$'
---
