---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

we run video transcoding for customer uploads on our own redis + celery setup and we're tired of babysitting it. we're looking at a hosted job queue called runwell to replace it. our load: about 40k jobs a day, each job runs 2 to 20 minutes, and when a customer bulk-uploads we get bursts of around 5k jobs at once. what we have so far: runwell's benchmark page shows 1 million jobs a minute at 10 ms dispatch latency. their site has three customer stories (a fintech, a photo-sharing app, a logistics company) all saying they cut queue ops work to near zero. their sales engineer told us on a call that long-running jobs are no problem, that retries and timeouts are handled automatically, and that bursts "just scale". pricing is per job plus an annual commit, and the commit discount ends this month. someone i know at another company mentioned their team tried runwell last year and went back to running their own, didn't say why. figure out whether we should sign. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
