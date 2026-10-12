---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 6
---
use the define skill for this.

our pottery studio's kiln log gets a firing summary: after each firing, members see the peak
temperature, total firing time, how long it held at peak, and the cooling rate, on the firing's
page. the numbers come from the kiln controller's sensor readings, one every 30 seconds, which we
already store.

things we know about the data: some firings have gaps where the controller lost wifi for a few
minutes. some firings were aborted partway. a few have zero readings because the controller was
unplugged.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
