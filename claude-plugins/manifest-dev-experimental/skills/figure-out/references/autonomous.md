# figure-out: --autonomous

Loaded when args contain `--autonomous` (typically passed by `/auto` chaining figure-out → define → do without user wait). Without the flag, default interactive behavior applies.

## What changes

For each load-bearing question on the tree:

1. Pose the question internally — the same one you'd otherwise ask the user.
2. Generate your recommended answer with brief rationale.
3. Adopt the recommended answer as the resolution.
4. Log the resolution (question, recommended answer, rationale) so the downstream encoder (`/define`) can consume it.
5. When confidence in the answer is low *and* the answer is load-bearing, flag for `Known Assumption` so `/define` records it as `ASM-*` with "Default chosen, impact if wrong" semantics. This is the user's hook to amend later if the default proves wrong.
6. Move to the next load-bearing question.

## What stays the same

- Walking every branch of the decision tree (design choices, diagnostic hypotheses, commitment questions).
- Leverage ordering — next load-bearing question first.
- Stack discipline — return to the original question after investigation detours.
- Explore instead of asking when discoverable (code, docs, the world) — already doesn't require the user.
- Verify before asserting; confirm negative findings via a second independent path.

## Stop condition

Stop when the high-leverage unknowns are resolved — remaining ones wouldn't shift the read. Surface the shared understanding in the transcript (or discovery log if one is open) so the next skill in the chain reads it as prior context.

## Note on "hold positions under pushback"

In autonomous mode there is no user pushback to hold a position against. The discipline still applies if a downstream skill (e.g., a verifier finding) contradicts a resolution — re-examine evidence rather than reflexively flipping.
