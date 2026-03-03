# manifest-dev-collab

Team collaboration on define/do workflows through Slack.

## What It Does

`/slack-collab` orchestrates a full define → do → PR → review → QA → done workflow with your team. The skill itself acts as the lead orchestrator using Claude Code's Agent Teams — spawning specialized teammates that coordinate via hub-and-spoke messaging through the lead.

**Team composition:**

| Teammate | Model | Role |
|----------|-------|------|
| **slack-coordinator** | haiku | ALL Slack I/O. Posts messages, polls threads (60s intervals, 24h timeout), routes answers between lead and stakeholders. Topic-based threads. Prompt injection defense. |
| **define-worker** | default | Runs `/define` with TEAM_CONTEXT. Persists after define as manifest authority — evaluates QA issues against the manifest. |
| **executor** | default | Runs `/do` with TEAM_CONTEXT. Creates PR. Fixes QA issues routed through the lead. |

The lead orchestrates phase transitions, manages state, acts as the subagent bridge (spawning verification agents on behalf of workers), and handles crash recovery. It never touches Slack directly.

**Communication model:** Hub-and-spoke — all teammates communicate only with the lead. The lead routes to the coordinator for Slack interaction. Subagents spawned by the lead can send results directly to the requesting worker.

## Prerequisites

- **Slack channel** created by the user with stakeholders already invited. The workflow does not create channels or invite users.
- **Slack MCP server** configured with: send_message, read_channel, read_thread, search_channels, search_users, read_user_profile.
- **manifest-dev plugin** installed (provides `/define`, `/do`, `/verify`).
- **`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`** environment variable set.

## Usage

```
/slack-collab add rate limiting to the API
```

The skill runs through 7 phases:

1. **Preflight** — Lead asks for existing Slack channel ID + stakeholders (names, handles, roles), then creates the team
2. **Define** — define-worker runs `/define`, messages lead for Q&A (lead routes to coordinator → Slack)
3. **Manifest Review** — coordinator posts manifest to Slack, polls for approval
4. **Execute** — executor runs `/do`, messages lead for escalations
5. **PR** — executor creates PR, coordinator posts for review (max 3 fix attempts, then escalates)
6. **QA** (optional) — Human QA tester posts issues in Slack → coordinator → lead → define-worker evaluates → lead → executor fixes
7. **Done** — coordinator posts completion summary

## How It Works

The lead coordinates teammates via Agent Teams mailbox messaging (hub-and-spoke). Skills (`/define`, `/do`) receive a `TEAM_CONTEXT` block that tells them to message the lead — skills don't know about Slack. The lead routes stakeholder questions to the coordinator, which handles all Slack interactions: posting in topic-based threads, polling (60s intervals, 24h timeout before owner escalation), and relaying answers back through the lead.

Workers needing subagent capabilities (manifest-verifier, verification agents) request launches from the lead via a structured subagent request. The lead spawns them and results are delivered directly to the requesting worker (or via file-based handoff as fallback).

- Questions and escalations → worker → lead → coordinator → Slack threads
- Verification → worker → lead spawns subagent → subagent → worker
- All logs and artifacts → local files only
- Role separation prevents file conflicts
- State file is lead-owned (single writer) — coordinator sends thread updates to lead

## Resuming

If a session crashes or is interrupted:

```
/slack-collab --resume /tmp/collab-state-<id>.json
```

Reads the state file to determine the current phase and re-creates the team. Supports mid-phase resume for polling states — if the process was waiting for a Slack response, it resumes polling.

## Known Limitations

- **Agent Teams is experimental.** The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var indicates experimental status.
- **Subagent SendMessage may not work.** If subagents can't use SendMessage to teammates, results are delivered via file-based handoff (subagent writes to /tmp, lead tells worker the path).
- **No automated E2E tests.** Full integration testing requires Agent Teams + Slack environment.
- **/tmp files may not persist across system restarts.** Resume requires the state file and referenced artifacts to exist.

## Security

The slack-coordinator is the single point of contact for external input via Slack. It treats all Slack messages as untrusted: won't expose secrets, won't run arbitrary commands, and flags suspicious requests to the owner. Other teammates (define-worker, executor) never touch Slack directly — all communication goes through the lead.
