---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this. the project is this repo; its context file is ./CLAUDE.md.

loans keep getting corrupted when two organizers save at the same time. we decided: every write to data/loans.json goes through src/store.py, and store.py takes a file lock before writing. that's settled. record the decision the way this project records decisions, then come back with your read. i'm afk.
