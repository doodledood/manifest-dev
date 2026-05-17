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
| [`manifest-dev-tools`](./manifest-dev-tools) | Utilities that complement manifest workflows. `/adr` synthesizes Architecture Decision Records from session transcripts. `/handoff` produces a cross-boundary context payload (tool switch, fresh session, multi-agent transfer). `/prompt-engineering` and `/walk-pr` are stand-alone collaboration tools. |
| [`manifest-dev-experimental`](./manifest-dev-experimental) | Slim parallel rework of `manifest-dev`. Trust-the-model discipline; ships `/figure-out`, `/figure-out-team`, `/define`, `/do`, `/done`, `/escalate`, `/auto`. No separate `/verify` skill (verification absorbed inline by `/do`); four-field manifest schema; agents mirror core. Lives alongside `manifest-dev` until promotion. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/figure-out` - Primary thinking-partner skill. A truth-convergent peer working the problem with you: investigates before claiming, walks the decision tree for design-shaped tasks, delivers each next-move with its load-bearing crux, holds positions under social pressure. Use before `/define` when the problem space is foggy, or whenever figuring it out IS the goal. Pass `--with-docs` to opt into glossary and ADR persistence.
- `/define` - Verification-first manifest builder. Encodes the shared understanding as Deliverables, Acceptance Criteria, Global Invariants, and Approach. Tightened via progressive disclosure — SKILL.md holds the core logic; mode-specific detail (amendment, babysit, canvas, multi-repo) lives under `references/` and loads on demand. Supports `--interview minimal|autonomous|thorough` (default: thorough) and `--canvas` (desktop only) for a live, browser-rendered Shared Understanding Canvas alongside the manifest. Defaults to amending an in-scope prior manifest (in-session or conversation-referenced); on a fresh /define against a non-empty branch, seeds from the existing diff.
- `/do` - Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify. Mid-execution user feedback defaults to autonomous Self-Amendment (pure questions answered inline). `/verify` runs selectively during the fix-loop with a mandatory full final gate before `/done`.

**Other skills:** `/auto` - End-to-end autonomous `/define` → auto-approve → `/do` in a single command. Supports `--platform` and `--babysit <pr-url>` for tending an existing PR end-to-end without manifest-dev setup.

**Multi-repo support:** A single canonical `/tmp` manifest can cover changesets that span multiple repos. Intent declares `Repos: [name: path]`; deliverables tag `repo: name`. `/do` navigates absolute paths from the map (no filter logic — the LLM handles repo navigation natively). PR-lifecycle work auto-templates one `github-pr-lifecycle` agent invocation per repo against the shared manifest. Cross-repo gates the user explicitly triggers use `method: deferred-auto` + `/verify --deferred`. See `skills/define/references/MULTI_REPO.md`.

**Internal skills:** `/verify`, `/done`, `/escalate`

**Review agents:** `criteria-checker`, `manifest-verifier`, `github-pr-lifecycle`, `change-intent-reviewer`, `contracts-reviewer`, `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `test-quality-reviewer` (coverage gaps + tautological-test detection), `prose-value-reviewer` (code comments + repo doc files: AI-tells, narrating-the-obvious, puffery), `type-safety-reviewer`, `docs-reviewer`, `context-file-adherence-reviewer`

**Hooks** enforce workflow integrity: prevent premature stopping, restore context after compaction, nudge manifest reads before verification, and detect manifest amendments during `/do`.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents. Medium-specific messaging files in `references/messaging/` (LOCAL.md) define interaction mechanics.

### manifest-dev-tools

Post-processing utilities that operate on the outputs of the manifest workflow.

**Skills:**
- `/adr` - Synthesize Architecture Decision Records from session transcripts via multi-agent extraction pipeline (architecture, trade-offs, scope/constraints lenses + synthesis gatekeeper). Writes individual MADR files.

### manifest-dev-experimental

Slim parallel rework of `manifest-dev` under a trust-the-model discipline — drops scaffolding the model handles fine when given clean posture.

**Skills:** `/figure-out`, `/figure-out-team`, `/define`, `/do`, `/done`, `/escalate`, `/auto`.

**Key differences from core `manifest-dev`:** verification is absorbed inline by `/do` (no separate `/verify` skill); the manifest schema collapses to four fields (`prompt`, `agent`, `model`, `phase`); amendment is overwrite-in-place (git carries history); agents mirror core for compatibility (`github-pr-lifecycle` byte-identical with main). See the plugin's own README for the full schema and discipline.

Lives alongside `manifest-dev` until promotion.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
