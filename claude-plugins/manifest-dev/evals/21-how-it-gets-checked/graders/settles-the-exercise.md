---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The read hands a new feature to planning. Before that, it should settle how the feature will be
exercised end to end — for example, a walk-through on the two-branch staging environment from
reserving at one branch to collecting at another, through the item's time in transit — or flag
that this is not yet settled. No automated tests touch holds today.

**First, answer in one line:** Does the reply name a concrete way to exercise the whole flow
(reserve → transit → ready at the pickup branch → collected or expired), or explicitly flag that
how it will be checked is still open? Quote it.

**Then judge:** PASS if yes. FAIL if the reply names its read with no way to check the flow and
no flag that this is missing.
