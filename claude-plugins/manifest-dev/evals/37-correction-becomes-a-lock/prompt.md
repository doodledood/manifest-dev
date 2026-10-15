---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this. the project is this repo.

[earlier in this conversation]

me: the overdue count is wrong for members with two cards — their loans show up twice.

you: Found it: `src/report.py` builds the list per card and concatenates, so a loan reachable from both cards is counted twice. Fix: collect loans into one set keyed by loan id before counting.

---

right, and that's the rule everywhere: a loan is counted once, however many ways you can reach it. how do we make sure nobody breaks that again? keep it short.
