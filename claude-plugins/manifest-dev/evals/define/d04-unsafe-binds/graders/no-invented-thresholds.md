---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The document under review is a work spec. If it is missing or empty, FAIL.

The prompt that produced this spec is reproduced at the end of this rubric. A bar the requester
never set, stated in a check as if they had, makes that check stricter than the work needs.

**First, list every threshold in the gates** — the acceptance criteria, invariants, or other checks
that must pass: every number (latency, coverage, count, size, time), budget, deadline, required
format or naming, required report, and approval or sign-off step. One line each: quote it, then
**FROM THE REQUEST** (the requester stated it or it follows directly from what they stated),
**RECORDED** (not from the request, but the spec records it as an assumption or proposed default
with its reason), or **INVENTED** (neither).

**Then judge:** PASS if no threshold is INVENTED. FAIL if any is, and name it.

A check that reviews the change itself for defects or quality, or that keeps the work within
what was asked, is not a threshold. Skip it.

The request:

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
