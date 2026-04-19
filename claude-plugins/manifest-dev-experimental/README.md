# manifest-dev-experimental

> **Status:** Experimental. Coexists with [`manifest-dev`](../manifest-dev/); nothing deprecated.

Cron-driven, tick-based driver that takes a manifest (or PR in babysit mode) all the way to a terminal state through repeated stateless ticks. Replaces `/do`'s monolithic fix-verify-loop-hook pattern with cross-tick convergence.

## What it ships

- **`/drive`** — user-invocable wrapper. Parses args, validates mode, resolves base branch, pre-flights `/loop` and `manifest-dev`, bootstraps (branch + empty commit + PR for github; branch + empty commit for none), then kicks off `/loop`.
- **`/drive-tick`** — the per-iteration brain. Lean. Each tick: grab lock, read the full execution log (memento), read state via platform adapter, check terminal states, handle inbox, implement inline, invoke `manifest-dev:verify`, fix failures, amend manifest if scope shifts, commit, push — and either return for the next scheduled iteration or end on terminal state or budget exhaust.
- **Pluggable adapters** — `skills/drive/references/platforms/{none,github}.md` and `skills/drive/references/sinks/local.md` follow a consistent markdown-state-report contract. Adding a new platform or sink is a copy-and-adjust.

## Mode matrix

| Mode | `--platform none` | `--platform github` |
|---|---|---|
| **manifest** (manifest path provided) | Valid. Local branch, no PR. Terminal = all `/verify` pass. | Valid. Bootstrap PR with empty commit; tend comments/CI; terminal = merge-ready. |
| **babysit** (no manifest path) | **Rejected at invocation** — no manifest + no PR = nothing to observe. | Valid. Looks up current branch's open PR; errors if missing. Terminal = merge-ready. |

## Quick usage

```bash
# Manifest + local-only loop
/drive .manifest/my-feature.md

# Manifest + GitHub PR lifecycle
/drive .manifest/my-feature.md --platform github

# Babysit an existing PR (manifest absent)
/drive --platform github
```

All flags:

| Flag | Default | Notes |
|---|---|---|
| `--platform` | `none` | `none` \| `github` |
| `--sink` | `local` | `local` |
| `--base` | auto-detect | Override when detection from `origin/HEAD` or `main` fails |
| `--interval` | `30m` | Minimum `30m` (matches lock TTL — prevents parallel ticks). No upper bound enforced. |
| `--max-ticks` | `100` | Positive integer. Tick budget — exceeding it escalates via sink and ends the loop. |

## Observing progress

Each tick writes a status entry to `/tmp/drive-log-{run-id}.md`. No console output between ticks — check the log:

```bash
# github mode: run-id is gh-{owner}-{repo}-{pr}
tail -f /tmp/drive-log-gh-owner-repo-42.md

# none mode: run-id is local-{timestamp}-{4-char-random}
tail -f /tmp/drive-log-local-*.md
```

If the log hasn't updated for a while, either the tick is still running (≤30m) or `/loop` has failed silently — see Gotchas.

## Composition model

Two adapter axes live inside the skill. Triggers are external (the wrapper kicks off `/loop`; other triggers may invoke `/drive-tick` directly in future — possibly from outside Claude Code).

| Axis | What it abstracts | v0 adapters | Future |
|---|---|---|---|
| **Platforms** | How state is read/written (branch, PR, comments, CI) | `none`, `github` | `gitlab`, `bitbucket` |
| **Sinks** | Where escalations/status go | `local` (log file) | `slack`, `discord`, `email` |

Each adapter returns a **markdown-formatted state report**. Platforms must include `## Git State` and `## Terminal Check`; `## Inbox`, `## CI/Checks`, and `## PR State` are included when applicable. Sinks expose `## Escalation Target` on-demand for documentation. The tick consumes the report directly — no structured-data marshalling.

Adding a new adapter = copy an existing one, adjust the sections. See `skills/drive/references/ADAPTER_CONTRACT.md`.

## Coexistence with manifest-dev

`/drive` does **not** replace `/do`, `/tend-pr`, `/tend-pr-tick`, or `/auto` in v0. They all still work and are appropriate in different contexts:

- `/do` — synchronous local execution, internal fix-verify loop, still best for interactive single-run work.
- `/tend-pr` + `/tend-pr-tick` — standalone PR lifecycle without a manifest-driven implementation pass.
- `/auto` — chain `/define` → `/do` → optional `/tend-pr` synchronously.
- `/drive` — cron-driven loop that unifies implement + verify + fix + tend, designed for autonomous long-running runs.

If `/drive` proves out, a later manifest can deprecate the overlapping skills. For now, pick the one that fits.

`manifest-dev-experimental` requires the `manifest-dev` plugin installed: the tick invokes `manifest-dev:verify` and `manifest-dev:define --amend --from-do` as Skill tool calls, and the github adapter preserves `manifest-dev:tend-pr-tick`'s semantics (classification, CI triage, PR sync, thread resolution, merge-ready) adapted to the adapter contract.

## Dependencies checked before bootstrap

`/drive` performs pre-flight checks before any branch/commit/push/PR side effects. It errors actionably if any of these are missing:

- **`/loop` skill** — the cron scheduler that invokes `/drive-tick` on the configured interval.
- **`manifest-dev:verify` and `manifest-dev:define`** — for per-tick verification and mid-tick manifest amendments.
- **GitHub MCP tools** (when `--platform github`) — for PR create/read/comment operations.
- **`/tmp/` persistence across sessions** — the tick reads its log from `/tmp/drive-log-{run-id}.md` on every wake (same assumption `tend-pr-tick` relies on).

If `/loop`'s cron stops firing (host sleep, session ended), `/drive` has no automatic recovery — `/tmp/drive-log-{run-id}.md` will go stale. Check the log; re-invoke `/drive` to resume.

## Recommended `.claude/settings.json` permissions

`manifest-dev-experimental` ships **no hooks**. Protection against irreversible actions is documentation, not enforcement. Add these to your project's `.claude/settings.json` (or user settings) before running `/drive` — especially in `--platform github` mode — so Claude Code prompts you on dangerous operations:

```json
{
  "permissions": {
    "deny": [
      "Bash(git push --force*)",
      "Bash(git push --force-with-lease*)"
    ],
    "ask": [
      "Bash(gh pr merge*)",
      "Bash(git push origin main*)",
      "Bash(git push origin master*)",
      "Bash(git reset --hard*)"
    ]
  }
}
```

Adjust to your workflow. These are **not enforced by the plugin** — they're Claude Code gates. Without them, a runaway or misconfigured tick could force-push, push to main, or merge unreviewed. General system hardening (e.g., blocking `rm -rf` outside the project) belongs in your base settings, not a plugin-specific snippet.

## v0 scope — what is NOT in v0

- **Sinks beyond `local`**: Slack, Discord, email sinks are deferred. Escalations go to the log only.
- **Platforms beyond `github`**: GitLab, Bitbucket, Jira. v0 ships `none` and `github`.
- **Triggers beyond cron**: no webhook listeners, no event-based ticks. External infrastructure can invoke `/drive-tick` directly, but no integration is shipped.
- **Terminal-channel user input**: no `/tell` command, no inbox file. PR comments are the only async input channel (github mode). Local mode has no mid-flight input — user stops by talking to Claude at the session level.
- **Correctness-during-work hooks**: `manifest-dev`'s `/do` ships `PreToolUse` / `PostToolUse` hooks that enforce process and log discipline. `manifest-dev-experimental` ships **none**. `/verify` is the sole gate; bad work in a tick is caught by the next tick's verify and fixed by the tick after.
- **Auto-escalation on no-progress**: loop runs indefinitely in continuing-states until a terminal state, budget exhaust, or user stop. Amendment oscillation has its own guard (escalates after 3 self-amendments without external input).

## Gotchas

- **`/loop` reliability is outside the plugin's control.** If the cron host sleeps or the Claude Code session ends, ticks stop. No recovery.
- **Long ticks (>30m) risk parallel execution.** The 30m lock TTL clears a stale lock after 30 min; if a real tick is still running at that point, the next cron fire will start a second tick. `--interval` is bounded ≥ 30m at invocation to minimize this, but a 60-min implementation pass can still parallelize. Accepted v0 limitation.
- **Lock TOCTOU.** Two ticks may see a stale lock simultaneously and both acquire. The tick re-verifies lock ownership immediately after creation (reads back PID/timestamp); mismatch → exit silently. Rare duplicate work is possible.
- **Crash recovery keeps WIP.** If a prior tick crashed mid-implementation, uncommitted working-tree changes persist. The next tick commits them if the last log entry is consistent with the WIP shape; otherwise it logs a manual-review flag and exits. Never force-resets.
- **Bot comments repeat after push.** Track findings by content, not comment ID. Same rule as `tend-pr-tick`.
- **Amendment oscillation.** If the tick self-amends the manifest repeatedly without new external input (user message or PR comment), it escalates via the sink rather than continuing. Exact threshold and semantics live in `skills/drive-tick/SKILL.md` §Amendment Loop Guard — the one place the number is defined.
- **Budget exhaust is terminal.** Default `--max-ticks 100`. When the completed-tick count in the log reaches the budget, the tick logs `BUDGET EXHAUSTED`, escalates via the sink, removes the lock, and ends the loop.
- **Same-second `none`-mode collisions.** Run IDs in none mode are `local-{timestamp}-{4-char-random}` specifically to avoid collision when two runs start within one second. Github mode uses `gh-{owner}-{repo}-{pr}` to avoid cross-repo PR-number collision when `/tmp` is shared.

## Rolling back

The plugin stores no durable state beyond transient `/tmp/drive-log-*` and `/tmp/drive-lock-*` files. To uninstall: run `/plugin` and uninstall `manifest-dev-experimental`. Any in-flight `/drive` runs should be stopped first (talk to Claude at the session level).

## See also

- [`manifest-dev`](../manifest-dev/) — the parent plugin (`/define`, `/do`, `/verify`, `/tend-pr`, `/auto`, etc.).
- Project root [`README.md`](../../README.md).
