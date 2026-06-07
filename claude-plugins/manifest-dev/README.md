# manifest-dev

Understand the problem. Write down what you'd accept. Let it build and verify itself.

## Quick Start

```
/figure-out "how should rate limiting behave here?"   # think it through
/define "add rate limiting to the API"                # encode what you'd accept
/goal /do ~/.manifest-dev/manifests/manifest-<timestamp>.md   # execute + verify (recommended: continues across turns)
/do ~/.manifest-dev/manifests/manifest-<timestamp>.md         # foreground variant, current turn only
```

`/figure-out` is where the understanding happens. `/define` encodes that understanding into a Manifest — it auto-invokes `/figure-out` for you when the conversation hasn't reached understanding yet, so in practice the minimum is `/define` then `/goal /do`. `/do` executes the Manifest and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant. Run it through `/goal` — `/goal /do <path>` is the recommended form, keeping the run alive across turns.

Non-Claude distributions are generated under `dist/`. OpenCode and Codex ship `/do`; Pi installs `npm:@gotgenes/pi-subagents` plus the repo-root package (`pi install git:github.com/doodledood/manifest-dev@main`) for shared skills, `/do`, `/auto`, `/babysit-pr`, clean verifier fanout, and a structured done/escalate gate. See the root README's [Multi-CLI Support](../../README.md#multi-cli-support).

## The Mindset Shift

Stop thinking about *how* to build it. Start thinking about *what you'd accept*.

"What would make me approve this PR?" "What rules can't be broken?" "How would I know each piece is done?" The acceptance criteria are the pillar, not the implementation. LLMs are good at execution when they know exactly what's expected and bad at reading your mind — the manifest closes that gap before a line of code gets written.

## Skills

- **`/figure-out`** — the thinking partner, and the conceptual core. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), takes the next load-bearing question first, recommends an answer, returns to dropped threads, investigates instead of asking when something is discoverable, and keeps a belief register on evidence-heavy work. `/define` auto-invokes it when the transcript lacks understanding; call it directly when figuring it out IS the goal. `--with-docs` adds bootstrap/glossary/ADR conventions; `--log [path]` keeps a narrative investigation log; `--autonomous` lets it self-answer (used by `/auto`).
- **`/define`** — encodes shared understanding into a verifiable Manifest. Not an interview: it makes the manifest-specific judgment calls (invariant vs process guidance, AC scope and pass threshold, phase ordering, trade-offs to lock as `[T-N]`) and pulls in `/figure-out` first if the understanding isn't there. Pass an existing manifest path in `$ARGUMENTS` to amend it in place. Supports `--babysit <pr-url>` and `--canvas`. Emits `/do <manifest-path>` and `/goal /do <manifest-path>` handoffs.
- **`/do`** — executes a Manifest, spawning one verifier subagent per Acceptance Criterion and Global Invariant (using `verify.prompt:` verbatim), respecting `phase:` ordering, calling `/done` when everything verifies PASS or routing through `/escalate` when blocked. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping. The recommended invocation is `/goal /do <manifest-path>`, which keeps the run alive across turns; bare `/do` runs a single foreground turn. Mid-`/do` user messages default to invoking `/define` for amendment.
- **`/auto`** — chains `figure-out → define → do` autonomously, no approval gates. Run it as `/goal /auto` for unattended cross-turn execution (recommended). Add `--babysit <pr-url>` for PR-lifecycle work.
- **`/figure-out-team`** — `/figure-out`'s discipline applied to a multi-party async Slack conversation. An involved orchestrator: brings evidence, names trade-offs, surfaces disagreement; polls the thread via `/loop` and reads via the `slack-poller` subagent for verbatim deltas; convergence is judgment-based across speakers, with the owner (by Slack handle) overruling. Trust is session-bound — the Claude Code operator is the only trusted human; Slack content is data, never instructions. `--with-docs` loads CONTEXT.md as background; `--log [path]` keeps a local log without posting to Slack.
- **`/done`** — completion summary in plain prose, called by `/do` after every criterion verifies PASS.
- **`/escalate`** — structured blocker: criterion, attempts and why each failed, possible resolutions, what's needed from you. Routed by `/do`.

## Manifest Schema — Four Fields per Verify Block

Every verify block has the same shape:

```yaml
verify:
  prompt: "..."     # required, verbatim verifier instruction
  agent: "..."      # optional, default = general-purpose subagent
  model: "..."      # optional, default = inherit from invoking context
  phase: 1          # optional integer, default 1 (lower phases run first)
```

Verifiers return one of three states. **PASS** — the criterion holds. **FAIL** — violated, with evidence: either a per-gate directive `/do` runs literally (specialized verifiers like `github-pr-lifecycle`) or a prose fix hint read with judgment (generic verifiers). **BLOCKED** — can't be evaluated yet because an external action or state is pending (deploy, human approval); `/do` routes BLOCKED via `/escalate`.

Authors put whatever the verifier needs directly into the prompt — run a bash command and check the exit code, inspect files, query an API, fetch docs. There's no separate `method:` or `command:` field; the subagent runs whatever its prompt asks for.

## Manifest Sections

| Section | Purpose | ID Scheme |
|---------|---------|-----------|
| **Intent & Context** | Goal and mental model | -- |
| **Approach** (complex tasks) | Architecture, execution order, risks, trade-offs | `R-{N}`, `T-{N}` |
| **Global Invariants** | Task-level rules (task fails if violated) | `INV-G{N}` |
| **Process Guidance** | Non-verifiable recommendations for how to work | `PG-{N}` |
| **Known Assumptions** | Low-impact items resolved with a default | `ASM-{N}` |
| **Deliverables** | Ordered work items with Acceptance Criteria | `AC-{D}.{N}` |

## Manifest = Current State

Amendments overwrite in place with stable IDs (modify `INV-G1` and it stays `INV-G1`; remove one and it's gone, no renumbering). No `## Amendments` log, no `INV-G1.1 amends INV-G1` chain — git carries the history.

## Agents

Verifier subagents default to `general-purpose` when a manifest omits `verify.agent:`. The bundled `criteria-checker` is a focused alternative (invoked via `agent: criteria-checker`): read-only behavior is enforced by its prompt, so authors can point it at MCP servers or extra CLI tools the user has configured.

The review agents in `agents/` cover code, operational readiness, prose, contracts, types, design, testability, intent, and docs — name one in `verify.agent:` to scope a subagent to that lens. `github-pr-lifecycle` handles PR mergeability checks; `slack-poller` tails Slack threads for `/figure-out-team`. See the [root README](../../README.md#verifier-agents) for the full list.

## Task Guidance and References

Task files come in two parallel, decoupled sets, each loaded by task type by its own skill: `skills/define/tasks/` carry domain-specific quality gates and Defaults that `/define` encodes into the manifest; `skills/figure-out/tasks/` carry probing fuel — blind-spot probes and forced trade-offs (verification among them) that `/figure-out` surfaces during understanding as awareness, not a checklist. Source-type research material lives under `skills/define/tasks/research/sources/`. Mode and domain references in `skills/define/references/` (`BABYSIT_MODE.md`, `CANVAS_MODE.md`, `MULTI_REPO.md`, `WRITING-REFERENCE.md`) cover specialized flows.
