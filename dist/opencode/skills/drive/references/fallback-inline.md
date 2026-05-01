# Inline-Fallback Scheduler

Loaded by `drive/SKILL.md` §Kickoff and `drive-tick/SKILL.md` §Output Protocol §Continuing when the run's scheduler is `inline-fallback` (see §Detection Result). Specifies the self-scheduling protocol that replaces `/loop`'s cron firing: at the end of a Continuing tick, `/drive-tick` sleeps for the configured interval and invokes itself.

## Detection Result

This file is loaded after `/drive` §Pre-flight has already determined `scheduler = inline-fallback` — i.e., the system-prompt skills list has no skill named `loop`. The detection itself is owned by `drive/SKILL.md` §Pre-flight §Scheduler resolution; this section records the precondition so readers of this file know what was true when they arrived here.

If `/drive` resolved `scheduler = loop` instead, this file is not loaded — `/drive` and `/drive-tick` follow their existing loop-mode paths (`drive/SKILL.md` §Kickoff §Scheduler: `loop`).

The scheduler value is recorded once in the drive execution-log seed header (see §Log-Header Directive) and never re-evaluated during the run.

## Announce Protocol

Once, during `/drive` §Pre-flight and before the first side-effecting operation, `/drive` prints exactly one line naming the mode so users notice the UX divergence:

```
/loop skill not installed — running /drive in inline-fallback mode. This session will be held for up to <max-ticks> ticks; close the session to abort.
```

Substitute `<max-ticks>` with the resolved `--max-ticks` value. This is the sole announcement for the run; do not add warnings, emoji, or re-print the line at subsequent tick boundaries.

## Log-Header Directive

The drive execution-log seed header includes a `scheduler:` field alongside the other header fields (see `drive/SKILL.md` §Execution Log Initialization for the full field list):

- Field name: `scheduler:`
- Values: `loop` or `inline-fallback`
- Written once by `/drive` at log initialization (the same step that writes the other header fields). Never rewritten on resume or retry.
- Why never rewritten: re-evaluating would let a resumed run switch schedulers mid-flight — prior log entries were produced under one scheduler and subsequent ticks would run under another, breaking parity with in-flight ticks.
- Read by `/drive-tick` as part of its full-log memento read at the top of every tick. No side channel, no separate state file.

## Chunked-Sleep Protocol

At the end of a Continuing tick (after the lock is released and the Continuing log entry is appended — see §Self-Invocation Directive for ordering), `/drive-tick` sleeps for the configured interval before invoking itself. The interval source is the `interval:` field from the drive-log seed header, converted to seconds.

The Bash tool caps each call at 10 minutes, so chunk the sleep under that cap: while remaining interval > 0, call `sleep min(600, remaining)` and subtract the slept amount. Never invoke `sleep 0`. The existing `/drive` interval range (`15m`–`24h`) governs the total — no additional chunk-count cap.

**On sleep error.** If any chunk's `sleep` call returns a non-zero exit (e.g., the environment blocks chained sleeps — see §Gotchas), exit the tick with the Bash error surfaced verbatim. Do not retry; do not fall through to the self-invoke step.

## Self-Invocation Directive

After the sleep completes, `/drive-tick` re-enters itself via the Skill tool with the current tick's flags forwarded verbatim:

```
Invoke the manifest-dev-experimental:drive-tick skill with: "--run-id <run-id> --mode <mode> --platform <platform> --sink <sink> --log <log-path> --max-ticks <N> [--manifest <manifest-path>] [--pr <pr-number>]"
```

Notation in the template: angle brackets `<value>` are placeholders — substitute the actual value the current tick received. Square brackets `[--flag <value>]` mark optional flags — when the upstream caller didn't pass the flag, omit the whole `--flag value` pair (and don't leave literal square brackets in the emitted string). Forward every flag the current tick received, verbatim; don't re-derive values.

Ordering inside the Continuing outcome is strict:

1. Release the lock (per `drive-tick/SKILL.md` §Concurrency Guard).
2. Append the Continuing log entry (per `drive-tick/SKILL.md` §Output Protocol).
3. Run the Chunked-Sleep Protocol.
4. Invoke the next tick as above.

Lock release precedes sleep so that a concurrent `/drive` invocation targeting the same run-id can recover cleanly via standard pre-flight.

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

**User action (not Claude) — after a session-close or mid-sleep interrupt.** A normal Continuing outcome releases the lock before sleeping (see §Self-Invocation Directive step 1), so Claude does remove the lock on the happy path. The steps below apply only when the tick dies mid-sleep and the lock is stranded:

1. Confirm no active Claude session is running `/drive` for this run-id (check other terminals/sessions). (Matches the pre-flight guidance in `drive/SKILL.md` §Pre-flight.)
2. Remove the stale lock: `rm /tmp/drive-lock-{run-id}` (substitute the run-id shown in the original run summary or `/tmp/drive-log-{run-id}.md`).
3. Re-invoke `/drive` with the same arguments the run was started with (see the log seed header for the original flag values); the tick picks up from log state. `drive/SKILL.md` §Pre-flight handles the lock-recovery branch on resume.

Never remove the lock while a tick is actively running.

## Gotchas

- **Chained `sleep 600` restriction.** The chunked-sleep protocol relies on multiple back-to-back `sleep 600` Bash invocations. Environments that block long-leading sleeps or chained sleeps (custom Claude Code hooks, some sandboxed runners) stall fallback mode mid-chunk. In-tick behavior on stall follows §Chunked-Sleep Protocol's "On sleep error" clause (exit with Bash error, no retry, no self-invoke). User mitigation (outside the tick): install `/loop` to bypass the limitation.
- **Session-held UX.** `/drive` does not exit after kickoff in fallback mode — the scheduler is the conversation. Plan accordingly; closing the session ends the run.
- **Per-chunk conversation blocking.** During each `sleep 600` chunk, Claude cannot take user input. Input is accepted between chunks and at tick start.
- **Context accumulation over long runs.** Every tick runs in the same conversation, so context grows with each iteration. Long runs (many ticks × deep `/do` convergence) may trigger auto-compression; set `--max-ticks` conservatively in fallback mode.
