# Definition: Order report

## 1. Intent
- **Problem:** A receiver needs the supplied orders in its report format.
- **Appetite:** The report, quantity summary and execution records.
- **Out of bounds:** Network requests and changing the source data or receipt.

## 3. Global Invariants

### INV-G1 — Preserve the source and receipt

The run preserves `orders.json`, `format.md`, and `receipt.txt` and makes no network requests.

Judgment gate.

## 6. Deliverables

### Deliverable 1: Order report

#### AC-1.1 — The report matches its data and format

`report.tsv` contains the data from `orders.json`. The report follows `format.md`.

Judgment gate.

#### AC-1.2 — The original receipt remains intact

`receipt.txt` contains exactly `RECEIVED A-7` followed by a newline.

Judgment gate.

#### AC-1.3 — The receipt check passes

Run `python3 -c 'from pathlib import Path; assert Path("receipt.txt").read_text() == "RECEIVED A-7\n"; print("receipt intact")'`. It exits zero.

Deterministic gate.

#### AC-1.4 — The quantity summary matches its input

`quantity.txt` contains the sum of the quantities in `orders.json` as a decimal integer followed by a newline.

Judgment gate.
