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
| `/define` | Manifest builder - YOU generate candidates, user validates (no open-ended questions) |
| `/do` | Manifest executor - iterates deliverables, satisfies ACs, calls /verify |

### Task-Specific Guidance

`/define` is domain-agnostic and works for any deliverable type. Task-specific guidance is loaded conditionally:

| Task Type | File | When Loaded |
|-----------|------|-------------|
| Code | `skills/define/tasks/CODING.md` | APIs, features, fixes, refactors, tests |
| Document | `skills/define/tasks/DOCUMENT.md` | Specs, proposals, reports, articles, docs |
| Other | (none) | Research, analysis, or doesn't fit above |

The universal flow (core principles, manifest schema) works without any task file.

### Internal

| Skill | Purpose |
|-------|---------|
| `/verify` | Runs all verifications, reports by type and deliverable |
| `/done` | Outputs hierarchical completion summary |
| `/escalate` | Structured escalation with type-aware context |

## Agents

| Agent | Purpose |
|-------|---------|
| `criteria-checker` | Verifies a single criterion with type awareness |
| `manifest-verifier` | Reviews manifests for gaps, outputs actionable continuation steps |

## Hooks

| Hook | Purpose |
|------|---------|
| `stop_do_hook.py` | Enforces verification before stopping |
| `pretool_escalate_hook.py` | Enforces /verify before /escalate |

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
