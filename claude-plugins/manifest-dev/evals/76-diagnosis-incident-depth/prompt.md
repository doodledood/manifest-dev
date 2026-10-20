---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

our payments API had a 40-minute outage yesterday afternoon. a config push dropped the database connection pool size from 50 to 5, requests started timing out, we rolled the config back and everything recovered — so it's fixed, and now i have to write the "what caused it" section of the incident report for friday's review. what else i know: the same config push went to staging on tuesday and nothing broke there. the API's error rate had been creeping up for about a week before the outage, from 0.2% to 0.9%, and nobody had looked at it. once the first timeouts hit, the mobile app started retrying and request volume roughly tripled within five minutes. the read replica that's meant to take load when the primary is saturated was itself 8 minutes behind, so it never took over. help me get that section right. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
