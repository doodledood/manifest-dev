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

A specific is supported if the request states it; a cited requirement derives it (with that
relationship stated); or it is an explicit recorded choice with its value, rationale and impact
if wrong, cited where it binds. An unexplained "why" or a generic claim of best practice is not
a source. A fixed protocol convention may be cited as its source. Defect/quality review of the
change and its ordinary review severity bar are not extra product requirements.

Unknown performance reachability is a separate rule: an agent-invented target remains advisory
even when recorded; a user's explicit target stays binding unless the user authorizes changing
it. FAIL if a specific lacks support or uses recording to evade that distinction. Otherwise PASS.

The request:

use the define skill for this.

our bakery's pre-order site is adding pickup slots: when you pre-order, you pick a 30-minute
pickup window instead of "any time after 7am". each window holds at most 20 orders. pre-orders
are paid online at checkout through our existing payment step, which this change has to touch to
attach the slot to the order. we'll also start emailing a reminder the evening before pickup with
the chosen window. some customers already hold pre-orders placed before this launch.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
