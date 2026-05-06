# Sink Adapter: `local`

Writes escalations and status notifications to the run's execution log file. No external integrations (no Slack, no Discord, no email). User observes by tailing the log.

**Degenerate sink.** The destination IS the log file. Escalate appends an `## ESCALATION` block; Report Status appends a `## TICK STATUS` block. The tick's own per-tick log entries (Terminal / Continuing / Skipped / Error) remain the authoritative cross-tick state per the contract invariant in `references/ADAPTER_CONTRACT.md` — sink writes are additive, not a replacement.

## Escalation Target

```markdown
## Escalation Target
Escalations are appended to the run log at `/tmp/drive-log-{run-id}.md` as a `## ESCALATION — <CODE>` marker block. No external notifications. User tails the log to observe.
```

## Escalate

Called by `/drive-tick` when something blocking emerges (see Escalation codes table for the full enumeration of triggers).

### Escalation block format

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
| `STALE_THREAD` | No | github platform: uncertain thread with no reply after the staleness window defined by the github adapter, or fixed-thread unresolved past that window. Loop continues. |
| `DO_MALFORMED_RESPONSE` | Yes | `/do` returned a response the tick can't parse; surfaced as a `/do` contract bug rather than patched in-tick. |
| `TICK_ERROR` | Yes | Unrecoverable Skill / push / sink failure within a tick. |

Additional codes can be added; follow the same `UPPERCASE_SNAKE_CASE` shape.

### Behavior after escalate

`escalate` is side-effect-only — it appends the block to the log. It does NOT end the loop on its own; the caller decides loop end based on the code's Terminal column above.

## Report Status

Called by `/drive-tick` on Terminal outcomes that name a status code (see Status codes table). Continuing and Skipped-lock-held ticks do not invoke the sink — the log's tick entry is the cross-tick state record per the contract invariant (see `drive-tick/SKILL.md` §Output Protocol). Sink writes are additive notification blocks.

### Status block format

Append this block to the run log:

```markdown
## TICK STATUS — <STATUS_CODE>

**Timestamp:** <ISO-8601>
**Tick:** <tick-number>
**Action:** <brief action summary — "implemented AC-3.4", "verified, all phases pass", "fixed failing lint on file X", "inbox: classified 2 comments, replied to 1, fixed 1">
**HEAD:** <current-sha>
**Next:** <"scheduled next tick" | "terminal: <state>">
```

### Status codes

| Code | Terminal? | When |
|---|---|---|
| `MANIFEST_SATISFIED` | Yes | `none` platform reached `all-verify-pass`. |
| `PR_MERGED` | Yes | github platform: PR was merged. |
| `PR_CLOSED` | Yes | github platform: PR was closed without merge. |
| `PR_DRAFTED` | Yes | github platform: PR converted to draft. |

## Gotchas

- **Sink raises on failure.** If `escalate` or `report-status` fails (disk full, permission error on `/tmp`), the sink raises — it does NOT swallow the error. Failure handling is the tick's responsibility (see `drive-tick/SKILL.md` §Output Protocol → Error).
- **No buffering.** Write each block immediately. Partial log is valuable; deferred log is useless.
