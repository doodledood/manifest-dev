---
type: regex
target:
  source: file
  path: docs/adr/20260301-orders-close-on-a-rolling-cutoff.md
pattern: '^\#\ ADR:\ Orders\ close\ on\ a\ rolling\ cutoff\n\n## Status\s+Superseded by[^\n]*20261024\-weekly\-cutoff[^\n]*\n\n\#\#\ Area\nOrdering\n\n\#\#\ Decided\ by\nThe\ user\n\n\#\#\ Context\nMembers\ asked\ for\ as\ much\ time\ as\ possible\ to\ change\ their\ box\.\n\n\#\#\ Decision\nEach\ member\ can\ change\ their\ box\ until\ 48\ hours\ before\ their\ own\ collection\ slot\.\n\n\#\#\ Alternatives\ Considered\n\-\ \*\*One\ weekly\ cutoff\ for\ everyone\*\*:\ simpler\ for\ packers\ —\ not\ chosen,\ members\ wanted\ flexibility\.\n\n\#\#\ Consequences\n\#\#\#\ Positive\n\-\ Members\ get\ the\ longest\ possible\ window\.\n\#\#\#\ Negative\n\-\ Packers\ never\ know\ the\ final\ count\ until\ the\ last\ slot\ closes\.\n\n\#\#\ Source\n\-\ Session:\ planning\ meeting\ notes\.\n(?![\s\S])'
---
