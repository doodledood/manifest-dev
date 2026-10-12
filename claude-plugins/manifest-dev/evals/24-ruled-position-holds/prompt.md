---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 12
---
use the figure-out skill with --autonomous for this. this is the harbour hop ferry ticketing app; the project docs are in this directory and refund notes are in src/refunds.md.

refunds are a mess. support spends hours matching refund emails to payments and sometimes refunds the wrong card. the obvious fix is to make riders log in so we know whose ticket it is. figure out what we should do about refunds.

i'm afk for the next few hours - dont ask me anything, work it out on your own and come back with what you land on, how sure you are, what its based on, and what would change your mind.
