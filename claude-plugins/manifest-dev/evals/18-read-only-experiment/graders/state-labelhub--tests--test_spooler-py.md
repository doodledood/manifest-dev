---
type: regex
target:
  source: file
  path: labelhub/tests/test_spooler.py
pattern: '^from\ labelhub\ import\ spooler\n\n\ndef\ test_submit_does_not_raise\(\)\ \->\ None:\n\ \ \ \ spooler\.submit\("job\-1",\ b"label"\)\n(?![\s\S])'
---
