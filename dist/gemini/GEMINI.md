# manifest-dev — Verification-First Manifest Workflows

Quality-focused workflows for Gemini CLI that define tasks precisely before implementation, then verify output against acceptance criteria.

## Workflow Overview

The core loop: **Define → Do → Verify → Done/Escalate**

1. `/define` — Interview-driven task specification producing a manifest with acceptance criteria, invariants, and verification methods
2. `/do` — Execute against the manifest, tracking progress in an execution log
3. `/verify` — Parallel verification of all criteria using specialized agents
4. `/done` — Formal completion after all criteria pass
5. `/escalate` — Structured handoff when blocked

## Available Skills

| Skill | Description |
|-------|-------------|
| `/define` | Interactive interview that produces a verification manifest |
| `/do` | Execute implementation against a manifest |
| `/verify` | Parallel verification of manifest criteria |
| `/done` | Formal completion with summary |
| `/escalate` | Structured escalation when blocked |
| `/learn-define-patterns` | Analyze past sessions to learn user preferences |

## Available Agents (12)

### Verification Agents

| Agent | Purpose |
|-------|---------|
| `criteria-checker` | Validates a single criterion (PASS/FAIL). Spawned by /verify in parallel. |
| `manifest-verifier` | Reviews manifests for gaps and outputs continuation questions. |

### Code Review Agents

| Agent | Domain |
|-------|--------|
| `code-bugs-reviewer` | Logical bugs, race conditions, data loss, edge cases |
| `code-design-reviewer` | Design fitness — right approach given what exists |
| `code-simplicity-reviewer` | Unnecessary complexity, over-engineering, cognitive burden |
| `code-maintainability-reviewer` | DRY, coupling, cohesion, consistency, dead code |
| `code-coverage-reviewer` | Test coverage gaps for changed code |
| `code-testability-reviewer` | Testability design — mock friction, logic buried in IO |
| `type-safety-reviewer` | Type holes, invalid states, narrowing gaps |
| `docs-reviewer` | Documentation accuracy against code changes |
| `claude-md-adherence-reviewer` | CLAUDE.md / GEMINI.md rule compliance |

### Analysis Agents

| Agent | Purpose |
|-------|---------|
| `define-session-analyzer` | Extracts user preference patterns from /define sessions |

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `pretool-verify` | BeforeTool (activate_skill) | Reminds agent to load manifest before /verify |
| `stop-do-enforcement` | AfterAgent | Blocks premature stops during /do — requires /done or /escalate |
| `post-compact-recovery` | SessionStart | Recovers /do context after session compaction |

## Setup

Enable agents in your Gemini CLI settings:

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```
