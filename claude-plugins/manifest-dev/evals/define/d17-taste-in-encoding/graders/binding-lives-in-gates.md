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

our bakery's pre-order site is adding pickup slots: when you pre-order, you pick a 30-minute
pickup window instead of "any time after 7am". each window holds at most 20 orders. pre-orders
are paid online at checkout through our existing payment step, which this change has to touch to
attach the slot to the order. we'll also start emailing a reminder the evening before pickup with
the chosen window. some customers already hold pre-orders placed before this launch.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
