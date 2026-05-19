# AGENTS.md — manifest-dev Workflow Context

## Overview

manifest-dev provides manifest-driven workflows for AI coding agents. The core flow is:

```
/define → manifest → /do (executes + verifies inline) → /done
```

- **/define** — Interactive manifest builder. Probes for requirements, quality gates, edge cases. Outputs a manifest with deliverables, acceptance criteria, and global invariants.
- **/do** — Manifest executor. Implements deliverables, follows process guidance, adapts approach when reality diverges. Verifies inline by spawning one subagent per Acceptance Criterion and Global Invariant using the verify prompt verbatim. Aggregates PASS / FAIL / BLOCKED, fixes failures, re-verifies.
- **/done** — Plain-prose completion summary called by /do after every criterion verifies PASS.
- **/escalate** — Structured blocker handoff for unrecoverable failures or pending external action.

Supporting workflows:
- **/auto** — End-to-end autonomous: /define → /do in one command. Supports `--babysit <pr-url>` for tending an existing PR end-to-end.
- **/figure-out** — Truth-convergent thinking partner. /define auto-invokes it when the problem space is foggy.
- **/figure-out-team** — /figure-out's discipline applied to a multi-party async Slack conversation.

## Manifest Schema — Four Fields

Every verify block has the same shape:

```yaml
verify:
  prompt: "..."     # required, verbatim verifier instruction
  agent: "..."      # optional, default = general-purpose subagent
  model: "..."      # optional, default = inherit from invoking context
  phase: 1          # optional integer, default 1 (lower phases run first)
```

The subagent returns **PASS**, **FAIL**, or **BLOCKED**. BLOCKED routes via /escalate (external action pending — deploy, human approval).

## PR Lifecycle

PR-lifecycle work composes the `github-pr-lifecycle` agent through `tasks/PR_LIFECYCLE.md` task guidance. `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. /do drives the PR to a mergeable state and stops — the merge button is left to a human or GitHub auto-merge.

## Agents

16 specialized subagents, all read-only:

| Agent | Purpose |
|-------|---------|
| change-intent-reviewer | Adversarial intent-behavior divergence analysis |
| code-bugs-reviewer | Mechanical defect detection (race conditions, leaks, edge cases) |
| operational-readiness-reviewer | Runtime and deployment readiness: environment wiring, migrations, retries, rollback, scale, CI, and observability |
| test-quality-reviewer | Coverage gap analysis plus independent behavioral-oracle checks |
| prose-value-reviewer | Comments and repo doc files: narrating-the-obvious, generic puffery, AI rhetorical patterns, sycophantic fragments — comments must be load-bearing-WHY |
| code-design-reviewer | Design fitness (reinvented wheels, wrong responsibility owner, under-engineering) |
| code-maintainability-reviewer | Code organization (DRY, coupling, cohesion, consistency) |
| code-simplicity-reviewer | Unnecessary complexity and over-engineering |
| code-testability-reviewer | Test friction analysis (mock count, logic in IO) |
| context-file-adherence-reviewer | Context file compliance (AGENTS.md/CLAUDE.md/GEMINI.md rules) |
| contracts-reviewer | API and interface contract correctness with source-of-truth evidence |
| criteria-checker | Single-criterion verifier — the default subagent when verify.agent is omitted |
| docs-reviewer | Documentation accuracy against code changes |
| github-pr-lifecycle | Steerable GitHub PR lifecycle inspection — returns natural-language hint for /do to dispatch. Read-only; never invokes the merge button. |
| slack-poller | Narrate new Slack messages in a channel or thread since a cursor. Used by /figure-out-team. |
| type-safety-reviewer | Type system improvements across typed languages |

## Plugin (Hooks)

The manifest-dev plugin (`.opencode/plugins/manifest-dev.ts`) provides:
- Workflow state tracking for /do
- Post-compaction context recovery

**Known limitation**: OpenCode cannot block session stopping (session.idle is fire-and-forget). The /do workflow contract is enforced via persistent system guidance, not a hard block.
