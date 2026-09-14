---
type: llm
focus: last_message
weight: 1
---
Judge whether the load-bearing claims in the response are tied to the specific artifact that
supports them, rather than asserted flatly.

PASS requires both:
1. At least two distinct claims that carry the conclusion are tied to a named artifact — a quoted
   log line or its timestamp, a specific config key and value, or a named line or call in the code
   (for example `compute_window` being called inside the loop, the 21:05:51Z timestamp, the
   20:45 UTC cron time, or the `matched 0` window bounds).
2. The response distinguishes what it established from the given evidence from what it is
   inferring or assuming — for example flagging that it cannot confirm the database contents, the
   real backoff timing, or what happened on nights it was not shown.

FAIL if the conclusion is stated without reference to which artifact produced it, or if inferences
are presented in the same register as things the evidence directly shows.

This grader is about grounding, not formatting. A response that weaves file and log references
into prose PASSES. A response with a section labelled "Evidence" that lists restated conclusions
without pointing at artifacts FAILS.
