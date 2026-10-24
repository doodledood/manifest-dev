---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Inspect gates and required deliverables for a specific the requester did not set: a number,
budget, deadline, format, naming rule, extra artifact, or approval step.

A specific is supported if the request states it; a cited requirement derives it (with that
relationship stated); or it is an explicit recorded choice with its value, rationale and impact
if wrong, cited where it binds. An unexplained "why" or a generic claim of best practice is not
a source. A fixed protocol convention may be cited as its source. Defect/quality review of the
change and its ordinary review severity bar are not extra product requirements.

Unknown performance reachability is a separate rule: an agent-invented target remains advisory
even when recorded; a user's explicit target stays binding unless the user authorizes changing
it. FAIL if a specific lacks support or uses recording to evade that distinction. Otherwise PASS.

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
