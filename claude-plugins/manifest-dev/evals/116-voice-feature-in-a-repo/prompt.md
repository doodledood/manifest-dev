---
# Holds the decision in docs/adr/20261119-figure-out-speaks-about-the-subject.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
# Asks: the drive offers no tool to put a question as options, so every ask is in prose.
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this. the repo is our climbing gym's class booking app.

when a class is full people just give up and go home. i want to add a waitlist so they can join it and get the spot if someone cancels.

(write any notes or logs you keep into the current directory rather than your home directory)
