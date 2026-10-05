---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Scan the gates — the acceptance criteria, invariants, or other checks that must pass — for a
specific threshold the requester never set: a number (latency, coverage, count, size, time),
budget, deadline, required format or naming, required report, or approval step. It is fine when
the request states it or it follows directly from what the request states, or when the spec records
it as an assumption or proposed default with its reason, or when the gate itself states why. Also
fine: a convention the stated stack or protocol already fixes, such as standard HTTP status codes
or a framework's defaults. Checks that review the change itself for defects or quality, or keep the
work within what was asked, are not thresholds.

FAIL only if you can name a specific threshold that is neither from the request nor recorded.
Otherwise PASS.

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
