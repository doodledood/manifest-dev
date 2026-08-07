# AGENTS.md — manifest-dev Workflow Context

## Overview

manifest-dev provides manifest-driven workflows for AI coding agents. The core flow is:

```
/define → manifest → /do (executes + verifies inline) → /done
```

- **/define** — Interactive manifest builder. Probes for requirements, quality gates, edge cases. Outputs a manifest with deliverables, acceptance criteria, and global invariants.
- **/do** — Manifest executor. Implements deliverables, weighs process guidance, adapts approach when reality diverges, and evaluates every gate using its verbatim instructions. `consolidated` is the independent default; `per-gate` is an opt-in higher-rigor mode and `self` an opt-in lower-assurance one. Optional `--verifier-model` applies to independent modes. It aggregates PASS / FAIL / BLOCKED, fixes failures, and re-evaluates — command-backed gates in full, judgment gates over their prior findings' repairs and the changed delta after one full look, with `--exhaustive-verification` restoring full re-sampling. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping.
- **/done** — Plain-prose completion summary called by /do after every criterion has fresh PASS evidence under the selected mode.
- **/escalate** — Structured blocker handoff for unrecoverable failures or pending external action.

Supporting workflows:
- **/auto** — End-to-end autonomous: /figure-out → /define → /do in one command. It forwards `/do`'s verification options without putting them in the Manifest. Its unattended parent goal should treat full autonomous Read anatomy as a checkpoint before manifest creation when figure-out runs, then use manifest written plus /do gate-ledger PASS as the terminal condition. Supports `--babysit <pr-url>` for tending an existing PR end-to-end.
- **/figure-out** — Truth-convergent thinking partner. /define auto-invokes it when the problem space is foggy.
- **/figure-out-team** — /figure-out's discipline applied to a multi-party async Slack conversation.
- **/ticket-up** — Splits a finished manifest into one self-sufficient, plain-prose ticket per deliverable plus explicit dependency edges, so teammates, agents, or later sessions can pick the work up in parallel — with or without manifest-dev. Files store by default; GitHub Issues out of the box; custom trackers from details you provide once.
- **/next-ticket** — Reads a ticket store and names the single best ready ticket to work on now, with the reason.
- **Tools skills** — /babysit-pr, /handoff, /prompt-engineering, /re-pitch, /review-pr, /teach-me, and /walk-pr ship alongside the core skills under their original names. /babysit-pr is the author-side companion to /review-pr and supports CI one-shot advancement via `--ci`; /teach-me turns a body of work — the session, a PR, an ADR, or any topic — into an incremental teaching loop with mastery checks.

## Manifest Schema — Evaluation Instructions

Every verify block has the same shape. It describes what evidence to gather and what PASS means without selecting execution topology or model — there is no `agent` field.

```yaml
verify:
  instructions: "..."  # required, topology-neutral evaluation procedure
  kind: judgment        # required: judgment | deterministic — no default, never inferred
  phase: 1              # optional integer, default 1 (lower phases run first)
```

`kind` declares what settles the gate. A `deterministic` gate re-runs in full every round; a `judgment` gate reads the whole change once and afterwards judges only its prior findings' repairs and the changed delta. A gate mixing a command with a judgment is `judgment`. A manifest whose gate omits `kind` is invalid.

Each gate evaluation returns **PASS**, **FAIL**, or **BLOCKED**. BLOCKED routes via /escalate (external action pending — deploy, human approval).

## PR Lifecycle

PR-lifecycle gate instructions activate the `check-pr` skill under the selected mode through `tasks/PR_LIFECYCLE.md` task guidance. `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. /babysit-pr uses manifest/PR grounding and runs the lifecycle; /do drives the PR to a mergeable state and stops — the merge button is left to a human or GitHub auto-merge.

## Code review

Quality review is the **`review-code` skill** (one dimension per invocation, each loading its own reference): `change-intent`, `code-bugs`, `contracts`, `type-safety` (defect-finders, no LOW+); `operational-readiness`, `code-design`, `code-maintainability`, `code-simplicity`, `code-testability`, `test-quality`, `docs`, `prose-value`, `context-file-adherence` (advisory, no MEDIUM+). Gate instructions activate `review-code` with the dimension.

## Agents

manifest-dev ships no agents. `/do` uses host execution contexts according to the selected mode; formerly-agent capabilities ship as skills (`check-pr`, `poll-slack`, and the tools-side `review-prompt`).

## Unattended Execution

Run `/do` with a durable goal-setting/continuation backstop whose contract is the auditable all-criteria-PASS condition when you want the host CLI to keep `/do` running across turns: every manifest gate listed with fresh evidence and evaluator provenance under the selected mode, not a summary claim. For `/auto`, use one full-chain parent goal whose terminal condition is manifest written plus `/do` gate-ledger PASS; when figure-out runs first, its full autonomous Read anatomy is a checkpoint before `/define`. Use a host-native goal-setting capability when available; otherwise copy the completion contract the skill prints into your continuation mechanism.
