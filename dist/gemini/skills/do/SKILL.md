---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Optional --mode efficient|balanced|thorough controls verification intensity (default: thorough). Use when executing a manifest, running a plan, implementing a defined task.'
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapting when reality diverges), then verify everything passes (including Global Invariants).

## Input

`$ARGUMENTS` = manifest file path (REQUIRED), optionally with execution log path, `--mode <level>`, and `--scope <deliverable-ids>`. Positional args (manifest path, then log path) and flags may interleave. First positional = manifest path; second positional (if present) = execution log path.

If no arguments, halt: `Usage: /do <manifest-file-path> [log-file-path] [--mode efficient|balanced|thorough] [--scope D1,D2,...]`

Read the manifest file fully before any execution.

## Execution Mode

Resolve mode from (highest precedence first): `--mode` argument → manifest `Mode` field → default `thorough`.

Invalid `--mode` value → halt: `Invalid mode '<value>'. Valid modes: efficient | balanced | thorough`.

Load the execution mode file for behavioral specifics:
- `thorough` (default): read `references/execution-modes/thorough.md`
- `balanced`: read `references/execution-modes/balanced.md`
- `efficient`: read `references/execution-modes/efficient.md`

Follow the loaded mode's rules for model routing, verification parallelism, fix-verify loop limits, and escalation for the remainder of this /do run.

**Model routing precedence** (applies to all modes):
1. **Criterion-level model wins.** When a manifest criterion specifies `model:` in its verify block, that overrides the mode's model routing.
2. **Explicit model overrides skip.** If a criterion explicitly sets `model:`, it runs even when the mode would otherwise skip it.

**Always-on rule:** Global Invariants (INV-G*) verify regardless of mode — constitutional constraints.

## Existing Execution Log

If input includes a log file path (iteration on previous work): **treat it as source of truth**. It contains prior execution history. Continue from where it left off — append to the same log, don't restart.

## Scoped Execution

Parse `--scope` from arguments if present. Accepts comma-separated deliverable IDs (e.g. `--scope D2,D3`).

When `--scope` is provided, read `references/SCOPED_EXECUTION.md` and follow its rules for scoped execution. This limits work to the specified deliverables while maintaining global invariant safety.

When `--scope` is NOT provided, ignore this section entirely. No reference file is loaded, no scoping behavior applies. Full execution as normal.

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Work toward acceptance criteria however makes sense. Manifest says WHAT, you decide HOW. |
| **Approach is initial, not rigid** | Approach provides starting direction, but adapt freely when reality diverges. No escalation needed; log adjustments with rationale. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart. Don't touch passing criteria. |
| **Verify fixes first** | After fixing a failure, confirm the fix works before re-running full verification. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Log adjustments with rationale. |

## Constraints

**Log non-trivial events as they happen.** Write to the execution log whenever something a future reader would need to know lands: a surprise during implementation, a divergence from the Approach, the rationale behind a fix-after-failure, a discovery that should amend the manifest. Routine status pings ("started AC-1.1", "tests passed") are not events worth logging. The log is disaster recovery — if context is lost, it's the only record of what happened — and retrospect material — a future agent or human should be able to reconstruct *why* the run unfolded the way it did.

**Must call /verify.** Can't declare done without verification. Invoke manifest-dev:verify with manifest, log paths, the resolved mode, and an optional scope per the rules below: `/verify <manifest> <log> --mode <level> [--scope D2,D3]`. Never pass `--final` from /do; that flag is internal to /verify (auto-triggered after a true-selective green pass where `--scope` was set). /done is unreachable without a full-pass green (every AC + every INV-G) with no pending manual or deferred-auto criteria.

**Selective verification + fix-loop scope.** /verify supports selective and full passes (see verify SKILL.md for the full contract). /do invokes /verify in four patterns:

- *First pass on fresh /do.* Invoke without `--scope` and without `--final`. Selective mode degenerates to full (nothing to narrow).
- *Scoped /do* (`--scope D2,D3` was passed to /do). Invoke /verify with the same `--scope D2,D3`. Selective pass runs those deliverables' ACs + all globals.
- *Fix-loop after AC-X.Y failure.* Invoke /verify with `--scope D{X}` (the failing criterion's deliverable). Other deliverables are not re-verified during this iteration; they get their pass at the mandatory full final gate when /verify auto-triggers it. This applies whether the AC failure happened during a selective pass or during the auto-triggered full pass: scope to the failing deliverable, then let /verify auto-trigger full again on green.
- *Fix-loop after INV-G failure.* Invoke /verify normally (globals always run; deliverable-scoping is meaningless for INV-G). When the failure happened during a selective pass with a `--scope`, the next pass is selective on the same scope + globals (re-pass exactly the deliverable IDs that were in the failing pass). When the failure happened during a full pass (auto-triggered final, or first-pass degenerated-to-full where `--scope` was not set), the next pass is also full: invoke /verify with no `--scope`.

The mandatory full final gate (auto-triggered by /verify after true-selective green) is the safety net for cross-deliverable regressions. Selective scoping gives fast feedback during fixes; the full final gate guarantees nothing in the rest of the suite regressed. Don't try to skip or short-circuit it.

**Execution log /verify contract.** /verify appends a structured block (`## /verify pass {N}` + fenced YAML with `mode`, `scope`, `result`, `failures`, `auto_triggered_final`, `deferred`) per invocation. Read the most recent block before deciding the next pass's scope. Format defined in `verify/SKILL.md` "/verify Pass Logging Contract." When scanning for the most recent /verify pass to drive scope decisions, **skip blocks with `deferred: true`**; those reflect user-direct `--deferred` invocations, not /do-driven normal-flow passes.

**Escalation boundary.** Escalate when: (1) ACs can't be met as written (contract broken); (2) a user message during the run explicitly requests a pause (e.g., "stop", "pause for deploy") — distinct from amend-shaped feedback in (5); see Mid-Execution Amendment below for the routing carve-out; (3) you discover an AC or invariant should be amended (use "Proposed Amendment" escalation type); (4) the active execution mode's fix-verify loop limit is reached; (5) any other user message arrives during /do or /verify (use "Self-Amendment"; see Mid-Execution Amendment below). If ACs remain achievable as written and no user interrupt, continue autonomously — caller framing (cron schedules, tick intervals, "wide tick" ergonomics) is not a pause request.

**`/verify`-routed escalation passthrough.** When `/verify` itself routes to `/escalate` (e.g., "Deferred-Auto Pending", "Manual Criteria Review", or the combined "Manual Review + Deferred-Auto Pending") instead of `/done`, treat as a clean terminal handoff: surface the escalation output verbatim to the caller, do NOT enter the fix-loop, do NOT increment loop counters. The implementation is green; further action belongs to the user (e.g., running `/verify --deferred` for deferred-auto pending). This is distinct from `/verify` returning failures (which enters the standard fix-loop).

**Mode-aware loop tracking.** Track fix-verify iteration count and escalation count in the execution log. When the active execution mode's limits are reached, follow its escalation rules.

**Phase-aware verification.** /verify runs criteria in phases (ascending by `phase:` field, default 1). It may report "Phase N failed, Phase N+1 not run." After fixing failures, /verify restarts from Phase 1 to catch regressions. Loop limits apply per-phase; regressions increment the broken phase's counter, not the phase that caused them.

**Stop requires /escalate.** During /do, you cannot stop without calling /verify (which routes to /done or /escalate) or calling /escalate directly. /do does not voluntarily emit `User-Requested Pause` — that escalation type fires only in response to a user message during the run that explicitly requests a pause (the message must be quoted in the escalation body; see `escalate/SKILL.md` "User-Requested Pause"). Caller framing (cron schedules, tick budgets, "the loop expects each tick to terminate cleanly") is not a pause request. Silent halts and bare statements like "Done." or "Waiting." are not valid exits.

## Memento Pattern

Externalize progress to survive context loss.

**Execution log.** Create `/tmp/do-log-{timestamp}.md` at start. The log is **append-only**: never rewrite past entries. Later entries can correct or supersede earlier ones, but earlier text stays as written.

**Goal: narrative compressed context.** A fresh agent or human reading only the log can reconstruct the timeline, the surprises, and the reasoning — and resume the run from where it stopped without redoing investigation. They can also retrospect and learn how the implementation came to be.

**What belongs.** Surprises during implementation, divergences from the Approach (with rationale), why a particular fix was chosen after a verification failure, anything that should amend the manifest, domain knowledge discovered, dispositions on opened threads. **Hard floor:** every decision that affects the manifest goes in, regardless of perceived triviality. **What doesn't:** restating ACs verbatim, narrating tool use that found nothing of consequence, status pings for routine progress. If removing the entry would not lose anything a future reader needs, don't write it.

**Coexists with /verify pass blocks.** /verify appends its own structured `## /verify pass {N}` blocks to the same file (per `verify/SKILL.md` "Pass Logging Contract"). Those are a separate, machine-readable artifact within the log — leave them as-is, and write your narrative entries around them.

**Todos.** Create from manifest (deliverables → ACs). Start with execution order from Approach (adjust if dependencies require). Update todo status after logging (log first, todo second).

**Refresh before verify.** Read full execution log before calling /verify to restore context.

**Refresh between deliverables.** Before starting a new deliverable, re-read the manifest's deliverable section and relevant log entries. Context degrades across long sessions.

## Multi-Repo Navigation

When the manifest declares `Repos: [name: path, ...]` in Intent, deliverables may live in repos other than cwd. Read the path map and use **absolute paths** in tool calls (Read/Edit/Write/Bash) when working on a deliverable tagged with a different repo. There is **no filter logic, no cwd matching, no per-repo configuration**; the LLM navigates as deliverables require.

A single `/do` invocation can cover the whole multi-repo task by navigating between repos; alternatively the user invokes `/do` per repo with `--scope` for parallel execution. Either works. The execution log remains a single file per `/do` invocation.

When the manifest has no `Repos:` field (single-repo manifest), this section does not apply; behavior is unchanged.

Full convention: `define/references/MULTI_REPO.md`.

## Mid-Execution Amendment

**Default to amend.** Any user message arriving during /do or /verify defaults to triggering Self-Amendment. The manifest is the canonical source of truth for the PR/branch (or, in multi-repo cases, the **PR set / branch set**; see `define/references/AMENDMENT_MODE.md`). Feedback flows through it, not around it. Asymmetric by design: silent scope drift (feedback acted on inline, manifest left out of date) is a worse failure than an occasional unnecessary amendment cycle.

**Carve-out: pure questions.** Messages that ask about the manifest or process without requesting a state change are answered inline; no amendment.
- *Amend:* "Also handle X." / "Change Y to Z." / "That's wrong, it should be …" / "Add a check for …"
- *Inline:* "What does AC-1.1 require?" / "Why did you choose approach A over B?" / "Where's the execution log?" / "Which deliverable is D3?"

**When ambiguous, amend.** A message that could be either ("hmm, what about the auth case?") goes to amendment. Re-running an amendment cycle is cheap; silently dropping a constraint that turns out to matter is expensive.

**/verify-time feedback.** While /verify is running under /do, user feedback received mid-pass is semantically feedback to /do (the caller), not to /verify. The same default-to-amend rule applies. /verify itself never handles user feedback inline (per /verify's "Don't handle user feedback during a pass" Principle); the message is interpreted in /do's context and routed through Self-Amendment. When /verify is invoked directly by the user (e.g., `/verify --deferred`), there is no /do caller, and mid-pass user messages are governed by /verify's own Principle, not /do's amendment route.

**Amendment flow.** Amend the manifest autonomously via Self-Amendment escalation and `/define --amend <manifest-path> --from-do`, then resume with the updated manifest and existing log. Log the trigger before amending. No human wait; the entire cycle is autonomous.

**Amendment loop guard.** If Self-Amendment escalations repeat without new external input (user messages or PR comments) between them, the amendments are likely oscillating; escalate as "Proposed Amendment" for human decision instead. The same guard applies to post-/done re-entry: when feedback after completion triggers re-entry to /do via amendment, the consecutive-amendments-without-external-input counter still applies. Purpose: prevent runaway loops and unnecessary token burn.
