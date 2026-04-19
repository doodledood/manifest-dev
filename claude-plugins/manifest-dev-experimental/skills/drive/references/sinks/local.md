# Sink Adapter: `local`

Writes escalations and status notifications to the run's execution log file. No external integrations (no Slack, no Discord, no email). User observes by tailing the log.

v0 default and only supported sink.

## Escalation Target

```markdown
## Escalation Target
Escalations are appended to the run log at `/tmp/drive-log-{run-id}.md` as a `## ESCALATION — <CODE>` marker block. No external notifications. User tails the log to observe.
```

## Escalate

Called by `/drive-tick` when something blocking emerges: amendment-loop guard tripped, budget exhausted, crash-recovery inconsistency detected (all platforms); stale uncertain thread, merge-ready prompt, empty-diff terminal, unresolved merge conflict (github platform only).

### Format

Append this block to the run log (`/tmp/drive-log-{run-id}.md`):

```markdown
## ESCALATION — <ESCALATION_CODE>

**Timestamp:** <ISO-8601>
**Run ID:** <run-id>
**Tick:** <tick-number>
**Reason:** <one-line summary>

**Context:**
<free-form markdown — relevant state, why this is an escalation, what the tick considered and rejected>

**Recommended next step:**
<concrete action the user can take — "re-invoke /drive with --max-ticks 200", "resolve merge conflict manually", "merge PR manually", "amend manifest to remove AC-3.4">
```

### Escalation codes

Use a stable uppercase code so operators can grep the log. At minimum:

| Code | Terminal? | When |
|---|---|---|
| `AMENDMENT_LOOP_GUARD` | Yes | Consecutive self-amendments without external input reached the guard threshold (defined in `drive-tick/SKILL.md`). |
| `BUDGET_EXHAUSTED` | Yes | Tick count reached `--max-ticks`. |
| `CRASH_RECOVERY_INCONSISTENT` | Yes | Uncommitted WIP does not match the last log entry; user must review manually. |
| `UNRESOLVED_CONFLICT` | Yes | github platform: merge conflict the tick can't confidently resolve. Maps to the `escalation` terminal state. |
| `EMPTY_DIFF` | Yes | github platform: PR has no diff. |
| `MERGE_READY_PROMPT` | Yes | github platform: PR is merge-ready; awaiting user confirmation. Loop ends; user merges manually. |
| `PROPOSED_AMENDMENT` | Yes | Scope change the tick does not want to auto-apply; user to decide. |
| `STALE_THREAD` | No | github platform: uncertain thread with no reply after the staleness window defined by the github adapter, or fixed-thread unresolved past that window. Loop continues. |
| `TICK_ERROR` | Yes | Unrecoverable Skill / push / sink failure within a tick. |

Additional codes can be added; follow the same `UPPERCASE_SNAKE_CASE` shape.

### Behavior after escalate

`escalate` is side-effect-only — it appends the block to the log. It does NOT end the loop on its own; the caller decides loop end based on the code's Terminal column above.

## Report Status

Called by `/drive-tick` every tick, on every outcome (terminal, continuing, skipped-lock-held). The sink's `report-status` is **additive** to the log's tick-entry discipline — the log already gets a tick entry; `report-status` writes a friendlier human-visible line for operators tailing the log.

### Format

Append this block to the run log:

```markdown
## TICK STATUS — <STATUS_CODE>

**Timestamp:** <ISO-8601>
**Tick:** <tick-number>
**Action:** <brief action summary — "implemented AC-3.4", "verified, all phases pass", "fixed failing lint on file X", "inbox: classified 2 comments, replied to 1, fixed 1", "lock held — skipped">
**HEAD:** <current-sha>
**Next:** <"scheduled next tick in <interval>" | "terminal: <state>" | "skipped — lock held">
```

### Status codes

| Code | Terminal? | When |
|---|---|---|
| `MANIFEST_SATISFIED` | Yes | `none` platform reached `all-verify-pass`. |
| `PR_MERGED` | Yes | github platform: PR was merged. |
| `PR_CLOSED` | Yes | github platform: PR was closed without merge. |
| `PR_DRAFTED` | Yes | github platform: PR converted to draft. |
| `TICK_COMPLETED` | No | Continuing-state tick successfully performed an action. |
| `TICK_SKIPPED` | No | Lock was held; this tick exited silently. |

## Why sink and log both

The log is the source of truth. The sink is the observer channel. In v0, the sink for `local` writes to the same file — redundant, but consistent with future sinks (Slack, email) where the log stays local and the sink ships a human-readable notification out-of-band.

When future sinks are added (e.g., `slack`), the log discipline stays unchanged — every tick still writes to the log. The sink additionally posts to Slack. Tooling that depends on the log does not change.

## Gotchas

- **Sink raises on failure.** If `escalate` or `report-status` fails (disk full, permission error on `/tmp`), the sink raises — it does NOT swallow the error. Failure handling is the tick's responsibility (see `drive-tick/SKILL.md` §Output Protocol → Error).
- **No buffering.** `local` sink writes immediately (append + flush). No batching. Partial log is valuable; deferred log is useless.
