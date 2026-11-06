# Definition: Export the supplied customer records

## 1. Intent
- **Outcome:** The receiver can consume every supplied customer record in its interchange format.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** The receiving service needs the customer records in its interchange format.
- **Appetite:** One export file from the supplied records.
- **Out of bounds:** Network access and changes to the source records or format standard.

## 3. Global Invariants

### INV-G1 — Keep the inputs intact and work locally

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

The run changes only `customers-export.json` and its execution records. It makes no network requests.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: Customer export

#### AC-1.1 — The receiving service can consume the export

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`customers-export.json` exports every record from `customers.json` under the acceptance standard in `interchange.md`.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.
