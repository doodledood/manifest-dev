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

our public api docs are a mess — about 40 markdown pages under docs/api/, one per endpoint
group, written by different people over four years. make them excellent: every statement
accurate, nothing missing, consistent style throughout.

what we have: an openapi spec generated from the code on every build (that's the source of
truth for endpoints, params, responses). a short style guide in docs/STYLE.md (sentence-case
headings, second person, one example request + response per endpoint). the people who read
these are external developers integrating for the first time.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
