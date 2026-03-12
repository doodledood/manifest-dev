# Interview Styles

Interview style controls **who decides** — the user or the agent. All protocols still run at every level; the difference is whether findings are presented via AskUserQuestion or auto-resolved by picking the recommended option.

Complexity triage is orthogonal: it determines **which** protocols run; interview style determines **how** each protocol's findings are handled.

## Style Routing Table

| Style | Principle | AskUserQuestion |
|-------|-----------|-----------------|
| **thorough** (default) | User decides everything. Current behavior — no change. | All questions go to user. |
| **minimal** | User decides scope, constraints, and high-impact items. Agent auto-resolves the rest by picking the recommended option. | Ask when: scope boundaries, hard constraints, or multiple options are equally valid (no clear recommended choice). |
| **autonomous** | Agent decides everything. Present the final manifest for approval — user accepts, rejects, or gives feedback. | No questions during the interview. All decisions auto-resolved. |

## Auto-Decided Items

When interview style causes an item to be auto-decided (agent picks recommended option instead of asking), encode it normally as INV/AC/PG with an "(auto)" annotation, AND list it in the Known Assumptions section with the reasoning for the chosen option.

## Style is Dynamic

The `--interview` flag sets the starting posture, not a rigid lock. If a user on autonomous explicitly asks questions or requests probing, engage. If a user on thorough signals "enough" or says "just build it", shift to autonomous for the remainder of the session. When the user or verifier gives feedback on an autonomous manifest, auto-resolve the concerns and stay in autonomous mode unless the user explicitly requests more interaction. Log any style shift to the discovery file.
