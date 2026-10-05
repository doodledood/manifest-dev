---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this.

bug: dates show in UTC instead of the account's timezone. customers have reported it on the
invoice PDF, the weekly summary email, and the reports page. accounts have a timezone setting;
it's just not being used in those places.

our date formatting is scattered — some places use a shared formatDate helper, some call the
date library directly, a few templates format dates inline. i'd assume there are more spots
than the three people have complained about.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
