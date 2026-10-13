---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Three places would change a loan's status. The obvious build lets each of them write the
status field directly.

**First, list** the shapes the reply considers and who writes the status in each.

**Then judge:** PASS if the reply sketches the shape before code (types or data shape and
where the status is set), compares at least two structurally different shapes, and settles
on one owner for the status — one module or function the three callers go through, or a
status derived from data rather than stored. FAIL otherwise.
