---
tags: [define]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the define skill for this. the project is in ./cardpress and the manifest is ./manifest.md.

[earlier in this conversation]

me: long recipes get cut off at the bottom of the printed card. can we fix it so they continue on a second card?

you: Here is the plan. The pain: a recipe with more than about 14 lines loses its last steps when printed. The plan: when a recipe does not fit, the layout continues it on a second card, with the title repeated and marked "(cont.)". What gets built: a change to the card layout and its tests, nothing else. How it is checked: a 30-line recipe must print across two cards with every line present and in order, and the test suite must pass. The plan is saved at ./manifest.md. Does this match what you want?

---

looks good
