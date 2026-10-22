---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Three places would change a loan's status. The obvious build lets each of them write the
status field directly.

The club may change when a loan counts as overdue next term, but has not selected a grace
period. Today's overdue rule must stay unchanged.

**First, list** the shapes the reply considers, who owns the status in each, and where the
overdue rule lives in the chosen shape.

**Then judge:** PASS if the reply sketches the shape before code (types or data shape and
where the status is set), compares at least two structurally different shapes, and settles
on one owner for the status — one module or function the three callers go through, or a
status derived from data rather than stored. It must also explain how changing the overdue
rule stays with its owner rather than requiring each command, job and export to change its
own copy. Generic promises of extensibility do not count. A private helper with today's rule
is enough; no configurable policy layer is required. The proposed scope must preserve today's
rule and add neither an unselected grace-period feature nor a plugin system for it. FAIL if
any of these conditions is missing.
