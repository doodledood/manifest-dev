# manifest-dev — Verification-First Manifest Workflows

## Workflow Overview

manifest-dev provides structured workflows for planning, executing, and verifying development tasks through manifests — documents that capture what to build, how to verify it, and what rules to follow.

### Core Workflow

1. **Define** (`/define`) — Build a manifest through structured interview: deliverables, acceptance criteria, global invariants, process guidance
2. **Execute** (`/do`) — Implement the manifest: satisfy acceptance criteria, follow process guidance, use approach as initial direction
3. **Verify** (`/verify`) — Spawn parallel verifiers for all criteria. On success, calls `/done`. On failure, fix and re-verify
4. **Auto** (`/auto`) — End-to-end: `/define` (autonomous) then `/do` in a single command

### Supporting Skills

- **`/figure-out`** — Collaborative deep understanding before acting. Truth-convergence over helpfulness
- **`/escalate`** — Structured escalation during `/do`: blocking issues, scope changes, pauses
- **`/done`** — Completion marker with hierarchical execution summary

### PR Lifecycle

PR-lifecycle work composes the `github-pr-lifecycle` agent through `tasks/PR_LIFECYCLE.md` task guidance. `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. `/auto --babysit <pr-url>` chains synthesis and execution in one command. /do drives the PR to a mergeable state and stops — the merge button is left to a human or GitHub auto-merge.

### Agents

Specialized review agents for code quality verification:

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
| criteria-checker | Single criterion PASS/FAIL verification |
| docs-reviewer | Documentation accuracy against code changes |
| github-pr-lifecycle | Steerable GitHub PR lifecycle inspection — returns natural-language hint for /do to dispatch. Read-only; never invokes the merge button. |
| manifest-verifier | Manifest gap detection with actionable questions |
| type-safety-reviewer | Type holes across typed languages |

### Hooks

Event-driven hooks enforce workflow discipline:

- **stop-do** — Blocks premature stop during `/do` (requires `/verify` or `/escalate`)
- **pretool-verify** — Reminds model to load manifest before `/verify`
- **prompt-submit-amendment** — Checks for manifest amendments on user input
- **post-compact** — Restores /do context after session compaction

## Configuration

Requires in `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```
