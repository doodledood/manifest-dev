---
name: drive
description: 'Experimental tick-based manifest runner. Bootstraps branch/PR state and kicks off /loop — or an inline-fallback scheduler when /loop isn''t available — to repeatedly invoke /drive-tick until a terminal state (all verify pass for none mode, merge-ready for github mode) or budget exhaust. Wide ticks with intra-tick convergence — /drive-tick delegates the full verify-fix loop to /do per tick. Use when you want /define → green without babysitting, or to autonomously tend a PR. Triggers: drive, run autonomously, take it to green, cron this to completion.'
user-invocable: true
---

# /drive — Experimental Cron-Driven Manifest Runner

## Goal

Take a manifest (or an existing PR in babysit mode) to a terminal state through repeated stateless ticks. This wrapper handles argument parsing, mode validation, pre-flight, and bootstrap, then hands control to the scheduler — `/loop` when available, the inline-fallback scheduler otherwise — to schedule `/drive-tick` on the configured interval. In loop mode, `/drive` exits immediately after kickoff and ongoing work happens in scheduled tick invocations. In inline-fallback mode, the scheduler runs inside the Claude session and `/drive` holds until a terminal state or budget exhaust — see `references/fallback-inline.md`.

Coexists with `/do`, `/tend-pr`, `/auto` — does not replace them.

**Multi-repo PR sets:** when the manifest declares `Repos:` in Intent (multi-repo changeset), each repo's PR is tended by its own `/drive` invocation pointing at the **same canonical `/tmp` manifest**. Run-id qualification (`gh-{owner}-{repo}-{pr-number}` in github mode) already isolates locks (`/tmp/drive-lock-{run-id}`) and execution logs (`/tmp/drive-log-{run-id}.md`) per-PR — no cross-repo collisions. Concurrent amendments to the shared manifest by different ticks are last-writer-wins (no locking; see `manifest-dev:tend-pr/SKILL.md` §Multi-Repo PR Sets and `manifest-dev:define/references/MULTI_REPO.md` §f). Single-repo manifests are unaffected.

## Input

`$ARGUMENTS` = `[<manifest-path>] [--platform none|github] [--sink local] [--base <branch>] [--interval <duration>] [--max-ticks <N>]`

- `<manifest-path>` — Optional. Absent = **babysit mode** (requires `--platform github`; tends an existing PR based on conversation context + PR comments). Present = **manifest mode** (verify-driven against the manifest).
- `--platform` — `none` (default) or `github`. `none` = local branch only, no PR. `github` = bootstrap PR, tend comments/CI.
- `--sink` — `local` (default). Where escalations and status notifications go.
- `--base` — Override base branch auto-detection.
- `--interval` — Default `15m`. Range `15m`–`24h` inclusive. The lower bound is set so that the cron fires at a cadence useful for typical ticks. While a tick holds its lock, subsequent cron fires exit silently — so the interval is a floor for poll frequency, not a hard cadence. Upper bound catches obvious typos.
- `--max-ticks` — Default `100`. Positive integer, `1`–`10000` inclusive. Tick budget cap — once exceeded, tick escalates via sink and ends loop. Prevents silent cost runaway.

### Usage error messages

- `--platform <unknown>`: "Platform '<value>' not supported. Supported: none | github"
- `--sink <unknown>`: "Sink '<value>' not supported. Supported: local"
- `--interval` outside `15m`–`24h`: "Interval '<value>' out of range. Must be between 15m and 24h."
- `--max-ticks` outside `1`–`10000`: "--max-ticks must be a positive integer between 1 and 10000."

## Mode Resolution

- Manifest mode: `<manifest-path>` provided AND the file exists. Must be a valid manifest per `manifest-dev:define` schema.
- Babysit mode: `<manifest-path>` absent. Requires `--platform github` — `babysit + platform=none` is rejected.

### Rejection

- Manifest mode with unreadable manifest path: "Manifest not found or unreadable: <path>"
- Babysit mode with `--platform none` (or no `--platform` flag): "babysit mode requires --platform github (no manifest + no PR = nothing to observe)"

## Pre-flight (before any side effects)

All pre-flight checks run BEFORE any branch creation, commit, push, or PR operation. If any check fails, the wrapper errors actionably and exits without modifying repository state.

- **Scheduler resolution.** Check Claude's system-prompt skills list for a skill with `name: loop`. If present, `scheduler = loop`. If absent, `scheduler = inline-fallback` and the run follows `references/fallback-inline.md` for the fallback protocol. Record the value once in the execution log seed header; never re-evaluate during the run.
- **Announce before side effects.** In inline-fallback only: print the line from `references/fallback-inline.md` §Announce Protocol before any side-effecting operation in this skill (covers at least the operations named in the opening paragraph of this section, plus lock creation and log initialization). Read-only pre-flight checks may precede the announcement; side-effecting ones may not.
- **`manifest-dev:do`, `manifest-dev:verify`, and `manifest-dev:define` available** (drive-tick invokes `manifest-dev:do` directly and `manifest-dev:define --amend` during Amendment; `manifest-dev:verify` is required transitively by `/do`). Error: "manifest-dev skills not found — /drive requires manifest-dev."
- **Inside a git repo.** Error: "Not inside a git repository."
- **Manifest mode: manifest file readable and parseable** as a `manifest-dev:define` manifest. Error: "Manifest not found, unreadable, or malformed: <path>"
- **`--platform github`:** `origin` remote configured (error: "No `origin` remote configured — required for --platform github") AND GitHub MCP tools loaded (error: "GitHub MCP not loaded — required for --platform github") AND, in babysit mode, exactly one open PR for the current branch (see Babysit Mode below).
- **`--platform none`:** nothing beyond the git repo check.
- **Resolve run-id (read-only lookup, no side effects).** In github mode, query for an existing open PR on the current branch via GitHub MCP (no PR creation). Use the returned PR number to compute `gh-{owner}-{repo}-{pr-number}`. If no open PR exists (first-time run on this branch), skip to bootstrap — no lock can exist for an unresolved run-id. In none mode, compute `local-{UTC-timestamp}-{4-char-random}` (fresh run-id every invocation — see §Run ID).
- **No conflicting lock for the resolved run-id.** Once the run-id is known, if `/tmp/drive-lock-{run-id}` exists, /drive halts with an error message naming the lock path, creation timestamp, and recorded PID. Three branches by PID liveness (via `kill -0 <pid>`):
  - **Alive** (signal succeeds): "A /drive run is already active for this PR — wait for it to complete or stop it at the Claude session level."
  - **Dead** (signal returns ESRCH): "A prior /drive run was interrupted or crashed. Remove the lock file and re-invoke /drive to resume."
  - **Ambiguous** (EPERM or liveness introspection unsupported — e.g., cross-UID containers): "Cannot determine whether the PID is live. If you're sure no other /drive is running, remove the lock file; otherwise wait."
  /drive never removes the lock itself — the user confirms before clearing.

## Base Branch Resolution

Applies in manifest mode only (babysit uses the existing PR's base).

Resolve in this order: `--base <branch>` flag → the remote's default branch (via `origin/HEAD`) → the literal branch `main`. If none resolve, error: "Could not detect base branch. Pass --base <branch>." Never silently fall back to `master`.

Record the resolved base branch in the execution log header.

## Run ID

Format:

- **github mode**: `gh-{repo-owner}-{repo-name}-{pr-number}` (example: `gh-doodledood-manifest-dev-42`). Repo owner/name come from the `origin` remote URL. PR number is finalized after bootstrap (newly created PR) or babysit PR lookup — run-id is therefore known before log initialization but not before pre-flight.
- **none mode**: `local-{UTC-timestamp}-{4-char-random}` (example: `local-20260419-152638-k8zq`). Timestamp is `YYYYMMDD-HHMMSS` in UTC. The 4-char random suffix (lowercase alphanumeric) prevents collision when two none-mode runs start within the same second.

Paths derived from run ID:

- Lock: `/tmp/drive-lock-{run-id}`
- Execution log: `/tmp/drive-log-{run-id}.md`

## Branch + Bootstrap (manifest mode)

Working-tree must be clean. If uncommitted changes exist, error: "Uncommitted changes on current branch. Commit, stash, or discard before starting /drive."

If the current branch equals the resolved base, create a new branch named `claude/<slug>-<4-char-hash>` from the manifest title (slug = lowercase, hyphenated, first 40 chars of the manifest's title heading or Intent.Goal; hash = 4 lowercase alphanumeric chars) and check it out. Otherwise reuse the current branch unmodified.

Then create an empty bootstrap commit identifying this as a `/drive` bootstrap for the named manifest.

**`--platform github`:** push the branch to `origin`. Retry transient push failures with exponential backoff. Never `--force`, never push to a base branch. Then open a PR via GitHub MCP with base = resolved base, head = current branch, title from the manifest's Goal, and body referencing the manifest path. If an open PR already exists for this branch, reuse it. Capture the PR number for run-id construction.

**`--platform none`:** no push, no PR.

### Babysit mode (`--platform github` only)

Skip branch creation, commit, push, and PR creation — the user is already on a branch with an open PR. Look up the current branch's open PR. Zero open PRs → error: "No open PR for current branch. Babysit mode requires an existing open PR." Multiple open PRs → error: "Multiple open PRs for current branch. Resolve ambiguity before invoking /drive." Capture the PR number.

## Execution Log Initialization

Create `/tmp/drive-log-{run-id}.md` if it does not already exist. If it does exist (resumption or collision), append to it — do not overwrite.

Seed header includes: manifest path, mode (manifest|babysit), platform, sink, base branch, current branch, PR number (if github), interval, max-ticks, scheduler (`loop` | `inline-fallback`), run-id, timestamp. The scheduler field is written once at initialization from the value resolved during §Pre-flight; it is never rewritten on resume.

## Kickoff

After all pre-flight, bootstrap, and log initialization succeed, branch by the scheduler recorded in the seed header.

### Scheduler: `loop`

Invoke `/loop` with the configured interval and `/drive-tick` plus its flag-based arguments:

```
Invoke the /loop skill with: "<interval> /drive-tick --run-id <run-id> --mode <mode> --platform <platform> --sink <sink> --log <log-path> --max-ticks <N> [--manifest <manifest-path>] [--pr <pr-number>]"
```

Include `--manifest` only in manifest mode; include `--pr` only when platform is github. Then exit — `/drive` does not wait for tick completion.

### Scheduler: `inline-fallback`

The mode announcement already fired during §Pre-flight (see §Scheduler resolution). Invoke `/drive-tick` directly per `references/fallback-inline.md` §Self-Invocation Directive, forwarding the current flags. Subsequent ticks are scheduled by `/drive-tick` itself per `references/fallback-inline.md` §Chunked-Sleep Protocol and §Self-Invocation Directive. `/drive` does not exit in this mode; the session is held until a terminal state, budget exhaust, or user interruption.

### Run summary

Print a run summary to the terminal: run-id, mode, platform, sink, scheduler, interval, budget, branch, PR number (github mode only), log path, and a `tail -f` hint for observing progress. In `loop`, `/drive` exits after kickoff and ongoing work happens in scheduled `/drive-tick` invocations. In `inline-fallback`, add a one-line reminder that the session is held until the run ends.

## Gotchas

- **`/loop` reliability is outside /drive's control.** If cron stops firing (session ends, host sleeps), ticks stop. No automatic recovery — the log will go stale. Re-invoke `/drive` to resume. The tick is designed to pick up from log state.
- **Inline-fallback scheduler holds the session.** When `/loop` is unavailable, `/drive` auto-selects the inline-fallback scheduler — see `references/fallback-inline.md` §Gotchas for observable effects (session-held, per-chunk blocking, context accumulation) and mitigation. Keep `--max-ticks` conservative, or install `/loop` to regain cron scheduling. Stale-lock recovery after mid-sleep interrupt: see §Pre-flight.
- **Base branch auto-detection can fail** on repos with unusual configurations (detached HEAD on remote, no `origin/HEAD`, no `main` branch). The error is explicit — no silent fallback to `master`. Pass `--base <branch>` to override.
- **Stale lock after crash** — see §Pre-flight.
- **Run-id collision mitigations.** Github-mode run-ids are qualified by repo owner/name to avoid collision when `/tmp` is shared across multiple repositories with overlapping PR numbers. None-mode run-ids include a 4-char random suffix to avoid collision when two none-mode runs start within the same second.
- **Budget exhaust stops the loop.** If the tick count in the log reaches `--max-ticks`, the tick escalates via the sink and ends the loop. Budget prevents silent cost runaway; raise `--max-ticks` explicitly if a run genuinely needs more ticks.
- **No explicit stop command.** `/drive` relies on Claude Code session-level interruption (user talks to Claude, who removes the lock if needed) or terminal states (merge, verify-pass, budget exhaust). Closing the Claude Code session also stops `/loop` from scheduling further ticks.
- **Uncommitted changes block bootstrap.** `/drive` refuses to bootstrap if the working tree is dirty — prevents clobbering in-progress user work. Commit, stash, or discard first.
- **Empty commit is intentional.** The bootstrap commit has no diff; it exists so github mode can open a PR from tick 0 (allowing CI and reviewers to engage immediately). If your CI fails on empty commits, this will fail the first tick's CI check — the tick's CI triage handles this by detecting "pre-existing / infrastructure" patterns, but your CI config may need adjustment.
