# Definition: Tax-inclusive prices

## 1. Intent
- **Outcome:** The shop shows prices with tax added, as a whole number of cents.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** Staff add sales tax to each price by hand.
- **Appetite:** One function, `add_tax`, in `money.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: `add_tax`

*What it is, and how it is exercised end-to-end:* `add_tax(cents, rate_percent)` called with a
price in cents and a tax rate in percent, as the price display will call it.

#### AC-1.1 — It returns the price with tax, in whole cents

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`add_tax(cents, rate_percent)` in `money.py` returns the price with tax added, as an `int` of
cents rounded half up: `add_tax(999, 8)` is `1079` and `add_tax(1000, 8)` is `1080`.
`test_money.py` has tests for both, and `python3 -m unittest` passes.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
