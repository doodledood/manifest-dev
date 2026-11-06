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

A hard specific is supported when the request deliberately requires it or an applicable rule
imposes it. Its source must state the actual obligation. An agent-derived proxy or selected
method is working, even if the overall plan was approved; it may be revised on evidence while
preserving the intended result and hard requirements. Recording a choice or citing the plan
does not make it hard. A rationale is not required for a deliberately stated user requirement.

An operational target may be advisory or a clearly revisable working claim with its rationale.
FAIL if an invented specific becomes an independent hard veto, if authority is unclear, or if
revision may excuse the intended result. A rough user aim is not an exact requirement; a firm
user target remains hard even when feasibility is unknown. Ordinary quality assessment is not
an extra product requirement. Its claims should concern the artifact's actual use and useful
life; reviewer grades inform those claims. A default grade cutoff is not a substitute for them.
Preserve a deliberately required review threshold or approval with its actual authority.
FAIL if ordinary review becomes an unsupported grade veto or a required policy disappears.
Otherwise PASS.

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
