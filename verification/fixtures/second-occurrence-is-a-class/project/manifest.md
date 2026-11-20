# Definition: Customer export

## 1. Intent
- **Outcome:** The office can export the customer list to a text file for the mailing house.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** Staff copy customer names into the mailing house's file by hand.
- **Appetite:** One function, `export_customers`, in `exporter.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: `export_customers`

*What it is, and how it is exercised end-to-end:* `export_customers(names, path)` called with a list
of names and a file path, as the office tool will call it.

#### AC-1.1 — It writes one name per line, accents included

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`export_customers(names, path)` in `exporter.py` writes each name on its own line, as UTF-8, so
that "Zoë" round-trips. `test_exporter.py` has a test for it, and `./check.sh` passes.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
