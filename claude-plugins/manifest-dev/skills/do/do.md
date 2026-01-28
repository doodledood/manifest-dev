---
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and Approach direction, then verify everything passes (including Global Invariants).

## Input

`$ARGUMENTS` = manifest file path (REQUIRED), optionally with execution log path for iterations

If no arguments: Output error "Usage: /do <manifest-file-path> [log-file-path]"

## Existing Execution Log

If input includes a log file path (iteration on previous work): **treat it as source of truth**. It contains execution history and decisions made. Continue from where it left off—don't restart.

When iterating:
1. Read the existing log to understand prior work
2. Append new progress to the same log (don't create a new file)
3. Focus on what changed or failed in the previous attempt

## Principles

**Manifest says WHAT, you decide HOW** — ACs define success. Work toward them however makes sense. Architecture guides direction, doesn't constrain tactics.

**On failure, target specifically** — Fix the failing criterion. Don't restart. Don't touch passing criteria. Verify the fix before re-running full verification.

**Consult trade-offs when risks materialize** — When R-* risks appear, use T-* trade-offs for decision criteria. Log adjustments.

## Constraints

**Log after every action** — Write to execution log after each AC attempt. The log is disaster recovery—if context is lost, another agent reading only the log could resume.

**Must call /verify** — Invoke manifest-dev:verify with manifest and log paths. Can't declare done without it.

**Escalate only when contract is broken** — If ACs can't be met as written, escalate. If ACs remain achievable, adjust and continue.

## Execution Log

Externalize progress to survive context loss.

**New execution**: Create `/tmp/do-log-{timestamp}.md` at start.

**Iteration**: Reuse existing log file from input. Append, don't overwrite.

**After each AC**: Log what happened and the outcome. Read full log before calling /verify.
