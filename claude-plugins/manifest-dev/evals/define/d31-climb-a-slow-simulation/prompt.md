---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 1
---
use the define skill for this.

we have a browser traffic simulation, about 40 modules and 30,000 lines of TypeScript, that people watch as it plays: cars merging, braking, queuing at lights. i want an agent to hill-climb how realistic the vehicle motion looks — try a change, keep it if the motion looks more realistic, repeat until changes stop helping. it must keep running at 50 frames per second or better on a mid-range laptop.

judging realism is the slow part. the real check is watching a recorded 10-minute playback at each of the 4 city presets, which takes about two hours a round. we also have a quick headless test that takes 30 seconds: it renders one still frame of one preset and checks car spacing and positions. that quick test has passed versions that looked plainly wrong once they were moving.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec to ./manifest.md in the current directory, not your home directory.
