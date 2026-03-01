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
| `manifest-dev` | Verification-first manifest workflows. Every criterion has explicit verification; execution can't stop without verification passing or escalation. |
| `manifest-dev-collab` | Slack-based team collaboration on define/do workflows. Orchestrates stakeholder Q&A, PR review, and QA sign-off through dedicated channels. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/define` - Verification-first requirements builder with proactive interview. YOU generate candidates, user validates.
- `/do` - Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify.

**Other skills:** `/learn-define-patterns` - Analyzes past /define sessions and writes preference patterns to CLAUDE.md

**Internal skills:** `/verify`, `/done`, `/escalate`

**Review agents:** `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `code-coverage-reviewer`, `type-safety-reviewer`, `docs-reviewer`, `claude-md-adherence-reviewer`

**Hooks** prevent premature stopping -- can't stop without verification passing or proper escalation.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents. Collaboration mode instructions in `skills/*/references/COLLABORATION_MODE.md` (progressive disclosure — only loaded when collab is active).

### manifest-dev-collab

Team collaboration on define/do workflows through Slack.

**Core skill:**
- `/slack-collab` - Agent Teams native orchestrator for collaborative define/do workflows through Slack. Spawns specialized teammates (slack-coordinator, define-worker, executor) that coordinate via mailbox messaging.

**Agents:** `slack-coordinator` (Slack I/O), `define-worker` (/define + manifest authority), `executor` (/do + PR + QA fixes)

**Prerequisites:** Slack MCP server configured, `manifest-dev` plugin installed, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` env var.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
