# Interview Mode: Autonomous

Agent decides everything. Present the final manifest for approval — user accepts, rejects, or gives feedback.

## Decision Authority

All decisions auto-resolved. Pick the recommended option for every item. No questions during the interview.

## Question Format

No user-facing questions during the interview. All findings are resolved autonomously. The only user interaction is the final manifest presentation.

## Interview Flow

Address all coverage goals internally. Resolve unknowns through exploration (search, file reads) before falling back to the recommended option — autonomous means no user questions, not no investigation. Log findings and resolutions to the discovery file.

## Checkpoint Behavior

No intermediate checkpoints. Present the complete manifest at the end for approval. The user accepts, rejects, or gives targeted feedback.

## Finding Sharing

All findings are resolved autonomously and encoded directly. The manifest itself is the finding-sharing mechanism — the user sees everything at once in the final presentation.

## Style Shifting

If the user asks questions or requests probing, shift to thorough mode. When the user or verifier gives feedback on the manifest, auto-resolve the concerns and stay in autonomous mode unless the user explicitly requests more interaction. Log any shift.

## Verifier CONTINUE

Auto-resolve the verifier's concerns, update the manifest, and re-invoke the verifier. Do not present to the user.

## Convergence

Apply SKILL.md's convergence requirements autonomously. Move to synthesis as soon as satisfied. When uncertain between options, pick the recommended one and log the reasoning in Known Assumptions. When a convergence test requires user preference that can't be inferred from context, pick the recommended option and proceed.
