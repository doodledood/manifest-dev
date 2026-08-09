# ADR: Gate text changes on the user's say-so, not the run's

## Status
Accepted

## Area
do

## Context

`/do` may amend the manifest when execution shows a manifest statement has gone false — an Architecture that no longer describes the work, a scope boundary the work has outgrown, a Known Assumption the run has settled. That route is sound for statements that do not bind: amending them reopens nothing.

Acceptance Criteria and Global Invariants are different. They are the binding layer, and `/define` — the skill the amendment route invokes — can sharpen or drop a criterion. So a route that reaches gate text lets a run conclude that a gate misdescribes its subject and amend the gate away. That is the executor grading itself, which is the property inline verification exists to remove.

The case is not hypothetical. A verifier can report that a criterion's own steering misdescribes what it is judging and still return PASS, because the criterion as written was satisfied. The observation is real and needs somewhere to go; the question is whether the run may act on it alone.

Bounding the capability was tried first: permit gate amendment only when a verifier sourced the objection, or only when the gate passed. Each bound narrows the hole without closing it — the run is still the party deciding that its own binding text is wrong — and each one adds a gate state that every completion surface then has to recognise.

## Decision

**A run never amends an Acceptance Criterion or Global Invariant on its own reading that the gate misdescribes what it judges** — passing or failing, verifier-sourced or execution-sourced. Gates are the binding layer, and a run that rewrites what binds it has none.

An impeached gate routes to `/escalate`, carrying what the verifier reported or what execution surfaced, and naming the decision being asked for: whether the gate's text changes. `/escalate`'s payload contract otherwise demands the attempts that failed and rejects escalations that show none — a gate that PASSED while impeaching its own criterion has no attempts — so the skill names this route explicitly and says what stands in for them.

**The route terminates on the user's ruling.** Affirming the text as written leaves the existing PASS standing. Amending it changes the gate's verification identity, so the gate returns to the ledger unverified and re-verifies like any other changed gate. Without a stated end, `/do` would resume into a rule keyed on the verifier's report rather than on whether a human had already answered, and re-escalate the same gate indefinitely.

Termination is scoped to match: a PASS whose criterion misdescribes what it judges is not a settled PASS, so an all-PASS ledger does not complete a run holding one. Escalation-pending is already a non-terminal state in every completion contract, so this adds no new state — it routes into one that exists.

## Alternatives Considered

- **Permit gate amendment when a verifier sourced the objection**: treat the verifier's independence as the safeguard — Rejected: the verifier reports; the run still decides what the report means and what the replacement text says. Independence at the reporting step does not make the amendment independent.
- **Permit gate amendment only for a gate that passed**: reason that a passing gate cannot be amended to escape a failure — Rejected: it removes the crudest abuse and leaves the substantive one. A run that finds a gate weaker than intended can still rewrite it, and "passing" is not evidence the criterion was right.
- **Record the impeachment in the Execution Log and complete**: leave the contract alone and note the discrepancy — Rejected: the log records the run deviating from the plan, and this is the plan being wrong. Noting a false contract in a journal completes the run on it.
- **Let `/define` adjudicate on re-invocation**: pass the objection to the encoder and let it decide — Rejected: `/define` invoked by the run is still the run acting. It has no independent view of whether the criterion was right, and it holds the capability to drop it.

## Consequences

### Positive
- The binding layer is genuinely out of the executor's hands. This is the one property gates exist to provide, and it now holds without conditions to reason about.
- Every prior guard was holding the capability in place rather than removing it. Removing it deleted the guards with it, and the downstream problem — which completion surfaces must recognise a new gate state — disappeared rather than needing an answer.
- A real observation still has a route. The run is not asked to ignore evidence that a gate is wrong; it is asked to hand that evidence to the party who can act on it.

### Negative
- An unattended run that meets an impeached gate stops for a human instead of finishing. That is the intended trade: the alternative is finishing against a contract the run rewrote for itself.
- The user carries a decision they did not previously see. The escalation payload is what makes that tractable — it names the discrepancy and the decision, rather than asking the user to re-derive it.

## Source
- Related: [20260726-only-gates-bind-process-guidance-is-advisory](20260726-only-gates-bind-process-guidance-is-advisory.md)
- Related: [20260722-state-verification-sufficiency-not-only-necessity](20260722-state-verification-sufficiency-not-only-necessity.md)
