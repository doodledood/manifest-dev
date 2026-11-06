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
