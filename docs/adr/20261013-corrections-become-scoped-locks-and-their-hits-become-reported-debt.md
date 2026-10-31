# ADR: A correction becomes a scoped lock where one exists, and the lock's hits across the repository are reported as debt

## Status
Accepted; narrowed by 20261031-do-takes-a-reaction-to-a-draft-as-direction-not-a-lock: a reaction to a disposable draft is not a correction; only what it shows reaches past the draft is locked

## Area
do

## Decided by
The user

## Context
A rule that lives only in prose depends on every contributor reading it. In one sampled codebase, a context file banned a cast pattern that still appeared several hundred times. A correction made once is repeated by the next agent, which copies what exists.

A study of about 700 review comments from one production codebase asked, for each correction, which check would have made the first version right. A reusable check existed for a minority, roughly 10% to 25%. Those clustered in type holes, contract mismatches between registries, concurrency primitives, and routing through a single entry point. Run across the repository, the candidate checks ranged from no noise to mostly noise. The noise came from immutable artifacts such as applied migrations, from test code, and from conventions the codebase did not actually follow. Several owner-stated rules had drifted from current practice or contradicted a recorded decision.

## Decision
- When do repairs a finding or receives a correction, it asks which check, type, or structure would have made the first version right. It prefers the strongest rung: a type or structure; a lint or architecture test; an invariant test; one owning site with a comment. Prose alone counts as no lock.
- Install a lock when the class fits in one sentence that does not name this case, the lock fails on the original mistake, and it checks structure rather than a count. An invariant the owner states may be locked on its first occurrence. An observed mistake needs a class. "One-off: <why>" is a valid outcome.
- Every lock declares its scope — for example production code only, a date cutoff, generated code excluded — or fails only when a change adds more. Noisy repository-wide hits mean the scope or the rule is wrong; they are not debt.
- Before locking a stated intent, check it against recorded decisions and current practice. A conflict is raised, not locked.
- The lock runs across the repository. Whether to fix its hits is the run's judgment within scope. Hits left unfixed, and structural refactors that no lock can create, join the below-threshold findings and pre-existing issues that done and escalate already report, with the offer to ticket them.
- A lock local to the fix ships with the fix. A repository-wide cleanup is reported, not folded into the fix.
- A new suppression of a lock carries its reason on the suppressing line and is reported as debt, so locks cannot wear away unnoticed. It needs no human approval to land; the user can leave the debt as it is.

## Alternatives Considered
- **Prose rules in context files**: they go unenforced.
- **Require recurrence evidence for every lock**: it blocks invariants the owner states.
- **Report every hit as debt without a scope**: the report floods and stops being read.
- **Fix every hit in the same change**: it bundles unrelated work into the fix.

## Consequences

### Positive
- A recurring class stops recurring, for every contributor, with or without this workflow.
- Remaining debt is visible at the end of a run, where the user decides what to do with it.

### Negative
- Scope is a judgment, and a wrong scope produces noise.
- A lock can freeze a drifted rule if the check against recorded decisions is skipped.
- No eval suite measures this yet, because it happens during execution.

## Enforced by
partly — eval cases `37-correction-becomes-a-lock`, `38-stated-rule-conflicts-with-a-record`, and `39-one-off-mistake` measure it once run; the harvest itself is judgment in the executor.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions; aggregate figures only.
- Related: 20260926-defect-remediation-requires-justified-prevention
