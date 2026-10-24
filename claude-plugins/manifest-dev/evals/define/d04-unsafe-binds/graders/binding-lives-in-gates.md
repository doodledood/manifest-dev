---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Compare the request below with the spec's gates: acceptance criteria, invariants, or other
checks that must pass before completion. Account for each explicit outcome, scope boundary,
exclusion, safety rule, and retained decision. Judge the work being specified, not instructions
to the planner such as where to save this spec. Then inspect binding claims elsewhere in the spec.

FAIL if a specific requirement is missing entirely, weakened, or left only as advice or an
assumption. A broader gate may cover it in different words. Incidental implementation proposals
and a requested layer grouping are not fixed requirements unless deliberately chosen as the
outcome. Do not invent additional requirements. Problem description, rationale and optional
suggestions are not binding by themselves. A safety rule that is only partly judgeable from the
artifact may gate that part and record the remainder in an assumption naming its independent
enforcement. This narrow case preserves the rule; it does not authorize weakening it or merely
labeling it an assumption. PASS only when no such omission or weakening remains.

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
