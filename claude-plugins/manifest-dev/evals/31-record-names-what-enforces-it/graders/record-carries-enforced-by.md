---
type: llm
focus: trace
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The run should have written a decision record for "every write goes through store.py,
which takes a file lock". Look at the files the run wrote under docs/adr/.

**First, quote** the record's section that says what enforces the decision, if any.

**Then judge:** PASS if a new record has an `Enforced by` section that names a check
(for example a test or lint that fails when code writes the file outside store.py), or
says `partly —` or `none —` with a reason. FAIL if no new record exists or it has no such
section.
