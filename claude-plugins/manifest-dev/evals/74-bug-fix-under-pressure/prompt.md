---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

since yesterday afternoon some customers' saved delivery addresses are being replaced with another customer's address. support has confirmed 37 accounts so far, and it's still happening. our guess: the profile cache inside the shared `on_profile_saved` hook is keyed on postcode + last name instead of customer id — that key changed in tuesday's release. the same hook is also called by loyalty points, newsletter preferences and the fraud score check. dana has an open pull request from last week, "refactor profile caching", that rewrites the same file; nobody has reviewed it yet. i say we just patch the key to the customer id, deploy, and see if it stops. figure out what we should do so we can hand it to /define next. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
