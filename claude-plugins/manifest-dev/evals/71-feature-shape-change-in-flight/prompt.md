---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

we're adding gift wrap to our online shop. checkout publishes each order as a json message on the `orders` queue and 12 workers consume it. the message gets three new fields: `gift_wrap`, `gift_note`, `wrap_sku`. for a gift order the worker charges the card, including the £3.50 wrap fee, then calls the warehouse api to reserve the item plus a wrap kit. the warehouse api is another team's and drops out for a few minutes most weeks. the worker also renders a temporary pdf gift tag into `/mnt/shared/labels/`, which the packing-station printer picks up; we expect around 800 gift orders a day. checkout deploys on its own; the workers deploy one at a time over about 20 minutes. existing orders need `gift_wrap = false` filled in, so priya says someone has to remember to run `backfill_gift_wrap.py` after the deploy. while we're in there i also want to swap our hand-rolled retry loop for a retry library tom liked, and rename the queue to `order-events` because the old name confuses people. figure out what this change should be so we can hand it to /define next. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
