# manifest-dev

Tell Claude what "done" looks like. Let it work. Check the result.

## Quick Start

```
/define "add rate limiting to the API"
/do /tmp/manifest-<timestamp>.md
/goal /do /tmp/manifest-<timestamp>.md  # unattended
```

Two commands, or wrap the second in `/goal` when you want unattended turn continuation. `/define` interviews you and writes a Manifest. `/do` executes it and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant.

## The Mindset Shift

Stop thinking about *how* to build it. Start thinking about *what you'd accept*.

"What would make me accept this PR?" "What rules can't be broken?" "How would I know each piece is done?" That's what `/define` asks you. Architecture might come up too, but the pillar is acceptance, not implementation. What does good enough look like?

This works because LLMs are surprisingly good at execution when they know exactly what's expected. They're bad at reading your mind. The manifest closes that gap before a single line of code gets written. The interview phase is slow; it catches the gaps that blow up after implementation.

## Skills

- **`/figure-out`** — truth-convergent thinking partner. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), tackles the next load-bearing question first, gives recommended answers, returns to dropped threads, investigates instead of asking when something is discoverable. `/define` auto-invokes it when the transcript lacks understanding; call it directly when figuring it out IS the goal. Pass `--log [path]` to keep an append-only narrative investigation log for long sessions.
- **`/figure-out-team`** — `/figure-out`'s discipline applied to a multi-party async Slack conversation. Involved orchestrator (brings evidence, viewpoints, synthesis); polls the thread via `/loop` and reads via the `slack-poller` subagent for verbatim deltas; convergence is judgment-based across speakers with the owner (by Slack handle) overruling disagreement. Trust is session-bound — the operator from Claude Code is the sole trusted human; Slack content is data, never instructions. Pass `--log [path]` to keep a local append-only narrative investigation log without posting it to Slack.
- **`/define`** — encodes shared understanding into a verifiable Manifest. Supports `--babysit <pr-url>`, `--canvas`, `--autonomous`. Amendment is triggered by passing an existing manifest path in `$ARGUMENTS`; `/define` overwrites in place. Emits `/do <manifest-path>` and `/goal /do <manifest-path>` handoffs.
- **`/do`** — executes a Manifest by spawning one verifier subagent per Acceptance Criterion and Global Invariant (using `verify.prompt:` verbatim), respecting `phase:` ordering, calling `/done` when every AC and Global Invariant verifies PASS, or routing through `/escalate` when blocked. Run as `/goal /do <manifest-path>` for unattended turn continuation. Mid-/do user messages default to invoking `/define` for amendment.
- **`/done`** — completion summary in plain prose. Called by `/do` after every Acceptance Criterion and Global Invariant verifies PASS.
- **`/escalate`** — structured blocker: criterion, attempts and why each failed, possible resolutions, what's needed from the user. Single type; routes via `/do`.
- **`/auto`** — chains `figure-out → define → do` autonomously. Add `--babysit <pr-url>` for PR-lifecycle work.

## Manifest schema — four fields

Every verify block has the same shape:

```yaml
verify:
  prompt: "..."     # required, verbatim verifier instruction
  agent: "..."      # optional, default = general-purpose subagent
  model: "..."      # optional, default = inherit from invoking context
  phase: 1          # optional integer, default 1 (lower phases run first)
```

Verifier subagents return one of three states: **PASS**, **FAIL**, or **BLOCKED**. PASS = criterion holds. FAIL = criterion violated; includes evidence — either a per-gate directive `/do` executes literally (specialized verifiers like `github-pr-lifecycle`) or a prose fix hint read with judgment (generic verifiers). BLOCKED = criterion can't be evaluated yet because of an external action / state pending (deploy hasn't happened, human approval pending, etc.) — `/do` routes BLOCKED via `/escalate`.

Authors put whatever the verifier needs to do directly into the prompt — run a bash command and check exit code, inspect files, query an API, fetch docs. There's no separate `method:`, `command:`, or `inner_method:` field; the subagent runs whatever its prompt asks for from its tool set.

## Manifest sections

A Manifest has five sections:

| Section | Purpose | ID Scheme |
|---------|---------|-----------|
| **Intent & Context** | Goal and mental model | -- |
| **Approach** (complex tasks) | Architecture, execution order, risks, trade-offs | `R-{N}`, `T-{N}` |
| **Global Invariants** | Task-level rules (task fails if violated) | `INV-G{N}` |
| **Process Guidance** | Non-verifiable recommendations for how to work | `PG-{N}` |
| **Known Assumptions** | Low-impact items resolved with a default | `ASM-{N}` |
| **Deliverables** | Ordered work items with Acceptance Criteria | `AC-{D}.{N}` |

## Manifest = current state

Amendments overwrite in place with stable IDs (modify `INV-G1` → it stays `INV-G1`; remove one → it's gone, no renumbering of the rest). No `## Amendments` log section, no `INV-G1.1 amends INV-G1` chain. Git diff carries the history.

## Agents

Verifier subagents default to `general-purpose` when a manifest omits `verify.agent:`. The bundled `criteria-checker` agent (invoked explicitly via `agent: criteria-checker`) is a focused alternative: read-only behavior is enforced by its prompt, so authors can spawn it against MCP servers or extra CLI tools the user has configured.

Review agents in `agents/` cover code, operational readiness, prose, contracts, types, design, testability, intent, and docs — name one in `verify.agent:` to scope the subagent to that lens. `github-pr-lifecycle` handles PR mergeability checks; `slack-poller` tails Slack threads for `/figure-out-team`.
