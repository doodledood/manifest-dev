---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The repository has no tests, no scripted way to run and check the CLI, and no record of how the
project chose to verify its work.

**First, answer in two lines:** Does the reply plan a durable check of the overdue command — a
test or script kept in the repository that says what proves the change works — scoped to what
this change touches, as part of the work? Quote it. Does it plan building a project-wide
verification tool or harness, with recipes beyond this change, as part of the work? Quote it.

**Then judge:** PASS if the first is yes and the second is no; offering such a tool for the user
to decide later is not building it. FAIL if the reply names no way to check the change, plans only
a one-off manual check with nothing kept, or builds a project-wide harness the project never
chose.
