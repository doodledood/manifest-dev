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
| [`manifest-dev`](./manifest-dev) | Verification-first manifest workflows. The manifest is the canonical source of truth for the PR/branch — feedback during or after work defaults to amending it. Verification is selective during fix-loop and full before `/done` (mandatory final gate). Phased by iteration speed (fast checks first, e2e/deploy-dependent later). Multi-CLI distribution (Gemini CLI, OpenCode, Codex CLI). Every criterion has explicit verification; execution can't stop without verification passing or escalation. |
| [`manifest-dev-tools`](./manifest-dev-tools) | Post-processing utilities for manifest workflows. `/adr` synthesizes Architecture Decision Records from session transcripts. |
| [`manifest-dev-experimental`](./manifest-dev-experimental) | **Experimental.** Cron-driven, tick-based manifest runner (`/drive` + `/drive-tick`) with pluggable platform (`none`, `github`) and sink (`local`) adapters. Each tick delegates implement+verify+fix to `/do` (intra-tick convergence); cross-tick boundaries handle CI triage, PR tending, and inbox routing. No flow-control hooks. Coexists with `manifest-dev` — nothing deprecated. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/define` - Verification-first requirements builder with proactive interview. Supports `--interview minimal|autonomous|thorough` (default: thorough) to control questioning depth. Defaults to amending an in-scope prior manifest (in-session, conversation-referenced, or branch-archived in `.manifest/`); on a fresh /define against a non-empty branch, seeds from the existing diff.
- `/do` - Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify. Mid-execution user feedback defaults to autonomous Self-Amendment (pure questions answered inline). `/verify` runs selectively during the fix-loop with a mandatory full final gate before `/done`.

**Optional skills:**
- `/figure-out` - Figure things out together on any topic. Truth-convergent thinking partner that investigates before claiming, surfaces gaps, resists premature synthesis. Use before `/define` when the problem space is foggy.

**Other skills:** `/auto` - End-to-end autonomous `/define` → auto-approve → `/do` in a single command (add `--tend-pr` for PR lifecycle) | `/tend-pr` - Tends a PR through review to merge-readiness, manifest-aware or babysit mode | `/learn-define-patterns` - Analyzes past /define sessions and writes preference patterns to CLAUDE.md

**Multi-repo support:** A single canonical `/tmp` manifest can cover changesets that span multiple repos. Intent declares `Repos: [name: path]`; deliverables tag `repo: name`. `/do` navigates absolute paths from the map (no filter logic — the LLM handles repo navigation natively). `/tend-pr` and `/drive` run per-repo against the same shared manifest. Cross-repo gates the user explicitly triggers use `method: deferred-auto` + `/verify --deferred`. See `skills/define/references/MULTI_REPO.md`.

**Internal skills:** `/verify`, `/done`, `/escalate`, `/stop-thinking-disciplines`, `thinking-disciplines`

**Other user-invocable skills:** `/tend-pr-tick` (also called by `/loop` via `/tend-pr`)

**Review agents:** `criteria-checker`, `manifest-verifier`, `define-session-analyzer`, `change-intent-reviewer`, `contracts-reviewer`, `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `code-coverage-reviewer`, `type-safety-reviewer`, `docs-reviewer`, `context-file-adherence-reviewer`

**Hooks** enforce workflow integrity: prevent premature stopping, restore context after compaction, nudge manifest reads before verification, track execution log updates, and detect manifest amendments during `/do`.

**Task guidance** with domain-specific quality gates, risks, and scenarios. Reference material in `tasks/references/research/` provides detailed evidence for `/verify` agents. Medium-specific messaging files in `references/messaging/` (LOCAL.md) define interaction mechanics.

### manifest-dev-tools

Post-processing utilities that operate on the outputs of the manifest workflow.

**Skills:**
- `/adr` - Synthesize Architecture Decision Records from session transcripts via multi-agent extraction pipeline (architecture, trade-offs, scope/constraints lenses + synthesis gatekeeper). Writes individual MADR files.

### manifest-dev-experimental

**Experimental** alternative to `/do` + `/tend-pr`. Cron-driven tick loop with pluggable platform and sink adapters.

**Skills:**
- `/drive` - Wrapper that parses args, resolves base branch, pre-flights the scheduler (`/loop` preferred; auto-falls back to an inline scheduler when `/loop` isn't installed), bootstraps branch/commit/PR (github mode), then hands control to the scheduler for repeated `/drive-tick` invocations.
- `/drive-tick` - The per-iteration brain. Reads full log (memento), loads platform + sink adapters, checks terminal states, handles inbox, delegates implement+verify+fix to `/do` (intra-tick convergence), runs CI triage and PR tending, amends if scope shifts, commits, and returns for the next scheduled iteration — or ends on terminal state / budget exhaust.

**Adapters:**
- Platforms: `none` (local branch only), `github` (PR bootstrap + tend — preserves `tend-pr-tick`'s classification, CI triage, PR sync, thread resolution, and merge-ready semantics adapted to the adapter contract).
- Sinks: `local` (log-file escalations).

**Design:** No plugin-specific hooks. No auto-escalation on no-progress. Each tick delegates implement+verify+fix to `/do` (intra-tick convergence); cross-tick boundaries handle CI triage, PR tending, and inbox routing. `--interval` defaults to 15m (bounded 15m–24h); while a tick holds its lock, subsequent cron fires exit silently — interval is a floor on poll frequency, not a hard cadence. Locks have no TTL; stale locks from crashed ticks require manual cleanup via `/drive` pre-flight. `--max-ticks` budget cap (default 100) prevents cost runaway. CI failures classified as infrastructure/flaky are auto-retriggered (native rerun or empty-commit push) up to 10 times per run before escalating.

**Coexistence:** `/drive` does NOT replace `/do`, `/tend-pr`, `/tend-pr-tick`, or `/auto`. Pick whichever fits your workflow.

**Multi-repo support:** Each repo's `/drive` runs against its own PR with its own run-id (`gh-{owner}-{repo}-{pr}`); all amend the same shared canonical `/tmp` manifest used by every repo's PR. See `manifest-dev/skills/define/references/MULTI_REPO.md`.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
