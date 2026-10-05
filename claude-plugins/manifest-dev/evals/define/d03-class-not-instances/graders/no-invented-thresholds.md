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

bug: dates show in UTC instead of the account's timezone. customers have reported it on the
invoice PDF, the weekly summary email, and the reports page. accounts have a timezone setting;
it's just not being used in those places.

our date formatting is scattered — some places use a shared formatDate helper, some call the
date library directly, a few templates format dates inline. i'd assume there are more spots
than the three people have complained about.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
