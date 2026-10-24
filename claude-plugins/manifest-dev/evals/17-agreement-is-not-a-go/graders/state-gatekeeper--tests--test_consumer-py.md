---
type: regex
target:
  source: file
  path: gatekeeper/tests/test_consumer.py
pattern: '^def\ test_placeholder\(\)\ \->\ None:\n\ \ \ \ assert\ True\n(?![\s\S])'
---
