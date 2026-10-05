---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this.

our account-balance api serves EU customers from us-east and their p99 is ~300ms. we want a
read replica in eu-west so EU p99 for balance reads drops under 50ms. requirement from finance:
a balance read must always reflect the latest committed write — we can't show a stale balance,
not even for a second, because people move money based on it.

writes stay in us-east. the replica would be postgres async streaming replication, typical lag
100–500ms.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
