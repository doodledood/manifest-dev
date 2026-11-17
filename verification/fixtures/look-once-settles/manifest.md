# Definition: Low-stock report

## 1. Intent
- **Outcome:** The shop owner runs `low_stock(items, threshold)` on the shelf list and gets the
  names of the items to reorder, sorted by name, including items whose quantity was never recorded.
- **Outcome evidence:** Read the function and its tests against this Outcome.
- **Problem:** The owner reorders by reading the whole shelf list by eye and misses items.
- **Appetite:** One small function and its tests.
- **Out of bounds:** none.

## 2. Initial Approach
- **Architecture:** One pure function in `inventory.py`, unit tests in `test_inventory.py`.

## 3. Global Invariants

### INV-G1 — The change stops at what this Manifest authorized

Authority: hard — the assignment authorizes only work serving the requested Outcome within
its stated scope and applicable instructions.

Done when the work this run added carries nothing beyond what the Outcome, Deliverables and the
other gates required. FAIL only on work none of them accounts for.

Evidence: Inspect the change against this Manifest.

Judgment gate.

### INV-G2 — The tests pass

Authority: hard — the project's only check.

`python3 -m unittest -q` passes.

Evidence: Run it on the final state.

Deterministic gate.

### INV-G3 — The tests are worth keeping

Authority: working — the coding task guidance's test-quality claim, applied to `test_inventory.py`.

Each test distinguishes the required behavior from a plausible wrong result, with expected values
taken from the Outcome rather than from the code under test.

Evidence: Look once. One full look by `review-code` dimensions `test-quality` and
`code-maintainability` on `test_inventory.py`, once every Deliverable is done. Fix each finding
that shows the claim false or reject it with a reason in the execution log. Each repair gets a
check: where the finding names a behavior, a test that fails without the repair and passes with
it; otherwise a read against its finding. That full look and those checks are this gate's
evidence for the finished change; no further review run is owed. A repair that changes product
behavior is seen by AC-1.1.

Judgment gate.

## 4. Process Guidance
- [PG-1] Description: Keep the function pure.

## 5. Known Assumptions
- [ASM-1] An item without a `qty` key counts as quantity 0 | Default: 0 | Impact if wrong: such items are reported for reorder.

## 6. Deliverables

### Deliverable 1: The low-stock report

*What it is, and how it is exercised end-to-end:* the function, called on a shelf list with mixed
items, including one with no recorded quantity.

#### AC-1.1 — The report lists the right items in the right order

Authority: hard — the owner's request in the Outcome.

`low_stock(items, threshold)` returns exactly the names of items whose quantity is below the
threshold, sorted by name; an item without a `qty` key counts as quantity 0 and never makes the
call raise.

Evidence: Look again. First full look: `review-code` dimensions `change-intent` and `code-bugs` on
`inventory.py` with this claim. After each repair batch, a continued look by `code-bugs` reports
outstanding findings and failures the batch introduced. This Manifest names no later review, so
after repairs settle, one fresh full look by `code-bugs` at the finished change; its findings get
fixes and repair checks, and no further fresh look follows.

Judgment gate.
