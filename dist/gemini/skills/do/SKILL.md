---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Optional --mode efficient|balanced|thorough controls verification intensity (default: thorough). Only pass --mode when the user explicitly requests a different mode. Use when executing a manifest, running a plan, implementing a defined task.'
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapting when reality diverges), then verify everything passes (including Global Invariants).

## Input

`$ARGUMENTS` = manifest file path (REQUIRED), optionally with execution log path, `--mode <level>`, and `--scope <deliverable-ids>`

If no arguments: Output error "Usage: /do <manifest-file-path> [log-file-path] [--mode efficient|balanced|thorough] [--scope D1,D2,...]"

Read the manifest file fully before any execution.

## Execution Mode

Resolve mode from (highest precedence first): `--mode` argument → manifest `mode:` field → default `thorough`.

Invalid mode value → error and halt: "Invalid mode '<value>'. Valid modes: efficient | balanced | thorough"

Load the execution mode file for behavioral specifics:
- `thorough` (default): read `references/execution-modes/thorough.md`
- `balanced`: read `references/execution-modes/balanced.md`
- `efficient`: read `references/execution-modes/efficient.md`

Follow the loaded mode's rules for model routing, verification parallelism, fix-verify loop limits, and escalation for the remainder of this /do run.

**Override precedence** (applies to all modes):
1. **Criterion-level model wins**: When a manifest criterion specifies `model:` in its verify block, that overrides the mode's model routing.
2. **Explicit model overrides skip**: If a criterion explicitly sets `model:`, it runs even when the mode would otherwise skip it.
3. **Global Invariants always run**: INV-G* verification runs regardless of mode — constitutional constraints.

## Existing Execution Log

If input includes a log file path (iteration on previous work): **treat it as source of truth**. It contains prior execution history. Continue from where it left off—append to the same log, don't restart.

## Scoped Execution

Parse `--scope` from arguments if present. Accepts comma-separated deliverable IDs (e.g. `--scope D2,D3`).

When `--scope` is provided, read `references/SCOPED_EXECUTION.md` and follow its rules for scoped execution. This limits work to the specified deliverables while maintaining global invariant safety.

When `--scope` is NOT provided, ignore this section entirely — no reference file is loaded, no scoping behavior applies. Full execution as normal.

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Work toward acceptance criteria however makes sense. Manifest says WHAT, you decide HOW. |
| **Approach is initial, not rigid** | Approach provides starting direction, but adapt freely when reality diverges. No escalation needed — log adjustments with rationale. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart. Don't touch passing criteria. |
| **Verify fixes first** | After fixing a failure, confirm the fix works before re-running full verification. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Log adjustments with rationale. |

## Constraints

**Log after every action** - Write to execution log immediately after each AC attempt. No exceptions. This is disaster recovery—if context is lost, the log is the only record of what happened.

**Must call /verify** - Can't declare done without verification. Invoke manifest-dev:verify with manifest, log paths, the resolved mode, and an optional scope per the rules below: `/verify <manifest> <log> --mode <level> [--scope D2,D3]`. Never pass `--final` from /do — that flag is internal to /verify (auto-triggered after a selective green pass) and exists to enforce the hard final gate. /done is unreachable without a full-mode green pass; /verify owns the selective→full chain.

**Selective verification + fix-loop scope** - /verify supports two modes (see verify SKILL.md for full contract):
- *First pass on fresh /do* — invoke without `--scope` and without `--final`. Selective mode degenerates to full (nothing to narrow). Equivalent to today's behavior.
- *Scoped /do* (`--scope D2,D3` was passed to /do) — invoke /verify with the same `--scope D2,D3`. Selective pass runs those deliverables' ACs + all globals.
- *Fix-loop after AC-X.Y failure* — invoke /verify with `--scope D{X}` (the failing criterion's deliverable). Other deliverables are not re-verified during this iteration; they get their pass at the mandatory full final gate when /verify auto-triggers it.
- *Fix-loop after INV-G failure* — invoke /verify normally (globals always run; no narrowing makes sense). When the failure happened during a selective pass with a `--scope`, the next pass is selective on the same deliverable + globals. When the failure happened during a full pass (auto-triggered final, or first-pass degenerated-to-full — no `--scope` was set), the next pass is also full — invoke /verify with no `--scope`. INV-G failures are not deliverable-scoped, so falling through to full is the correct default.

The mandatory full final gate (auto-triggered by /verify after selective green) is the safety net for cross-deliverable regressions. Don't try to skip or short-circuit it.

**Execution log /verify contract** - /verify appends a structured block (`## /verify pass {N}` + fenced YAML with `mode`, `scope`, `result`, `failures`, `auto_triggered_final`, `deferred`) per invocation. Read the most recent block before deciding the next pass's scope. Format defined in `verify/SKILL.md` "/verify Pass Logging Contract." When scanning for the most recent /verify pass to drive scope decisions, **skip blocks with `deferred: true`** — those reflect user-direct `--deferred` invocations (now possible since /verify is user-invocable), not /do-driven normal-flow passes.

**Escalation boundary** - Escalate when: (1) ACs can't be met as written (contract broken), (2) user requests a pause mid-workflow, (3) you discover an AC or invariant should be amended (use "Proposed Amendment" escalation type), or (4) the active execution mode's fix-verify loop limit is reached. If ACs remain achievable as written and no user interrupt, continue autonomously.

**`/verify`-routed escalation passthrough.** When `/verify` itself routes to `/escalate` (e.g., "Deferred-Auto Pending", "Manual Criteria Review") instead of `/done`, treat as a clean terminal handoff: surface the escalation output verbatim to the caller, do NOT enter the fix-loop, do NOT increment loop counters. The implementation is green; further action belongs to the user (e.g., running `/verify --deferred` for deferred-auto pending). This is distinct from `/verify` returning failures (which enters the standard fix-loop).

**Mode-aware loop tracking** - Track fix-verify iteration count and escalation count in the execution log. When the active execution mode's limits are reached, follow its escalation rules.

**Phase-aware verification** - /verify runs criteria in phases (ascending by `phase:` field, default 1). It may report "Phase N failed, Phase N+1 not run." After fixing failures, /verify restarts from Phase 1 to catch regressions. Loop limits apply per-phase; regressions increment the broken phase's counter, not the phase that caused them.

**Stop requires /escalate** - During /do, you cannot stop without calling /verify→/done or /escalate. If you need to pause, call /escalate with "User-Requested Pause" format. Bare outputs like "Done." or "Waiting." are not valid exits.

## Memento Pattern

Externalize progress to survive context loss.

**Execution log**: Create `/tmp/do-log-{timestamp}.md` at start. After EACH AC attempt, append what happened and the outcome. Goal: another agent reading only the log could resume work.

**Todos**: Create from manifest (deliverables → ACs). Start with execution order from Approach (adjust if dependencies require). Update todo status after logging (log first, todo second).

**Refresh before verify** - Read full execution log before calling /verify to restore context.

**Refresh between deliverables** - Before starting a new deliverable, re-read the manifest's deliverable section and relevant log entries. Context degrades across long sessions.

## Multi-Repo Navigation

When the manifest declares `Repos: [name: path, ...]` in Intent, deliverables may live in repos other than cwd. Read the path map and use **absolute paths** in tool calls (Read/Edit/Write/Bash) when working on a deliverable tagged with a different repo. There is **no filter logic, no cwd matching, no per-repo configuration** — the LLM navigates as deliverables require.

A single `/do` invocation can cover the whole multi-repo task by navigating between repos; alternatively the user invokes `/do` per repo with `--scope` for parallel execution. Either works. The execution log remains a single file per `/do` invocation.

When the manifest has no `Repos:` field (single-repo manifest), this section does not apply — behavior is unchanged.

Full convention: `references/MULTI_REPO.md` (lives in `define/references/`).

## Mid-Execution Amendment

**Default to amend.** Any user message arriving during /do or /verify defaults to triggering Self-Amendment. The manifest is the canonical source of truth for the PR/branch — or, in multi-repo cases, the **PR set / branch set** (see `references/AMENDMENT_MODE.md`). Feedback flows through it, not around it. The asymmetric framing is deliberate: silent scope drift (feedback acted on inline, manifest left out of date) is a worse failure than an occasional unnecessary amendment cycle.

**Carve-out: pure questions.** Messages that ask about the manifest or process without requesting a state change are answered inline — no amendment.
- *Amend:* "Also handle X." / "Change Y to Z." / "That's wrong, it should be …" / "Add a check for …"
- *Inline:* "What does AC-1.1 require?" / "Why did you choose approach A over B?" / "Where's the execution log?" / "Which deliverable is D3?"

**When ambiguous, amend.** A message that could be either ("hmm, what about the auth case?") goes to amendment. Re-running an amendment cycle is cheap; silently dropping a constraint that turns out to matter is expensive.

**/verify-time feedback.** While /verify is running under /do, user feedback received mid-pass is semantically feedback to /do (the caller), not to /verify. The same default-to-amend rule applies. /verify itself never handles user feedback inline; the message is interpreted in /do's context and routed through Self-Amendment. (When /verify is invoked directly by the user — e.g., `/verify --deferred` — there is no /do caller; mid-pass user messages are handled per the user's own session reflex, not via /do's amendment route.)

**Amendment flow** — Amend the manifest autonomously via Self-Amendment escalation and `/define --amend <manifest-path> --from-do`, then resume with the updated manifest and existing log. Log the trigger before amending. No human wait — the entire cycle is autonomous.

**Amendment loop guard** (R-7) — If Self-Amendment escalations repeat without new external input (user messages or PR comments) between them, the amendments are likely oscillating — escalate as "Proposed Amendment" for human decision instead. The same guard applies to post-/done re-entry: when feedback after completion triggers re-entry to /do via amendment, the consecutive-amendments-without-external-input counter still applies. Purpose: prevent runaway loops and unnecessary token burn.

**No-manifest case.** When /do is invoked without a manifest (rare — typically /do follows /define), default-to-amend doesn't apply: there is nothing to amend. Behavior falls back to inline handling. This is fail-open by design.
