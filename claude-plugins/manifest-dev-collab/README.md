# manifest-dev-collab

Team collaboration on define/do workflows through Slack.

## What It Does

`/slack-collab` orchestrates a full define → do → PR → review → QA → done workflow with your team. A Python script drives phase transitions deterministically, invoking Claude Code CLI for intelligent work (stakeholder Q&A, manifest building, code execution). Slack is the collaboration medium — stakeholder Q&A, manifest review, escalations, PR review.

## Prerequisites

- **Slack MCP server** configured and available. The script checks for Slack tools on launch and fails fast if they're missing.
- **manifest-dev plugin** installed (provides `/define`, `/do`, `/verify`).
- **Python 3.8+** available on PATH.
- **Claude Code CLI** (`claude`) available on PATH.

## Usage

```
/slack-collab add rate limiting to the API
```

The skill launches a background Python process that runs autonomously:

1. **Pre-flight** — Gathers stakeholders, creates Slack channel, sets up Q&A threads
2. **Define** — Runs `/define` interview through stakeholder Q&A threads
3. **Manifest Review** — Posts manifest to Slack, polls for owner approval
4. **Execute** — Runs `/do` with escalations via Slack
5. **PR** — Creates PR, posts for review, auto-fixes comments (max 3 attempts, then escalates)
6. **QA** (optional) — Tags QA stakeholders, handles feedback
7. **Done** — Posts completion summary

The owner has final say on all decisions and can answer on behalf of any stakeholder to unblock.

## How It Works

The Python orchestrator (`scripts/slack-collab-orchestrator.py`) controls phase transitions and passes a `COLLAB_CONTEXT` block to `/define` and `/do` that switches their behavior:

- AskUserQuestion → Slack thread posts + polling
- Escalation → owner's stakeholder thread
- All logs and artifacts → local files only (Slack is for collaboration, not observability)

State is persisted to a JSON file in `/tmp` after every phase transition, enabling crash recovery.

## Resuming

If a session crashes or the process is interrupted:

```
/slack-collab --resume /tmp/collab-state-<id>.json
```

Reads the state file to determine the current phase and continues from where it left off.

## Security

All Slack messages are treated as untrusted input. The orchestrator and skill prompts won't execute unrelated requests, expose secrets, or run arbitrary commands from Slack — even if a stakeholder asks. Suspicious requests get flagged to the owner.
