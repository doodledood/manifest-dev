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
| [`manifest-dev`](./manifest-dev) | Verification-first manifest workflows. The manifest is the canonical source of truth for the PR/branch — feedback during or after work defaults to amending it. Verification is selective during fix-loop and full before `/done` (mandatory final gate). Phased by iteration speed (fast checks first, e2e/deploy-dependent later). PR-lifecycle work composes the `github-pr-lifecycle` agent through PR_LIFECYCLE.md task guidance; `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. Multi-CLI distribution (Gemini CLI, OpenCode, Codex CLI). Every criterion has explicit verification; execution can't stop without verification passing or escalation. |
| [`manifest-dev-tools`](./manifest-dev-tools) | Post-processing utilities for manifest workflows. `/adr` synthesizes Architecture Decision Records from session transcripts. |
| [`manifest-dev-experimental`](./manifest-dev-experimental) | **Placeholder.** Currently ships no skills — reserved for future experiments. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/define` - Verification-first requirements builder with proactive interview. Supports `--interview minimal|autonomous|thorough` (default: thorough) to control questioning depth, and `--canvas` (desktop only) to generate a Shared Understanding Canvas alongside the manifest — a live, browser-rendered visual side-channel that surfaces intent, flow, and scope at a glance, so the user can spot misalignment during the chat interview. Mermaid diagrams and before/after panels render in the user's default browser; the canvas updates as the interview unfolds. Defaults to amending an in-scope prior manifest (in-session or conversation-referenced); on a fresh /define against a non-empty branch, seeds from the existing diff.
- `/do` - Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify. Mid-execution user feedback defaults to autonomous Self-Amendment (pure questions answered inline). `/verify` runs selectively during the fix-loop with a mandatory full final gate before `/done`.

**Optional skills:**
- `/figure-out` - Figure things out together on any topic. Truth-convergent thinking partner that investigates before claiming, surfaces gaps, resists premature synthesis. Use before `/define` when the problem space is foggy. Pass `--with-docs` to opt into glossary and ADR persistence.

**Other skills:** `/auto` - End-to-end autonomous `/define` → auto-approve → `/do` in a single command. Supports `--platform` and `--babysit <pr-url>` for tending an existing PR end-to-end without manifest-dev setup.

**Multi-repo support:** A single canonical `/tmp` manifest can cover changesets that span multiple repos. Intent declares `Repos: [name: path]`; deliverables tag `repo: name`. `/do` navigates absolute paths from the map (no filter logic — the LLM handles repo navigation natively). PR-lifecycle work auto-templates one `github-pr-lifecycle` agent invocation per repo against the shared manifest. Cross-repo gates the user explicitly triggers use `method: deferred-auto` + `/verify --deferred`. See `skills/define/references/MULTI_REPO.md`.

**Internal skills:** `/verify`, `/done`, `/escalate`

**Review agents:** `criteria-checker`, `manifest-verifier`, `github-pr-lifecycle`, `change-intent-reviewer`, `contracts-reviewer`, `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `test-quality-reviewer` (coverage gaps + tautological-test detection), `prose-value-reviewer` (code comments + repo doc files: AI-tells, narrating-the-obvious, puffery), `type-safety-reviewer`, `docs-reviewer`, `context-file-adherence-reviewer`

**Hooks** enforce workflow integrity: prevent premature stopping, restore context after compaction, nudge manifest reads before verification, track execution log updates, and detect manifest amendments during `/do`.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents. Medium-specific messaging files in `references/messaging/` (LOCAL.md) define interaction mechanics.

### manifest-dev-tools

Post-processing utilities that operate on the outputs of the manifest workflow.

**Skills:**
- `/adr` - Synthesize Architecture Decision Records from session transcripts via multi-agent extraction pipeline (architecture, trade-offs, scope/constraints lenses + synthesis gatekeeper). Writes individual MADR files.

### manifest-dev-experimental

**Placeholder** plugin. Currently ships no skills — reserved for future experiments that need a separate, opt-in surface from the core plugin.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
