---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 3
---
use the figure-out skill with --autonomous for this.

we want a `shelfnote remind` command that emails every member with an overdue loan a short reminder. plan is a new `reminders.py` with a ReminderService class — get_overdue(), compose(), send() — that the command calls, so the logic has a home. figure out what this should be so we can hand it to /define. i'm afk.
