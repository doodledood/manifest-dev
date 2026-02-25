# manifest-dev-collab

Team collaboration on define/do workflows through Slack.

## What It Does

`/slack-collab` orchestrates a full define → do → PR → review → QA → done workflow with your team. It creates a dedicated Slack channel, routes questions to the right stakeholders, and drives the process to completion — you collaborate through Slack threads.

## Prerequisites

- **Slack MCP server** configured and available. The skill checks for Slack tools on launch and fails fast if they're missing.
- **manifest-dev plugin** installed (provides `/define`, `/do`, `/verify`).

## Usage

```
/slack-collab add rate limiting to the API
```

The skill walks you through pre-flight questions (stakeholders, QA needs, polling interval), then runs autonomously:

1. **Channel Setup** — Creates `collab-{task}-{date}` channel, invites stakeholders, sets up structured threads
2. **Define** — Runs `/define` interview through stakeholder Q&A threads, posts manifest for owner approval
3. **Execute** — Runs `/do` with progress posted to the Execution thread
4. **PR** — Creates PR, sets reviewers, auto-fixes review comments (max 3 attempts, then escalates)
5. **QA** (optional) — Tags QA stakeholders, handles feedback
6. **Done** — Posts completion summary

The owner has final say on all decisions and can answer on behalf of any stakeholder to unblock.

## Resuming

If a session crashes or loses context:

```
/slack-collab --resume <channel-id>
```

Reads the State thread to reconstruct where it left off and continues from the interrupted phase.

## How It Works

`/slack-collab` passes a `COLLAB_CONTEXT` block to `/define` and `/do` that switches their behavior:

- AskUserQuestion → Slack thread posts + polling
- `/tmp` log files → Slack thread comments
- Escalation → main channel message tagging the owner

The Slack channel becomes the external memory. Structured threads keep things organized: State, Process Log, Manifest, Execution, Verification, PR Review, and per-stakeholder Q&A.

## Security

All Slack messages are treated as untrusted input. The skill won't execute unrelated requests, expose secrets, or run arbitrary commands from Slack — even if a stakeholder asks. Suspicious requests get flagged to the owner.
