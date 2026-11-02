# Definition: Invoice totals

## 1. Intent
- **Problem:** The shop adds up each invoice by hand from its lines.
- **Appetite:** One function, `invoice_total`, in `invoice.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Judgment gate.

## 6. Deliverables

### Deliverable 1: `invoice_total`

*What it is, and how it is exercised end-to-end:* `invoice_total(lines)` called with a list of
`(quantity, unit_cents)` pairs, as the checkout code will call it.

#### AC-1.1 — It returns the invoice's total in cents

`invoice_total(lines)` in `invoice.py` returns the sum of `line_total` over the lines, in integer
cents, and 0 for no lines. `test_invoice.py` has tests for both, and `python3 -m unittest` passes.

Deterministic gate.
