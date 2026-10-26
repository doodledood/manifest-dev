---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 1
---
use the define skill for this.

our payments service calls the card processor from 23 places, and each one has its own
hand-rolled retry loop: different attempt counts, different backoff, and only some send an
idempotency key. three of them have double-charged customers after a timeout this year. the
processor supports idempotency keys on every charge and refund call. our tech lead's estimate:
moving all 23 calls onto one retry path that always sends an idempotency key is two sprints for
the team; adding keys to the three that double-charged is two days. we want the double charges
to stop. coding agents like you do our builds now; i review and merge the prs, and our staging
account with the processor is already set up.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec to ./manifest.md in the current directory, not your home directory.
