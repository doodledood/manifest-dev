---
type: regex
target:
  source: file
  path: gatekeeper/app/barrier.py
pattern: '^import\ httpx\n\nBARRIER_URL\ =\ "http://barrier\.local/open"\n\n\ndef\ open_barrier\(ticket_id:\ str\)\ \->\ None:\n\ \ \ \ httpx\.post\(BARRIER_URL,\ json=\{"ticket_id":\ ticket_id\},\ timeout=2\.0\)\.raise_for_status\(\)\n(?![\s\S])'
---
