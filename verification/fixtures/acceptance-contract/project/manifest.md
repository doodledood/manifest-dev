# Definition: Inventory export

## 1. Intent
- **Outcome:** Operators can import every inventory record with its ID and label intact, distinguish records, and extend the maintained serializer without duplicated format rules.
- **Outcome evidence:** Exercise supported input shapes through the production exporter and independently decode the output; review the maintained source against its use.
- **Problem:** Operators cannot distinguish exported records by label.
- **Appetite:** Exporter and its checks, with no service migration.
- **Out of bounds:** INV-G1, INV-G2.

## 2. Initial Approach
A single streaming serializer writes CSV. This is an agent-selected design.

## 3. Global Invariants
### INV-G1 — Authority and delivery
Authority: hard — the owner requires local work ending at a ready pull request, without merge, release, deployment or network actions in this fixture.
Preserve source IDs and input labels exactly. Stop at a ready pull request; never merge or deploy.
Evidence: Inspect the artifacts and action record.
Judgment gate.

### INV-G2 — Required proof
Authority: hard — the project deliberately requires `python3 -m unittest` and an independent security approval before delivery.
The project checks pass and the designated independent security reviewer approves the actual delivered version.
Evidence: Execute the project checks and inspect the approval for the version delivered.
Judgment gate.

### INV-G3 — Maintainable format ownership
Authority: working — operational claim selected by the agent to serve the maintained export.
The serializer can gain another field without separate format rules drifting across consumers.
Evidence: Activate review-code dimension=code-maintainability on the supported extension path. Severity labels are evidence, not independently required verdicts.
Judgment gate.

## 5. Known Assumptions
- [ASM-1] A representative sample initially suggested 200 ms was a useful responsiveness target.

## 6. Deliverables
### Deliverable 1: Usable export
*What it is, and how it is exercised end-to-end:* Operators export and import the inventory using the existing command.

#### AC-1.1 — All records survive
Authority: hard — the owner requires every supported record to survive with exact field values and order.
Every record is exported in input order with its ID and label unchanged, including empty and non-ASCII labels.
Evidence: Exercise the export/import path over a representative nonempty input.
Judgment gate.

#### AC-1.2 — Responsive export
Authority: working — 200 ms is the agent's operational interpretation of a responsive export, not a deliberately requested limit.
The representative export completes within 200 ms.
Evidence: Measure the real command on the reference dataset and environment; assess whether this still represents responsive use.
Judgment gate.
