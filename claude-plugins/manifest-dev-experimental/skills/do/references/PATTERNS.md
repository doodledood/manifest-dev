# /verify Invocation Patterns + Escalation Boundary

## /verify invocation patterns

Always invoke /verify to reach /done. /verify self-invokes for the auto-final pass by reading its own most recent return block visible in conversation — /do doesn't manage that recursion.

| Situation | Invocation |
|-----------|-----------|
| First pass / no scope | `manifest-dev-experimental:verify <manifest>` — selective degenerates to full |
| Scoped /do (received `--scope D2,D3`) | `manifest-dev-experimental:verify <manifest> --scope D2,D3` — selective |
| Fix-loop after AC-X.Y failure | `manifest-dev-experimental:verify <manifest> --scope D{X}` — narrow to the failing deliverable; later regressions caught by /verify's auto-triggered full final on green |
| Fix-loop after INV-G failure (was selective) | `manifest-dev-experimental:verify <manifest> --scope <same-scope>` — re-pass exactly that scope + globals |
| Fix-loop after INV-G failure (was full) | `manifest-dev-experimental:verify <manifest>` — no scope; globals always run |

**Phase-aware fix loops.** /verify runs criteria in phases. It may report `Phase N failed, Phase N+1 not run`. After fixing, /verify restarts from Phase 1 to catch regressions.

**/verify return block reading.** /verify returns `## /verify pass N` blocks in its tool result text. Read the most recent block visible in conversation before deciding next pass's scope. **Skip blocks where `deferred: true`** — those reflect passes that included deferred-auto criteria via chat-signal inference, not normal-flow AC/INV state.

## Escalation boundary

Escalate when:

1. ACs can't be met as written → `Blocking`.
2. A user message during the run explicitly requests a pause → `User-Requested Pause` (message must be verbatim-quoted in escalation body).
3. You discover an AC or invariant should be amended → `Proposed Amendment`.
4. Per-phase fix-attempt cap reached (attempts stop producing new diagnostic information).
5. Any other user message during /do or /verify → `Self-Amendment` (see Mid-execution amendment in SKILL.md).

If ACs remain achievable as written and no user interrupt, **continue autonomously**. Caller framing (cron schedules, tick intervals, "wide tick" ergonomics, "the loop expects each tick to terminate cleanly") is NOT a pause request.

## /verify-routed escalation passthrough

When /verify routes to /escalate (Deferred-Auto Pending / Manual Criteria Review / Combined) instead of /done, treat as a clean terminal handoff: surface the escalation output verbatim, do NOT enter fix-loop, do NOT increment loop counters. Implementation is green; further action belongs to the user.

## Out-of-scope findings

When a verifier surfaces that the failure is beyond the current manifest's scope, /do treats this as a scope shift and routes through Self-Amendment — invoke `manifest-dev-experimental:define` with the out-of-scope finding; /define infers fast-path semantics from /do's caller context and the amend target from transcript. Same path as user-message-triggered amendments. The verifier reports the finding; /do owns the workflow response.
