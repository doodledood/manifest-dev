# Execution Mode: Thorough

Full verification depth. No shortcuts — every criterion verified, unlimited fix cycles, full model capability.

## Model Routing

- **Criteria-checker**: inherit (session model)
- **Quality gate reviewers**: inherit — all run

## Verification Parallelism

Launch all verifiers in a single message within each phase. Maximize parallelism for fastest feedback.

## Fix-Verify Loops

Unlimited fix-code attempts. Keep iterating until all criteria pass or you need to escalate a specific blocker.

**Action-aware fix-cap.** The fix-verify counter only increments on `fix-code` actions dispatched from a verifier hint (see /do SKILL.md "Hint Dispatch"). The other action labels are explicitly non-counting:

- `sleep` — non-counting (a wait, not a fix attempt)
- `retrigger-ci` — non-counting (re-runs CI without modifying code)
- `reply-thread` — non-counting (posts a reply, no code change)
- `push-update` — non-counting (sync-shaped action: merge base, update description, push a re-format)
- `amend-manifest` — non-counting (routes through Self-Amendment; the amended manifest's ACs start their own fresh fix-loop)

Per-AC `verify.timeout:` is the wall-clock cap that bounds total time on a criterion regardless of action mix — see /do SKILL.md "Per-criterion timeout."

## Escalation

No automatic escalation mechanism. Escalate only when a criterion is genuinely blocking after multiple attempts (standard /escalate evidence requirements apply).

## Manifest Verification (/define)

Run the manifest-verifier with the full repeat loop until COMPLETE. On CONTINUE, present questions, update manifest, re-invoke.
