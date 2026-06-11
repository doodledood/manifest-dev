# figure-out: --autonomous

Loaded when args contain `--autonomous` (typically passed by `/auto` chaining figure-out → define → do without user wait). The investigation and all of its discipline are unchanged; only the counterparty changes — there is no user to wait on.

- At each load-bearing question, pose it, generate your recommended answer with brief rationale, and adopt that answer as the resolution — the same one you'd have recommended to the user.
- Surface each resolution (question, answer, rationale) in the conversation so downstream consumers (e.g. `/define`) can read it as prior context.
- When confidence in a load-bearing resolution is low, flag it as a Known Assumption candidate so `/define` records it as `ASM-*` ("default chosen, impact if wrong") — the user's hook to amend later if the default proves wrong.
- Stop when the read is named: surface it with its full anatomy and end the turn — chaining onward belongs to the caller.

With no user pushback to hold positions against, the hold-positions discipline applies to downstream contradictions instead (e.g. a verifier finding) — re-examine the evidence rather than reflexively flipping.
