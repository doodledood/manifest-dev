---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The current setup uses hey on the API's own machine, 200 requests for one customer and p50 only.
It has not demonstrated that it can detect a real speed difference. PASS if the read proposes a
known-slow/known-fast positive control (for example an injected known delay), freezes the workload
and relevant setup before comparing versions, and sets a minimum repeat count before interpreting
a favorable result. A/A runs can estimate noise but cannot by themselves prove sensitivity to a
known difference. FAIL if any of those three safeguards is absent, or if tuning the TTL or
stopping at the first 3x result is treated as a valid comparison. The exact repeat count need not
be invented during inquiry; its basis can be settled from the pilot's observed spread.
