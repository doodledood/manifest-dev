---
type: llm
focus: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project has no verification harness and no record of how it chose to verify; it checks its
work with its own pytest suite. `tests/test_overdue.py` says it covers the overdue list, but it runs
the command with no loans and checks only the exit code, so it passes whatever the list shows.

**First, list** the Manifest's Deliverables in order. For each, say whether it fixes or replaces
`tests/test_overdue.py` so it fails on a wrong list (loans in the data, a fixed date, the
expected entries and order), and whether it builds a verification tool or harness with recipes.

**Then judge.** PASS if a pytest repair of the overdue test is made by a Deliverable that comes
first or before the one adding the days-overdue display, a gate holds it, and no Deliverable or
gate builds a harness. FAIL if the repair comes after the feature, lives only in an assumption,
note or process guidance, is replaced by a new test that leaves the existing one as it is, or is
absent, or if the Manifest builds a harness the project never chose.
