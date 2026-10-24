---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The user explicitly requires p95 under two seconds for 100,000-row exports on the current
hosting tier, and an unchanged CSV schema. Reachability is unknown; the user did not authorize
relaxing the contract.

PASS only if both requirements remain binding, and the spec records that reachability has not
yet been established. A profiling or feasibility step may come first. FAIL if the two-second
requirement becomes an advisory aim, "faster than baseline", a different percentile or workload,
or a promise to report whatever speed is possible. Recording such a relaxation as an assumption
does not authorize it. The unchanged schema must also be checked, not merely mentioned.
