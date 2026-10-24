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

bug: dates show in UTC instead of the account's timezone. customers have reported it on the
invoice PDF, the weekly summary email, and the reports page. accounts have a timezone setting;
it's just not being used in those places.

our date formatting is scattered — some places use a shared formatDate helper, some call the
date library directly, a few templates format dates inline. i'd assume there are more spots
than the three people have complained about.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
