---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

A restructure of `compute_total` must leave every total it returns unchanged, and several of its
behaviours are easy to alter by accident when splitting it up: partners get `order.subtotal`
returned untouched (no discounts, tax or rounding); the 4.99 fee is decided on the discounted,
unrounded subtotal and is never taxed; the subtotal is rounded half-down before tax; tax is rounded
half-up; an unknown country pays no tax.

**First, answer in two lines:** Does the reply name specific behaviours that must not change —
at least two concrete ones like those above, not just "behaviour stays the same"? Quote it. Does
it say how preservation will be checked — for example comparing old and new totals over recorded
real orders, or tests pinned to current outputs? Quote it.

**Then judge:** PASS if both are yes. FAIL if the reply says only that behaviour should be
preserved, without naming what must stay the same or how that will be confirmed.
