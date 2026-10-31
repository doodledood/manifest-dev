# Definition: A monthly spending dashboard

## 1. Intent
- **Problem:** The household reads its spending from a raw `ledger.csv` and cannot see at a glance
  where the month's money went.
- **Appetite:** One script, `dashboard.py`, that writes one static `dashboard.html` from
  `ledger.csv`, and its tests.
- **Out of bounds:** INV-G1.

## 3. Global Invariants

### INV-G1 — The change stops at what this Manifest authorized

Done when the work this run added carries nothing beyond what the Deliverables, Acceptance
Criteria, and Global Invariants required.

Judgment gate.

## 5. Known Assumptions

- [ASM-1] The dashboard's direction was open, so three disposable draft variants were shown to the
  person as one throwaway page with fake data: A, a dense table of every entry; B, a chart of
  spending by category with totals beside it; C, one card per category. The direction waits for
  their reaction | Impact if wrong: the dashboard is rebuilt to another direction.

## 6. Deliverables

### Deliverable 1: The dashboard

*What it is, and how it is exercised end-to-end:* `python3 dashboard.py` run beside `ledger.csv`,
and `dashboard.html` opened in a browser.

#### AC-1.1 — It shows the month's spending in the chosen direction

`python3 dashboard.py` exits 0 and writes `dashboard.html`, which shows every category in
`ledger.csv` with its total, laid out in the direction the person chose from the draft.
`python3 -m unittest` passes.

Judgment gate.
