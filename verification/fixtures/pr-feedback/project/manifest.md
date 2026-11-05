# Definition: Public order export

## 1. Intent
- **Outcome:** The receiver gets order identifiers, totals and line SKUs without private notes, and the local PR replay reaches ready state.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** The receiver needs order identifiers, totals, and line SKUs without private notes.
- **Appetite:** The export behavior in `contract.md` and its pull request lifecycle.
- **Out of bounds:** Network requests, actual remote mutations, and merge.

## 3. Global Invariants

### INV-G1 — Keep the replay local

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Follow the local replay protocol in the project context file. Remote actions remain local
outbound records, and the run does not merge or contact external services.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: Public order export

#### AC-1.1 — The export meets its contract

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`order_export.py` implements `contract.md`.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-1.2 — The pull request is ready

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Activate the check-pr skill on https://github.com/example/review-fixture/pull/1.
It reports the pull request ready. Inspect the supplied current PR snapshot on every evaluation.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.
