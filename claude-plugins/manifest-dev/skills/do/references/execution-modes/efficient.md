# Execution Mode: Efficient

Maximizes savings by using a cheaper model for verification and skipping reviewer agents. Accept this only when iteration speed matters more than verification depth.

## Model Routing

- **Criteria-checker**: haiku
- **Quality gate reviewers**: SKIPPED for deliverable-level ACs

**What still runs in efficient mode:**
- All bash/codebase checks (regardless of deliverable level)
- All INV-G* verification (regardless of method) — Global Invariants are constitutional
- Any AC with an explicit `model:` in its verify block — explicit model signals deliberate intent

## Verification Parallelism

Sequential — launch verifiers one at a time within each phase. Minimizes concurrent quota usage.

## Fix-Verify Loops

Max 1 per phase.

## Escalation

Two-stage escalation:

1. **Model upgrade**: When a criterion fails twice at haiku, auto-upgrade that criterion's verifier to inherit (session model) and re-verify. This is automatic — no user involvement.
2. **User escalation**: If the criterion still fails after the model upgrade, escalate to the user via /escalate.

Track total model upgrades across the run. After 3 total upgrades, suggest to the user: "Efficient mode is escalating frequently. Consider switching to balanced."

## Manifest Verification (/define)

Skip the manifest-verifier entirely. Proceed directly to Summary for Approval.
