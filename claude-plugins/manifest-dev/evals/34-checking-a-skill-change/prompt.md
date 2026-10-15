---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

our `summarize-ticket` skill in skills/summarize-ticket/SKILL.md keeps writing summaries longer than our support agents want. we want it to stay under five lines unless the ticket has more than three separate problems. figure out what the change has to be and how we'd know it worked, so we can hand it to /define. i'm afk.
