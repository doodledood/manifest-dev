# ADR: `/do` states verification sufficiency, not only necessity

## Status
Accepted

## Context

`/do` drives a Do/Verify Loop: implement Deliverables, then verify every Acceptance Criterion and Global Invariant with an independent verifier execution per gate, repairing FAILs and re-verifying gates whose implementation changed, until every gate holds a fresh PASS. The skill prompt expressed this as a one-directional pressure toward completeness — "all must PASS fresh," "re-verify stale gates," and (in the unattended backstop) "do not accept self-attestation or 'looks done.'" Every line pushed against stopping too early.

None of those lines stated the *other* boundary: that an all-gates-fresh-PASS state is **enough** — a terminal condition at which the executor should stop. That ceiling was left implicit.

Whether an implicit ceiling is safe depends on the executing model. A model with a strong prior toward declaring completion supplies the missing stop on its own, so the prompt's completeness pressure lands as a useful correction and the loop terminates. A model without that prior has nothing to convert the necessity pressure into a stopping point: with the finish line unstated, it keeps re-verifying already-passing gates and re-editing already-satisfied work, and the loop runs far past the point where the artifact is done. The same prompt that correctly counteracts one default bias amplifies the opposite one. This makes loop termination depend on an unstated model property rather than on the contract itself — a portability defect, since the workflow targets multiple agent hosts and models.

A related amplifier lived in the staleness rule. "Implementation changes after a PASS mark affected gates stale" is correct, but read literally it lets any touch — including re-reading or a cosmetic edit — re-stale a passing gate, giving an over-thorough executor a standing pretext to re-open settled work.

## Decision

State verification **sufficiency** explicitly, as the complement to the necessity the prompt already carried. `/do`'s done-condition is framed as an equivalence: a fresh independent verifier PASS on every Acceptance Criterion and Global Invariant is both **necessary and sufficient** for done. The necessity half is retained unchanged (never declare done on self-attestation or a "looks done" judgment in place of verifier output). The sufficiency half is the addition: once every gate holds a fresh PASS the run is complete — call `/done` and stop, do not re-verify a gate whose implementation has not changed since its PASS, and do not keep refining past the gates.

The staleness rule is narrowed in the same edit: only a **substantive** implementation change to a gate's subject re-stales its PASS; re-reading, re-examining, and cosmetic or no-op edits do not. A genuine substantive change still re-stales and still requires re-verification — the rule is tightened, not removed.

This is a bounding of the loop, not a relaxation of it. Verification is unchanged in rigor: still every gate, still independent verifier executions, still a fresh PASS required. The sufficiency statement supplies the ceiling; the host goal-setting / continuation backstop, where present, supplies the floor (keep going until every gate passes). The two meet at exactly all-gates-fresh-PASS, which is why the addition is a no-op for a model that already stops there and the whole fix for one that does not.

## Alternatives Considered

- **A user-facing strictness knob / escape hatch** (a flag or config to loosen verification): rejected. It leaves the root cause — an unstated finish line — in place, shifts a "know when to flip it" burden onto users, cannot help unattended runs where no one flips it, and contradicts the product stance of opinionated workflows that work without tuning. If a run genuinely needs more verification, the correct surface is the Manifest's gates, not a global dial.
- **Relax verification and let the model self-judge whether/how a gate is verified, leaning on the host goal controller to confirm "done"**: rejected. A continuation/goal capability audits *that the verifier protocol ran and produced PASS evidence*; it is not a substitute verifier. Removing the independent per-gate checks leaves it nothing to audit, collapsing back to self-attestation — the process-trust failure that independent-verifier artifact trust exists to prevent. It also does not fix the presenting symptom: a model without a doneness prior, given more discretion, verifies more, not less. The over-runner needs a ceiling, not freedom.
- **A standalone "do not gold-plate / do not exceed the Manifest" rule**: rejected as a separate mechanism. A broad "do no extra" instruction carries an edge risk that an over-corrective model reads it as license to under-deliver on a legitimate gate. Folding "stop once every gate passes" into the sufficiency statement removes the post-completion re-editing at the same choke point without that risk.
- **Per-model conditional prompt text**: rejected as unnecessary complexity. The equivalence framing is portable — a no-op where the ceiling is already supplied by the model and the fix where it is not — so no host- or model-specific branching is needed.

## Consequences

### Positive

- Loop termination is a property of the contract, not of an unstated model trait, so `/do` behaves consistently across hosts and models.
- Verification rigor and independent-verifier artifact trust are fully preserved; the change only bounds when the loop ends.
- No new user-facing surface, flag, or configuration to maintain or document.
- The sufficiency ceiling and the host continuation floor compose cleanly, meeting at a single well-defined completion point.

### Negative

- Slightly more prose in the executor's completion logic; the necessity idea now appears both in the Execution equivalence and in the unattended-launch backstop contract (the latter must stay self-contained for a continuation checker to audit).
- Correct behavior still depends on the executor honoring the stated ceiling; a model that ignores explicit instruction could still over-run. If observed, the fallback is prompt-internal — extend runaway protection, which today trips only on failure-retry loops, to also trip on success-reverification loops — not a user-facing control.

The same shape — relentlessness stated, termination left implicit — plausibly recurs in other convergence loops that push against early stopping (for example figure-out's relentless pressing, and the drive-to-green PR lifecycle loops). The general principle is that any loop calibrated to counter premature stopping needs an explicit terminal condition, since that stop only self-supplies on models that already carry the prior. Those loops are not changed here; this ADR records the principle so the pattern can be applied deliberately rather than rediscovered per skill.

## Source
- Related: See also `20260606-figure-out-process-trust-vs-define-do-artifact-trust`, `20260623-use-host-continuation-as-optional-do-backstop`.
