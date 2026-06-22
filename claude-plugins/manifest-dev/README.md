# manifest-dev

Understand the problem. Write down what you'd accept. Let it build and verify itself.

## Quick Start

```
/figure-out "how should rate limiting behave here?"   # think it through
/define "add rate limiting to the API"                # encode what you'd accept
# recommended — /goal's fresh-model evaluator re-runs turns until the condition holds (continues across turns):
/goal Run /do ~/.manifest-dev/manifests/manifest-<timestamp>.md until every Acceptance Criterion and Global Invariant verifies PASS and /done is reported; don't stop while any gate is unverified, FAIL, or escalation-pending. Resolve every question you can yourself and record low-confidence calls as assumptions, halting only for a blocker that genuinely needs me. Stop after N turns if it stalls.
/do ~/.manifest-dev/manifests/manifest-<timestamp>.md         # foreground variant, current turn only
```

`/figure-out` is where the understanding happens. `/define` encodes that understanding into a Manifest — it auto-invokes `/figure-out` for you when the conversation hasn't reached understanding yet, so in practice the minimum is `/define` then `/do` under a `/goal`. `/do` executes the Manifest and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant. Run it through `/goal` — a `/goal` whose argument is the all-criteria-PASS completion condition is the recommended form, keeping the run alive across turns (the fresh-model evaluator re-opens the turn until the condition holds).

Non-Claude distributions are generated under `dist/`. OpenCode and Codex ship `/do`; Pi installs the repo-root package (`pi install git:github.com/doodledood/manifest-dev@main`) for shared skills, `/do`, `/auto`, `/babysit-pr`, manifest-dev-owned JSON subprocess verifier fanout, and a structured done/escalate gate. See the root README's [Multi-CLI Support](../../README.md#multi-cli-support).

## The Mindset Shift

Stop thinking about *how* to build it. Start thinking about *what you'd accept*.

"What would make me approve this PR?" "What rules can't be broken?" "How would I know each piece is done?" The acceptance criteria are the pillar, not the implementation. LLMs are good at execution when they know exactly what's expected and bad at reading your mind — the manifest closes that gap before a line of code gets written.

## Skills

- **`/figure-out`** — the thinking partner, and the conceptual core. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), takes the next load-bearing question first, recommends an answer, returns to dropped threads, investigates instead of asking when something is discoverable, and keeps a belief register on evidence-heavy work. Its read ships with an Evidence Ledger (load-bearing claims with provenance and verified/inferred/assumed status), confidence, and overturn conditions; loads probe task files by topic shape (code change, diagnosis, research) and runs an independent fresh-context re-derivation before confident reads nobody will audit. `/define` auto-invokes it when the transcript lacks understanding; call it directly when figuring it out IS the goal. `--with-docs` adds bootstrap/glossary/ADR conventions; `--log [path]` keeps a narrative investigation log; `--autonomous` lets it self-answer (used by `/auto`); `--team` moves the deliberation into a Slack channel or thread (used by `/figure-out-team`).
- **`/define`** — encodes shared understanding into a verifiable Manifest. Not an interview: it makes the manifest-specific judgment calls (invariant vs process guidance, AC scope and pass threshold, phase ordering, trade-offs to lock as `[T-N]`) and pulls in `/figure-out` first if the understanding isn't there. Pass an existing manifest path in `$ARGUMENTS` to amend it in place. Supports `--babysit <pr-url>` and `--canvas`. Emits a foreground `/do <manifest-path>` handoff and a `/goal` whose condition is all-criteria-PASS.
- **`/do`** — executes a Manifest, running one verifier execution context per Acceptance Criterion and Global Invariant (using `verify.prompt:` verbatim), respecting `phase:` ordering, calling `/done` when everything verifies PASS or routing through `/escalate` when blocked. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping. The recommended invocation wraps `/do` in a `/goal` whose argument is the manifest's completion condition (every criterion PASS, `/done` reported), which keeps the run alive across turns; bare `/do` runs a single foreground turn. Mid-`/do` user messages default to invoking `/define` for amendment.
- **`/auto`** — chains `figure-out → define → do` autonomously, no approval gates. Run it under a `/goal` (chain-complete completion condition) for unattended cross-turn execution (recommended). Add `--babysit <pr-url>` for PR-lifecycle work.
- **`/figure-out-team`** — thin discovery wrapper over `/figure-out --team`: the full figure-out discipline applied to a multi-party async Slack conversation, with the Slack mechanics (session-bound trust, `/loop` polling with `poll-slack` reads, mrkdwn, owner-by-Slack-handle convergence) living in figure-out's `references/team.md` overrides so team sessions inherit every figure-out upgrade. `--with-docs` loads CONTEXT.md as background; `--log [path]` keeps a local log without posting to Slack.
- **`/done`** — completion summary in plain prose, called by `/do` after every criterion verifies PASS.
- **`/escalate`** — structured blocker: criterion, attempts and why each failed, possible resolutions, what's needed from you. Routed by `/do`.
- **`/review-code`** — quality review along **one dimension per invocation** (bugs, design, simplicity, maintainability, testability, test quality, type safety, contracts, operational readiness, docs, prose value, change intent, or CLAUDE.md adherence). Loads exactly that dimension's reference (progressive disclosure) and returns a PASS/FAIL report. Verifier execution contexts activate it from a `verify.prompt`; it replaces the per-dimension reviewer agents.

## Manifest Schema — Three Fields per Verify Block

Every verify block has the same shape:

```yaml
verify:
  prompt: "..."     # required, verbatim instruction to a general-purpose verifier (may activate a skill)
  model: "..."      # optional, default = inherit from invoking context
  phase: 1          # optional integer, default 1 (lower phases run first)
```

Verifiers return one of three states. **PASS** — the criterion holds. **FAIL** — violated, with evidence: either a per-gate directive `/do` runs literally (when the prompt activates a specialized skill like `check-pr`) or a prose fix hint read with judgment (plain prompts). **BLOCKED** — can't be evaluated yet because an external action or state is pending (deploy, human approval); `/do` routes BLOCKED via `/escalate`.

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

## Verification Skills

manifest-dev ships **no agents of its own**. Every criterion is verified by a general-purpose subagent driven by `verify.prompt`, which can run bash, inspect files, query external tools, or activate a skill. Read-only behavior is enforced by the prompt, so authors can point a verifier at MCP servers or extra CLI tools the user has configured.

Quality review (code, operational readiness, prose, contracts, types, design, testability, intent, docs) is the **`review-code` skill** — one dimension per invocation; a verifier activates it from `verify.prompt`. The other functional skills are `check-pr` (PR mergeability checks) and `poll-slack` (tails Slack threads for `/figure-out-team`). See the [root README](../../README.md#verification-skills) for the full list.

## Task Guidance and References

Task files come in two parallel, decoupled sets, each loaded by task type by its own skill: `skills/define/tasks/` carry domain-specific quality gates and Defaults that `/define` encodes into the manifest; `skills/figure-out/tasks/` carry probing fuel — blind-spot probes and forced trade-offs (verification among them) that `/figure-out` surfaces during understanding as awareness, not a checklist. Source-type research material lives under `skills/define/tasks/research/sources/`. Mode and domain references in `skills/define/references/` (`BABYSIT_MODE.md`, `CANVAS_MODE.md`, `MULTI_REPO.md`, `WRITING-REFERENCE.md`) cover specialized flows.
