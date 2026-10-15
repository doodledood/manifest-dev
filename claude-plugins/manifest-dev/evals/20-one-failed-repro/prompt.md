---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 3
---
use the figure-out skill with --autonomous for this.

our dental clinic booking service double-books a chair now and then — two patients get the same 10:30 slot with the same hygienist. it happens a few times a month, nearly always on monday mornings when the reminder emails go out and lots of people rebook at once.

what we have:

- booking does `SELECT ... WHERE slot_id = ? AND status = 'free'`, then `UPDATE slots SET status = 'booked'` in a separate statement. no row lock, no unique constraint on (slot_id, status='booked').
- a teammate suspected a race. they ran two booking requests against the same slot from their laptop, against a local database with nothing else running, once. both did not collide — the second got "slot taken". they wrote in the ticket: "race ruled out, not reproducible."
- from production logs for last monday's double-booking:

```
09:02:17.118 req=a91 slot=4471 select free -> 1 row
09:02:17.141 req=c07 slot=4471 select free -> 1 row
09:02:17.158 req=a91 slot=4471 update booked -> 1 row
09:02:17.183 req=c07 slot=4471 update booked -> 1 row
```

- other ideas on the ticket: the admin calendar sync job, and patients double-clicking "confirm".

i'm afk for the next few hours - dont ask me anything, work it out on your own and come back with what you land on, how sure you are, what its based on, and what would change your mind.
