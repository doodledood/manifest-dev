---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this.

we added a nullable `fulfillment_region` column to `orders` last sprint. now it needs backfilling
from the warehouse each order shipped from (`shipments.warehouse_id` -> `warehouses.region`), and
then the reporting queries that currently join through shipments should read the column directly.
about 40M rows.

the backfill gets developed and tested against the shared staging database — other teams' work
lives in there too, so nothing destructive, it has to be safe to re-run, and nothing that locks
the orders table for minutes. and obviously nothing in this work runs against prod; prod rollout
is a separate ticket owned by the dba.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
