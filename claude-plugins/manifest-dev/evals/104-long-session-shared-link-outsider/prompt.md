---
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this.

Beacon is a B2B reporting tool: marketing agencies connect their clients' ad accounts and build reports from them. we're closing a tenant-isolation hole: report URLs are /r/<numeric id>, so anyone can walk the ids. help me figure out the engineering: switching to unguessable ids, adding an authorization check on every report route, and the backfill.
<!-- next turn -->
facts you'll want:

- rails monolith, about 120k reports. a pentest found the enumeration last week.
- today a report URL opens for anyone, signed in or not. there is no check at all.
- the agencies' account managers email report links to their clients every week. those clients are mostly not Beacon users.
<!-- next turn -->
the access rule is already decided: from now on every report route requires sign-in plus membership in the report's workspace. a non-member, or anyone signed out, gets our standard 404 page, so we never leak whether a report exists. it ships as one deploy behind no flag, since it's a security fix.

what else engineering-wise?
<!-- next turn -->
that's everything i know, and i'm out of time. name the read now, i'll take it straight to define.
