# figure-out: --autonomous

Loaded when args contain `--autonomous` (typically passed by `/auto` chaining figure-out → define → do without user wait). There is no user to wait on — and no user to **press back**. In interactive mode the user is a second presser, catching branches you skipped and demanding depth, with the one-question-per-turn cadence pacing that across turns; autonomous mode removes both the presser and the cadence, so the completeness bar **rises** — you play both roles. And the master frame's *explore-don't-ask* default goes absolute here: you must clear every patch of fog that investigation or derivation can clear without the user — dig to the truth rather than guessing, because here trustworthiness and truth outrank speed. An assumption is the last resort, never a shortcut around work you could have done yourself: only fog that genuinely needs the user — a true preference, a call unknowable without asking — falls to a low-confidence assumption.

Your first action on activation — before the first question, before any investigation — is to establish a durable goal-setting backstop for the run. If the active harness exposes a goal-setting or continuation capability, set the goal directly with the Read's completion contract; otherwise print this copy-pasteable contract for the user to apply manually:

```
Investigate <topic> until the Read is named with full anatomy — every load-bearing branch pressed, the independent re-derivation run, the rival set no longer moving; do not stop at a first-pass read. Clear all fog you can without me — investigate to the truth rather than guessing, since trustworthiness outranks speed — recording an assumption only for what genuinely needs me, and halting only for a blocker that truly requires my input. Record compact progress checkpoints when the leading read, evidence, assumptions, blockers, or next crux changes. Stop after N turns if it stalls.
```

This is the standalone-run backstop. Suppress it when you can clearly see `--autonomous` is chained under a broader parent workflow that owns continuation (typically `/auto`; also an explicit parent `/define` or `/do` amendment flow). When in doubt, set or print it — a missing backstop costs more than a redundant one.

- At each load-bearing question, pose it, generate your recommended answer with brief rationale, and adopt that answer as the resolution — the same one you'd have recommended to the user.
- Surface each resolution (question, answer, rationale) in the conversation so downstream consumers (e.g. `/define`) can read it as prior context.
- When confidence in a load-bearing resolution is low, flag it as a Known Assumption candidate so `/define` records it as `ASM-*` ("default chosen, impact if wrong") — the user's hook to amend later if the default proves wrong.
- Before naming the read, self-supply the presses a user would otherwise force from you — those the master pre-naming gate and the topic's probe file already name; the absence of someone asking is not license to skip them. And because in this mode no one audits the read before it's relied on — the condition under which the master discipline already calls for an independent re-derivation — run that re-derivation pass before naming, not only when the read is contested.
- Then surface the read with its full anatomy and stop — chaining into execution belongs to the caller.

With no user pushback to hold positions against, the hold-positions discipline applies to downstream contradictions instead (e.g. a verifier finding) — re-examine the evidence rather than reflexively flipping.
