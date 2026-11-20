---
# Holds the decision in docs/adr/20261119-figure-out-speaks-about-the-subject.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
# Asks: the drive offers no tool to put a question as options, so every ask is in prose.
tags: [figure-out]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write]
model: opus
runs: 1
---
use the figure-out skill for this.

we're a team of nine split across lisbon, new york and singapore. the daily standup is a 25 minute video call at 9am new york time, which is 9pm in singapore, so our two people there either join from home at night or skip it. i want to replace it with a written update everyone posts in slack before their own 10am, and keep one live call a week. help me think this plan through before i announce it on monday.

(write any notes or logs you keep into the current directory rather than your home directory)
