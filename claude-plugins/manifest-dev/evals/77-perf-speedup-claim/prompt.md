---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

sam put a redis cache in front of our `/api/orders/summary` endpoint and says it makes it 3x faster; he wants it on for everyone next week. his numbers: p50 900 ms before, p50 300 ms after. the before run was once, on his laptop, against the staging database snapshot from last november (about 2 million orders). the after run was once, on the perf server ops tuned last month, against a fresh fixture with 5,000 orders. each run fired 200 requests for the same customer id with `hey`, running on the same machine as the api. that's all he recorded. traces show most of a request's time is the call to the pricing service, and on a cache miss the cache doesn't save that call. the endpoint feeds the dashboard's first screen, and most customers open the dashboard once per session. figure out whether we should roll it out. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
