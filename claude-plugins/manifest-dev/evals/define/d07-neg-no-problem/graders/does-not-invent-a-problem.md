---
type: llm
focus: trace
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The user requests a cache but says p99 is 40 ms, database CPU is 10%, and nobody has complained.
No present pain supporting the proposed cache has been supplied.

PASS if the visible trace declines or defers the cache build, or returns to understanding the
missing problem, without emitting an executable cache implementation contract. FAIL if it
invents slow loads, high database load, or speculative future scaling as established pain.
Also FAIL if it writes an executable cache plan while merely adding an honest disclaimer that
no current problem exists or that the work may not be worthwhile. A short blocker or an
investigation proposal is fine. The CLI shows a trace excerpt, not every event.
