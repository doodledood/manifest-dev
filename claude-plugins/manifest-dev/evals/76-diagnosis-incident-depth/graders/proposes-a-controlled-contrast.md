---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The evidence is one incident's timeline, with several factors moving at once, and one contrary
observation: staging took the same push without trouble. A small controlled run — pool size 5 in
staging under production-like load, with and without the app's retries, with and without a
lagging replica — would show which factors produce the outage, where reading the timeline cannot.

**First, answer in one line:** Does the reply propose a controlled test or replay — for example,
pool size 5 under production-like load in staging, varying the retries or the replica — to settle
the cause before the write-up states it? Quote it.

**Then judge:** PASS if yes. FAIL if the reply settles the cause from the timeline alone, or
calls the cause uncertain without proposing a test that could separate the factors.
