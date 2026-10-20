---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

`compute_total` prices every order for checkout and finance's invoice export, and has no tests.
Restructuring it into smaller functions with nothing pinning today's outputs leaves no way to tell
whether a total moved. The paths needing cover are distinct: partner orders, wholesale, lines of
10 or more, subtotals under 50 (the 4.99 fee), each country and an unknown one, and half-cent
subtotals.

**First, answer in one line:** Does the reply propose, before any restructuring, tests that record
what the current code returns — for example running today's function over real or generated orders
covering those paths and asserting its exact totals — as a step that comes first? Quote it.

**Then judge:** PASS if yes. FAIL if the reply goes straight to the restructured code, adds tests
only for the new functions afterwards, or writes tests asserting what the totals should be rather
than what the current code returns.
