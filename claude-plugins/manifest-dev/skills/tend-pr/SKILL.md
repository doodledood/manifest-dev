---
name: tend-pr
description: 'Tend a PR through review to merge-readiness. Classifies comments (bot/human, actionable/FP/uncertain), fixes issues via manifest amendment + scoped /do (or directly in babysit mode), tends CI, syncs PR description, and asks before merging. Use when a PR needs tending through review, or to babysit a PR. Triggers: tend pr, babysit pr, review loop, get this merged, tend this PR.'
user-invocable: true
---

# /tend-pr - PR Lifecycle Automation

## Goal

Set up a PR for review and start a polling loop that tends it to merge-readiness. Each iteration is handled by `/tend-pr-tick`. This skill handles setup only, then delegates iteration work.

Two modes:
- **Manifest-aware**: When given a manifest (or one is inferrable from conversation context), routes fixes through manifest amendment + scoped `/do`. The manifest is the intermediary — no direct code fixes.
- **Babysit**: When no manifest is available, fixes actionable comments directly. Same classification and loop structure, but without the manifest intermediary.

## Input

`$ARGUMENTS` = manifest path, PR URL, or omitted. Optionally with `--platform <platform>`, `--interval <duration>`, `--reviewers <usernames>`, and `--log <execution-log-path>`.

**Mode detection:**
1. If argument is a file path ending in `.md` pointing to an existing manifest → **manifest-aware mode**
2. If no argument but conversation context contains a manifest path from a prior `/do` or `/define` run → **manifest-aware mode** (use the inferred manifest)
3. If argument is a PR URL or no manifest is inferrable → **babysit mode** (identify the PR from the argument URL or from the current branch)

**PR resolution (babysit mode without a PR URL argument):** Look up the open PR for the current branch. If no open PR exists, error and halt — babysit mode requires an existing PR to tend (it does not create PRs).

**Flags:**
- `--platform`: PR platform. Default: `github`. Controls how PR operations (create, read comments, check CI) are performed.
- `--interval`: Polling interval for `/loop`. Default: `10m`. Accepts duration format (e.g. `5m`, `15m`).
- `--reviewers`: Comma-separated usernames to request review from (e.g. `--reviewers alice,bob`). Optional — if omitted, no reviewers are requested.
- `--log`: Path to the `/do` execution log from a prior run. Used in manifest-aware mode to pass to scoped `/do` invocations. Optional — if omitted, locate the most recent `/tmp/do-log-*.md` or from conversation context.

**Errors:**
- No argument, no manifest inferrable, and no open PR for current branch: "Error: No manifest or open PR found. Provide a manifest path or PR URL. Usage: /tend-pr <manifest-path-or-pr-url> [--platform github] [--interval 10m] [--reviewers user1,user2]"
- `--platform` value not supported: "Error: Platform '<value>' not yet supported. Currently supported: github"

## Multi-Repo PR Sets

When the manifest declares `Repos:` in Intent (multi-repo changeset), each repo's PR is tended by its own `/tend-pr` invocation pointing at the **same canonical `/tmp` manifest**. PR descriptions stay summary-only — manifests are internal and never embedded in PRs.

All `/tend-pr-tick` instances amend the same shared manifest. There is **no locking and no concurrency engineering**. Concurrent amendments are last-writer-wins; the later write may overwrite the earlier write's amendment block. Recovery: the user notices the missing amendment in the next iteration and re-triggers the lost tick (e.g., re-add the comment, re-run `/tend-pr-tick`). **Do not add file locking** — collisions are rare and the recovery cost is small.

Single-repo manifests (no `Repos:` field) are unaffected — one `/tend-pr`, one PR, no shared-manifest considerations.

Full convention: `references/MULTI_REPO.md` (in `define/references/`) §f.

## Setup

**Manifest-aware mode:** Ensure a non-draft PR exists for the current branch — create one if none exists. Use the manifest's Intent section for PR title/description. If `--reviewers` was provided, request review from those users. Resolve the execution log path (from `--log`, most recent `/tmp/do-log-*.md`, or conversation context).

**Babysit mode:** The PR must already exist (resolved during input). If `--reviewers` was provided, request review from those users.

Create a log file at `/tmp/tend-pr-log-{pr-number}.md`.

Output the PR link: "PR ready for review: <url>"

## Start Loop

Build the tick arguments based on mode:
- **Manifest-aware:** `<pr-number> manifest <manifest-path> <log-path>`
- **Babysit:** `<pr-number> babysit`

Invoke the `/loop` skill with: `<interval> /tend-pr-tick <tick-arguments>`

The tick handles its own lifecycle — terminal states (merge-ready, merged, closed, draft, escalation) are handled within the tick, including user interaction and loop termination.
