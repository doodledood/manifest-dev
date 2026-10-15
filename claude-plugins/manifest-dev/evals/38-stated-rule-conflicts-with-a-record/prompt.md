---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this. the project's context file is ./CLAUDE.md.

the reminder email and the reminder text message have almost the same wording in src/messages/. that's duplication. add a rule so nobody ever duplicates message text again — a check in CI. figure out what it should be and come back with your read. i'm afk.
