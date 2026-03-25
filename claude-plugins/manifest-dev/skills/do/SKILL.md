---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Optional --mode efficient|balanced|thorough controls verification intensity (default: thorough). Only pass --mode when the user explicitly requests a different mode. Use when executing a manifest, running a plan, implementing a defined task.'
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapting when reality diverges), then verify everything passes (including Global Invariants).

**Why quality execution matters**: The manifest front-loaded the thinking—criteria are already defined. Your job is implementation that passes verification on first attempt. Every verification failure is rework.

## Input

`$ARGUMENTS` = manifest file path (REQUIRED), optionally with execution log path and `--mode <level>`

If no arguments: Output error "Usage: /do <manifest-file-path> [log-file-path] [--mode efficient|balanced|thorough]"

## Execution Mode

Resolve mode from (highest precedence first): `--mode` argument → manifest `mode:` field → default `thorough`.

Invalid mode value → error and halt: "Invalid mode '<value>'. Valid modes: efficient | balanced | thorough"

If mode is not `thorough`: read `references/BUDGET_MODES.md` for routing rules, escalation logic, and parallelism overrides. Follow those rules for the remainder of this /do run.

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

**Must call /verify** - Can't declare done without verification. Invoke manifest-dev:verify with manifest, log paths, and the resolved mode: `/verify <manifest> <log> --mode <level>`.

**Escalation boundary** - Escalate when: (1) ACs can't be met as written (contract broken), (2) user requests a pause mid-workflow, (3) you discover an AC or invariant should be amended (use "Proposed Amendment" escalation type), or (4) mode-specific fix-verify loop limit is reached (see `references/BUDGET_MODES.md`). If ACs remain achievable as written and no user interrupt, continue autonomously. Approach pivots don't require escalation — log adjustments with rationale and continue.

**Mode-aware loop tracking** - Track fix-verify iteration count and escalation count in the execution log. Loop counters are per-phase — each phase has its own counter. When mode limits are reached for a phase, follow the escalation rules in `references/BUDGET_MODES.md`. In efficient mode, also track total escalations and suggest mode switch after 3.

**Phase-aware verification** - /verify runs criteria in phases (ascending by `phase:` field, default 1). It may report "Phase N failed, Phase N+1 not run." After fixing failures, /verify restarts from Phase 1 to catch regressions — a fix for a Phase 2 failure could break Phase 1 criteria. If a Phase 2 fix regresses Phase 1, Phase 1's loop counter increments (the failure IS in Phase 1).

**Stop requires /escalate** - During /do, you cannot stop without calling /verify→/done or /escalate. If you need to pause (user requested, waiting on external action), call /escalate with "User-Requested Pause" format. Short outputs like "Done." or "Waiting." will be blocked.

**Refresh before verify** - Read full execution log before calling /verify to restore context.

**Refresh between deliverables** - Before starting a new deliverable, re-read the manifest's deliverable section and relevant execution log entries. Context degrades gradually across a long session — don't rely on what you remember from D1 when starting D3.

## Memento Pattern

Externalize progress to survive context loss. The log IS the disaster recovery mechanism.

**Execution log**: Create `/tmp/do-log-{timestamp}.md` at start. After EACH AC attempt, append what happened and the outcome. Goal: another agent reading only the log could resume work.

**Todos**: Create from manifest (deliverables → ACs). Start with execution order from Approach (adjust if dependencies require). Update todo status after logging (log first, todo second).

## Mid-Execution Amendment

**When to trigger** — User input or a PR review comment changes scope: new requirements, contradicted ACs, missing coverage. Clarifications and confirmations are NOT amendments — only act when the manifest's criteria themselves need to change.

**Amendment flow** — Amend the manifest autonomously via Self-Amendment escalation and `/define --amend <manifest-path> --from-do`, then resume with the updated manifest and existing log. Log the trigger before amending. No human wait — the entire cycle is autonomous.

**PR review comments** — Same trigger. During the review phase, a comment that contradicts or extends the manifest is an amendment trigger.

**Amendment loop guard** (R-7) — If Self-Amendment escalations repeat without new external input (user messages or PR comments) between them, the amendments are likely oscillating — escalate as "Proposed Amendment" for human decision instead.

## Collaboration Mode

When the manifest's `Medium:` field is not `local`, read `references/COLLABORATION_MODE.md` for routing rules. If medium is `local` (default) or absent, ignore this — all other sections apply as written.
