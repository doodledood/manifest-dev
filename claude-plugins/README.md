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
| [`manifest-dev`](./manifest-dev) | Verification-first manifest workflows. The manifest is the canonical source of truth for the PR/branch — feedback during or after work defaults to amending it. Verification is selective during fix-loop and full before `/done` (mandatory final gate). Phased by iteration speed (fast checks first, e2e/deploy-dependent later). Includes `/drive` — a cron-driven PR-lifecycle runner. Multi-CLI distribution (Gemini CLI, OpenCode, Codex CLI). Every criterion has explicit verification; execution can't stop without verification passing or escalation. |
| [`manifest-dev-tools`](./manifest-dev-tools) | Post-processing utilities for manifest workflows. `/adr` synthesizes Architecture Decision Records from session transcripts. |
| [`manifest-dev-experimental`](./manifest-dev-experimental) | **Placeholder.** Currently ships no skills — reserved for future experiments. `/drive` and `/drive-tick` graduated from this plugin into `manifest-dev`. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/define` - Verification-first requirements builder with proactive interview. Supports `--interview minimal|autonomous|thorough` (default: thorough) to control questioning depth, and `--canvas` (desktop only) to generate a live, browser-rendered Shared Understanding Canvas alongside the manifest — a layered visual artifact (mermaid diagrams, deliverable cards, before/after flows) that updates as the interview unfolds and auto-opens in the user's default browser. Defaults to amending an in-scope prior manifest (in-session or conversation-referenced); on a fresh /define against a non-empty branch, seeds from the existing diff.
- `/do` - Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify. Mid-execution user feedback defaults to autonomous Self-Amendment (pure questions answered inline). `/verify` runs selectively during the fix-loop with a mandatory full final gate before `/done`.

**Optional skills:**
- `/figure-out` - Figure things out together on any topic. Truth-convergent thinking partner that investigates before claiming, surfaces gaps, resists premature synthesis. Use before `/define` when the problem space is foggy.

**Other skills:** `/auto` - End-to-end autonomous `/define` → auto-approve → `/do` in a single command (add `--drive` for PR lifecycle or local loop) | `/drive` - Cron-driven loop that takes a manifest (or existing PR) to terminal state via repeated stateless ticks. Pluggable platform (`none`, `github`) and sink (`local`) adapters.

**Multi-repo support:** A single canonical `/tmp` manifest can cover changesets that span multiple repos. Intent declares `Repos: [name: path]`; deliverables tag `repo: name`. `/do` navigates absolute paths from the map (no filter logic — the LLM handles repo navigation natively). `/drive` runs per-repo against the same shared manifest. Cross-repo gates the user explicitly triggers use `method: deferred-auto` + `/verify --deferred`. See `skills/define/references/MULTI_REPO.md`.

**Internal skills:** `/verify`, `/done`, `/escalate`, `/stop-thinking-disciplines`, `thinking-disciplines`

**Other user-invocable skills:** `/drive-tick` (also called by `/loop` via `/drive`)

**Review agents:** `criteria-checker`, `manifest-verifier`, `change-intent-reviewer`, `contracts-reviewer`, `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `test-quality-reviewer` (coverage gaps + tautological-test detection), `prose-value-reviewer` (code comments + repo doc files: AI-tells, narrating-the-obvious, puffery), `type-safety-reviewer`, `docs-reviewer`, `context-file-adherence-reviewer`

**Hooks** enforce workflow integrity: prevent premature stopping, restore context after compaction, nudge manifest reads before verification, track execution log updates, and detect manifest amendments during `/do`.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents. Medium-specific messaging files in `references/messaging/` (LOCAL.md) define interaction mechanics.

### manifest-dev-tools

Post-processing utilities that operate on the outputs of the manifest workflow.

**Skills:**
- `/adr` - Synthesize Architecture Decision Records from session transcripts via multi-agent extraction pipeline (architecture, trade-offs, scope/constraints lenses + synthesis gatekeeper). Writes individual MADR files.

### manifest-dev-experimental

**Placeholder** plugin. Currently ships no skills — reserved for future experiments that need a separate, opt-in surface from the core plugin.

`/drive` and `/drive-tick` graduated from this plugin into [`manifest-dev`](#manifest-dev). For drive's full design — pluggable platform (`none`, `github`) and sink (`local`) adapters, intra-tick `/do` convergence, CI triage, multi-repo PR-set handling, lock semantics, and budget caps — see `manifest-dev/skills/drive/SKILL.md` and the references under `manifest-dev/skills/drive/references/`.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
