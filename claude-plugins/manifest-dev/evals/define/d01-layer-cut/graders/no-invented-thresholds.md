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
