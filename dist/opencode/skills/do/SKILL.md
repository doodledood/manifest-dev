---
name: do
description: 'Manifest executor. Works through Deliverables verifying every Acceptance Criterion and Global Invariant. Use when executing a manifest, running a plan, implementing a defined task, or when the user asks to run, execute, implement, or ship a manifest-backed plan.'
argument-hint: '<manifest-path> [--no-log]'
user-invocable: true
---

## Execution

### What binds the run

Work toward the manifest's Deliverables in the order listed. Acceptance Criteria and Global Invariants are the binding layer — they are what the run owes, and gates are the only thing that can hold it open. Process Guidance is advisory: recommendations on how to work, weighed rather than enforced, and set aside when the work is better for it — name every departure on whichever terminal path the run takes — completion summary, escalation payload, or pending summary — and in the execution log too when a log is being kept, since advisory only stays safe while departing stays visible. The Initial Approach and the Deliverable order are likewise plan, not contract: pivot either when reality diverges, and name the deviation the same way a departure is named. Resequence when execution changes what the order was built on — a real dependency the order missed, or a shift in which Deliverable is now least proven, since proving the leading approach is exactly what ordering by uncertainty is for.

### Running the verifiers

Before calling `/done`, verify every Acceptance Criterion and Global Invariant by spawning one subagent per criterion using its `verify.prompt:` verbatim — no rewording. (Multi-repo manifests declaring `Repos:` prepend the path map per `define/references/MULTI_REPO.md`; otherwise nothing wraps the author's prompt.)

Every verifier is a **general-purpose** subagent driven by `verify.prompt` — when a gate needs specialized behavior the prompt activates a skill (e.g. the `review-code` skill with a dimension, or the `check-pr` skill). There is no `verify.agent` field. The optional `verify.model:` selects the model. Respect `phase:` ordering — serial across phases, parallel within.

### The gate ledger

Each verifier returns PASS, FAIL, or BLOCKED; track each gate's latest verdict and its freshness in a gate ledger. A substantive change to a gate's subject after a PASS marks that gate stale; re-reading, re-examining, and cosmetic or no-op edits do not. Manifest amendments invalidate evidence for new or definition-changed gates as described under Steering & amendment. Stale and unverified gates re-verify before `/done`; a settled PASS does not re-run.

### When the run is done

A fresh independent PASS on every Acceptance Criterion and Global Invariant is both **necessary and sufficient** for done: necessary — never declare done on self-attestation or a "looks done" judgment in place of verifier output; sufficient — once every gate holds a fresh PASS the run is complete, so call `/done` and stop. Do not keep refining past the gates: a passing gate is settled, not provisional, and the verifier's PASS is the evidence that ends the loop.

### Acting on verdicts

Any BLOCKED routes via `/escalate`. FAIL bodies carry findings or a natural-language hint — read them and act on what they say.

## Failure routing

Code-change fix attempts iterate until they pass or `/do` judges them genuinely unrecoverable → `/escalate`. Other retry shapes (waiting, retriggering, replying with or without resolving, mechanical syncs) aren't fix attempts — they follow the verifier's findings directly.

**Bound repairs by subject, not by count.** When a gate FAILs again with substantive findings in a subject already repaired — the same code path, document section, or design decision an earlier finding named — stop and route to `/escalate` instead of patching again: findings that keep landing in one place mean the design is wrong rather than the wording, and the next patch tends to spawn the finding after it. Judge substantive from the finding itself, not from a severity label: graded verifiers report MEDIUM-or-higher, and the many gates that emit no severities at all still report defects that count. Distinct findings in distinct subjects are the loop working normally and don't trip this. Keep it separate from runaway protection below — that bounds the *same* fix retried; this bounds *different* fixes converging on one subject.

**When a hint or finding indicates terminal / unrecoverable / human-decision-needed, route to `/escalate` — autonomously amending the manifest to suppress the block is forbidden.**

## External review input

When a finding carries **external review input** — a PR review comment or bot suggestion, as opposed to the manifest's own Acceptance Criteria and Global Invariants, which stay authority and must be satisfied — judge it before acting instead of implementing it to make the thread go away.

Weigh whether it's correct, whether it serves this PR's intent, and whether addressing it is proportionate to that intent — a valid point that needs work beyond the PR's intent belongs in separate work, not this PR. Adopt the comments that clear that bar; on the ones that don't — a false positive, or a valid-but-separate-scope ask — reply with your reasoning rather than changing code.

Push back even on a human reviewer when you are confident, with a respectful reply that leaves the thread open for them to resolve; when you are not — a borderline-valid point, or a substantive design objection — surface it to the user, or in an autonomous run reply non-committally and leave it for a human rather than bulldozing. Making this call autonomously is safe because `/do` drives to mergeable, never merged — a human still reviews the diff before the button.

When the user does want a beyond-intent ask incorporated, that is an amendment: invoke `define` again with the manifest path and the amendment context — `/define` reads "manifest path in args = amend" and applies targeted changes.

## Caller overlays

Caller overlays may narrow retry cadence without changing the manifest. In CI one-shot / no-wait contexts, execute immediately actionable findings (fix, test, commit/push when authorized, retrigger, reply, resolve, sync), then stop instead of executing long wait directives such as `bash sleep <N>; reinvoke`.

If only wait-shaped findings remain, report the waiting state as pending; do not call `/done`, do not call `/escalate`, and do not keep the runner alive.

## Execution log

Execution history never lives in the manifest — logged or not, the manifest stays the acceptance contract. Unless parsed options include `--no-log`, load `references/LOG.md` and keep an append-only execution log — deviations from the Initial Approach or Deliverable order, Process Guidance departures, dead-end memory, and operational notes; a caller-supplied journal path is that log. Under `--no-log`, run without one — the log is an aid, not a precondition.

**Runaway protection.** Holds regardless of logging; the log is where its memory lives. Lifecycle verifiers like `check-pr` are stateless and report current state without counting cycles, so you own the stop condition — when the log (when kept) plus your run memory show a fix or wait has been retried well past the point of progress, route to `/escalate` (or, in no-wait mode, a pending summary) rather than looping.

## Steering & amendment

Mid-/do user messages default to invoking `define` for amendment — the manifest is the source of truth, silent scope drift is worse than an extra amendment cycle. A message that *reverses or redefines a rule* rather than adding work amends too: it widens no scope, so the drift rationale never reaches it, yet it is the class most likely to leave the manifest describing a system that no longer exists. After the amendment returns, re-read the full Manifest and reconcile the active gate ledger before resuming.

**When the manifest itself is what's wrong.** Verifiers and execution both surface evidence that a manifest statement has gone false — an Architecture that no longer describes the work, a scope boundary the work has outgrown, a `verify.prompt` whose own steering misdescribes what it is judging. That is not execution history and does not belong in the log: the log records the run deviating from the plan, and this is the plan deviating from reality. Amend — but never as the answer to that gate's own FAIL. A failing gate whose premise looks wrong routes to `/escalate` instead: a run that may rewrite the gate blocking it has no binding layer left, which is the one thing gates exist to prevent. Impeaching evidence has to arrive from somewhere other than the failure it would excuse. A gate that passes while reporting its own premise is wrong is still telling you the contract needs repair, and noting it in a completion summary is not repairing it.

**Reconciling the ledger.** A gate's verification identity is its complete effective verifier input: ID, criterion/invariant text, `verify.prompt`, `verify.model` (default: inherit), `verify.phase` (default: 1), and any caller-injected wrapper context such as a multi-repo path map. New gates and gates whose identity changed become unverified, with prior verdicts retained only as history; removed gates retire from the active ledger; unchanged gates retain their verdict and freshness subject to relevant changes in their subject. Run outstanding verification in normal phase order.

Then surface a one-line digest of what the amendment assumed (the new or changed `(auto)`/ASM entries) so a user who steered and left can audit on return. Pure questions about the manifest or process are answered inline.

## Unattended launch

When /do is the top-level execution entrypoint, establish a durable goal-setting backstop whose completion contract is auditable from the transcript after /do reads the manifest.

**What the contract must require.** A gate ledger covering every Acceptance Criterion and Global Invariant: gate id, phase, `verify.prompt` source, latest independent verifier verdict, evidence, and freshness relative to the last relevant change to its subject. Completion requires every listed gate to have fresh PASS evidence and `/done` reported. Unverified, FAIL, stale, BLOCKED/actionable, or escalation-pending gates are non-terminal. A substantive change to a gate's subject after a PASS marks that gate stale; re-reading, re-examining, and cosmetic or no-op edits do not. Stale gates re-verify before `/done`. Do not accept self-attestation, "looks done", or summary claims in place of verifier output.

**Where the contract lives.** If a broader parent workflow backstop is already visible (for example `/auto`'s full-chain contract or `/babysit-pr`'s PR-tend contract) and it carries this manifest gate-ledger condition, do not set or print a second narrower goal; operate under the parent contract. If the visible parent lacks that condition, supplement it by setting or printing the manifest-completion contract before continuing. Otherwise, if the active harness exposes a goal-setting or continuation capability, set the manifest-completion contract directly; if not, print the copy-pasteable contract for the user to apply manually.

The contract should also carry the objective, constraints, stop/block condition, and compact progress expectations when useful, so continuation keeps running until all gates pass rather than stopping at the first turn's end.

## Input

`<manifest-path>` — required; no args → halt with usage. Interpret only top-level skill options as flags; quoted or topic mentions of `--no-log` are text. Read the manifest fully before any execution. Multi-repo manifests (declare `Repos: [name: path, ...]` in Intent) — use absolute paths in tool calls when working in a non-cwd repo.
