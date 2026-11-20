# Definition: Free shipping on large orders

## 1. Intent
- **Outcome:** Customers who order 50 units or more pay no shipping.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** Staff refund the shipping charge by hand on large orders.
- **Appetite:** One function, `order_shipping_cents`, in `shipping.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: `order_shipping_cents`

*What it is, and how it is exercised end-to-end:* `order_shipping_cents(units, grams)` called with
an order's unit count and parcel weight, as checkout will call it.

#### AC-1.1 — Orders of 50 units or more ship free

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`order_shipping_cents(units, grams)` in `shipping.py` returns 0 when `units` is 50 or more, and
`shipping_cents(grams)` otherwise. `test_shipping.py` has tests for 49 and 50 units, and
`python3 -m unittest` passes.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
