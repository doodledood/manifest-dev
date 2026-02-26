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

**Internal skills:** `/verify`, `/done`, `/escalate`

**Review agents:** `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `code-coverage-reviewer`, `type-safety-reviewer`, `docs-reviewer`, `claude-md-adherence-reviewer`

**Hooks** prevent premature stopping -- can't stop without verification passing or proper escalation.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents.

### manifest-dev-collab

Team collaboration on define/do workflows through Slack.

**Core skill:**
- `/slack-collab` - Launches a Python orchestrator that drives collaborative define/do workflows through Slack. Handles stakeholder Q&A, manifest review, PR review, and QA sign-off.

**Prerequisites:** Slack MCP server configured, `manifest-dev` plugin installed, Python 3.8+.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
