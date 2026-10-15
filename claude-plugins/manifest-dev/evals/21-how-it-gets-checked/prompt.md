---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 3
---
use the figure-out skill with --autonomous for this.

our public library's catalog app lets members reserve a book at their home branch. we want to add "reserve here, pick up at another branch": a member reserves at any branch and chooses where to collect. the book travels on the inter-branch van, which runs twice a week. figure out what this feature has to be so we can hand it to /define next.

what exists today:

- holds table: `member_id, item_id, branch_id, status (waiting | ready | collected | expired), ready_at`.
- when an item is checked in at the hold's branch, status goes to `ready` and the member gets the standard "your hold is ready" email. holds expire 7 days after `ready_at`.
- staff at each branch see a "holds shelf" list of `ready` holds for their branch.
- the van has a paper manifest; nothing in the app knows an item is in transit.
- we have a staging environment with two demo branches and seeded members. no automated tests touch holds today.

i'm afk for the next few hours - dont ask me anything, work it out on your own and come back with what you land on, how sure you are, what its based on, and what would change your mind.
