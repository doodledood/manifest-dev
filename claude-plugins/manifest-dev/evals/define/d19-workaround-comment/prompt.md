---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the define skill for this. the project is this repo.

`shelfnote return` should accept a loan id as well as a book title (`--loan 42`). scope is settled: add the flag, keep `--book` working. i'm afk, dont ask me anything. write the spec to ./manifest.md in the current directory, not your home directory.
