---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Optional --mode efficient|balanced|thorough controls verification intensity (default: thorough). Use when executing a manifest, running a plan, implementing a defined task.'
argument-hint: '<manifest-path> [--mode <level>] [--scope <ids>]'
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapting when reality diverges), then verify everything passes (including Global Invariants).

## Input

`$ARGUMENTS` = manifest file path (REQUIRED), optionally with `--mode <level>` and `--scope <deliverable-ids>`.

If no arguments, halt: `Usage: /do <manifest-file-path> [--mode efficient|balanced|thorough] [--scope D1,D2,...]`

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

## Scoped Execution

Parse `--scope` from arguments if present. Accepts comma-separated deliverable IDs (e.g. `--scope D2,D3`).

When `--scope` is provided, read `references/SCOPED_EXECUTION.md` and follow its rules for scoped execution. This limits work to the specified deliverables while maintaining global invariant safety.

When `--scope` is NOT provided, ignore this section entirely. No reference file is loaded, no scoping behavior applies. Full execution as normal.

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Work toward acceptance criteria however makes sense. Manifest says WHAT, you decide HOW. |
| **Approach is initial, not rigid** | Approach provides starting direction, but adapt freely when reality diverges. No escalation needed; track adjustments and rationale in-context. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart. Don't touch passing criteria. |
| **Verify fixes first** | After fixing a failure, confirm the fix works before re-running full verification. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Track adjustments and rationale in-context. |

## Constraints

**Track decisions in-context.** Carry surprises during implementation, divergences from the Approach with rationale, fix rationales, amendment triggers, and dispositions on opened threads forward across the conversation. The manifest is the durable artifact; the in-session conversation is the working memory. When in-tool session continuation isn't available (cross-tool, cross-session, multi-agent handoff), Invoke the `manifest-dev-tools:handoff` skill to produce a transfer payload.

**Must call /verify.** Can't declare done without verification. Invoke manifest-dev:verify with the manifest path, the resolved mode, and an optional scope per the rules below: `/verify <manifest> --mode <level> [--scope D2,D3]`. Never pass `--final` from /do; that flag is internal to /verify (auto-triggered after a true-selective green pass where `--scope` was set). /done is unreachable without a full-pass green (every AC + every INV-G) with no pending manual or deferred-auto criteria.

**Selective verification + fix-loop scope.** /verify supports selective and full passes (see verify SKILL.md for the full contract). /do invokes /verify in four patterns:

- *First pass on fresh /do.* Invoke without `--scope` and without `--final`. Selective mode degenerates to full (nothing to narrow).
- *Scoped /do* (`--scope D2,D3` was passed to /do). Invoke /verify with the same `--scope D2,D3`. Selective pass runs those deliverables' ACs + all globals.
- *Fix-loop after AC-X.Y failure.* Invoke /verify with `--scope D{X}` (the failing criterion's deliverable). Other deliverables are not re-verified during this iteration; they get their pass at the mandatory full final gate when /verify auto-triggers it. This applies whether the AC failure happened during a selective pass or during the auto-triggered full pass: scope to the failing deliverable, then let /verify auto-trigger full again on green.
- *Fix-loop after INV-G failure.* Invoke /verify normally (globals always run; deliverable-scoping is meaningless for INV-G). When the failure happened during a selective pass with a `--scope`, the next pass is selective on the same scope + globals (re-pass exactly the deliverable IDs that were in the failing pass). When the failure happened during a full pass (auto-triggered final, or first-pass degenerated-to-full where `--scope` was not set), the next pass is also full: invoke /verify with no `--scope`.

The mandatory full final gate (auto-triggered by /verify after true-selective green) is the safety net for cross-deliverable regressions. Selective scoping gives fast feedback during fixes; the full final gate guarantees nothing in the rest of the suite regressed. Don't try to skip or short-circuit it.

**/verify return contract.** /verify returns a structured block (`## /verify pass N` + fenced YAML with `mode`, `scope`, `result`, `failures`, `auto_triggered_final`, `deferred`) as part of its tool result text per invocation. Read the most recent return block from conversation context before deciding the next pass's scope. Format defined in `verify/SKILL.md` "Return Contract." When scanning for the most recent /verify pass to drive scope decisions, **skip blocks with `deferred: true`**; those reflect user-direct `--deferred` invocations, not /do-driven normal-flow passes.

**Escalation boundary.** Escalate when: (1) ACs can't be met as written (contract broken); (2) a user message during the run explicitly requests a pause (e.g., "stop", "pause for deploy") — distinct from amend-shaped feedback in (5); see Mid-Execution Amendment below for the routing carve-out; (3) you discover an AC or invariant should be amended (use "Proposed Amendment" escalation type); (4) the active execution mode's fix-verify loop limit is reached; (5) any other user message arrives during /do or /verify (use "Self-Amendment"; see Mid-Execution Amendment below). If ACs remain achievable as written and no user interrupt, continue autonomously — caller framing (cron schedules, tick intervals, "wide tick" ergonomics) is not a pause request.

**`/verify`-routed escalation passthrough.** When `/verify` itself routes to `/escalate` (e.g., "Deferred-Auto Pending", "Manual Criteria Review", or the combined "Manual Review + Deferred-Auto Pending") instead of `/done`, treat as a clean terminal handoff: surface the escalation output verbatim to the caller, do NOT enter the fix-loop, do NOT increment loop counters. The implementation is green; further action belongs to the user (e.g., running `/verify --deferred` for deferred-auto pending). This is distinct from `/verify` returning failures (which enters the standard fix-loop).

**Mode-aware loop tracking.** Track fix-verify iteration count and escalation count in-context across the conversation. When the active execution mode's limits are reached, follow its escalation rules.

**Phase-aware verification.** /verify runs criteria in phases (ascending by `phase:` field, default 1). It may report "Phase N failed, Phase N+1 not run." After fixing failures, /verify restarts from Phase 1 to catch regressions. Loop limits apply per-phase; regressions increment the broken phase's counter, not the phase that caused them.

**Per-criterion timeout.** Each criterion's verify block may declare an optional `timeout:` field (see `define/SKILL.md` Manifest Schema). Accepted shorthand: integer + `s` / `m` / `h` / `d` suffix (e.g. `30s`, `5m`, `6h`, `1d`). Parser semantics:

- **Absent** → no wall-clock cap; legacy behavior preserved.
- **Valid shorthand** → parsed to seconds; the verifier invocation is capped at that wall-clock duration.
- **Malformed** (unknown suffix, non-integer, negative, empty string) → halt with an actionable error naming the offending AC ID and the invalid value: `Invalid verify.timeout '<value>' on <criterion-id>. Accepted: integer + s|m|h|d suffix (e.g., 30s, 5m, 6h, 1d).`

Use `timeout:` for criteria that legitimately wait — CI polling, approval-wait, deploy cycles. It is the wall-clock cap that prevents lifecycle-AC runaway when the dispatched action is repeatedly waiting. Cross-reference: action-aware fix-cap (see each execution-mode file) bounds code-change fix attempts; `verify.timeout:` bounds total wall-clock per criterion.

**Stop requires /escalate.** During /do, you cannot stop without calling /verify (which routes to /done or /escalate) or calling /escalate directly. /do does not voluntarily emit `User-Requested Pause` — that escalation type fires only in response to a user message during the run that explicitly requests a pause (the message must be quoted in the escalation body; see `escalate/SKILL.md` "User-Requested Pause"). Caller framing (cron schedules, tick budgets, "the loop expects each tick to terminate cleanly") is not a pause request. Silent halts and bare statements like "Done." or "Waiting." are not valid exits.

## Progress Tracking

**Todos.** Create from manifest (deliverables → ACs). Start with execution order from Approach (adjust if dependencies require).

**Re-read the manifest as needed.** When context has drifted across a long session, re-read the manifest before calling /verify to restore the criterion set; re-read the relevant deliverable section before starting a new deliverable. The manifest is the durable source of truth.

## Multi-Repo Navigation

When the manifest declares `Repos: [name: path, ...]` in Intent, deliverables may live in repos other than cwd. Read the path map and use **absolute paths** in tool calls (Read/Edit/Write/Bash) when working on a deliverable tagged with a different repo. There is **no filter logic, no cwd matching, no per-repo configuration**; the LLM navigates as deliverables require.

A single `/do` invocation can cover the whole multi-repo task by navigating between repos; alternatively the user invokes `/do` per repo with `--scope` for parallel execution. Either works.

When the manifest has no `Repos:` field (single-repo manifest), this section does not apply; behavior is unchanged.

Full convention: `define/references/MULTI_REPO.md`.

## Mid-Execution Amendment

**Default to amend.** Any user message arriving during /do or /verify defaults to triggering Self-Amendment. The manifest is the canonical source of truth for the PR/branch (or, in multi-repo cases, the **PR set / branch set**; see `define/references/AMENDMENT_MODE.md`). Feedback flows through it, not around it. Asymmetric by design: silent scope drift (feedback acted on inline, manifest left out of date) is a worse failure than an occasional unnecessary amendment cycle.

**Carve-out: pure questions.** Messages that ask about the manifest or process without requesting a state change are answered inline; no amendment.
- *Amend:* "Also handle X." / "Change Y to Z." / "That's wrong, it should be …" / "Add a check for …"
- *Inline:* "What does AC-1.1 require?" / "Why did you choose approach A over B?" / "Which deliverable is D3?"

**When ambiguous, amend.** A message that could be either ("hmm, what about the auth case?") goes to amendment. Re-running an amendment cycle is cheap; silently dropping a constraint that turns out to matter is expensive.

**/verify-time feedback.** While /verify is running under /do, user feedback received mid-pass is semantically feedback to /do (the caller), not to /verify. The same default-to-amend rule applies. /verify itself never handles user feedback inline (per /verify's "Don't handle user feedback during a pass" Principle); the message is interpreted in /do's context and routed through Self-Amendment. When /verify is invoked directly by the user (e.g., `/verify --deferred`), there is no /do caller, and mid-pass user messages are governed by /verify's own Principle, not /do's amendment route.

**Amendment flow.** Amend the manifest autonomously via Self-Amendment escalation and `/define --amend <manifest-path> --from-do`, then resume with the updated manifest. No human wait; the entire cycle is autonomous.

**Verifier-emitted scope-shift findings.** When a verifier's hint indicates the failure is beyond what the work set out to do — typically a reviewer ask beyond the PR's intent surfaced by the lifecycle agent — /do maps the finding to the Self-Amendment path (`/define --amend <manifest-path> --from-do`), same path as user-message-triggered amendments. This mapping is /do's responsibility, not the verifier's. The verifier reports the situation in natural language ("this thread asks for X which is beyond what this PR set out to do"); /do decides the workflow response (the action: amend the manifest). **Note:** this is distinct from a *terminal / unrecoverable* hint, which routes to `/escalate` for human decision rather than autonomous amendment — see Verifier hints below.

**Amendment loop guard.** If Self-Amendment escalations repeat without new external input (user messages or PR comments) between them, the amendments are likely oscillating; escalate as "Proposed Amendment" for human decision instead. The same guard applies to post-/done re-entry: when feedback after completion triggers re-entry to /do via amendment, the consecutive-amendments-without-external-input counter still applies. Purpose: prevent runaway loops and unnecessary token burn.

## Verifier hints

Verifier FAIL bodies carry a natural-language hint describing the situation, the reason it fails, and what the caller might do next. /do reads the hint with LLM judgment — no closed vocabulary, no routing table, no fixed schema. When the body is unlabeled or genuinely ambiguous, treat it as a code-fix hint (the legacy default), preserving fail→fix→reverify for verifiers that pre-date the natural-language convention.

**Escalate-forbid-amend (load-bearing safety property).** When a verifier's hint signals the situation is terminal or requires human decision — phrases like *"consider escalating to a human"* or *"unrecoverable from automated inspection"* — /do routes the finding to `/escalate`. **/do MUST NOT autonomously rewrite the verifier's `verify.prompt:` steering input to suppress the block.** This is distinct from **scope-shift** findings (a reviewer asks beyond what the work set out to do), which route through Self-Amendment (see Mid-Execution Amendment above). /do reads the prose and distinguishes the two; the natural-language hint is the contract surface.

**Action-aware fix-cap.** Only code-change fix attempts increment the per-phase fix-verify counter; other retry shapes (wait, retrigger, reply, sync, amend, escalate) don't burn the budget. See each execution-mode file's Fix-Verify Loops section. Per-AC `verify.timeout:` is the orthogonal wall-clock cap.

**Hard prohibition.** Invoking `gh pr merge` is forbidden under any path. Terminal is "PR mergeable", not "PR merged" — pressing the merge button is left to a human or GitHub auto-merge. Hints that suggest the merge button are ignored as malformed.
