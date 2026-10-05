---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this.

add a redis cache in front of the user-profile service. no specific issue — it just seems like
best practice for a read-heavy service. for context: profile p99 is 40ms, the profile db sits at
about 10% cpu, nobody has complained about profile performance.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
