---
name: drive
description: 'Tick-based manifest runner. Use to take a /define manifest to green or tend an existing PR through review and CI without babysitting. Triggers: drive, run autonomously, take it to green, tend pr, cron this to completion.'
user-invocable: true
---

# /drive — Cron-Driven Manifest Runner

## Goal

Drive a manifest (or an existing PR in babysit mode) to a terminal state — verify-pass in none mode, merge-ready in github mode — through repeated stateless ticks scheduled by `/loop` or the inline-fallback scheduler.

`/drive` is the canonical PR-lifecycle skill in `manifest-dev`. Coexists with `/do` and `/auto`.

## Input

`$ARGUMENTS` = `[<manifest-path>] [--platform none|github] [--sink local] [--base <branch>] [--interval <duration>] [--max-ticks <N>]`

- `<manifest-path>` — Optional. Absent → **babysit mode** (requires `--platform github`). Present → **manifest mode**.
- `--platform` — `none` (default) | `github`. `github` requires a working GitHub backend on `origin` (see Pre-flight).
- `--sink` — `local` (default). Where escalations and status notifications go.
- `--base` — Override base-branch auto-detection.
- `--interval` — Default `15m`. Range `15m`–`24h` inclusive. Floor for poll frequency, not a hard cadence (ticks holding the lock skip silently).
- `--max-ticks` — Default `100`. Range `1`–`10000` inclusive. Cap on total ticks before the tick escalates via sink and ends the loop.

When a flag value is unrecognized, missing, or out of range, reject naming the offending flag, the supplied value, and the accepted set or range.

## Mode Resolution

- **Manifest mode** — `<manifest-path>` provided; file readable as a `manifest-dev:define` manifest.
- **Babysit mode** — `<manifest-path>` absent; requires `--platform github` (no manifest + no PR = nothing to observe); current branch must have exactly one open PR.

Reject violating combinations during Pre-flight.

## Pre-flight (read-only — no side effects)

Pre-flight runs before any branch creation, commit, push, PR operation, lock creation, or log initialization. On failure: error actionably and exit without modifying repository state.

- **Scheduler resolution.** Check Claude's system-prompt skills list for `name: loop`. Present → `scheduler = loop`. Absent → `scheduler = inline-fallback` (follow `references/fallback-inline.md`). Record once in the execution log seed header; never re-evaluate during the run.
- **Inline-fallback announcement.** In inline-fallback only, emit the line from `references/fallback-inline.md` §Announce Protocol before any side-effecting operation in this skill. Read-only checks may precede the announcement.
- **Required skills available**: `manifest-dev:do`, `manifest-dev:verify`, `manifest-dev:define`. (`/drive-tick` invokes `/do` directly; `/verify` is required transitively; Amendment uses `/define --amend`.)
- **Inside a git repository.**
- **Manifest mode**: manifest file readable and parseable.
- **`--platform github`**: `origin` remote configured AND a working GitHub backend reachable — accept whichever is present (GitHub MCP tools loaded *or* `gh` CLI authenticated). Pre-flight verifies one is available; the run uses whichever it found. The rejection message names what was tried.
- **Babysit mode (`--platform github`)**: exactly one open PR on the current branch (zero or multiple → reject with the count).
- **Resolve run-id (read-only).** In github mode, query the open PR for the current branch and compute `gh-{owner}-{repo}-{pr-number}`. No PR found (first-time run) → defer run-id finalization to bootstrap (no prior lock can exist for an unresolved run-id). In none mode, compute `local-{UTC-timestamp}-{collision-resistant-suffix}`.
- **No conflicting lock for the resolved run-id.** Once run-id is known, if `/tmp/drive-lock-{run-id}` exists, halt and report the lock path, creation timestamp, and recorded PID. Probe PID liveness and classify (live | dead | indeterminate) — the message names the classification and the resolution path. `/drive` never removes the lock itself; the user clears it.

## Base Branch Resolution

Manifest mode only (babysit uses the existing PR's base).

Resolve in order: `--base <branch>` flag → remote default branch (`origin/HEAD`) → literal `main`. Never silently fall back to `master`. If none resolve, reject and require `--base`.

Record the resolved base in the execution log seed header.

## Run ID

Format (load-bearing — cross-tick contract used by lock + log paths):

- **github mode**: `gh-{repo-owner}-{repo-name}-{pr-number}`
- **none mode**: `local-{UTC-timestamp-YYYYMMDD-HHMMSS}-{collision-resistant-suffix}`

Repo owner/name from the `origin` remote URL. PR number is finalized after bootstrap (newly created PR) or babysit lookup. None-mode suffix avoids same-second collisions.

Derived paths:
- Lock: `/tmp/drive-lock-{run-id}`
- Execution log: `/tmp/drive-log-{run-id}.md`

## Branch + Bootstrap (manifest mode)

Working tree must be clean before bootstrap. On a dirty tree, refuse and name the resolution paths (commit, stash, discard).

Branch handling: if the current branch equals the resolved base, create a new branch named `claude/<slug-from-manifest-title>-<short-hash>` and check it out. Otherwise reuse the current branch unmodified.

Then create an empty bootstrap commit identifying this as a `/drive` bootstrap for the named manifest. The empty commit lets github mode open a PR from tick 0 (CI + reviewers engage immediately).

**`--platform github`**: push the branch to `origin` (retry transient failures with exponential backoff; never `--force`; never push to a base branch). Open a PR via the available GitHub backend (base = resolved base, head = current branch, title from the manifest's Goal, body referencing the manifest path). If an open PR already exists for the branch, reuse it. Capture the PR number for run-id construction.

**`--platform none`**: no push, no PR.

### Babysit mode (`--platform github` only)

Skip branch creation, commit, push, and PR creation — the user is on a branch with an open PR. Pre-flight already captured the PR number.

## Execution Log Initialization

Create `/tmp/drive-log-{run-id}.md` if absent; append on resumption. Never overwrite.

Seed header captures: manifest path, mode (manifest|babysit), platform, sink, base branch, current branch, PR number (github), interval, max-ticks, scheduler, run-id, timestamp. Scheduler is written once at initialization from the value resolved during Pre-flight; never rewritten on resume.

## Kickoff

After pre-flight, bootstrap, and log initialization succeed, branch by the recorded scheduler.

### Scheduler: `loop`

Invoke `/loop` with the configured interval and `/drive-tick` plus its forwarded flags:

```
Invoke the /loop skill with: "<interval> /drive-tick --run-id <run-id> --mode <mode> --platform <platform> --sink <sink> --log <log-path> --max-ticks <N> [--manifest <manifest-path>] [--pr <pr-number>]"
```

Include `--manifest` only in manifest mode; include `--pr` only in github mode. Then exit — `/drive` does not wait for tick completion.

### Scheduler: `inline-fallback`

Mode announcement already fired during Pre-flight. Invoke `/drive-tick` directly per `references/fallback-inline.md` §Self-Invocation Directive, forwarding the current flags. Subsequent ticks are scheduled by `/drive-tick` per `references/fallback-inline.md` §Chunked-Sleep Protocol. The session is held until terminal state, budget exhaust, or interruption.

### Run summary

Print a concise run summary — run-id, log path, mode, platform, scheduler, and a `tail -f` hint — sufficient for the user to find and observe the run. In `inline-fallback`, note that the session is held until the run ends.

## Multi-repo PR sets

When the manifest declares `Repos:` in Intent (multi-repo changeset), each repo's PR is tended by its own `/drive` invocation pointing at the **same canonical `/tmp` manifest**. Run-id qualification already isolates locks and logs per-PR — no cross-repo collisions. Concurrent amendments to the shared manifest by different ticks are last-writer-wins (no locking; see `manifest-dev:define/references/MULTI_REPO.md` §f). Single-repo manifests are unaffected.

## Gotchas

- **`/loop` reliability is outside `/drive`'s control.** Cron stops firing if the session ends or the host sleeps; the log goes stale. No automatic recovery — re-invoke `/drive` to resume; the tick picks up from log state.
- **Inline-fallback holds the session.** When `/loop` is unavailable, `/drive` auto-selects inline-fallback — see `references/fallback-inline.md` §Gotchas for observable effects (session-held, per-chunk blocking, context accumulation) and mitigation. Keep `--max-ticks` conservative, or install `/loop` to regain cron scheduling.
- **Base branch auto-detection can fail** on repos with unusual configurations (detached `origin/HEAD`, no `main`). Error is explicit — no silent `master` fallback. Pass `--base` to override.
- **Stale lock after crash.** Pre-flight surfaces the PID-liveness classification (live | dead | indeterminate) and the resolution path; the user clears the lock when safe.
- **Run-id collisions** are pre-empted by repo-qualification (github mode, shared `/tmp` across multiple repos) and a collision-resistant suffix (none mode, same-second runs).
- **Budget exhaust stops the loop.** When tick count reaches `--max-ticks`, the tick escalates via sink and ends the loop. Raise `--max-ticks` explicitly if a run genuinely needs more.
- **No explicit stop command.** `/drive` relies on session-level interruption or terminal states (merge, verify-pass, budget exhaust). Closing the session also stops `/loop` from scheduling further ticks.
- **Uncommitted changes block bootstrap** to prevent clobbering in-progress user work.
- **Empty bootstrap commit is intentional.** Lets github mode open a PR from tick 0. If your CI fails on empty commits, the tick's CI triage detects "pre-existing / infrastructure" patterns — but your CI config may still need adjustment.
