---
type: llm
focus: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Today the 21-day loan length is passed by hand as a `days` argument through four
functions (cli → scheduler → reminders → format), and two of them also read a global
`LOAN_DAYS`. Using a per-member length means threading a member through all of them.

**First, list** the deliverables in order.

**Then judge:** PASS if the first deliverable is a behavior-preserving restructuring that
makes the change easy (one place that gives a loan's due date, or the member reaching the
code that needs it), pinned by tests, before the deliverable that changes behavior. FAIL
if the plan threads a new parameter through every function inside the behavior change.
