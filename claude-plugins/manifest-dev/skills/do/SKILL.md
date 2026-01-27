---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and Approach direction, then verify everything passes (including Global Invariants).

**Why quality execution matters**: The manifest front-loaded the thinking—criteria are already defined. Your job is implementation that passes verification on first attempt. Every verification failure is rework.

## Input

`$ARGUMENTS` = manifest file path (REQUIRED)

If no arguments: Output error "Usage: /do <manifest-file-path>"

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Work toward acceptance criteria however makes sense. Manifest says WHAT, you decide HOW. |
| **Architecture is direction** | Follow approach's architecture as starting direction. Adapt tactics freely—architecture guides, doesn't constrain. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart. Don't touch passing criteria. |
| **Verify fixes first** | After fixing a failure, confirm the fix works before re-running full verification. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Log adjustments with rationale. |

## Constraints

**Log after every action** - Write to execution log immediately after each AC attempt. No exceptions. This is disaster recovery—if context is lost, the log is the only record of what happened.

**Must call /verify** - Can't declare done without verification. Invoke manifest-dev:verify with manifest and log paths.

**Escalation boundary** - Escalate only when ACs can't be met as written (contract broken). If ACs remain achievable, adjust and continue autonomously.

**Refresh before verify** - Read full execution log before calling /verify to restore context.

## Memento Pattern

Externalize progress to survive context loss. The log IS the disaster recovery mechanism.

**Execution log**: Create `/tmp/do-log-{timestamp}.md` at start. After EACH AC attempt, append what happened and the outcome. Goal: another agent reading only the log could resume work.

**Todos**: Create from manifest (deliverables → ACs). Follow execution order from Approach. Update todo status after logging (log first, todo second).
