---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

we want loans to have a status — out, overdue, returned — that shows in `shelfnote overdue` and in the CSV export. the checkout command, a nightly overdue job, and the return command will all need to change it. figure out what this should be so we can hand it to /define. i'm afk.

today an unreturned loan is overdue once its due date has passed. the club is considering a grace period next term, but has not picked one; this change must keep today's behavior.
