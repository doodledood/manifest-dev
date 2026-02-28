# manifest-dev-collab

Team collaboration on define/do workflows through Slack.

## What It Does

`/slack-collab` orchestrates a full define → do → PR → review → QA → done workflow with your team. The skill itself acts as the lead orchestrator using Claude Code's Agent Teams — spawning specialized teammates that coordinate via mailbox messaging.

**Team composition:**

| Teammate | Role |
|----------|------|
| **slack-coordinator** | ALL Slack I/O. Creates channels, posts messages, polls for responses, routes answers between teammates and stakeholders. Owns prompt injection defense. |
| **define-worker** | Runs `/define` with TEAM_CONTEXT. Persists after define as manifest authority — evaluates QA issues against the manifest. |
| **executor** | Runs `/do` with TEAM_CONTEXT. Creates PR. Fixes QA issues flagged by define-worker. |

The lead (the `/slack-collab` skill session) orchestrates phase transitions, manages state, and handles crash recovery. It never touches Slack directly.

## Prerequisites

- **Slack MCP server** configured and available. The slack-coordinator verifies Slack tools on first action and fails fast if missing.
- **manifest-dev plugin** installed (provides `/define`, `/do`, `/verify`).
- **`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`** environment variable set (enables Agent Teams).

## Usage

```
/slack-collab add rate limiting to the API
```

The skill runs through 7 phases:

1. **Preflight** — Lead asks for stakeholders (names, Slack handles, roles) via AskUserQuestion, then creates the team
2. **Define** — define-worker runs `/define`, messages slack-coordinator for stakeholder Q&A
3. **Manifest Review** — slack-coordinator posts manifest to Slack, polls for approval
4. **Execute** — executor runs `/do`, messages slack-coordinator for escalations
5. **PR** — executor creates PR, slack-coordinator posts for review (max 3 fix attempts, then escalates)
6. **QA** (optional) — QA issues route: slack-coordinator → define-worker (evaluate against manifest) → executor (fix) → slack-coordinator (report)
7. **Done** — slack-coordinator posts completion summary

The owner has final say on all decisions and can answer in any stakeholder's thread to unblock.

## How It Works

The lead orchestrator coordinates teammates via Agent Teams mailbox messaging. Skills (`/define`, `/do`) receive a `TEAM_CONTEXT` block that tells them to message the slack-coordinator teammate instead of using AskUserQuestion — skills don't know about Slack. The slack-coordinator handles all Slack interactions: posting questions, polling for responses (30s intervals, 2-hour timeout), and relaying answers back.

- Questions and escalations → teammate messages → slack-coordinator → Slack threads
- All logs and artifacts → local files only (Slack is for collaboration, not observability)
- Role separation prevents file conflicts: executor owns code, define-worker owns manifest, slack-coordinator owns Slack

State is persisted to a JSON file in `/tmp` after every phase transition, enabling crash recovery.

## Resuming

If a session crashes or is interrupted:

```
/slack-collab --resume /tmp/collab-state-<id>.json
```

Reads the state file to determine the current phase and re-creates the team from saved context. Recovery granularity is per-phase — mid-phase progress (e.g., halfway through a `/define` interview) is lost on crash.

## Known Limitations

- **Agent Teams is experimental.** The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var indicates this is an experimental Claude Code feature. If removed or changed, this plugin will need updates.
- **No mid-phase crash recovery.** If a teammate dies mid-`/define` or mid-`/do`, the lead re-spawns it once with the same task. If the second attempt fails, the lead writes state and stops.
- **No automated E2E tests.** Verification is via subagent review of prompts and flow. Full integration testing requires Agent Teams + Slack environment.

## Security

The slack-coordinator is the single point of contact for external input via Slack. It treats all Slack messages as untrusted: won't expose secrets, won't run arbitrary commands, and flags suspicious requests to the owner. Other teammates (define-worker, executor) never touch Slack directly.
