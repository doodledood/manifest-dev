---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The endpoint feeds the dashboard's first screen, and most customers open the dashboard once per
session, so what they wait for is the first request of a session, end to end — which may miss the
cache, depending on how long entries live, and on a miss still makes the pricing-service call. A
p50 over repeated server-side requests is not that number.

**First, answer in one line:** Does the reply name the number to judge the rollout by as what a
customer waits for on the dashboard's first screen, end to end, on their first load of a session
(which may miss the cache and still makes the pricing call on a miss), and say the repeated-request
p50 is not that number? Quote it.

**Then judge:** PASS if yes. FAIL if the reply judges the rollout by a server-side or
repeated-request figure, such as a better p50 or p95 from a rerun, or never says which number a
customer feels.
