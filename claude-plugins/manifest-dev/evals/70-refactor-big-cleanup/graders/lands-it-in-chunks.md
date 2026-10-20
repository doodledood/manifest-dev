---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Renaming and moving a module that 40 files import, and changing how it reports errors, does not
have to land at once: new names and files can sit beside the old (the old names re-exported or
aliased), importers can move over in batches, and the old forms can be deleted last, each step
merged and run through the nightly sync before the next.

**First, answer in one line:** Does the reply propose landing the change as a sequence of steps that
each leave the code working and can be merged on their own — such as new beside old, migrate
importers in batches, then remove the old — or argue, from the case's facts, why it must land at
once? Quote it.

**Then judge:** PASS if yes. FAIL if the reply splits the work only into pull requests stacked on a
long-lived branch that merge together at the end, or never says how the change reaches the main
branch safely.
