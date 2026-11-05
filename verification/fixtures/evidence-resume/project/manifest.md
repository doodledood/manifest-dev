# Definition: Order report

## 1. Intent
- **Outcome:** The receiver gets a correct order report and quantity summary while the original receipt remains intact.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** A receiver needs the supplied orders in its report format.
- **Appetite:** The report, quantity summary and execution records.
- **Out of bounds:** Network requests and changing the source data or receipt.

## 3. Global Invariants

### INV-G1 — Preserve the source and receipt

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

The run preserves `orders.json`, `format.md`, and `receipt.txt` and makes no network requests.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: Order report

#### AC-1.1 — The report matches its data and format

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`report.tsv` contains the data from `orders.json`. The report follows `format.md`.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-1.2 — The original receipt remains intact

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`receipt.txt` contains exactly `RECEIVED A-7` followed by a newline.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-1.3 — The receipt check passes

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Run `python3 -c 'from pathlib import Path; assert Path("receipt.txt").read_text() == "RECEIVED A-7\n"; print("receipt intact")'`. It exits zero.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.4 — The quantity summary matches its input

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`quantity.txt` contains the sum of the quantities in `orders.json` as a decimal integer followed by a newline.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.
