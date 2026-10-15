---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 6
---
use the define skill for this. the project is this repo.

the overdue page should also show how many days each loan is overdue, and sort by that. scope is settled: one new column, sort descending by days overdue, nothing else changes. the repo has a verification harness, scripts/verify. i'm afk, dont ask me anything. write the spec to ./manifest.md in the current directory, not your home directory.
