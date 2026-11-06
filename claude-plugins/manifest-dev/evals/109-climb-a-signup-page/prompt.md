---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

i run a small budgeting app and want to hill-climb its landing page so more visitors sign up: an agent tries changes to the page, keeps what works better, and repeats. the page gets about 900 visitors a week and about 3% of them sign up. it also has to stay fast (it loads in about 1.2 s on a phone today) and clear about what the app does and costs, which it is right now. i was going to let an ai rate each version for "how likely would you sign up, 1 to 10" and keep whatever scores higher.

before anything gets built, figure out how this climb should be set up. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
