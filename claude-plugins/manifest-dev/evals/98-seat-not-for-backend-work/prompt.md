---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this. i'm afk, dont ask me anything.

our nightly job that rebuilds the product search index went from about 20 minutes to just over 3 hours last week. nothing a customer sees has changed — search results are the same, the job just runs much longer and now overlaps the morning traffic. what changed that week: we moved the job from postgres driver psycopg2 to psycopg 3, raised the batch size from 500 to 5,000 rows, and the database got a minor version upgrade (15.4 to 15.6). the job reads products in batches with a server-side cursor, builds documents, and bulk-writes them to the search cluster. the job's log shows each batch now takes about 40 seconds where it took about 6. figure out why, and what we should do.
