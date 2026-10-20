---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

our billing-sync module is about 6,000 lines across four files, written in 2019, and everyone hates touching it. it runs the nightly sync of invoices to our accounting system, and about 40 other files in the codebase import from it. it has a test suite that passes, roughly 70% line coverage. the plan for this sprint (two weeks) is a big cleanup in one pull request: rename everything to our new naming scheme, move it into maybe 15 files by concern, switch it from returning error codes to raising exceptions like the rest of the codebase does, and generally make it nicer while we're in there. dana is the only person who knows it well enough to review it, and she's on call this sprint. we've been putting this off for a year so i want to finally get it over with. figure out how we should go about it so we can hand it to /define next. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
