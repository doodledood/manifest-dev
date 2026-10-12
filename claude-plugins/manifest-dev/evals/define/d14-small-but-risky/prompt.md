---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 6
---
use the define skill for this.

one-line fix in our restaurant app's bill-splitting: when a party splits the tip evenly, we round
each share down to the penny, so a £10.00 tip split three ways charges £3.33 each and the server
loses a penny. change it so the shares add up to the tip exactly (one person pays £3.34). the
function is `split_tip()` in `billing/split.py`. the project's checks are `make test`,
`make lint`, and `make typecheck`.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
