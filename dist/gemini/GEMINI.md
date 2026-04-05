# manifest-dev — Verification-First Manifest Workflows

## Workflow Overview

manifest-dev provides structured workflows for planning, executing, and verifying development tasks through manifests — documents that capture what to build, how to verify it, and what rules to follow.

### Core Workflow

1. **Define** (`/define`) — Build a manifest through structured interview: deliverables, acceptance criteria, global invariants, process guidance
2. **Execute** (`/do`) — Implement the manifest: satisfy acceptance criteria, follow process guidance, use approach as initial direction
3. **Verify** (`/verify`) — Spawn parallel verifiers for all criteria. On success, calls `/done`. On failure, fix and re-verify
4. **Auto** (`/auto`) — End-to-end: `/define` (autonomous) then `/do` in a single command

### Supporting Skills

- **`/figure-out`** — Collaborative deep understanding before acting. Truth-convergence over helpfulness. End with `/stop-thinking-disciplines`
- **`/escalate`** — Structured escalation during `/do`: blocking issues, scope changes, pauses
- **`/done`** — Completion marker with hierarchical execution summary
- **`/tend-pr`** — PR lifecycle automation: classify comments, route fixes, tend CI, sync description
- **`/learn-define-patterns`** — Extract user preferences from past `/define` sessions into GEMINI.md

### Internal Skills

- **`thinking-disciplines`** — Core thinking disciplines invoked by `/figure-out` and `/define`. Not user-invocable
- **`/stop-thinking-disciplines`** — Deactivate thinking disciplines

### Agents

Specialized review agents for code quality verification:

| Agent | Purpose |
|-------|---------|
| change-intent-reviewer | Adversarial intent-behavior divergence analysis |
| code-bugs-reviewer | Mechanical defect detection (race conditions, leaks, edge cases) |
| code-coverage-reviewer | Test coverage gap analysis with concrete scenarios |
| code-design-reviewer | Design fitness: right approach given what exists |
| code-maintainability-reviewer | DRY, coupling, cohesion, consistency, dead code |
| code-simplicity-reviewer | Unnecessary complexity and over-engineering |
| code-testability-reviewer | Test friction: mock count, IO-buried logic |
| context-file-adherence-reviewer | Compliance with GEMINI.md project rules |
| contracts-reviewer | API contract correctness with evidence |
| criteria-checker | Single criterion PASS/FAIL verification |
| define-session-analyzer | Per-session preference pattern extraction |
| docs-reviewer | Documentation accuracy against code changes |
| manifest-verifier | Manifest gap detection with actionable questions |
| type-safety-reviewer | Type holes across typed languages |

### Hooks

Event-driven hooks enforce workflow discipline:

- **stop-do** — Blocks premature stop during `/do` (requires `/verify` or `/escalate`)
- **pretool-verify** — Reminds model to load manifest before `/verify`
- **posttool-log** — Reminds model to update execution log after milestones
- **prompt-submit-amendment** — Checks for manifest amendments on user input
- **thinking-disciplines-prompt** — Reinforces thinking disciplines against sycophantic drift
- **thinking-disciplines-pretool** — Reinforces disciplines before asking user questions
- **post-compact** — Restores /do and thinking disciplines context after session compaction

## Configuration

Requires in `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```
