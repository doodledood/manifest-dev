---
name: drive
description: 'Experimental cron-driven manifest runner. Bootstraps branch/PR state and kicks off /loop to repeatedly invoke /drive-tick until a terminal state (all verify pass for none mode, merge-ready for github mode) or budget exhaust. Wide ticks, cross-tick convergence, no flow-control hooks. Use when you want /define → green without babysitting, or to autonomously tend a PR. Triggers: drive, run autonomously, take it to green, cron this to completion.'
user-invocable: true
---

# /drive — Experimental Cron-Driven Manifest Runner

## Goal

Take a manifest (or an existing PR in babysit mode) to a terminal state through repeated stateless ticks. This wrapper handles argument parsing, mode validation, `/loop` pre-flight, and bootstrap. After bootstrap, it hands control to `/loop`, which schedules `/drive-tick` on the configured interval until a terminal state, budget exhaust, or user stop.

Coexists with `/do`, `/tend-pr`, `/auto` — does not replace them.

## Input

`$ARGUMENTS` = `[<manifest-path>] [--platform none|github] [--sink local] [--base <branch>] [--interval <duration>] [--max-ticks <N>]`

- `<manifest-path>` — Optional. Absent = **babysit mode** (requires `--platform github`; tends an existing PR based on conversation context + PR comments). Present = **manifest mode** (verify-driven against the manifest).
- `--platform` — `none` (default) or `github`. `none` = local branch only, no PR. `github` = bootstrap PR, tend comments/CI.
- `--sink` — `local` (default). Where escalations and status notifications go.
- `--base` — Override base branch detection. Auto-detected via `git symbolic-ref refs/remotes/origin/HEAD` with `main` fallback.
- `--interval` — Default `30m`. Minimum `30m` (matches lock TTL — prevents parallel ticks when a wide tick exceeds interval). Maximum `24h`.
- `--max-ticks` — Default `100`. Integer `1`–`10000`. Tick budget cap — once exceeded, tick escalates via sink and ends loop. Prevents silent cost runaway.

### Usage error messages

- No `--platform` flag, no manifest path: "Usage: /drive [<manifest-path>] [--platform none|github] [--sink local] [--base <branch>] [--interval <duration>] [--max-ticks <N>]"
- `--platform <unknown>`: "Platform '<value>' not supported. Supported: none | github"
- `--sink <unknown>`: "Sink '<value>' not supported. Supported: local"
- `--interval` outside `30m`–`24h`: "Interval '<value>' out of range. Must be between 30m and 24h (min matches lock TTL to prevent parallel ticks)."
- `--max-ticks` not a positive integer or outside `1`–`10000`: "--max-ticks must be a positive integer between 1 and 10000."

## Mode Resolution

- Manifest mode: `<manifest-path>` provided AND the file exists. Must be a valid manifest per `manifest-dev:define` schema.
- Babysit mode: `<manifest-path>` absent. Requires `--platform github` — `babysit + platform=none` is rejected.

### Rejection

- Manifest mode with unreadable manifest path: "Manifest not found or unreadable: <path>"
- Babysit mode with `--platform none` (or no `--platform` flag): "babysit mode requires --platform github (no manifest + no PR = nothing to observe)"

## Pre-flight (before any side effects)

All pre-flight checks run BEFORE any branch creation, commit, push, or PR operation. If any check fails, the wrapper errors actionably and exits without modifying repository state.

### /loop availability

Use ToolSearch or equivalent mechanism to confirm `/loop` is loaded. If missing: "/loop skill not found — ensure manifest-dev or a compatible loop provider is installed."

### manifest-dev availability

Babysit mode and manifest-mode amendments rely on `manifest-dev:verify` and `manifest-dev:define --amend`. Confirm both are available via ToolSearch. If missing: "manifest-dev skills not found — /drive requires manifest-dev 0.87.0 or newer."

### Git repository

Confirm `git rev-parse --is-inside-work-tree` succeeds. If not: "Not inside a git repository."

### Platform-specific pre-flight

**`--platform github`:**

- Remote configured: `git config remote.origin.url` must return a value. Else: "No `origin` remote configured — required for --platform github."
- GitHub MCP tools available (e.g., `mcp__github__list_pull_requests`). If missing: "GitHub MCP not loaded — required for --platform github."
- Babysit mode requires existing open PR (see Babysit Mode section below).

**`--platform none`:** nothing additional beyond git repository check.

## Base Branch Resolution

Applies in manifest mode only (babysit uses existing PR's base).

1. If `--base <branch>` flag provided: use that.
2. Else: try `git symbolic-ref refs/remotes/origin/HEAD` and strip the `refs/remotes/origin/` prefix.
3. If that fails, try the literal branch `main` (`git rev-parse --verify main`).
4. If none of the above yields a branch: error "Could not detect base branch (no origin/HEAD, no main branch). Pass --base <branch>." Do NOT silently fall back to `master` or any other branch.

Record the resolved base branch in the execution log header.

## Run ID

- **github mode**: `gh-{repo-owner}-{repo-name}-{pr-number}`. Example: `gh-doodledood-manifest-dev-42`.
  - Repo owner/name resolved from `git config remote.origin.url` (parse `github.com/<owner>/<repo>.git`).
  - PR number from bootstrap (newly created PR) or babysit lookup.
- **none mode**: `local-{timestamp}-{4-char-random}`. Example: `local-20260419-152638-k8zq`.
  - Timestamp = ISO-ish `YYYYMMDD-HHMMSS`.
  - Random suffix = 4 lowercase alphanumeric chars. Prevents collision when two none-mode runs start within the same second.

Paths derived from run ID:

- Lock: `/tmp/drive-lock-{run-id}`
- Execution log: `/tmp/drive-log-{run-id}.md`

## Branch Resolution

Applies in manifest mode only.

1. Read current branch: `git symbolic-ref --short HEAD`.
2. If current branch equals resolved base branch:
   - Generate a new branch name: `claude/<slug-from-manifest-title>-<4-char-hash>`.
     - Slug = lowercase, hyphenated, first 40 chars of `Title` from manifest's heading or Intent.Goal.
     - Hash = 4 lowercase alphanumeric chars (same generator as run-id random suffix).
   - Create and check out: `git checkout -b <new-branch>`.
3. If current branch differs from base: use current branch as-is. Do not modify.

Uncommitted changes on the branch before bootstrap:

- If any uncommitted changes exist: error "Uncommitted changes on current branch. Commit, stash, or discard before starting /drive."

## Bootstrap

Applies in manifest mode.

### `--platform github`

1. Create an empty commit: `git commit --allow-empty -m "drive: bootstrap for <manifest-title>"`.
2. Push: `git push -u origin <branch-name>`. Retry on network failure per CLAUDE.md `git push` protocol.
3. Open PR via `mcp__github__create_pull_request` (base = resolved base, head = branch, title from manifest `## 1. Intent & Context` Goal, body references manifest path). If `mcp__github__list_pull_requests` already shows an open PR for this branch, skip creation and reuse the existing PR.
4. Capture PR number for run-id construction.

### `--platform none`

1. Create an empty commit (same form as github mode).
2. No push, no PR.

### Babysit Mode (`--platform github` only)

1. Skip branch creation, commit, push, PR — user is already on a branch with an open PR.
2. Look up current branch's open PR:
   - `mcp__github__list_pull_requests` with `head = <current-branch>`, `state = open`.
   - If zero open PRs: error "No open PR for current branch. Babysit mode requires an existing open PR."
   - If multiple open PRs: error "Multiple open PRs for current branch. Resolve ambiguity before invoking /drive."
3. Capture PR number.

## Execution Log Initialization

Create `/tmp/drive-log-{run-id}.md` if it does not already exist. If it does exist (resumption or collision), append to it — do not overwrite.

Seed header includes: manifest path, mode (manifest|babysit), platform, sink, base branch, current branch, PR number (if github), interval, max-ticks, run-id, timestamp.

## /loop Kickoff

After all pre-flight, bootstrap, and log initialization succeed, invoke `/loop` with the configured interval and `/drive-tick` plus flag-based arguments (no positional args — optional flags can be absent without disturbing the rest of the invocation):

```
Invoke the /loop skill with: "<interval> /drive-tick --run-id <run-id> --mode <mode> --platform <platform> --sink <sink> --log <log-path> --interval <interval> --max-ticks <N> [--manifest <manifest-path>] [--pr <pr-number>]"
```

Include `--manifest` only in manifest mode; include `--pr` only when platform is github. The `--interval` is passed through so the tick can schedule its own next iteration with the same cadence.

Then exit. `/drive` returns after /loop acknowledges the schedule — it does not wait for tick completion.

Print the run summary to the terminal:

```
/drive started — run-id: <run-id>
Mode: <mode> | Platform: <platform> | Sink: <sink> | Interval: <interval> | Budget: <max-ticks> ticks
Branch: <branch>  [PR #<pr-number> if github]
Log: /tmp/drive-log-<run-id>.md

Observe progress with: tail -f /tmp/drive-log-<run-id>.md
```

## Gotchas

- **`/loop` reliability is outside /drive's control.** If cron stops firing (session ends, host sleeps), ticks stop. No automatic recovery — the log will go stale. Re-invoke `/drive` to resume. The tick is designed to pick up from log state.
- **Base branch auto-detection can fail** on repos with unusual configurations (detached HEAD on remote, no `origin/HEAD`, no `main` branch). The error is explicit — no silent fallback to `master`. Pass `--base <branch>` to override.
- **Interval/TTL coupling.** `--interval ≥ 30m` is enforced at invocation because the lock TTL is 30m. If a wide tick takes longer than the interval, a second cron fire could acquire a stale lock and parallelize work. The enforcement reduces this risk but does not eliminate it for real ticks exceeding 30m (accepted v0 limit).
- **Run-id collision mitigations.** Github-mode run-ids are qualified by repo owner/name to avoid collision when `/tmp` is shared across multiple repositories with overlapping PR numbers. None-mode run-ids include a 4-char random suffix to avoid collision when two none-mode runs start within the same second.
- **Budget exhaust stops the loop.** If the tick count in the log reaches `--max-ticks`, the tick escalates via the sink and ends the loop. Budget prevents silent cost runaway; raise `--max-ticks` explicitly if a run genuinely needs more ticks.
- **No explicit stop command.** `/drive` relies on Claude Code session-level interruption (user talks to Claude, who removes the lock if needed) or terminal states (merge, verify-pass, budget exhaust). Closing the Claude Code session also stops `/loop` from scheduling further ticks.
- **Uncommitted changes block bootstrap.** `/drive` refuses to bootstrap if the working tree is dirty — prevents clobbering in-progress user work. Commit, stash, or discard first.
- **Empty commit is intentional.** The bootstrap commit has no diff; it exists so github mode can open a PR from tick 0 (allowing CI and reviewers to engage immediately). If your CI fails on empty commits, this will fail the first tick's CI check — the tick's CI triage handles this by detecting "pre-existing / infrastructure" patterns, but your CI config may need adjustment.
