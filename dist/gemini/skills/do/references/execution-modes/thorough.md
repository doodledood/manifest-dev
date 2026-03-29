# Execution Mode: Thorough

Full verification depth. No shortcuts — every criterion verified, unlimited fix cycles, full model capability.

## Model Routing

- **Criteria-checker**: inherit (session model)
- **Quality gate reviewers**: inherit — all run

## Verification Parallelism

Launch all verifiers in a single message within each phase. Maximize parallelism for fastest feedback.

## Fix-Verify Loops

Unlimited. Keep iterating until all criteria pass or you need to escalate a specific blocker.

## Escalation

No automatic escalation mechanism. Escalate only when a criterion is genuinely blocking after multiple attempts (standard /escalate evidence requirements apply).

## Manifest Verification (/define)

Run the manifest-verifier with the full repeat loop until COMPLETE. On CONTINUE, present questions, update manifest, re-invoke.
