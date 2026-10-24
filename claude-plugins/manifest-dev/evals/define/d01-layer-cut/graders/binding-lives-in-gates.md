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

we're adding saved searches to our internal support admin (django backend, react frontend).
agents run the same ticket searches all day — "open, priority high, tagged billing" — and
retype the filters every time. they want to save a search with a name, see their saved searches
in the sidebar, click one to run it, and delete ones they don't need. saved searches are private
to the agent who made them. we talked it through already, scope is settled — no sharing, no
editing a saved search (delete and re-save is fine), max 50 per agent.

plan it in three deliverables:
1. the SavedSearch model + migration
2. the REST endpoints (create / list / delete)
3. the react sidebar UI

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
