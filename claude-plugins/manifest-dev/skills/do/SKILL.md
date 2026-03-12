---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass.'
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapting when reality diverges), then verify everything passes (including Global Invariants).

**Why quality execution matters**: The manifest front-loaded the thinking—criteria are already defined. Your job is implementation that passes verification on first attempt. Every verification failure is rework.

## Input

`$ARGUMENTS` = manifest file path (REQUIRED), optionally with execution log path and `--policy=<name>`

If no arguments: Output error "Usage: /do <manifest-file-path> [log-file-path] [--policy=<name>]"

## Execution Policy

Accepted execution policies for v1: `economy`, `balanced`, `max-quality`.

If policy is omitted, default to backward-compatible current behavior and record `policy_source: default`.

If an unknown policy is supplied, warn and fall back to backward-compatible current behavior.

Precedence rules:

- Fresh run with explicit CLI policy: use it and record `policy_source: cli`.
- Fresh run with no CLI policy: use the default behavior and record `policy_source: default`.
- If resuming with an existing execution log, treat the log as the source of truth for active policy.
- If CLI policy conflicts with the log policy on resume, keep the log value, warn, and do not switch policy mid-run.

## Existing Execution Log

If input includes a log file path (iteration on previous work): **treat it as source of truth**. It contains prior execution history. Continue from where it left off—append to the same log, don't restart.

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Work toward acceptance criteria however makes sense. Manifest says WHAT, you decide HOW. |
| **Approach is initial, not rigid** | Approach provides starting direction, but plans break when hitting reality. Adapt freely when you discover better patterns, unexpected constraints, or dependencies that don't work as expected. Log adjustments with rationale. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart. Don't touch passing criteria. |
| **Verify fixes first** | After fixing a failure, confirm the fix works before re-running full verification. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Log adjustments with rationale. |

## Constraints

**Log after every action** - Write to execution log immediately after each AC attempt. No exceptions. This is disaster recovery—if context is lost, the log is the only record of what happened.

**Must call /verify** - Can't declare done without verification. Invoke manifest-dev:verify with manifest and log paths.

**Escalation boundary** - Escalate when: (1) ACs can't be met as written (contract broken), or (2) user requests a pause mid-workflow. If ACs remain achievable and no user interrupt, continue autonomously.

**Stop requires /escalate** - During /do, you cannot stop without calling /verify→/done or /escalate. If you need to pause (user requested, waiting on external action), call /escalate with "User-Requested Pause" format. Short outputs like "Done." or "Waiting." will be blocked.

**Refresh before verify** - Read full execution log before calling /verify to restore context.

## Memento Pattern

Externalize progress to survive context loss. The log IS the disaster recovery mechanism.

**Execution log**: Create `/tmp/do-log-{timestamp}.md` at start. After EACH AC attempt, append what happened and the outcome. Goal: another agent reading only the log could resume work.

Execution log entries must record both `active_policy` and `policy_source`.

**Todos**: Create from manifest (deliverables → ACs). Start with execution order from Approach (adjust if dependencies require). Update todo status after logging (log first, todo second).

## Policy Checkpoints

Checkpoint guidance about model choice must remain recommendation-only.

Do not claim automatic model switching or automatic effort changes.

When policy suggests a cheaper or stronger path, frame it as a user recommendation or checkpoint note, not as a direct runtime control.

## Collaboration Mode

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, read `references/COLLABORATION_MODE.md` for full collaboration mode instructions. If no `TEAM_CONTEXT:` block is present, ignore this — all other sections apply as written.
