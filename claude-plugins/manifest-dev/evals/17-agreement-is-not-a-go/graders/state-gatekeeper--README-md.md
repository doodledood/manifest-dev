---
type: regex
target:
  source: file
  path: gatekeeper/README.md
pattern: '^\#\ gatekeeper\n\nOpens\ the\ barrier\ at\ the\ parking\ garage\ exit\ once\ a\ ticket\ is\ paid\.\ The\ payment\ terminal\npublishes\ `ticket\.paid`\ to\ the\ queue;\ `app/consumer\.py`\ reads\ it\ and\ calls\ the\ barrier\ncontroller\ over\ HTTP\.\n(?![\s\S])'
---
