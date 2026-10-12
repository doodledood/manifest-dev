---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Scan the gates — the acceptance criteria, invariants, or other checks that must pass — and the
deliverables the spec requires, for a specific threshold the requester never set: a number
(latency, coverage, count, size, time), budget, deadline, required format or naming, required
report or write-up (a runbook, change notes, a release or support note), or approval step. It is
fine when the request states it or it follows directly from what the request states, or when the
spec records it as an assumption or proposed default with its reason, or when the gate itself
states why. Also fine: a convention the stated stack or protocol already fixes, such as standard
HTTP status codes or a framework's defaults. Checks that review the change itself for defects or
quality, including the severity bar they apply, or keep the work within what was asked, are not
thresholds.

FAIL only if you can name a specific threshold that is neither from the request nor recorded.
Otherwise PASS.

The request:

use the define skill for this.

one-line fix in our restaurant app's bill-splitting: when a party splits the tip evenly, we round
each share down to the penny, so a £10.00 tip split three ways charges £3.33 each and the server
loses a penny. change it so the shares add up to the tip exactly (one person pays £3.34). the
function is `split_tip()` in `billing/split.py`. the project's checks are `make test`,
`make lint`, and `make typecheck`.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
