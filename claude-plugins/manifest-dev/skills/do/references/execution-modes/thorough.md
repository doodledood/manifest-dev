# Execution Mode: Thorough

Full verification depth. No shortcuts — every criterion verified, unlimited fix cycles, full model capability.

## Model Routing

- **Criteria-checker**: inherit (session model)
- **Quality gate reviewers**: inherit — all run

## Verification Parallelism

Launch all verifiers in a single message within each phase. Maximize parallelism for fastest feedback.

## Fix-Verify Loops

Unlimited code-change fix attempts. Keep iterating until all criteria pass or a criterion is genuinely blocking.

**Action-aware fix-cap.** Only code-change fix attempts count toward the cap. Other retry shapes — re-verifying after a wait, retriggering a transient failure, posting a thread reply, pushing a sync update (merge base into branch, update PR description), routing a scope shift through Self-Amendment — are not fix attempts. They're shape-of-progress, not shape-of-fix. The principle: what counts is what changes code in response to the failure.

Per-AC `verify.timeout:` is the wall-clock cap that bounds total time on a criterion regardless of retry shape — see /do SKILL.md "Per-criterion timeout."

## Escalation

No automatic escalation mechanism. Escalate only when a criterion is genuinely blocking after multiple attempts (standard /escalate evidence requirements apply).

## Manifest Verification (/define)

Run the manifest-verifier with the full repeat loop until COMPLETE. On CONTINUE, present questions, update manifest, re-invoke.
