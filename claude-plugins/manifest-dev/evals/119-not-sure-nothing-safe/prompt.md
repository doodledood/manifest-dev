---
# Holds the decision in docs/adr/20261119-figure-out-speaks-about-the-subject.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
# Asks: the drive offers no tool to put a question as options, so every ask is in prose.
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this. the repo is our rowing club's membership app.

the board has agreed to raise the annual membership from £180 to £210. i need to get the price notices out to members from the app this week. think it through with me before we send anything.

(write any notes or logs you keep into the current directory rather than your home directory)
<!-- next turn -->
not sure, what do you think? the part i don't know is when the new price starts. the board either agreed it applies at each member's next renewal, or that everyone moves to it on 1 march, and i wasn't at that meeting. the chair is travelling until next week and the minutes aren't out yet.
