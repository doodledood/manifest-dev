# ADR: `/do`'s verification layer is bookkeeping and a stop condition, not a checking aid

## Status
Accepted

## Area
do

## Context

Current frontier models verify and correct their own work without being told to, and vendor prompting guidance has caught up. Anthropic's Claude Opus 5 pages state that explicit verification instructions — "include a final verification step for any non-trivial task," "use a subagent to verify" — cause over-verification, that removing them "reduces wasted tokens with no loss in quality," and that "the same applies to legacy harness scaffolding that adds separate verification steps." The subagent section adds "do not use subagents to verify or double-check your own work." OpenAI's current guidance runs parallel on prompt leanness, reporting eval gains from leaner system prompts, while explicitly telling authors to keep "hard constraints, approval boundaries, and success criteria."

Read quickly, that is an argument for retiring most of what `/do` does, or for stripping verify blocks out of the Manifest and handing a model the goal alone.

Two distinctions decide it.

**A verification nudge is not a statement of done.** "Double-check your answer" is redundant with trained behaviour and should go. "PASS only if no MEDIUM-or-higher findings from this review dimension over this diff" is task specification. The same Anthropic page that says to delete the first says the model "performs best when given the complete task specification up front and left to run," warns that it "can expand the scope of a task, adding steps that weren't requested," and tells authors to "constrain scope explicitly." A Manifest's Acceptance Criteria and Out of bounds are those two recommendations. An audit of this repository's prompts against the nudge pattern found no instances of it.

**Checking is a capability; ruling that a run is finished is not.** A model handed a goal alone is both the party doing the work and the party deciding it is done. No improvement in self-verification changes that, because it is a question of position rather than skill.

The same page's capability list says the model "coordinates teams of subagents well, with effective writer-verifier patterns," and reaches the do-not-use-subagents-to-verify line through the pointer "For cost-sensitive workloads, cap delegation." The guidance therefore prices the writer-verifier split rather than rejecting it. `docs/CUSTOMER.md` (since absorbed into `NORTH_STAR.md`) names cost optimizers as an audience this project does not serve.

## Decision

Keep the Manifest's verify blocks and `/do`'s verification layer, and record that the layer's value is bookkeeping and a stop condition rather than compensation for a model that cannot check itself.

Four things survive independent of how well a model self-verifies:

- **The gate ledger** — after a repair, which gates went stale and owe fresh evidence, over a run long enough to compact.
- **The completion contract** — fresh PASS evidence on every gate is both necessary and sufficient. The sufficiency half is a stop, not a bar, and a goal-driven run has no equivalent.
- **Threshold discipline** — findings beneath a gate's bar are handed to the user rather than repaired, which bounds exactly the scope expansion the vendor guidance warns about.
- **Escalation routing** — separating a wording problem from a design problem instead of patching a fifth time.

None of those is checking.

Evaluator independence is a separate question and stays run-level policy chosen at `/do` launch, never Manifest content. It is worth most on a Judgment Gate, where a fresh reader is the finding mechanism, and least on a Deterministic Gate, whose evidence is command output that reads the same from either evaluator.

Verification cost — the concern that opened this question — is addressed by the Ratchet and the consolidated default, not by removing verification.

## Alternatives Considered

- **Strip verify blocks from criteria, leaving prose statements of done**: The evaluator receives gate IDs, criterion text, phase, and instructions — not the Manifest's Intent sections. A gate's instructions are the entire specification from where the evaluator stands, which is also why a ceiling invariant restates its own scope rather than repeating itself needlessly. Trimming those blocks to suit a self-evaluating executor additionally writes a verification mode into an artifact meant to run under any of them.
- **Make `self` the default verification mode**: Rejected on recorded evidence. In the run that prompted this ADR, an executor on a current frontier model, self-verifying throughout, did not catch a task-file template that would have emitted Manifests `/do` rejects as invalid, a validator in a neighbouring skill that would have rejected every Manifest `/define` now writes, or a false statement introduced by its own repair of an earlier finding. `self` remains available for cost-sensitive runs.
- **Route independence by gate kind, skipping independent evaluation for Deterministic Gates**: Under the consolidated default there is one evaluator execution per round, so excluding Deterministic Gates from it shortens a briefing rather than saving an execution. The mechanism would cost more than it returns.
- **Replace `/do` with a bare goal against the Manifest**: Verification timing is not the difference — `/do` already implements first and evaluates when the work is done, then repairs and re-checks the delta. What a bare goal removes is the ledger, the stop condition, threshold discipline, and escalation routing.
- **Add a verifier effort selector as the cost lever**: Lower effort holds review accuracy per the same guidance, but the existing verifier-model selector already carries effort, so no separate mechanism is warranted.

## Consequences

### Positive

- A future reader meeting "remove verification instructions" in vendor documentation finds the reasoning already recorded instead of re-opening it from scratch.
- The nudge-versus-done distinction gives a concrete audit test for this repository's prompts against future model guidance: delete lines telling a model to check; keep lines saying what passing means.
- Verification cost stays a tuning question — mode, Ratchet, verifier model and effort — rather than a question of whether to verify at all.

### Negative

- The decision rests on one recorded run, and one that favoured independent evaluation: a change spread across many files where most defects were two statements disagreeing, which is what a fresh reader catches and an author does not. A self-contained change with a strong test suite would test the claim less kindly.
- Vendor guidance is followed selectively, so runs cost more tokens than the leanest configuration those pages describe. That trade matches this project's stated audience, but it is a real cost paid on every run.
- Keeping a bar that a model would clear unaided risks paying for a check twice as models improve. The evidence that would retire it is a bare-goal run whose output passes the gates when evaluated afterwards, and that experiment has not been run.

## Source

- Session: figure-out investigation, 2026-08-06 — current Anthropic and OpenAI prompting guidance read at source, audited against this repository's prompts and the recorded `/do` run of 2026-08-05
- Related: 20260805-ratchet-judgment-gate-reverification, 20260730-consolidated-default-verification-mode, 20260728-move-verification-execution-policy-to-do, 20260722-state-verification-sufficiency-not-only-necessity
