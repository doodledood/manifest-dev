# Claude Code Plugins

Front-load the thinking so AI agents get it right the first time.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/manifest-dev
/plugin list
/plugin install manifest-dev@manifest-dev-marketplace
```

## Available Plugins

| Plugin | What It Does |
|--------|--------------|
| `manifest-dev` | Verification-first manifest workflows with phased verification (fast checks first, e2e/deploy-dependent later) and multi-CLI distribution (Gemini CLI, OpenCode, Codex CLI). Every criterion has explicit verification; execution can't stop without verification passing or escalation. |
| `manifest-dev-collab` | Slack and GitHub/GitLab team collaboration on define/do workflows. Autonomous lead orchestrator with dynamic teammate spawning, phase-anchored threading, verification hard gates, VCS selection (`--vcs github\|gitlab`), and strict role boundaries. |
| `manifest-dev-orchestrate` | Platform-agnostic collaborative workflow orchestration. Supports any messaging medium (local, Slack, custom) and any review platform (GitHub, none, custom). Intent-based lead orchestrator with hub-and-spoke teammate coordination. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/define` - Verification-first requirements builder with proactive interview. Supports `--interview minimal|autonomous|thorough` (default: thorough) to control questioning depth.
- `/do` - Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify.

**Other skills:** `/auto` - End-to-end autonomous `/define` → auto-approve → `/do` in a single command | `/learn-define-patterns` - Analyzes past /define sessions and writes preference patterns to CLAUDE.md

**Internal skills:** `/verify`, `/done`, `/escalate`

**Review agents:** `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `code-coverage-reviewer`, `type-safety-reviewer`, `docs-reviewer`, `context-file-adherence-reviewer`

**Hooks** prevent premature stopping -- can't stop without verification passing or proper escalation.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents. Collaboration mode instructions in `skills/*/references/COLLABORATION_MODE.md` (progressive disclosure — only loaded when collab is active).

### manifest-dev-collab

Team collaboration on define/do workflows through Slack and GitHub or GitLab.

**Core skill:**
- `/slack-collab` - Agent Teams native orchestrator for collaborative define/do workflows through Slack and GitHub or GitLab. Spawns specialized teammates (slack-coordinator, github-coordinator or gitlab-coordinator, define-worker, executor) that coordinate via mailbox messaging. Use `--vcs github|gitlab` to select VCS backend.

**Agents:** `slack-coordinator` (Slack I/O), `github-coordinator` (GitHub PR I/O), `gitlab-coordinator` (GitLab MR I/O), `define-worker` (/define + manifest authority), `executor` (/do + PR/MR + QA fixes)

**Prerequisites:** Slack MCP server configured, GitHub access (`gh` CLI or GitHub MCP) for GitHub runs, GitLab access (`glab` CLI or GitLab MCP) for GitLab runs, `manifest-dev` plugin installed, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` env var.

### manifest-dev-orchestrate

Platform-agnostic collaborative workflow orchestration. Replaces Slack-specific assumptions with configurable mediums and review platforms.

**Core skill:**
- `/orchestrate` - Platform-agnostic lead orchestrator for collaborative define/do workflows. Supports `--medium local|slack|custom` and `--review-platform github|none|custom`. Defaults to local + GitHub.

**Agents:** `slack-coordinator` (Slack I/O), `github-coordinator` (GitHub PR I/O), `manifest-define-worker` (/define + manifest authority), `manifest-executor` (/do + PR + QA fixes)

**Prerequisites:** `manifest-dev` plugin installed, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` env var. Medium/review-platform specific prerequisites depend on flags.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
