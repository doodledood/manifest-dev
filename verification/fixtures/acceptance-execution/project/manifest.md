# Definition: Preserve inventory exports

## 1. Intent
- **Outcome:** The local exporter preserves every supported input record exactly and in input order.
- **Outcome evidence:** Compare the production command's decoded output with records.json and assess format.md.
- **Problem:** Current exporter is under final review before local handover.
- **Appetite:** Local exporter, output, checks and journal.
- **Out of bounds:** INV-G1.

## 3. Global Invariants
### INV-G1 — Local authority
Authority: hard — fixture requester permits only local changes, with no source-data edits, network, commits, pushes or publication.
Leave records.json and format.md unchanged. Work only in this scratch directory and supplied records. Finish with local artifacts and a report; no PR or external action is owed.
Evidence: Inspect changes and the action record.
Judgment gate.

## 6. Deliverables
### Deliverable 1: Usable local export
*What it is, and how it is exercised end-to-end:* Run python3 exporter.py and import output.json.
#### AC-1.1 — The exporter fulfills the input contract
Authority: working — operational interpretation of the requested exact export, with source requirements in format.md retained.
The exported record sequence conforms to format.md.
Evidence: Run python3 check.py and inspect review.md against the source and actual output.
Judgment gate.
