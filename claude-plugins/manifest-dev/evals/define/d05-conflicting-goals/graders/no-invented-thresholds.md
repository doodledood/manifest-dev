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

our account-balance api serves EU customers from us-east and their p99 is ~300ms. we want a
read replica in eu-west so EU p99 for balance reads drops under 50ms. requirement from finance:
a balance read must always reflect the latest committed write — we can't show a stale balance,
not even for a second, because people move money based on it.

writes stay in us-east. the replica would be postgres async streaming replication, typical lag
100–500ms.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
