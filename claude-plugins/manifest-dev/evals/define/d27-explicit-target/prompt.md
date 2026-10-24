---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 1
---
use the define skill for this.

our customer CSV export takes about eight seconds for 100,000 rows. the customer contract
requires p95 under two seconds for exports of that size on our current hosting tier. that
number is firm, not a wish. nobody has profiled the exporter yet, so we don't know whether the
current design can reach it. keep the CSV schema unchanged. scope is settled.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec to ./manifest.md in the current directory, not your home directory.
