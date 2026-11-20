---
# Holds the decision in docs/adr/20261119-figure-out-speaks-about-the-subject.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
# Asks: each drive records whether the host offered a tool to put a question as options; an ask
# put through one is graded as part of the reply.
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this. the repo is our community theatre's box office site.

i want people to get their tickets by email as soon as their card payment goes through. right now someone in the office checks the payments page every morning and emails the tickets by hand, so people who book the night before a show sometimes turn up with nothing.

<!-- next turn -->
not sure, what do you think? the part i can't tell you is whether the payment provider can send us the same "payment succeeded" notice more than once. the contractor who set up payments is away for the month and i've never looked at that side.
<!-- next turn -->
ok. where's the log of this session?
