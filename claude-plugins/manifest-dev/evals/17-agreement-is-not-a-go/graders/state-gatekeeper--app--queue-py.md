---
type: regex
target:
  source: file
  path: gatekeeper/app/queue.py
pattern: '^def\ publish\(topic:\ str,\ payload:\ dict\)\ \->\ None:\n\ \ \ \ raise\ NotImplementedError\("wired\ to\ the\ broker\ in\ production"\)\n(?![\s\S])'
---
