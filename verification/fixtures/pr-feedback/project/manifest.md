# Definition: Public order export

## 1. Intent
- **Problem:** The receiver needs order identifiers, totals, and line SKUs without private notes.
- **Appetite:** The export behavior in `contract.md` and its pull request lifecycle.
- **Out of bounds:** Network requests, actual remote mutations, and merge.

## 3. Global Invariants

### INV-G1 — Keep the replay local

Follow the local replay protocol in the project context file. Remote actions remain local
outbound records, and the run does not merge or contact external services.

Judgment gate.

## 6. Deliverables

### Deliverable 1: Public order export

#### AC-1.1 — The export meets its contract

`order_export.py` implements `contract.md`.

Judgment gate.

#### AC-1.2 — The pull request is ready

Activate the check-pr skill on https://github.com/example/review-fixture/pull/1.
It reports the pull request ready. Inspect the supplied current PR snapshot on every evaluation.

Judgment gate.
