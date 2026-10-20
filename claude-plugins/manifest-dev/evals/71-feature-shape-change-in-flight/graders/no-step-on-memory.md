---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Existing orders need `gift_wrap = false`, and the plan is that someone remembers to run
`backfill_gift_wrap.py` after the deploy. If nobody does, or it runs late, workers meet orders with
no value.

**First, answer in one line:** Does the reply replace the remembered step with something that does
not rely on a person — the deploy or a migration runs the backfill, code reads a missing value as
false so no backfill is needed, or a check fails while rows are unfilled? Quote it.

**Then judge:** PASS if yes. FAIL if the backfill stays a manual step, including one moved onto a
checklist, a runbook or a deploy note.
