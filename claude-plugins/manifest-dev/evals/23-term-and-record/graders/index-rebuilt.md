---
type: regex
target:
  source: file
  path: docs/adr/README.md
pattern: '(?=[\s\S]*\]\((?!20260301-)2026\d{4}-[a-z0-9-]+\.md\))(?=[\s\S]*20260301-orders-close-on-a-rolling-cutoff\.md\) *\| *Superseded by)'
---
