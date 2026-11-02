# Definition: Partial refunds

## 1. Intent
- **Problem:** Support staff cannot refund part of an order; they refund all of it and charge again.
- **Appetite:** One function, `refund(order_id, amount)`, in `orders.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Judgment gate.

## 6. Deliverables

### Deliverable 1: `refund`

*What it is, and how it is exercised end-to-end:* `refund(order_id, amount)` called the way the
support tool calls it, with an order id and a dollar amount.

#### AC-1.1 — A partial refund is recorded and capped at the order's amount

`refund(order_id, amount)` records a row in the `refunds` table holding the order id and the
amount, and raises `ValueError` when the amount is not positive or exceeds the order's amount less
what was already refunded. `test_orders.py` covers each case, and `python3 -m unittest` passes.

Deterministic gate.
