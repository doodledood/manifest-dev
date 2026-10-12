---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 6
---
use the define skill for this.

our food bank's volunteer app is slow. volunteers tap "check in" when they arrive for a shift and
then wait 6–8 seconds on the older android phones most of them carry before the screen moves on.
it needs to feel instant for them — under a second from tap to the next screen on those phones.

what we've measured: the check-in API answers in about 90 ms. after it answers, the app re-renders
the full shift list for the whole week. production has about 400 shifts live in a week; our test
fixture has 12, which is why nobody saw it in testing.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
