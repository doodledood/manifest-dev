# ADR: Repairs track the accepted promise across findings and commits

## Status
Accepted

## Area
do

## Decided by
The user, for tracking repairs by the underlying promise; an agent implements the recovery and evaluation wording under that ruling. Merging remains with the maintainer.

## Context
Issue #419 reports repeated failed repairs that were not recognized as sharing a premise. Finding IDs changed, and each repair commit claimed a stronger property. The existing instruction to test a premise after two failed repairs did not identify what survives those changes of identity.

This fits the North Star's purpose of trusted progress without repeated supervision. A run needs enough durable history to recognize one promise being repaired repeatedly, and an acceptance source that does not grow with its repair prose.

## Decision
Track related repairs by the underlying promise they try to satisfy. Keep the promise, its source in the accepted contract, attempted repairs and outcomes in the existing execution log or checkpoint notes. A new finding ID or commit does not reset that history.

After two repairs on the same promise have failed, test its premise against the accepted contract, Appetite and scope before attempting another repair. Determine whether the promise is actually owed and whether a simpler repair meets it. This is a premise test, not a retry cap or permission to stop repairing a substantive defect.

An accepted contract bounds change-intent reconstruction. Repair commits, comments and tests explain implementation; they cannot strengthen acceptance on their own. A binding promise stays intact. A false binding premise uses the existing blocker and amendment boundary rather than an executor weakening the requirement.

This extends the existing finite-batch and continued-review rules. It adds no runtime database, counter, Manifest field or configurable limit; the current execution record already carries the state needed for recovery.

## Alternatives Considered
- **Track only finding IDs:** different examples of one premise can produce new IDs indefinitely.
- **Treat each repair commit as fresh intent:** lets the repair itself raise the acceptance bar without the owner's decision.
- **Stop after a fixed number of rounds:** cannot distinguish an unowed cosmetic promise from an owed correctness repair.
- **Add a separate repair-state service:** duplicates the existing execution log and introduces an ownership boundary this workflow does not need.

## Consequences

### Positive
- Interrupted or continued runs can recover which premise has already failed.
- New edge cases prompt a premise test instead of silently widening acceptance.
- Correctness and safety obligations keep their original bar.

### Negative
- The run must record the promise and its actual source accurately.
- Determining whether two repairs share a promise remains a judgment; the record makes it auditable but does not automate it.

## Enforced by
partly — `tests/test_review_convergence.py::test_repair_history_survives_finding_and_commit_identity_changes` locks the executor, recovery and change-intent handoffs in source and Codex copies. `verification/recipes/do.md` → *promise-convergence* seeds two related failed repairs under different IDs and an independently mislabelled fee defect. The case ran through native GPT-6.1 Sol/xhigh contexts before and after. Both left label normalization alone, fixed the fee error and passed the unchanged check. The after-run log grouped the repairs by their underlying promise and tested it before another repair. This is a conformance result, with no measured uplift on this explicit-contract fixture.

## Source
- The owner's instruction to track repairs by the underlying promise in the work request for [Issue 419](https://github.com/doodledood/manifest-dev/issues/419).
- Extends 20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges.
- Related: 20261105-review-severity-follows-consequence and 20260805-ratchet-judgment-gate-reverification.
