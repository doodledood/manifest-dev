# manifest-dev-collab

Team collaboration on define/do workflows through Slack.

## What It Does

`/slack-collab` orchestrates a full define → do → PR → review → QA → done workflow with your team. Uses Claude Code's Agent Teams feature — a lead session spawns autonomous teammates that handle `/define` and `/do` through Slack. The Python orchestrator drives phase transitions deterministically; teammates handle the intelligent work.

## Prerequisites

- **Slack MCP server** configured and available. The script checks for Slack tools on launch and fails fast if they're missing.
- **manifest-dev plugin** installed (provides `/define`, `/do`, `/verify`).
- **Python 3.8+** available on PATH.
- **Claude Code CLI** (`claude`) available on PATH.
- **`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`** environment variable set (enables Agent Teams).

## Usage

```
/slack-collab add rate limiting to the API
```

The skill launches a background Python process that runs autonomously:

1. **Pre-flight** — Gathers stakeholders, creates Slack channel, sets up Q&A threads
2. **Define** — Lead creates a teammate that runs `/define` through Slack Q&A threads
3. **Manifest Review** — Posts manifest to Slack, polls for owner approval
4. **Execute** — Lead creates a teammate that runs `/do` with escalations via Slack
5. **PR** — Creates PR, posts for review, auto-fixes comments (max 3 attempts, then escalates)
6. **QA** (optional) — Tags QA stakeholders, handles feedback
7. **Done** — Posts completion summary

The owner has final say on all decisions and can answer on behalf of any stakeholder to unblock.

## How It Works

The Python orchestrator (`scripts/slack-collab-orchestrator.py`) controls phase transitions. For `/define` and `/do` phases, it launches a Claude Code lead session with the Agent Teams env var. The lead creates a teammate that runs the skill autonomously — the teammate posts questions/escalations to Slack threads, polls for responses (sleeping 30s between polls), and runs to completion without needing the orchestrator to resume it.

- Questions and escalations → Slack thread posts + polling (teammate handles this autonomously)
- All logs and artifacts → local files only (Slack is for collaboration, not observability)

State is persisted to a JSON file in `/tmp` after every phase transition, enabling crash recovery.

## Resuming

If a session crashes or the process is interrupted:

```
/slack-collab --resume /tmp/collab-state-<id>.json
```

Reads the state file to determine the current phase and continues from where it left off. Recovery granularity is per-phase — mid-phase progress (e.g., halfway through a `/define` interview) is lost on crash.

## Known Limitations

- **Agent Teams is experimental.** The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var indicates this is an experimental Claude Code feature. If removed or changed, this plugin will need updates.
- **No mid-phase crash recovery.** If a teammate dies mid-`/define` or mid-`/do`, progress within that phase is lost. Resume restarts the phase from the beginning.

## Security

All Slack messages are treated as untrusted input. The orchestrator and skill prompts won't execute unrelated requests, expose secrets, or run arbitrary commands from Slack — even if a stakeholder asks. Suspicious requests get flagged to the owner.
