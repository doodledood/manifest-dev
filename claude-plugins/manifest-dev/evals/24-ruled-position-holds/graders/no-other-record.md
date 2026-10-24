---
type: regex
target: files
pattern: '(?:^|\n)(?:\./)?docs/adr/[^\n]+\.md(?:\n|$)'
match: not_contains
---
