# Definition: Partial refunds

## 1. Intent
- **Outcome:** Support can record partial refunds without exceeding the unrefunded order amount.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** Support staff cannot refund part of an order; they refund all of it and charge again.
- **Appetite:** One function, `refund(order_id, amount)`, in `orders.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: `refund`

*What it is, and how it is exercised end-to-end:* `refund(order_id, amount)` called the way the
support tool calls it, with an order id and a dollar amount.

#### AC-1.1 — A partial refund is recorded and capped at the order's amount

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`refund(order_id, amount)` records a row in the `refunds` table holding the order id and the
amount, and raises `ValueError` when the amount is not positive or exceeds the order's amount less
what was already refunded. `test_orders.py` covers each case, and `python3 -m unittest` passes.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
