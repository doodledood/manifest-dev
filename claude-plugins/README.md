# Claude Code Plugins

Loop engineering's missing half: define what "done" means, then verify it. The loop is the easy part — these plugins are the understanding and the verification that wrap around it.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/manifest-dev
/plugin list
/plugin install manifest-dev@manifest-dev
```

## Available Plugins

| Plugin | What It Does |
|--------|--------------|
| [`manifest-dev`](./manifest-dev) | The core workflow: figure it out, encode what you'd accept, let it build and verify itself. `/figure-out` is the thinking partner; `/define` encodes that understanding into a Manifest; `/do` executes it and evaluates every gate under a run-level mode. `consolidated` is the independent default; `per-gate` is an opt-in higher-rigor mode and `self` an opt-in lower-assurance one. The manifest is the canonical source of truth for the PR/branch — feedback during `/do` or after `/done` defaults to amending it. Multi-CLI distribution (OpenCode, Codex CLI, and a Pi package target). Running `/do` with a durable goal-setting/continuation backstop whose contract is auditable all-criteria-PASS — every manifest gate in a ledger with fresh mode-appropriate evidence — is the recommended unattended form; the backstop keeps the run alive across turns. |
| [`manifest-dev-tools`](./manifest-dev-tools) | Tools alongside the workflow. `/prompt-engineering` builds and reviews prompts. `/walk-pr` (collaborative review), `/review-pr` (autonomous review with `--loop` follow-through), and `/babysit-pr` (author-side PR lifecycle babysitting that runs manifest machinery) cover PR collaboration. `/handoff` packages context for a fresh agent or a side-session. `/teach-me` turns a body of work — the session, a PR, an ADR, or any topic — into an incremental teaching loop with mastery checks. `/re-pitch` re-pitches a message that didn't land, in plain words with the missing context. |

## At a Glance

**manifest-dev** separates *what to build* (Deliverables with Acceptance Criteria) from *rules to follow* (Global Invariants). The three beats answer the three ways an autonomous loop goes wrong — skipping understanding, never defining "done," and faking it:

- **`/figure-out`** — reach shared understanding of the problem. A peer that investigates before it claims, walks the decision tree, and holds positions under pushback. The conceptual core; call it directly when figuring it out IS the goal. Supports `--canvas` (a refreshable browser-rendered map of where the session has reached, annotatable and handed back in one paste).
- **`/define`** — encode that understanding into a Manifest. Auto-invokes `/figure-out` when the understanding isn't there yet. Supports `--babysit <pr-url>`.
- **`/do`** — execute and verify. It preserves each gate's `verify.instructions` while applying a run-level policy: `consolidated` (default, one independent verifier for the outstanding gate set), `per-gate` (one fresh independent verifier per gate, for maximum rigor), or `self` (executor evaluation). Optional `--verifier-model` applies only to the independent modes. It aggregates PASS / FAIL / BLOCKED, fixes failures, and re-evaluates — command-backed gates in full, judgment gates over their prior findings' repairs and the delta after one full look, with `--exhaustive-verification` restoring full re-sampling. Caller overlays can narrow retry cadence for CI one-shot workflows. Use the host's goal-setting/continuation backstop with the auditable all-criteria-PASS completion contract (the recommended unattended form): every manifest gate in a ledger with fresh mode-appropriate evidence and provenance, not a summary claim. `/auto` chains all three autonomously; use one chain-complete goal contract there too, with the autonomous Read as a checkpoint before manifest encoding and terminal completion judged by `/do` gate-ledger PASS.

- **`/ticket-up` and `/next-ticket`** — split a finished Manifest into self-sufficient tickets anyone can pick up (files, GitHub Issues, or a custom tracker), and pull the top ready ticket back out with the reason it leads.

Full schema, verify-block fields, verification skills, and task guidance live in the [manifest-dev README](./manifest-dev).

For non-Claude installs and updates, see the root README's [Multi-CLI Support](../README.md#multi-cli-support). Pi installs the repo-root package (`pi install git:github.com/doodledood/manifest-dev@main`); it ships the full skill set plus prompt-template aliases for `/do`, `/auto`, and `/babysit-pr`. Host goal/continuation support is optional and acts as an outer backstop for unattended runs.

**manifest-dev-tools** sits next to the workflow rather than inside it — prompt engineering, PR review and walkthroughs, PR babysitting, context handoff, incremental teaching, and a re-pitch corrective. Details in the [manifest-dev-tools README](./manifest-dev-tools).

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
