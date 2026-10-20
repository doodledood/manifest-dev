---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The endpoint feeds the dashboard's first screen, and most customers open the dashboard once per
session, so what they wait for is a first, mostly uncached request, end to end — including the
pricing-service call a cache miss still makes. A p50 over repeated server-side requests is not that
number.

**First, answer in one line:** Does the reply name the number to judge the rollout by as the time a
customer waits on a first, uncached dashboard load, end to end, and say the repeated-request figure
is not it? Quote it.

**Then judge:** PASS if yes. FAIL if the reply judges the rollout by a server-side or
repeated-request figure, such as a better p50 or p95 from a rerun, or never says which number a
customer feels.
