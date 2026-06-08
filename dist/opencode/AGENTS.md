# AGENTS.md — manifest-dev Workflow Context

## Overview

manifest-dev provides manifest-driven workflows for AI coding agents. The core flow is:

```
/define → manifest → /do (executes + verifies inline) → /done
```

- **/define** — Interactive manifest builder. Probes for requirements, quality gates, edge cases. Outputs a manifest with deliverables, acceptance criteria, and global invariants.
- **/do** — Manifest executor. Implements deliverables, follows process guidance, adapts approach when reality diverges. Verifies inline by spawning one subagent per Acceptance Criterion and Global Invariant using the verify prompt verbatim. Aggregates PASS / FAIL / BLOCKED, fixes failures, re-verifies. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping.
- **/done** — Plain-prose completion summary called by /do after every criterion verifies PASS.
- **/escalate** — Structured blocker handoff for unrecoverable failures or pending external action.

Supporting workflows:
- **/auto** — End-to-end autonomous: /define → /do in one command. Supports `--babysit <pr-url>` for tending an existing PR end-to-end.
- **/figure-out** — Truth-convergent thinking partner. /define auto-invokes it when the problem space is foggy.
- **/figure-out-team** — /figure-out's discipline applied to a multi-party async Slack conversation.
- **Tools skills** — /adr, /babysit-pr, /handoff, /prompt-engineering, /review-pr, /teach-me, and /walk-pr install with the `-manifest-dev-tools` suffix. /babysit-pr is the author-side companion to /review-pr and supports CI one-shot advancement via `--ci`; /teach-me turns a body of work — the session, a PR, an ADR, or any topic — into an incremental teaching loop with mastery checks.

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

PR-lifecycle work activates the `github-pr-lifecycle` skill (via a general-purpose verifier) through `tasks/PR_LIFECYCLE.md` task guidance. `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. /babysit-pr uses manifest/PR grounding and runs the lifecycle; /do drives the PR to a mergeable state and stops — the merge button is left to a human or GitHub auto-merge.

## Code review

Quality review is the **`code-review` skill** (one dimension per invocation, each loading its own reference): `change-intent`, `code-bugs`, `contracts`, `type-safety` (defect-finders, no LOW+); `operational-readiness`, `code-design`, `code-maintainability`, `code-simplicity`, `code-testability`, `test-quality`, `docs`, `prose-value`, `context-file-adherence` (advisory, no MEDIUM+). A verifier spawns a general-purpose subagent and activates `code-review` with the dimension.

## Agents

manifest-dev ships no agents. Verification is a general-purpose subagent that activates the relevant skill — formerly-agent capabilities now ship as skills (`criteria-checker`, `github-pr-lifecycle`, `slack-poller`, and the tools-side `prompt-reviewer`).

## Unattended Execution

Run `/goal /do <manifest-path>` when you want the host CLI to keep `/do` running across turns.
