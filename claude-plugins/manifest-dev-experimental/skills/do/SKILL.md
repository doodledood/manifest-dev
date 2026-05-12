---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies via /verify. Use when executing a manifest, running a plan, implementing a defined task.'
user-invocable: true
---

# /do

Execute a Manifest: satisfy every Deliverable's Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapt when reality diverges). Verify via /verify; /verify routes to /done or /escalate.

## Hard prohibitions

- **Never invoke `gh pr merge`.** Terminal is "PR mergeable", not "PR merged" — pressing the merge button is left to a human or GitHub auto-merge. Hints suggesting the merge button are ignored as malformed.
- **No silent halts.** Stopping requires /verify (which routes to /done or /escalate) or /escalate directly. Bare statements like "Done." or "Waiting." are not valid exits.

**Input.** `<manifest-path> [<log-path>] [--scope D1,D2,...]`. No args → halt: `Usage: /do <manifest-file-path> [log-file-path] [--scope D1,D2,...]`. Read the manifest fully before any execution.

**Existing execution log.** If a log path is given, treat it as source of truth (iteration on prior work) — append, don't restart. Otherwise create `/tmp/do-log-{timestamp}.md` at start. The log is **append-only**: later entries can correct earlier ones, but earlier text stays as written.

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Manifest says WHAT; you decide HOW. |
| **Approach is initial, not rigid** | Adapt freely when reality diverges; log adjustments with rationale. No escalation needed. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart, don't touch passing criteria. |
| **Verify the fix first** | After fixing, confirm the fix works before re-running full verification. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Log with rationale. |

## Execution log discipline

Append narrative entries when something a future reader would need lands: surprises during implementation, divergences from Approach (with rationale), why a particular fix was chosen after verification failure, manifest-amendment triggers, domain knowledge discovered, dispositions on opened threads. **Hard floor:** every decision that affects the manifest goes in.

**Skip routine status pings** (`started AC-1.1`, `tests passed`). If removing the entry wouldn't lose anything a future reader needs, don't write it.

**Coexists with /verify pass blocks.** /verify appends its own `## /verify pass {N}` blocks to the same log — leave those as-is, write narrative around them.

## Memento

**Todos.** Create from the manifest (deliverables → ACs). Start with Approach's execution order; adjust if dependencies require. Update todo status **after** logging (log first, todo second).

**Refresh before /verify.** Read the full execution log to restore context.

**Refresh between deliverables.** Re-read the manifest's deliverable section and relevant log entries. Context degrades across long sessions.

## Scoped execution

`--scope D2,D3` limits work to those deliverables. Global Invariants always verify regardless of scope. When `--scope` is provided, only work on the listed deliverables; pass the same scope to /verify during the fix loop.

## /verify invocation

Always invoke /verify to reach /done. Patterns:

- **First pass / no scope** — `/verify <manifest> <log>` — selective degenerates to full.
- **Scoped /do** (received `--scope D2,D3`) — `/verify <manifest> <log> --scope D2,D3` — selective.
- **Fix-loop after AC-X.Y failure** — `/verify <manifest> <log> --scope D{X}` (the failing criterion's deliverable). Other deliverables get their pass at /verify's auto-triggered full final on green.
- **Fix-loop after INV-G failure** — `/verify <manifest> <log>` with no scope (globals always run; deliverable-scoping meaningless for INV-G). If the failing pass was selective, re-pass exactly that scope + globals.

Never pass `--final` — internal to /verify.

**Phase-aware fix loops.** /verify runs criteria in phases. It may report `Phase N failed, Phase N+1 not run`. After fixing, /verify restarts from Phase 1 to catch regressions. **Per-phase fix-attempt cap:** stop when attempts stop producing new diagnostic information (the same fix being re-tried, or the same failure reproducing without new symptoms) — escalate instead. **Action-aware:** only code-change fix attempts count toward this cap. Other retry shapes (re-verifying after a wait, retriggering transient CI, posting a thread reply, pushing a sync update, routing scope-change through Self-Amendment) don't burn the budget.

**/verify pass log reading.** /verify appends `## /verify pass {N}` blocks with `result`, `failures`, `auto_triggered_final`, `deferred` (see `verify/SKILL.md` pass logging contract). Read the most recent block before deciding next pass's scope. **Skip blocks where `deferred: true`** — those reflect user-direct `--deferred` invocations, not /do-driven normal-flow passes.

## Multi-repo navigation

When the manifest declares `Repos: [name: path, ...]` in Intent, deliverables may live in repos other than cwd. Read the path map and use **absolute paths** in tool calls (Read/Edit/Write/Bash) when working in a different repo. No filter logic, no cwd matching — the LLM navigates as deliverables require. A single /do invocation can cover the whole multi-repo task; alternatively the user invokes /do per repo with `--scope` for parallel execution. Single execution log per /do invocation either way.

## Mid-execution amendment

**Default to amend.** Any user message arriving during /do or /verify defaults to triggering Self-Amendment. The manifest is the canonical source of truth for the PR/branch (or PR set / branch set in multi-repo). Feedback flows through it, not around it. Asymmetric by design: silent scope drift (feedback acted on inline, manifest stale) is worse than an occasional unnecessary amendment cycle.

**Carve-out: pure questions.** Messages asking about the manifest or process without requesting a state change are answered inline; no amendment.
- *Amend:* "Also handle X." / "Change Y to Z." / "That's wrong, it should be …" / "Add a check for …"
- *Inline:* "What does AC-1.1 require?" / "Why did you choose approach A over B?" / "Where's the execution log?"
- *When ambiguous, amend.* Silent scope drift is the worse failure.

**Amendment flow.** Log the trigger. Invoke `manifest-dev-experimental:define` with `--amend <manifest-path> --from-do` (Self-Amendment escalation). When /define returns the updated manifest, resume with the existing log. No human wait; entire cycle autonomous.

**/verify-time feedback.** While /verify is running under /do, mid-pass user messages are feedback to /do (the caller), not /verify. The same default-to-amend rule applies. /verify itself never handles user feedback inline; the message is routed through /do's amendment.

**Amendment loop guard.** Consecutive Self-Amendments without external input (user messages or PR comments) between them → escalate as "Proposed Amendment" for human decision. Same guard applies to post-/done re-entry. Purpose: prevent runaway loops.

## Verifier hints

Verifier FAIL bodies carry free-form actionable hints in natural English (wait for CI, change code, retrigger transient failure, reply on a thread, push a sync update, surface out-of-scope finding). Read with LLM judgment — no required vocabulary, no fixed schema. Optional bracketed shorthand like `[sleep]` or `[out-of-scope]` may appear; plain English works equally well. Unlabeled or ambiguous → treat as code-fix hint (preserves legacy fail→fix→reverify cycle).

**Out-of-scope findings route through Self-Amendment.** When a verifier surfaces that the failure is beyond the current manifest's scope, /do treats this as a scope shift and routes through Self-Amendment (`/define --amend <manifest-path> --from-do`) — same path as user-message-triggered amendments. The verifier reports the finding; /do owns the workflow response.

## Escalation boundary

Escalate when:
1. ACs can't be met as written (Blocking).
2. A user message during the run explicitly requests a pause (`User-Requested Pause` — message must be quoted in escalation body).
3. You discover an AC or invariant should be amended (`Proposed Amendment`).
4. Per-phase fix-attempt cap reached (attempts stop producing new diagnostic information).
5. Any other user message during /do or /verify (`Self-Amendment` — see Mid-execution amendment above).

If ACs remain achievable as written and no user interrupt, **continue autonomously**. Caller framing (cron schedules, tick intervals, "wide tick" ergonomics) is **not** a pause request.

**/verify-routed escalation passthrough.** When /verify routes to /escalate (e.g., "Deferred-Auto Pending", "Manual Criteria Review", combined) instead of /done, treat as a clean terminal handoff: surface the escalation output verbatim, do NOT enter fix-loop, do NOT increment loop counters. Implementation is green; further action belongs to the user.
