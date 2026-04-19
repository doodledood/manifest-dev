# Sink Adapter: `local`

Writes escalations and status notifications to the run's execution log file. No external integrations (no Slack, no Discord, no email). User observes by tailing the log.

v0 default and only supported sink.

## Escalation Target

```markdown
## Escalation Target
Escalations are appended to the run log at `/tmp/drive-log-{run-id}.md` as a `## ESCALATION` marker block. No external notifications. User tails the log to observe.
```

## Escalate

Called by `/drive-tick` when something blocking emerges: amendment-loop guard tripped, budget exhausted, crash-recovery inconsistency detected, unresolved merge conflict, stale uncertain thread (github), merge-ready prompt awaiting user decision, or empty-diff terminal.

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

| Code | When |
|---|---|
| `AMENDMENT_LOOP_GUARD` | Three consecutive self-amendments without external input. |
| `BUDGET_EXHAUSTED` | Tick count reached `--max-ticks`. |
| `CRASH_RECOVERY_INCONSISTENT` | Uncommitted WIP does not match the last log entry. |
| `UNRESOLVED_CONFLICT` | github platform: merge conflict the tick can't confidently resolve. |
| `STALE_THREAD` | github platform: uncertain thread with no reply for 30+ min, or fixed-thread unresolved for 30+ min. |
| `MERGE_READY_PROMPT` | github platform: PR is merge-ready; awaiting user confirmation. |
| `EMPTY_DIFF` | github platform: PR has no diff. |
| `PROPOSED_AMENDMENT` | Scope change the tick does not want to auto-apply; user to decide. |

Additional codes can be added as needed; follow the same `UPPERCASE_SNAKE_CASE` shape.

### Behavior after escalate

`escalate` is side-effect-only — it appends the block to the log. It does NOT end the loop; the caller (tick's decision tree) decides whether to end the loop (usually yes, for terminal escalations like `BUDGET_EXHAUSTED`, `EMPTY_DIFF`).

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

| Code | When |
|---|---|
| `MANIFEST_SATISFIED` | `none` platform reached `all-verify-pass`. Terminal. |
| `PR_MERGED` | github platform: PR was merged. Terminal. |
| `PR_CLOSED` | github platform: PR was closed without merge. Terminal. |
| `PR_DRAFTED` | github platform: PR converted to draft. Terminal. |
| `TICK_COMPLETED` | Continuing-state tick successfully performed an action. |
| `TICK_SKIPPED` | Lock was held; this tick exited silently. |

## Why sink and log both

The log is the source of truth. The sink is the observer channel. In v0, the sink for `local` writes to the same file — redundant, but consistent with future sinks (Slack, email) where the log stays local and the sink ships a human-readable notification out-of-band.

When future sinks are added (e.g., `slack`), the log discipline stays unchanged — every tick still writes to the log. The sink additionally posts to Slack. Tooling that depends on the log does not change.

## Gotchas

- **Sink never silences the log.** If `escalate` or `report-status` fails for any reason (disk full, permission error on `/tmp`), the failure is itself an escalation-worthy condition — `/drive-tick` should catch the sink failure and, at minimum, attempt to write the failure to the log directly before exiting.
- **Order: log entry first, sink second.** The tick's action log entry (`## Tick N — ...`) always precedes the sink call. If the sink fails, the log still records what happened.
- **No buffering.** `local` sink writes immediately (append to file, flush). No batching. Partial log is valuable; deferred log is useless.
