# Inline-Fallback Scheduler

Loaded by `drive/SKILL.md` §Kickoff and `drive-tick/SKILL.md` §Output Protocol §Continuing when the run's scheduler is `inline-fallback`. Specifies the self-scheduling protocol that replaces `/loop`'s cron firing: at the end of a Continuing tick, `/drive-tick` sleeps for the configured interval and invokes itself.

The detection itself (no skill named `loop` in the system-prompt skills list) is owned by `drive/SKILL.md` §Pre-flight §Scheduler resolution; the resolved value is recorded once in the execution-log seed header and never re-evaluated during the run.

## Announce Protocol

Once, during `/drive` §Pre-flight and before the first side-effecting operation, `/drive` prints exactly one line naming the mode so users notice the UX divergence:

```
/loop skill not installed — running /drive in inline-fallback mode. This session will be held for up to <max-ticks> ticks; close the session to abort.
```

Substitute `<max-ticks>` with the resolved `--max-ticks` value. This is the sole announcement for the run; do not add warnings, emoji, or re-print the line at subsequent tick boundaries.

## Log-Header Directive

The drive execution-log seed header includes a `scheduler:` field with values `loop` or `inline-fallback`, written once at log init (see `drive/SKILL.md` §Execution Log Initialization). Never rewritten — switching schedulers mid-run would split the run across two scheduling regimes. Read by `/drive-tick` from the log only — never passed via flag, env, or other side channel.

## Chunked-Sleep Protocol

At the end of a Continuing tick (after the lock is released and the Continuing log entry is appended — see §Self-Invocation Directive for ordering), `/drive-tick` sleeps for the `interval:` from the seed header (converted to seconds). The Bash tool caps each call at 10 minutes — chunk under the cap; never `sleep 0`. The `15m`–`24h` interval range governs the total — no additional chunk-count cap.

**On sleep error.** If any chunk's `sleep` call returns a non-zero exit (e.g., the environment blocks chained sleeps — see §Gotchas), exit the tick with the Bash error surfaced verbatim. Do not retry; do not fall through to the self-invoke step.

## Self-Invocation Directive

After the sleep completes, `/drive-tick` re-enters itself via the Skill tool with the current tick's flags forwarded verbatim:

```
Invoke the manifest-dev:drive-tick skill with: "--run-id <run-id> --mode <mode> --platform <platform> --sink <sink> --log <log-path> --max-ticks <N> [--manifest <manifest-path>] [--pr <pr-number>]"
```

Substitute `<placeholders>` with the values the current tick received; omit `[optional]` flags the upstream caller didn't pass; never re-derive values.

Within the Continuing outcome (see `drive-tick/SKILL.md` §Output Protocol), the chunked-sleep + self-invoke steps run **after** lock release and log append. Lock release precedes sleep so a concurrent `/drive` targeting the same run-id can recover cleanly via standard pre-flight.

## Parity Statements

The following behaviors are identical between schedulers. Only the scheduling mechanism differs.

- **Lock acquisition, TOCTOU check, lock-held-skip behavior.** Unchanged. A second `/drive` invocation on the same run-id while a fallback tick is sleeping sees the existing lock and exits per standard pre-flight — identical to loop-mode collision behavior.
- **Budget check.** Unchanged. Counted completed tick entries in the log; skipped ticks do not count; `--max-ticks` is the terminal cap in both schedulers.
- **Terminal-state detection.** Unchanged. Platform adapter's terminal check, `## Execution Complete` marker handling, CI-triage terminal signals, Budget exhaustion, and Crash Recovery flagging all fire identically.
- **Crash recovery.** Unchanged. Uncommitted-changes reconciliation at tick start follows `drive-tick/SKILL.md` §Crash Recovery.
- **Inbox Handling.** Unchanged. Platform-adapter contract drives bot/human classification, actionable/FP/uncertain triage, and thread replies.
- **Do Invocation (manifest mode).** Unchanged. `/do` is invoked with the same arguments, the same marker detection (`## Execution Complete`, `## Escalation:`), and the same retrigger-only skip optimization.
- **Amendment flow.** Unchanged. `manifest-dev:define --amend --from-do` is invoked inline during a tick; subsequent `/do` re-runs against the amended manifest. Amendment never interacts with the scheduler.
- **CI Failure Triage and Retrigger.** Unchanged. Platform adapter's classification, retrigger cap, and `retrigger-empty-commit: <sha>` marker emission are the same in both schedulers.
- **Tend PR (Write Outputs + Thread Hygiene).** Unchanged. Commit, push, PR description sync, and thread resolution follow the adapter contract identically.
- **Log format for tick entries.** Unchanged. `## Tick N — Terminal | Continuing | Skipped | Error` blocks, `retrigger-empty-commit:` and `execution-complete-head:` lines, escalation markers — all written in the same shape.

## Interruption & Crash Semantics

The fallback scheduler lives inside the Claude Code session. If the user closes the session, interrupts Claude during a sleep, or the host suspends mid-chunk, the tick dies and the lock remains at `/tmp/drive-lock-{run-id}`. This is the same terminal symptom as `/loop`'s cron-firing stopping in loop mode — no automatic recovery.

**User action (not Claude) — after a session-close or mid-sleep interrupt.** A normal Continuing outcome releases the lock before sleeping, so Claude does remove the lock on the happy path. When the tick dies mid-sleep and the lock is stranded: confirm no active `/drive` session is running for this run-id, remove `/tmp/drive-lock-{run-id}`, re-invoke `/drive` with the original args (visible in the log seed header). `drive/SKILL.md` §Pre-flight owns the lock-recovery branch on resume.

Never remove the lock while a tick is actively running.

## Gotchas

- **Chained `sleep 600` restriction.** The chunked-sleep protocol relies on multiple back-to-back `sleep 600` Bash invocations. Environments that block long-leading sleeps or chained sleeps (custom Claude Code hooks, some sandboxed runners) stall fallback mode mid-chunk. In-tick behavior on stall follows §Chunked-Sleep Protocol's "On sleep error" clause (exit with Bash error, no retry, no self-invoke). User mitigation (outside the tick): install `/loop` to bypass the limitation.
- **Session-held UX.** `/drive` does not exit after kickoff in fallback mode — the scheduler is the conversation. Plan accordingly; closing the session ends the run.
- **Per-chunk conversation blocking.** During each `sleep 600` chunk, Claude cannot take user input. Input is accepted between chunks and at tick start.
- **Context accumulation over long runs.** Every tick runs in the same conversation, so context grows with each iteration. Long runs (many ticks × deep `/do` convergence) may trigger auto-compression; set `--max-ticks` conservatively in fallback mode.
