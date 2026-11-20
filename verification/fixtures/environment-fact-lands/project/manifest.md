# Definition: Low-stock report

## 1. Intent
- **Outcome:** The warehouse sees which items are low on stock, from the report command.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** Staff scan the full stock list by eye to find items running low.
- **Appetite:** One subcommand, `low`, in `report.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

### INV-G2 — The project's checks pass

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`./check.sh` passes.

Evidence: Run `./check.sh`.

Deterministic gate.

## 6. Deliverables

### Deliverable 1: `report.py low`

*What it is, and how it is exercised end-to-end:* `python3 report.py low <threshold>` run by hand
from the project directory, as warehouse staff will run it.

#### AC-1.1 — It lists the items below the threshold

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Run by hand from the project directory after `./check.sh`, `python3 report.py low 5` prints one
line `<name>: <qty>` for each item whose quantity is below 5, sorted by name, and nothing else.
`test_report.py` has a test for it.

Evidence: Run `./check.sh`, then run `python3 report.py low 5` by hand and read its output.

Judgment gate.
