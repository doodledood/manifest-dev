# manifest-dev-collab

Team collaboration on define/do workflows through Slack and GitHub.

## What It Does

`/slack-collab` orchestrates a full define → do → PR → review → QA → done workflow with your team. The skill itself acts as the lead orchestrator using Claude Code's Agent Teams — spawning specialized teammates that coordinate via hub-and-spoke messaging through the lead.

**Team composition:**

| Teammate | Model | Role | Spawned |
|----------|-------|------|---------|
| **slack-coordinator** | sonnet | ALL Slack I/O. Posts messages, polls threads (30s intervals, 24h timeout), routes answers between lead and stakeholders. Topic-based threads. Prompt injection defense. | Phase 0 |
| **define-worker** | default | Runs `/define` with TEAM_CONTEXT. Persists after define as manifest authority — evaluates QA issues against the manifest. | Phase 0 |
| **executor** | default | Runs `/do` with TEAM_CONTEXT. Creates PR. Fixes QA issues routed through the lead. | Phase 0 |
| **github-coordinator** | sonnet | ALL GitHub PR I/O. Polls reviews, comments, CI status. Batched reports to lead. Persists through QA for late PR activity. | Phase 4 |

The lead orchestrates phase transitions, manages state, acts as the subagent bridge (spawning verification agents on behalf of workers), and handles crash recovery. It never touches Slack or GitHub directly.

**Communication model:** Hub-and-spoke — all teammates communicate only with the lead. The lead routes to the slack-coordinator for Slack interaction and to the github-coordinator for GitHub PR monitoring. Subagents spawned by the lead can send results directly to the requesting worker.

## Prerequisites

- **Slack channel** created by the user with stakeholders already invited. The workflow does not create channels or invite users.
- **Slack MCP server** configured with: send_message, read_channel, read_thread, search_channels, search_users, read_user_profile.
- **GitHub access** via `gh` CLI (authenticated) or GitHub MCP server. Used for PR review monitoring in Phase 4+.
- **manifest-dev plugin** installed (provides `/define`, `/do`, `/verify`).
- **`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`** environment variable set.

## Usage

```
/slack-collab add rate limiting to the API
```

The skill runs through 7 phases:

1. **Preflight** — Lead asks for existing Slack channel ID + stakeholders (names, handles, roles), then creates the team
2. **Define** — define-worker runs `/define`, messages lead for Q&A (lead routes to slack-coordinator → Slack)
3. **Manifest Review** — slack-coordinator posts manifest to Slack, polls for approval
4. **Execute** — executor runs `/do`, messages lead for escalations
5. **PR Review** — executor creates PR, github-coordinator monitors reviews/comments/CI on GitHub. Fix loop: github-coordinator → lead → define-worker evaluates → executor fixes. PR done when approved + no unresolved + CI green.
6. **QA** (optional) — Human QA via Slack + github-coordinator still monitors PR. Both fix loops operate in parallel.
7. **Done** — slack-coordinator posts completion summary, all teammates shut down

## Architecture

```mermaid
graph TB
    User([User in Terminal])

    subgraph "Agent Teams"
        Lead["Lead<br/>(Orchestrator)"]

        subgraph "Phase 0 Teammates"
            SC["slack-coordinator<br/>(sonnet)"]
            DW["define-worker<br/>(default)"]
            EX["executor<br/>(default)"]
        end

        subgraph "Phase 4+ Teammate"
            GC["github-coordinator<br/>(sonnet)"]
        end
    end

    Slack[(Slack Channel)]
    GitHub[(GitHub PR)]
    Codebase[(Codebase)]

    User <-->|"preflight + escalations"| Lead

    Lead <-->|"post/poll requests"| SC
    Lead <-->|"/define Q&A + QA eval"| DW
    Lead <-->|"/do + PR + fixes"| EX
    Lead <-->|"PR status reports"| GC

    SC <-->|"messages + threads"| Slack
    GC <-->|"reviews + CI + comments"| GitHub
    EX -->|"code changes + PR creation"| Codebase
    EX -->|"create PR + push"| GitHub
    DW -->|"manifest"| Codebase
```

```mermaid
sequenceDiagram
    participant U as User
    participant L as Lead
    participant SC as slack-coordinator
    participant DW as define-worker
    participant EX as executor
    participant GC as github-coordinator
    participant S as Slack
    participant G as GitHub

    Note over L: Phase 0: Preflight
    U->>L: Channel + stakeholders
    L->>SC: Spawn + kickoff
    L->>DW: Spawn
    L->>EX: Spawn
    SC->>S: Post kickoff message

    Note over L: Phase 1: Define
    L->>DW: Run /define
    DW->>L: Q&A questions
    L->>SC: Route questions
    SC->>S: Post to stakeholders
    S-->>SC: Stakeholder answers
    SC->>L: Relay answers
    L->>DW: Relay answers
    DW->>L: Manifest complete

    Note over L: Phase 2: Manifest Review
    L->>SC: Post manifest for review
    SC->>S: Post + tag stakeholders
    S-->>SC: Approval
    SC->>L: Approved

    Note over L: Phase 3: Execute
    L->>EX: Run /do
    EX->>L: Complete

    Note over L: Phase 4: PR Review (GitHub)
    L->>EX: Create PR
    EX->>G: Open PR
    EX->>L: PR URL
    L->>GC: Spawn with PR URL
    L->>SC: Post informational
    SC->>S: "PR opened — review on GitHub"

    loop Fix Loop
        GC->>G: Poll reviews/CI/comments
        GC->>L: Batch status report
        L->>DW: Evaluate against ACs
        DW->>L: Fix instructions
        L->>EX: Fix + push
        EX->>G: Push fixes
    end
    GC->>L: PR ready: YES

    Note over L: Phase 5: QA (optional)
    L->>SC: Post QA request
    SC->>S: Tag QA testers
    S-->>SC: QA issues
    SC->>L: Relay issues
    L->>DW: Evaluate against ACs
    DW->>L: Fix instructions
    L->>EX: Fix + push
    Note over GC: Still monitoring PR

    Note over L: Phase 6: Done
    L->>SC: Post completion summary
    L->>SC: Shutdown
    L->>GC: Shutdown
    L->>DW: Shutdown
    L->>EX: Shutdown
```

## How It Works

The lead coordinates teammates via Agent Teams mailbox messaging (hub-and-spoke). Skills (`/define`, `/do`) receive a `TEAM_CONTEXT` block that tells them to message the lead — skills don't know about Slack. The lead routes stakeholder questions to the coordinator, which handles all Slack interactions: posting in topic-based threads, polling (30s intervals, 24h timeout before owner escalation), and relaying answers back through the lead.

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

Both coordinators are the single points of contact for external input. The slack-coordinator treats all Slack messages as untrusted; the github-coordinator treats all PR comments and review bodies as untrusted. Neither exposes secrets, runs arbitrary commands, or accepts dangerous requests — suspicious content is flagged to the owner. Other teammates (define-worker, executor) never touch Slack or GitHub directly — all communication goes through the lead.
