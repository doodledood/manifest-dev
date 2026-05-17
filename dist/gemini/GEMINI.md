# manifest-dev — Manifest-Driven Workflows

## Workflow Overview

manifest-dev provides structured workflows for planning, executing, and verifying development tasks through manifests — documents that capture what to build, how to verify it, and what rules to follow.

### Core Workflow

1. **Define** (`/define`) — Build a manifest through structured interview: deliverables, acceptance criteria, global invariants, process guidance
2. **Execute and verify** (`/do`) — Implement the manifest and verify inline: spawn one subagent per Acceptance Criterion and Global Invariant using the verify prompt verbatim, aggregate PASS / FAIL / BLOCKED, fix failures, re-verify
3. **Auto** (`/auto`) — End-to-end: `/define` (autonomous) then `/do` in a single command

### Supporting Skills

- **`/figure-out`** — Truth-convergent thinking partner. `/define` auto-invokes it when the problem space is foggy; call it directly when figuring it out IS the goal
- **`/figure-out-team`** — `/figure-out`'s discipline applied to a multi-party async Slack conversation
- **`/escalate`** — Structured blocker handoff: criterion, attempts, possible resolutions, what's needed from the user
- **`/done`** — Plain-prose completion summary called by `/do` after every criterion verifies PASS

### PR Lifecycle

PR-lifecycle work composes the `github-pr-lifecycle` agent through `tasks/PR_LIFECYCLE.md` task guidance. `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. `/auto --babysit <pr-url>` chains synthesis and execution in one command. /do drives the PR to a mergeable state and stops — the merge button is left to a human or GitHub auto-merge.

### Agents

Specialized subagents spawned by `/do` for criterion verification. Name one in `verify.agent:` to scope to its lens:

| Agent | Purpose |
|-------|---------|
| change-intent-reviewer | Adversarial intent-behavior divergence analysis |
| code-bugs-reviewer | Mechanical defect detection (race conditions, leaks, edge cases) |
| test-quality-reviewer | Coverage gap analysis plus tautological-test detection (mirror-impl, mock-SUT, trivial-asserts, snapshot-without-intent) |
| prose-value-reviewer | Comments and repo doc files: narrating-the-obvious, generic puffery, AI rhetorical patterns, sycophantic fragments — comments must be load-bearing-WHY |
| code-design-reviewer | Design fitness: right approach given what exists |
| code-maintainability-reviewer | DRY, coupling, cohesion, consistency, dead code |
| code-simplicity-reviewer | Unnecessary complexity and over-engineering |
| code-testability-reviewer | Test friction: mock count, IO-buried logic |
| context-file-adherence-reviewer | Compliance with GEMINI.md project rules |
| contracts-reviewer | API contract correctness with evidence |
| criteria-checker | Single criterion PASS/FAIL verification — default subagent when verify.agent is omitted |
| docs-reviewer | Documentation accuracy against code changes |
| github-pr-lifecycle | Steerable GitHub PR lifecycle inspection — returns natural-language hint for /do to dispatch. Read-only; never invokes the merge button. |
| slack-poller | Narrate new Slack messages in a channel or thread since a cursor. Used by /figure-out-team. |
| type-safety-reviewer | Type holes across typed languages |

### Hooks

Event-driven hooks enforce workflow discipline:

- **stop-do** — Blocks premature stop during `/do` (requires `/done` or `/escalate`)
- **post-compact** — Restores `/do` context after session compaction

## Configuration

Requires in `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```
