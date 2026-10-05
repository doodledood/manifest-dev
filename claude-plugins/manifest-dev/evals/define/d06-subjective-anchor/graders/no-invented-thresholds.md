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

the empty state of our analytics dashboard (what a new workspace sees before any data comes in)
feels dead — grey box, "no data", nothing to do. redesign it so it doesn't. i like how linear's
empty inbox feels: calm, one small illustration, one clear thing to do next. for us the one
thing is "connect a data source". dana from design signs off on visual changes; if dana and i
disagree, dana's call.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
