# ADR: Gate criteria and evidence travel with execution

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
A gate can delegate most of its acceptance standard to another skill or reference. Reading only
its name leaves construction uninformed until review. A continued evaluator can also receive
the artifact without the prior findings or assessed state and take another unrestricted look.
The execution log already records gate evidence, but the caller and evaluator need to agree on
what a continuation means.

## Decision
Understanding a gate includes consulting its applicable delegated standards before making the
choices those standards constrain. Construction and evaluation use the same thresholds,
exceptions, and trade-offs. The run still chooses its method and evaluation order. This replaces
the mandatory late advisory sweep in 20260805-ratchet-judgment-gate-reverification; it adds no
mandatory preliminary review or blanket reference load.

The executor maintains the applicability of evidence against its criteria and actual subject,
including relevant local work and external state. Continued evaluations receive the assessed
state, reporting scope, findings, verified repairs, and intervening changes. Judgment evaluations
check outstanding findings and failures introduced or exposed by those changes. Deterministic
checks run in full. A new invocation revalidates evidence instead of discarding its history.
A new standalone review retains its requested scope.

This is a shared caller/evaluator convention under
20261015-do-states-the-goal-and-its-conventions-and-leaves-method-to-the-run. It does not restore
retired verification modes or prescribe reviewer topology. The existing log and PR journal
carry continuity; no separate state store is added.

## Alternatives Considered
- **Run the same full review before formal verification:** can relabel a repair round without
  reducing total work, and does not make criteria available during the choices they constrain.
- **Restart every judgment review on a new invocation:** loses supported dispositions and
  repeatedly samples unchanged material.
- **Trust a prior verdict because the commit is unchanged:** misses changed criteria, local
  edits, and external evidence.

## Consequences

### Positive
- Applicable standards can prevent avoidable repair work during construction.
- Callers and evaluators share the evidence needed for scoped continuation and resumption.

### Negative
- Evidence applicability remains a judgment; a commit identifier alone cannot settle it.
- Whether these instructions reduce repair work remains unmeasured.

## Enforced by
partly — `tests/test_dist_skill_references.py::test_do_log_prompts_preserve_journal_boundaries`
pins the continuation contract. `tests/test_drive_scripts.py` checks the isolated construction,
review, and resumption fixtures through the real runner with a CLI stand-in. The `do` and
`review-code` recipes judge agent behavior; those ask-first scenarios remain unmeasured.

## Source
- [Issue 377](https://github.com/doodledood/manifest-dev/issues/377)
- Amends 20260805-ratchet-judgment-gate-reverification
- Clarifies 20261015-do-states-the-goal-and-its-conventions-and-leaves-method-to-the-run
- Related: 20261024-external-review-feedback-needs-an-adoption-decision
