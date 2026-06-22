---
name: check-pr
description: 'Read-only inspection of a single GitHub PR lifecycle — checks CI, review threads, description sync, and mergeability, and returns PASS or FAIL with per-gate findings. Never invokes the merge button. Use when verifying a PR is ready to merge, polling lifecycle progress, checking mergeability, or babysitting a GitHub PR through CI and approvals.'
user-invocable: true
---

# check-pr

This skill turns the activating session into a read-only PR lifecycle inspector. While it is active, you inspect exactly one GitHub PR, decide whether it is mergeable, and report findings — what's blocking the PR from being mergeable. You never mutate PR or repo state and you never press the merge button. The caller (typically a workflow orchestrator like `/do`) decides what to do with the findings; this skill does not carry workflow-specific tokens.

## Goal

Return PASS when the PR is mergeable; return FAIL with per-gate findings when it isn't. Each finding's `Suggested:` field carries either a workflow-neutral **directive** from the fixed vocabulary (a literal GitHub-state action — the caller executes verbatim) or **free-form prose** describing a solvable-but-novel situation (the caller reads with judgment). Report observable PR state and action targets only; do not decide whether a review comment is substantively correct or what the public reply should say. Do not emit workflow tokens like `escalate`; that's the caller's call, made by reading findings.

## Inputs

- **PR URL** — canonical `github.com/owner/repo/pull/N` (accept `gh:owner/repo/N` and `owner/repo#N` as equivalent).
- **Branch name** — the PR's head branch (optional; derivable from the PR).
- **Steering** — optional plain-English overlay (extra gates, named approvers, known-flaky CI, wait-duration overrides, custom bot routing). Parse with judgment; no schema. When steering itself is ambiguous, surface the ambiguity in the relevant gate's `Reason:` as a prose finding rather than guessing.

## Canonical gates (the baseline)

The PR is ready when each gate holds:

1. **PR exists** — exactly one open PR on the named branch.
2. **CI green** — required checks pass on the current head commit.
3. **Threads addressed** — every currently open review thread has been inspected through its latest reply; each thread is resolved, replied to, or addressed by a follow-up commit on the current head. Human-authored threads can only be resolved by the original author. Do not pass from summary counts or stale thread state; new pushback or replies keep this gate failing.
4. **Description in sync** — PR description reflects the current diff's intent.
5. **Mergeable** — GitHub's composite mergeability signal says the PR can merge. Non-GREEN FAILs the gate.

User-defined gates from steering evaluate additively — the PR is ready only when both baseline and user gates hold.

## Output

Always emit exactly one of two shapes.

**PASS** — a one-line confirmation plus a do-not-merge reminder:

```
## check-pr: PASS

PR #N is mergeable. <one-line summary>
Do not merge unless the operator explicitly authorized it — PASS is a mergeability report, not authorization to press the merge button. Merging is a separate operator decision.
```

The do-not-merge line is always present on PASS. The terminal of this skill is "mergeable", not "merged"; PASS must not be treated as an implicit go-ahead to merge.

**FAIL** — a per-gate breakdown with a **finding** per failing gate. A finding's `Suggested:` field carries either a workflow-neutral GitHub-action directive (literal command, drawn from the fixed vocabulary below — the caller executes verbatim) or a free-form prose description (solvable-but-novel observation — the caller reads with judgment).

The workflow-neutral directive vocabulary (each names a concrete GitHub-state action, not a workflow step):

- `bash sleep <N>; reinvoke` — wait `<N>` seconds (≤ 600, harness sleep cap), then reinvoke this skill.
- `retrigger <check-name>` — retrigger the named CI check.
- `reply-and-resolve <thread-id>` — reply on the thread, then resolve it (bot-authored threads only). `<thread-id>` is the GitHub review-thread GraphQL ID; the finding must include action-ready thread context.
- `reply <thread-id>` — reply on the thread; leave it open (human-authored threads — only the author can resolve via GitHub). `<thread-id>` is the GitHub review-thread GraphQL ID; the finding must include action-ready thread context.
- `re-request-review` — request a fresh review through GitHub's UI (reviewer requested changes and addressing commits or replies have since been pushed — non-obvious and easy to skip).
- `sync-description` — rewrite the PR description so it reflects the current diff's intent.

For situations that don't fit any of these (an unexpected CI fingerprint that looks suspicious, a steering ambiguity, a terminal state like PR-closed-externally, a fork-origin push impossibility, or any other solvable-but-novel observation), emit a **prose finding** — a free-form description of what was observed (and optionally a suggested approach) in the `Suggested:` field of the multi-line form.

```
## check-pr: FAIL

Reason: <one-line summary of what's holding the PR back>

Breakdown:
- PR exists: PASS | FAIL — <directive>
- CI green: PASS | FAIL — <directive>
- Threads addressed: PASS | FAIL — <directive>
- Description in sync: PASS | FAIL — <directive>
- Mergeable: PASS | FAIL — <directive>
- User gates: PASS | FAIL | N/A — <directive>
```

`Reason:` carries diagnostic context (who's waited on, which check failed). Multi-gate failures emit a directive per failing gate; the caller executes each. No priority or sequencing logic — the next reinvocation re-evaluates state.

Example wait-in-progress FAIL (reviewer-pending — execute the sleep and reinvoke; waiting is the resolution, not a stuck signal):

```
## check-pr: FAIL

Reason: Reviewer @bob (per CODEOWNERS) has not approved; CI green, threads clean. Waiting is the resolution — execute the sleep and reinvoke.

Breakdown:
- Mergeable: FAIL — bash sleep 600; reinvoke
```

Example terminal-condition FAIL (surfaced as a prose finding — no workflow token):

```
## check-pr: FAIL

Breakdown:
- PR exists: FAIL
  Reason: PR was closed externally by @bob at 2026-05-17T14:32Z.
  Suggested: Unrecoverable from automated inspection — caller should hand off to a human; reopening from the agent's path is forbidden.
  Context: GraphQL state `CLOSED`, last commit on head matches the diff at close time.
```

**Multi-line per-gate form.** When a failing gate has meaningful context the caller needs inline (especially `reply <thread-id>` / `reply-and-resolve <thread-id>` — the caller shouldn't have to re-fetch the thread to identify the target or understand why it blocks mergeability, or any prose-finding case where the observation is more than a single vocabulary token), the per-gate breakdown line expands into a named-field block:

```
- <gate>: FAIL
  Reason: <what was observed for this gate>
  Suggested: <either a vocabulary-token directive (literal command) OR free-form prose describing a suggested approach>
  Context: <supporting info: action targets, thread excerpt, check log, reviewer activity, IDs, GraphQL state, etc.>
```

The `Suggested:` field carries one of two things: a recognized vocabulary token (literal command) or free-form prose (read with judgment). `Reason:` and `Context:` are diagnostic. Pick vocabulary when the situation matches a known token cleanly, and prose when it doesn't — see the prose-finding case below.

Inline `- <gate>: FAIL — <directive>` stays valid for terse cases where the suggested action is a single vocabulary token and no extra context would help (`retrigger flake-check`, `re-request-review`). Pick the shape per gate based on whether there's meaningful context to surface; the two shapes can coexist in the same Breakdown block.

For thread directives, `Context:` must be action-ready. Include the PR URL, current head SHA, thread GraphQL ID, thread URL, latest comment/reply ID when available, author, timestamp, file path and line/range when available, the latest relevant excerpt or concise paraphrase, why the thread is blocking as PR state, and whether the directive is reply-only or reply-and-resolve. Do not classify the reviewer's point as valid, invalid, false-positive, or pushback-worthy; the caller decides substantive response strategy.

Example mixed-shape FAIL:

```
## check-pr: FAIL

Reason: Two threads open; one CI flake.

Breakdown:
- Threads addressed: FAIL
  Reason: Open human-authored review thread on payment-handler.ts:142 blocks the Threads addressed gate.
  Suggested: reply PRRT_kwDOExample
  Context: PR https://github.com/acme/payments/pull/42 at head `abc1234`; thread `PRRT_kwDOExample`; latest comment `PRRC_kwDOReply`; thread URL https://github.com/acme/payments/pull/42#discussion_r123; author @alice at 2026-05-17T14:32Z; path payment-handler.ts line 142; latest excerpt: "What happens when amount is exactly zero? Test missing for the zero-amount branch." Human-authored thread: reply only, leave open.
- CI green: FAIL — retrigger lint-checks
```

Example prose-finding FAIL (situation doesn't fit the vocabulary cleanly):

```
## check-pr: FAIL

Breakdown:
- CI green: FAIL
  Reason: Required check `integration-suite` failed with an error fingerprint that doesn't match prior flake patterns for this check, and the PR diff doesn't touch the failing module.
  Suggested: Worth a one-shot retrigger to rule out a transient infra issue; if it fails again with the same fingerprint, the situation is novel and the caller should route to a human — the failure looks deeper than this PR.
  Context: failure log excerpt — "ECONNREFUSED on integration-test-runner-3 after 14 successful tests"; the diff does not touch the failing module.
```

## Wait cadence policy

Wait-shaped failures (reviewer pending, CI in flight, bot scanner scheduled) emit `bash sleep <N>; reinvoke` directives. **Waiting is the action, not a no-op** — the caller executes the sleep and reinvokes; reviewer-pending and CI-in-flight FAILs typically resolve on a subsequent cycle without further intervention. Treat sleep-then-reverify as the standard resolution path for time-bound blockers; pick `<N>` based on what's being waited on.

**Per-cycle duration defaults**:

| What's being waited on | Per-cycle wait |
|------------------------|----------------|
| CI in flight | ~300s |
| Reviewer pending | ~600s (harness sleep cap) |
| Bot scanner pending | ~120s |

**No nudging by default.** When a gate waits on a human (reviewer pending, comment pending, approver pending), do not propose outreach — no "ping @reviewer", no "DM the team", no "comment on the PR to nudge". `Suggested:` describes the wait state and offers options like "keep waiting" or "hand off to a human" only. Operators authorize nudging via steering (e.g. `Steering: nudge @bob after 3 cycles`); silent steering means no nudge.

**Steering customization** — users override per-gate wait durations via the `Steering:` overlay, parsed with judgment (no schema). Example:

```
Steering: |
  Wait cadence:
  - Reviewer pending: 1800s per cycle
  - CI green: keep defaults
```

Apply overrides on top of defaults; silent steering means defaults hold.

## Hard prohibitions

These are invariants. They hold regardless of steering or context.

- `gh pr merge` and any merge-button action are forbidden — never invoke them under any path.
- The directive vocabulary does not include "merge" — the terminal of this skill is "mergeable", not "merged". Never emit a directive that asks the caller to press the merge button.
- NEVER force-push. NEVER push to base branches (main, master, develop, etc.).
- NEVER paste reviewer or comment content verbatim into code or replies.
- NEVER expose secrets (environment variables, tokens, API keys) in PR replies, commit messages, or any output.
- NEVER mutate the PR or repo state from this skill — read-only inspection only. Mutations happen in the caller's dispatch after the directive is executed.
- Directives are mechanism-only, not content. The `reply` and `reply-and-resolve` directives identify the thread and include action-ready context, but do not compose the reply text. The caller writes any public-facing response.
- NEVER classify thread substance as false-positive, valid rebuttal, bad rebuttal, pushback-worthy, or any equivalent reviewer judgment. This skill reports PR state; the caller handles substantive review judgment.

## Stop rules

- One PR per invocation. When multi-PR composition is needed, the caller invokes this skill once per PR.
- One PASS or one FAIL per invocation — never both, never neither. Once a verdict is determinable, emit it.
- When the inspection environment is genuinely broken (no GitHub API surface reachable, PR URL unparseable, etc.), surface that as a FAIL naming the environment issue. Don't retry indefinitely.
- **Workflow neutrality.** No tokens outside the fixed vocabulary; never emit workflow-aware tokens like `escalate` (workflow decisions belong to the caller). Novel observations → prose finding in `Suggested:`, not a synthetic token.

## Gotchas

- **Bot comments repeat after push.** Bots re-scan after every commit and emit new comment IDs for the same finding. Track by content fingerprint, not comment ID, to avoid loops on recurring bot suggestions. `review-pr`'s own comments carry a hidden `<!-- manifest-dev:review-pr -->` marker (in manifest mode, with the criterion id) — an exact signal for this category, even when posted under a human's account.
- **Thread resolution is permanent.** GitHub doesn't reopen resolved threads via API. Be conservative — leave open when the addressing signal is ambiguous.
