# figure-out: --autonomous

Loaded when args contain `--autonomous` (typically passed by `/auto` chaining figure-out → define → do without user wait). There is no user to wait on — and no user to **press back**. In interactive mode the user is a second presser, catching branches you skipped and demanding depth, with the one-question-per-turn cadence pacing that across turns; autonomous mode removes both the presser and the cadence, so the completeness bar **rises** — you play both roles.

- At each load-bearing question, pose it, generate your recommended answer with brief rationale, and adopt that answer as the resolution — the same one you'd have recommended to the user.
- Surface each resolution (question, answer, rationale) in the conversation so downstream consumers (e.g. `/define`) can read it as prior context.
- When confidence in a load-bearing resolution is low, flag it as a Known Assumption candidate so `/define` records it as `ASM-*` ("default chosen, impact if wrong") — the user's hook to amend later if the default proves wrong.
- Before naming the read, self-supply the presses a user would otherwise force from you — those the master pre-naming gate and the topic's probe file already name; the absence of someone asking is not license to skip them. And because in this mode no one audits the read before it's relied on — the condition under which the master discipline already calls for an independent re-derivation — run that re-derivation pass before naming, not only when the read is contested.
- Then surface the read with its full anatomy and stop — chaining into execution belongs to the caller.

With no user pushback to hold positions against, the hold-positions discipline applies to downstream contradictions instead (e.g. a verifier finding) — re-examine the evidence rather than reflexively flipping.
