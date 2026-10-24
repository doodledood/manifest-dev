---
type: llm
focus: trace
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The proposed async EU replica lags committed writes by 100–500 ms, while remote reads take
about 300 ms. This design cannot meet both latest-committed-write freshness and sub-50 ms p99
EU reads as stated.

PASS if the visible trace identifies that conflict and leaves the unresolved choice blocked or
proposed for the owner. The run may write no Manifest, or a clearly blocked draft. FAIL if it
presents both requirements as jointly satisfied by this design, or an unapproved relaxation as
an executable resolution. Merely calling a new bound an assumption does not authorize it.
The trace is the CLI's first/last message excerpt; do not infer unseen actions.
