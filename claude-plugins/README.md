# Claude Code Plugins

Front-load the thinking so the agent gets it right the first time.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/manifest-dev
/plugin list
/plugin install manifest-dev@manifest-dev-marketplace
```

## Available Plugins

| Plugin | What It Does |
|--------|--------------|
| [`manifest-dev`](./manifest-dev) | The core workflow: figure it out, encode what you'd accept, let it build and verify itself. `/figure-out` is the thinking partner; `/define` encodes that understanding into a Manifest; `/do` executes it and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant. The manifest is the canonical source of truth for the PR/branch — feedback during `/do` or after `/done` defaults to amending it. Multi-CLI distribution (OpenCode, Codex CLI). Use `/goal /do <manifest-path>` for unattended turn continuation. |
| [`manifest-dev-tools`](./manifest-dev-tools) | Tools alongside the workflow. `/prompt-engineering` builds and reviews prompts. `/walk-pr` (collaborative review) and `/review-pr` (autonomous review with `--loop` follow-through) cover PR review; `/babysit-pr` wraps PR lifecycle babysitting around `/goal /do`. `/adr` synthesizes Architecture Decision Records from a session. `/handoff` packages context for a fresh agent or a side-session. |

## At a Glance

**manifest-dev** separates *what to build* (Deliverables with Acceptance Criteria) from *rules to follow* (Global Invariants). The three beats:

- **`/figure-out`** — reach shared understanding of the problem. A peer that investigates before it claims, walks the decision tree, and holds positions under pushback. The conceptual core; call it directly when figuring it out IS the goal.
- **`/define`** — encode that understanding into a Manifest. Auto-invokes `/figure-out` when the understanding isn't there yet. Supports `--canvas` (a live browser-rendered understanding surface) and `--babysit <pr-url>`.
- **`/do`** — execute and verify. One subagent per criterion using its `verify.prompt:` verbatim, aggregating PASS / FAIL / BLOCKED, fixing failures, re-verifying. `/auto` chains all three autonomously.

Full schema, verify-block fields, agents, and task guidance live in the [manifest-dev README](./manifest-dev).

**manifest-dev-tools** sits next to the workflow rather than inside it — prompt engineering, PR review and walkthroughs, PR babysitting, ADR synthesis, and context handoff. Details in the [manifest-dev-tools README](./manifest-dev-tools).

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
