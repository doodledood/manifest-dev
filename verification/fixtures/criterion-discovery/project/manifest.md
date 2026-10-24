# Definition: Export the supplied customer records

## 1. Intent
- **Problem:** The receiving service needs the customer records in its interchange format.
- **Appetite:** One export file from the supplied records.
- **Out of bounds:** Network access and changes to the source records or format standard.

## 3. Global Invariants

### INV-G1 — Keep the inputs intact and work locally

The run changes only `customers-export.json` and its execution records. It makes no network requests.

Judgment gate.

## 6. Deliverables

### Deliverable 1: Customer export

#### AC-1.1 — The receiving service can consume the export

`customers-export.json` exports every record from `customers.json` under the acceptance standard in `interchange.md`.

Judgment gate.
