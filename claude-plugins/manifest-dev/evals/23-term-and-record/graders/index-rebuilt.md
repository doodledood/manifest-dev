---
type: regex
target:
  source: file
  path: docs/adr/README.md
pattern: '(?=[\s\S]*\]\(20261024-weekly-cutoff\.md\))(?=[\s\S]*20260301-orders-close-on-a-rolling-cutoff\.md\) *\| *Superseded by[^\n]*20261024-weekly-cutoff)'
---
