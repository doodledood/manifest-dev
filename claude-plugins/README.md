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
| `manifest-dev-tools` | Post-processing utilities for manifest workflows. `/adr` synthesizes Architecture Decision Records from session transcripts. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/define` - Verification-first requirements builder with proactive interview. Supports `--interview minimal|autonomous|thorough|collaborative` (default: thorough) to control questioning depth.
- `/do` - Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify.

**Other skills:** `/auto` - End-to-end autonomous `/define` → auto-approve → `/do` in a single command | `/learn-define-patterns` - Analyzes past /define sessions and writes preference patterns to CLAUDE.md

**Internal skills:** `/verify`, `/done`, `/escalate`

**Review agents:** `criteria-checker`, `manifest-verifier`, `define-session-analyzer`, `change-intent-reviewer`, `contracts-reviewer`, `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `code-coverage-reviewer`, `type-safety-reviewer`, `docs-reviewer`, `context-file-adherence-reviewer`

**Hooks** enforce workflow integrity: prevent premature stopping, restore context after compaction, nudge manifest reads before verification, track execution log updates, and detect manifest amendments during `/do`.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents. Medium-specific messaging files in `references/messaging/` (LOCAL.md, SLACK_MESSAGING.md, GENERIC.md) define interaction mechanics per platform.

### manifest-dev-tools

Post-processing utilities that operate on the outputs of the manifest workflow.

**Skills:**
- `/adr` - Synthesize Architecture Decision Records from session transcripts via multi-agent extraction pipeline (architecture, trade-offs, scope/constraints lenses + synthesis gatekeeper). Writes individual MADR files.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
