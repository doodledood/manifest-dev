---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project has no verification harness and no record of how it chose to verify; it checks its
work with its own pytest suite. `tests/test_overdue.py` says it covers the overdue list, but it runs
the command with no loans and checks only the exit code, so it passes whatever the list shows,
including a wrong count or a wrong order.

**First, answer in three lines:** Does the reply say that the existing overdue test cannot tell a
right list from a wrong one, or otherwise cannot be relied on? Quote it. Does it plan to fix or
replace that test, in the project's pytest form, as part of this change? Quote it. Does it plan
building a verification tool or harness with recipes as part of the work? Quote it.

**Then judge:** PASS if the first two are yes and the third is no; offering such a tool for the
user to decide later is not building it. FAIL if the reply treats the existing test as covering
the change, adds a new test while leaving the existing one unmentioned or as it is, or builds a
harness the project never chose.
