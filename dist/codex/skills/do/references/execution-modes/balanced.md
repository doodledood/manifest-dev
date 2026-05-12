# Execution Mode: Balanced

Saves quota by limiting parallelism and verification cycles while keeping full model capability.

## Model Routing

- **Criteria-checker**: inherit (session model)
- **Quality gate reviewers**: inherit — all run

## Verification Parallelism

Batched — launch max 4 concurrent verifiers per phase. When a batch completes, launch the next.

## Fix-Verify Loops

Max 2 code-change fix attempts per phase. Each phase has its own counter. When the limit is hit, escalate via /escalate — the fix isn't converging, human judgment needed.

**Action-aware fix-cap.** Only code-change fix attempts count toward the cap. Other retry shapes — re-verifying after a wait, retriggering a transient failure, posting a thread reply, pushing a sync update, routing a scope shift through Self-Amendment — are not fix attempts. They're shape-of-progress, not shape-of-fix.

Per-AC `verify.timeout:` is the wall-clock cap that bounds total time on a criterion regardless of retry shape — see /do SKILL.md "Per-criterion timeout."

## Escalation

Escalate when fix-verify loop limit (2) is hit for any phase. Follow standard /escalate evidence requirements.

## Manifest Verification (/define)

Run the manifest-verifier **once**. If it returns CONTINUE, present its questions, update the manifest, then proceed to Summary for Approval. No repeat loop.
