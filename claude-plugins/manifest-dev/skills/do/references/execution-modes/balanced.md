# Execution Mode: Balanced

Saves quota by limiting parallelism and verification cycles while keeping full model capability.

## Model Routing

- **Criteria-checker**: inherit (session model)
- **Quality gate reviewers**: inherit — all run

## Verification Parallelism

Batched — launch max 4 concurrent verifiers per phase. When a batch completes, launch the next.

## Fix-Verify Loops

Max 2 `fix-code` actions per phase. Each phase has its own loop counter. When the limit is hit, escalate via /escalate — the fix isn't converging, human judgment needed.

**Action-aware fix-cap.** The fix-verify counter only increments on `fix-code` actions dispatched from a verifier hint (see /do SKILL.md "Hint Dispatch"). The other action labels are explicitly non-counting:

- `sleep` — non-counting (a wait, not a fix attempt)
- `retrigger-ci` — non-counting (re-runs CI without modifying code)
- `reply-thread` — non-counting (posts a reply, no code change)
- `push-update` — non-counting (sync-shaped action)
- `out-of-scope` — non-counting (verifier finding; /do maps to Self-Amendment)

Per-AC `verify.timeout:` is the wall-clock cap that bounds total time on a criterion regardless of action mix — see /do SKILL.md "Per-criterion timeout."

## Escalation

Escalate when fix-verify loop limit (2) is hit for any phase. Follow standard /escalate evidence requirements.

## Manifest Verification (/define)

Run the manifest-verifier **once**. If it returns CONTINUE, present its questions, update the manifest, then proceed to Summary for Approval. No repeat loop.
