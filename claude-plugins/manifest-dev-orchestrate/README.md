# manifest-dev-orchestrate

Platform-agnostic collaborative workflow orchestration.

## What It Does

`/orchestrate` runs a full define → do → PR → review → QA → done workflow with your team. The messaging medium and review platform are independently configurable — default is local terminal + GitHub.

**Supported mediums:**

| Medium | Coordinator | Description |
|--------|------------|-------------|
| `local` (default) | None | Lead uses AskUserQuestion directly. Synchronous flow. |
| `slack` | slack-coordinator (sonnet) | Full Slack integration with lean diff polling, threading, stakeholder routing. |
| `custom` | LLM-generated | Lead composes coordinator from `--medium-details`. |

**Supported review platforms:**

| Platform | Coordinator | Description |
|----------|------------|-------------|
| `github` (default) | github-coordinator (sonnet) | Full GitHub PR monitoring with bot/human labeling, CI triage. |
| `none` | None | Skip PR review and QA phases entirely. |
| `custom` | LLM-generated | Lead composes coordinator from `--review-platform-details`. |

**Team composition:**

| Teammate | Model | Role | Spawned |
|----------|-------|------|---------|
| **messaging coordinator** | sonnet | Platform-specific messaging I/O (if medium ≠ local) | Phase 0 |
| **manifest-define-worker** | default | Runs `/define` with TEAM_CONTEXT. Persists as manifest authority for QA evaluation. | Phase 0 |
| **manifest-executor** | default | Runs `/do` with TEAM_CONTEXT. Code implementation only. Creates PR. | Phase 0 |
| **review coordinator** | sonnet | Platform-specific review I/O (if review-platform ≠ none) | Phase 4 |
| *ad-hoc teammates* | varies | Lead spawns on-the-fly for tasks that don't fit existing roles. | As needed |

Workers (define-worker, executor) are **medium-blind** — they message the lead only, with no awareness of which coordinator exists or what platform is in use.

## Prerequisites

- **manifest-dev plugin** installed (provides `/define`, `/do`, `/verify`).
- **`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`** environment variable set.

**Medium-specific:**
- `slack`: Slack MCP server configured with send_message, read_channel, read_thread, search_channels, search_users, read_user_profile.
- `custom`: Depends on `--medium-details`.

**Review-platform-specific:**
- `github`: GitHub access via `gh` CLI (authenticated) or GitHub MCP server.
- `custom`: Depends on `--review-platform-details`.

## Usage

```
# Default: local + GitHub
/orchestrate add rate limiting to the API

# Slack + GitHub
/orchestrate --medium slack add rate limiting to the API

# Custom medium
/orchestrate --medium custom --medium-details "We use Mattermost at chat.example.com" add rate limiting

# No review (skip PR phases)
/orchestrate --review-platform none add rate limiting to the API

# Custom review platform
/orchestrate --review-platform custom --review-platform-details "GitLab at gitlab.example.com" add rate limiting
```

**Additional flags** (forwarded to downstream skills):
- `--interview <level>` → `/define` (`minimal | autonomous | thorough`)
- `--mode <level>` → `/do` (`efficient | balanced | thorough`)

Flags are stored in the state file and persist across `--resume`. Flags provided alongside `--resume` override stored values.

**Phases:**

1. **Preflight** — Gather context (channel/stakeholders or just stakeholders for local), create team
2. **Define** — define-worker runs `/define`, Q&A routed through messaging coordinator (or AskUserQuestion in local mode)
3. **Manifest Review** — Stakeholder approval via messaging coordinator (or AskUserQuestion in local mode)
4. **Execute** — manifest-executor runs `/do`, escalations routed to stakeholders
5. **PR Review** (skip if review-platform=none) — Review coordinator monitors PR, fix loop driven by lead
6. **QA** (optional) — Human QA via messaging medium + review coordinator still monitors PR
7. **Done** — Completion summary, all teammates shut down

## Resuming

```
/orchestrate --resume /tmp/orchestrate-state-<id>.json
```

Reads the state file to determine current phase, medium, and review platform config. Re-creates the team with the right coordinators.

## Known Limitations

- **Agent Teams is experimental.** The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var indicates experimental status.
- **Subagent SendMessage may not work.** File-based handoff is available as fallback.
- **No automated E2E tests.** Full integration testing requires Agent Teams + platform environment.
- **/tmp files may not persist across system restarts.**

## Security

Coordinators are the single points of contact for external input. They treat all external messages as untrusted — neither exposes secrets, runs arbitrary commands, or accepts dangerous requests. Workers never touch external platforms directly.
