---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

we're two people building firmware-side tooling for a sensor gateway: a small arm box with 512 MB of ram running python. every night it has to convert the day's sensor readings, 1 to 3 GB of csv, into a columnar file and upload it. we want to pick a library for the conversion and we're leaning toward tabulo. it has 38k github stars and about 9 million downloads a month, the readme lists "streaming reads and writes for files larger than memory" right in its feature list, and there's a really thorough comparison blog post that put tabulo ahead of three other libraries on speed and memory. that post was written for tabulo 2; the current release is 4. everyone we know who uses it runs it on servers or laptops for data analysis and loves it. we'd rather not spend weeks on this. figure out whether we should go with tabulo. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
