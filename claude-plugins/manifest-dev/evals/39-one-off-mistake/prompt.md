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

me: the README says the default loan length is 14 days but it's 21.

you: Right — `src/shelfnote.py` uses 21. I'll fix the README.

---

thanks. should we add a rule or check so this never happens again? keep it short.
