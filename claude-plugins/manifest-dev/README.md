# manifest-dev

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

## Overview

A structured approach to task definition and execution:

1. **Approach** (complex tasks) - Validated implementation direction: architecture, execution order, risks, trade-offs
2. **Global Invariants** - Rules that apply to the ENTIRE task (e.g., "tests must pass")
3. **Deliverables** - Specific items to complete, each with **Acceptance Criteria**
   - ACs can be positive ("user can log in") or negative ("passwords are hashed")

## The Manifest Schema

```markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts/architecture]

## 2. Approach (Complex Tasks Only)
*Validated implementation direction.*

- **Architecture:** [High-level HOW - validated direction]
- **Execution Order:** D1 → D2 → D3 | Rationale: [why]
- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
- **Trade-offs:**
  - [T-1] [A] vs [B] → Prefer [A] because [reason]

## 3. Global Invariants (The Constitution)
- [INV-G1] Description | Verify: [method]
- [INV-G2] Description | Verify: [method]

## 4. Deliverables (The Work)

### Deliverable 1: [Name]
- **Acceptance Criteria**:
  - [AC-1.1] Description | Verify: [method]
  - [AC-1.2] Description | Verify: [method]
```

## ID Scheme

| Type | Pattern | Purpose | Used By |
|------|---------|---------|---------|
| Global Invariant | INV-G{N} | Task-level rules | /verify (verified) |
| Process Guidance | PG-{N} | Non-verifiable HOW constraints | /do (followed) |
| Risk Area | R-{N} | Pre-mortem flags | /do (watched) |
| Trade-off | T-{N} | Decision criteria for adjustment | /do (consulted) |
| Acceptance Criteria | AC-{D}.{N} | Deliverable completion | /verify (verified) |

## Interview Philosophy

**YOU generate, user validates.** Users have surface-level knowledge. Don't ask open-ended questions - generate candidates from domain knowledge, present concrete options, learn from reactions.

**Phase order** (high info-gain first):
1. Intent & Context (task type, scope, risk)
2. Deliverables (what are we building?)
3. Acceptance Criteria (how do we know each is done?)
4. Approach (complex tasks: architecture, execution order, risks, trade-offs)
5. Global Invariants & Process Guidance (auto-detect + generate candidates)

## Skills

### User-Invocable

| Skill | Description |
|-------|-------------|
| `/define` | Manifest builder with verification criteria. Converts known requirements into Deliverables + Invariants. Outputs executable manifest. |
| `/do` | Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. |

### Task-Specific Guidance

`/define` is domain-agnostic and works for any deliverable type. Task-specific guidance is loaded conditionally:

| Task Type | File | When Loaded |
|-----------|------|-------------|
| Code | `skills/define/tasks/CODING.md` | APIs, features, fixes, refactors, tests |
| Document | `skills/define/tasks/DOCUMENT.md` | Specs, proposals, reports, articles, docs |
| Blog | `skills/define/tasks/BLOG.md` | Blog posts, content writing |
| Research | `skills/define/tasks/RESEARCH.md` | Research tasks, analysis, investigation |
| Other | (none) | Doesn't fit above categories |

The universal flow (core principles, manifest schema) works without any task file.

### Internal

| Skill | Purpose |
|-------|---------|
| `/verify` | Manifest verification runner. Spawns parallel verifiers for Global Invariants and Acceptance Criteria. |
| `/done` | Completion marker. Outputs hierarchical execution summary showing Global Invariants respected and all Deliverables completed. |
| `/escalate` | Structured escalation with evidence. Surfaces blocking issues for human decision, referencing the Manifest hierarchy. |

## Agents

### Core Workflow

| Agent | Purpose |
|-------|---------|
| `criteria-checker` | Read-only verification agent. Validates a single criterion using commands, codebase analysis, file inspection, reasoning, or web research. Returns structured PASS/FAIL. |
| `manifest-verifier` | Reviews /define manifests for gaps and outputs actionable continuation steps. Returns specific questions to ask and areas to probe. |

### Code Reviewers

Specialized review agents spawned in parallel during `/verify`:

| Agent | Focus |
|-------|-------|
| `code-bugs-reviewer` | Audits code changes for logical bugs without making modifications |
| `code-coverage-reviewer` | Verifies code changes have adequate test coverage, reports gaps |
| `code-maintainability-reviewer` | DRY violations, coupling, cohesion, consistency, dead code, architectural boundaries |
| `code-simplicity-reviewer` | Unnecessary complexity, over-engineering, cognitive burden |
| `code-testability-reviewer` | Code that requires excessive mocking, business logic hard to verify in isolation |
| `type-safety-reviewer` | TypeScript type holes, opportunities to make invalid states unrepresentable |
| `claude-md-adherence-reviewer` | Verifies code changes comply with CLAUDE.md instructions and project standards |
| `docs-reviewer` | Audits documentation accuracy against recent code changes |

## Hooks

| Hook | Purpose |
|------|---------|
| `stop_do_hook.py` | Enforces verification before stopping |
| `post_compact_hook.py` | Restores /do workflow context after session compaction |
| `pretool_verify_hook.py` | Reminds to read manifest/log before verification |

## Workflow

```
/define "task" → Interview → Manifest file
                    │
                    ├─ Intent & Context
                    ├─ Deliverables (with ACs)
                    ├─ Approach (complex tasks: architecture, order, risks, trade-offs)
                    └─ Global Invariants & Process Guidance
                                   ↓
/do manifest.md → Follow execution order, watch for risks
                    │
                    ├─ Risk detected? → Consult trade-offs → Adjust approach
                    │                   (ACs achievable? Continue : /escalate)
                    │
                    └─ For each Deliverable: Satisfy ACs
                                   ↓
                  /verify → (failures) → Fix specific criterion → /verify again
                         ↓
                  All pass → /done
                         ↓
                  (stuck) → /escalate
```

## Execution Semantics

| Phase | Check | Failure Impact |
|-------|-------|----------------|
| After each deliverable | Acceptance Criteria | Deliverable incomplete |
| Final verification | Global Invariants + all ACs | Must all pass for /done |

## Status

Use when you want quality-focused autonomous execution with clear separation of constraints and deliverables.
