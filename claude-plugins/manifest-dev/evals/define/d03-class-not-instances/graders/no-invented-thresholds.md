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

bug: dates show in UTC instead of the account's timezone. customers have reported it on the
invoice PDF, the weekly summary email, and the reports page. accounts have a timezone setting;
it's just not being used in those places.

our date formatting is scattered — some places use a shared formatDate helper, some call the
date library directly, a few templates format dates inline. i'd assume there are more spots
than the three people have complained about.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
