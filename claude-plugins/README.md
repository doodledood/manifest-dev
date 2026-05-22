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
| [`manifest-dev`](./manifest-dev) | Manifest-driven workflows. `/define` interviews and writes a Manifest; `/do` executes it and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant. The manifest is the canonical source of truth for the PR/branch — feedback during `/do` or after `/done` defaults to amending it. PR-lifecycle work composes the `github-pr-lifecycle` agent through PR_LIFECYCLE.md task guidance; `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. Multi-CLI distribution (OpenCode, Codex CLI). Execution can't stop without every criterion verifying PASS or proper escalation. |
| [`manifest-dev-tools`](./manifest-dev-tools) | Utilities that complement manifest workflows. `/adr` synthesizes Architecture Decision Records from session transcripts. `/handoff` produces a context payload for cross-boundary transfer or DIY sub-agent flows (spin off a focused side-session and hand back). `/prompt-engineering`, `/walk-pr`, and `/review-pr` are stand-alone collaboration tools — `/walk-pr` for collaborative review, `/review-pr` for autonomous PR review with `--loop` follow-through. |

## Plugin Details

### manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

**Core skills:**
- `/figure-out` — Primary thinking-partner skill. A truth-convergent peer working the problem with you: investigates before claiming, walks the decision tree for design-shaped tasks, delivers each next-move with its load-bearing crux, holds positions under social pressure. `/define` auto-invokes it when the problem space is foggy; call it directly when figuring it out IS the goal. Pass `--with-docs` to opt into bootstrap, inline glossary captures, and ADR offers.
- `/figure-out-team` — `/figure-out`'s discipline applied to a multi-party async Slack conversation. Involved orchestrator: brings evidence, names trade-offs, surfaces disagreements. Polls the thread via `/loop`, reads via the `slack-poller` subagent. Owner-by-Slack-handle overrules. Pass `--with-docs` (read-only) to load CONTEXT.md as background context for the deliberation.
- `/define` — Manifest builder. Encodes shared understanding as Deliverables, Acceptance Criteria, Global Invariants, and Approach. Defaults to amending an in-scope prior manifest (in-session or conversation-referenced); on a fresh /define against a non-empty branch, seeds from the existing diff. Supports `--canvas` (desktop only) for a live, browser-rendered Shared Understanding Canvas alongside the manifest.
- `/do` — Manifest executor. Iterates Deliverables, satisfies ACs, then verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant using the verify prompt. Aggregates PASS / FAIL / BLOCKED, fixes failures, re-verifies. Calls `/done` when everything passes; routes to `/escalate` when blocked. Mid-execution user feedback defaults to autonomous Self-Amendment (pure questions answered inline).
- `/auto` — End-to-end autonomous `/define` → auto-approve → `/do` in a single command. Supports `--platform` and `--babysit <pr-url>` for tending an existing PR end-to-end without manifest-dev setup.

**Manifest schema — four fields per verify block:**

```yaml
verify:
  prompt: "..."     # required, verbatim verifier instruction
  agent: "..."      # optional, default = general-purpose subagent
  model: "..."      # optional, default = inherit from invoking context
  phase: 1          # optional integer, default 1 (lower phases run first)
```

The subagent returns PASS, FAIL, or BLOCKED. BLOCKED routes via `/escalate` (external action pending — deploy, human approval).

**Multi-repo support:** A single canonical manifest covers changesets that span multiple repos. Intent declares `Repos: [name: path]`; deliverables tag `repo: name`. `/do` navigates absolute paths from the map (no filter logic — the LLM handles repo navigation natively). PR-lifecycle work auto-templates one `github-pr-lifecycle` agent invocation per repo against the shared manifest. See `skills/define/references/MULTI_REPO.md`.

**Internal skills:** `/done`, `/escalate`

**Review agents:** `criteria-checker`, `github-pr-lifecycle`, `slack-poller`, `change-intent-reviewer`, `contracts-reviewer`, `code-bugs-reviewer`, `operational-readiness-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `code-testability-reviewer`, `test-quality-reviewer`, `prose-value-reviewer`, `type-safety-reviewer`, `docs-reviewer`, `context-file-adherence-reviewer`

**Hooks** enforce workflow integrity: `stop_do_hook` prevents premature stopping during `/do`; `post_compact_hook` restores context after compaction.

**Task guidance** files in `skills/define/tasks/` provide domain-specific quality gates, risks, and scenarios. Source-type research material lives under `skills/define/tasks/research/sources/`. Mode-specific references in `skills/define/references/` (`BABYSIT_MODE.md`, `CANVAS_MODE.md`, `MULTI_REPO.md`) cover specialized flows.

### manifest-dev-tools

Post-processing utilities that operate on the outputs of the manifest workflow.

**Skills:**
- `/adr` — Synthesize Architecture Decision Records from session transcripts via multi-agent extraction pipeline (architecture, trade-offs, scope/constraints lenses + synthesis gatekeeper). Writes individual MADR files.
- `/handoff` — Produces a context payload that lets a fresh agent continue without re-deriving understanding. Two triggers: cross-boundary transfer (tool switch, fresh session, multi-agent) and DIY sub-agent (spin off a focused side-session and hand back to the parent).
- `/prompt-engineering` — Create, update, or review an LLM prompt — system prompt, skill, or agent. State the goal, trust the model, add only what closes a real gap in natural behavior. Branches on intent (create / update / review / diagnose); references load on demand for archetype-specific guidance (system prompts, skills, knowledge skills, agents, patterns, review, metaprompting).
- `/review-pr` — Autonomous PR review. Spawns a tiered reviewer fleet in parallel, filters to medium+ findings, runs a holistic coherence pass grounded against PR history, bundle context, and the author's manifest, then submits a single GitHub review with human-voiced comments. `--loop` bypasses approval and watches the PR with backoff: per-comment verifier decides addressed-by-fix / addressed-by-valid-reply / needs-pushback (one round of pushback per thread, then drop); reruns the pipeline on success; terminates at 3 cycles, 24h, or clean lgtm.
- `/walk-pr` — Collaboratively walks through a PR or large diff, sub-changeset by sub-changeset.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
