---
name: review-pr
description: 'Autonomous PR review that posts high-signal, human-voiced comments under your account. Use when reviewing someone else''s PR or your own manifest-driven PR, when you want a precision-tuned review you can walk away from, or when the user asks to review a PR, post a PR review, autoreview, loop review, or watch a PR.'
argument-hint: '[pr-url] [--manifest <path>] [--bundle <urls>] [--loop]'
user-invocable: true
---

High-signal autonomous PR review posted under your account. A review you'd put your name on — precision over coverage.

**Inputs.** `pr-url` from the arg or the current branch's upstream PR. `--manifest <path>` switches the skill into **manifest mode** (see Manifest Mode): it skips the generic reviewer fleet and independently verifies *only* the manifest's contract — it does not merely ground the fleet against author intent. Without `--manifest`, review runs the generic `review-code` fleet. The skill does not auto-discover a manifest from any folder convention. `--bundle <urls>` plus PR-description linked-PR parsing (`Depends on #N`, `Stack:`, `Co-changes:`, GitHub PR URLs) provides cross-PR context for coupled changes. Resolve the PR, current head SHA, our prior GitHub reviews/comments/replies, open review threads, author commits, PR description, and linked-PR context before deciding what to do.

## One-Shot Pass

Every invocation, including non-`--loop`, performs one complete PR-state advance:

1. **Advance our existing threads.** For every unresolved thread we authored or replied to, run the per-comment verifier below. Post needed thread replies, resolve terminal threads, and leave genuinely pending threads open.
2. **Verify the change.** **Manifest mode** (`--manifest`): run Manifest Mode verification below against the PR head — the generic reviewer fleet is skipped entirely. **No-manifest mode:** run the generic reviewer fleet over the review range — determine that range from durable GitHub state: if we have a prior review on this PR, use that review's commit/head SHA as the lower bound and review `last-reviewed-by-us..current-head`; otherwise review the full PR diff. In either mode, if the head is unchanged from our latest review, skip re-verifying the code only after thread advancement has run.
3. **Post outcomes.** Submit new surviving findings as a single GitHub review with decision `comment`. Thread replies are posted on their existing threads, not as new review comments. End with the cycle summary below.

The one-shot pass is CI-shaped: it must make useful progress from only GitHub state and the current checkout. Do not rely on session memory such as `last-reviewed-sha`; derive it from our prior review/comment metadata and the PR history each run.

## Manifest Mode

With `--manifest <path>`, the skill independently re-verifies the manifest's contract instead of running the generic reviewer fleet. Read the manifest fully, then spawn one **general-purpose** subagent per Acceptance Criterion and per Global Invariant, each driven by that criterion's `verify.prompt:` **verbatim** — no rewording — evaluated against the PR head. This is the same fanout `/do` runs in-session (`do`): the optional `verify.model:` selects the subagent's model — running on a different tool/model is where the cross-model independence comes from — and `phase:` ordering is respected, serial across phases and parallel within. Each subagent returns PASS, FAIL, or BLOCKED.

The generic `review-code` fleet is **not** also run. `/define` default-injects a `review-code` Global Invariant, so generic code-quality review already travels inside the manifest and runs *as* one of these verifications; the manifest is the single source of truth for what "done" requires. Running both would reintroduce a second source of truth and noisy duplicate comments on a contract-driven PR.

**PR-head checkout.** `verify.prompt`s execute the code at PR head (tests, builds, greps). Like `/do` and `babysit-pr`, manifest mode runs against the current working checkout: ensure it is at the PR head SHA before spawning verifiers — check the head out if the runner isn't already on it — and derive head from GitHub each run, never from session memory.

**Posting & approval.** Surface each FAIL or BLOCKED as one voice-compliant comment naming the failing criterion (its manifest id) and the verifier's concrete finding, anchored to the file:line the finding points at, else file- or PR-level; submit them through the shared **Posting** path (a single batched review, decision `comment`). When every criterion PASSes there are zero comments to post: take the shared **Zero comments to post** path — manifest-mode "all green" is the approval signal (user-confirmed in interactive sessions, no PR action under `--loop`/CI).

**Fingerprint, don't re-post.** PASS/FAIL comments recur every push, so track each by a content fingerprint (criterion id + finding substance), not comment id: re-post a criterion's FAIL only when its finding changes, and prune a FAIL whose criterion now PASSes. This keeps the thread clean and keeps `/do`/`babysit-pr` ingestion — which treats these comments as external review input it judges before acting — from looping on stale repeats.

Thread advancement (the Per-Comment Verifier below) runs in both modes; only the code-verification half of step 2 branches.

## Per-Comment Verifier

For every unresolved thread we authored or replied to, spawn one verifier subagent. The subagent receives:

- The original finding: anchor, body, review commit/head SHA, and concrete concern.
- Every author reply on this thread since our last message, plus every prior reply we posted on this thread.
- Current code at the anchor, with nearby context, and any commits since the original review that touched the relevant range.
- Full PR history: all comments, review threads, commit messages, current PR description, and our prior review/comment bodies.
- Bundle context for each linked PR (≤5): diff, description, top-level conversation.
- The voice profile below for drafting replies.

The subagent returns exactly one disposition:

- **`addressed-by-fix`** — A commit after our review modified the relevant code AND removes the concrete failure mode. Resolve the thread. Straightforward code fixes do not need a reply unless there was active discussion to answer.
- **`addressed-by-valid-reply`** — The author replied on this or another thread with an argument a fair-minded human reviewer would concede: correct factual context, deliberate owner trade-off, valid out-of-scope boundary, or code elsewhere already covering the concern. Post a short concession/acknowledgment reply, then resolve.
- **`false-positive-or-stale`** — Our comment was wrong, stale, or disproven by current PR history. Post a brief correction that owns the miss, then resolve.
- **`needs-our-pushback`** — The author replied or changed code, but the concrete concern remains. Post a short reply on the existing thread and keep it pending.
- **`still-pending`** — No relevant new author reply and no relevant code change since our last look. Keep the thread pending without posting.

Push back only on new signal, and stay on the specific point under contention. Do not repost the same argument without a new author reply or code change.

**Reviewer fleet.** No-manifest mode only — skipped entirely in manifest mode (see Manifest Mode). Each lens is a **dimension** of the `review-code` skill — spawn one general-purpose subagent per dimension and have it activate the review-code skill with that dimension against the review range. Always-on dimensions: `change-intent`, `code-bugs`, `code-design`, `code-maintainability`, `code-simplicity`, `context-file-adherence`. Add when the diff fits: `type-safety` on typed code; `test-quality` and `code-testability` on source; `contracts` on API surfaces; `operational-readiness` on CI/infra/env/migrations/workers/queues/secrets; `docs` and `prose-value` on prose. For prompts/skills/agents, spawn a general-purpose subagent that activates the `review-prompt` skill (plus, if available, the external prompt-engineering-plugin agents `prompt-token-efficiency-verifier` and `prompt-compression-verifier`). Forward the manifest to every spawned reviewer when present.

**Narrow-lens reviewers.** Reviewer agents never receive PR conversation, linked-PR diffs, or linked-PR conversation. That context flows only to the holistic pass — narrow lens is what keeps each reviewer precise.

**Holistic coherence pass.** Collect findings from the fleet, drop Low severity, and spawn one subagent with what remains plus:

- PR history: all comments and threads on the PR (including our own from any prior review pass), the author's recent commit messages on the branch, the PR description.
- Bundle context for each linked PR: diff, description, top-level conversation. No inline review comments from linked PRs.
- The manifest if present.
- The reviewed range for this invocation.
- Any truncation the caller did, carried forward.

The subagent:

- **Prunes** any finding already covered on the PR: any prior comment (ours from a previous run, or another reviewer's), any concession or rebuttal on an existing thread, anything contradicted by the manifest, a commit message, or the PR description, or piling on an active thread.
- **Dedupes** across reviewers: merge near-duplicates into one comment when they raise the same underlying concern.
- **Bounds** surfaced findings to issues introduced or exposed by the reviewed range, unless this is the first review and the range is the full PR.
- **Anchors** each surviving finding to exactly one of inline file:line (default), file-level (whole-file concern), or PR-level (cross-cutting, no specific anchor).
- **Rewrites** every comment body and any drafted reply in the voice profile below.
- **Omits a summary header by default** — adds one only when there's a real overall take the per-comment list misses (one short sentence, voice-compliant, no boilerplate).

Returns: comments to post (anchor + voice-compliant body), summary header text if any, truncation notes, and a brief dropped-findings tally with dominant reasons.

**Voice.** Each comment is one thought: state the problem, point to evidence inline (file:line, short code excerpt when load-bearing), suggest the fix. Direct, concrete, no softeners.

Never in a posted body, header, or thread reply: severity labels (`[High]`, `⚠️`, `Critical:`); emoji of any kind; em-dash rhetorical flourishes ("It's not just X — it's Y" / "not just A, but B"); softeners ("I think", "I recommend", "It seems", "Perhaps consider"); opener boilerplate ("Great PR!", "Nice change, but..."); "at the location above" / "as mentioned" (always name file:line inline); AI disclosure footer.

Structural defaults: prose, not bullets, for a single suggestion; no markdown headers or bold-the-takeaway when the comment is one thought. Headers and bullets are fine when a comment genuinely covers multiple distinct thoughts or parallel items.

Target voice: *"Empty input skips the null check — `if (input?.value)` at `parser.ts:42` short-circuits before the parse at `parser.ts:47`, so `{}` reaches `parse()` without the guard. Tighten to `if (input?.value != null)`, or move the `parse()` call inside the existing branch."*

**Posting.** When the holistic pass returns comments to post, submit a single GitHub PR review with decision `comment` — all comments batched atomically. In CI or non-interactive contexts, do not wait for approval.

**Zero comments to post.** When the holistic pass returns nothing and all our existing threads reached terminal disposition, report clean. In interactive sessions only, ask: `"Looks good to me. Post as approval on the PR?"`. Approve → submit decision `approve` with body `Looks good to me.`; decline → take no PR action. In CI or non-interactive contexts, take no approval action.

**Cycle summary.** Every one-shot pass ends with an operator-facing summary, whether it posted comments, resolved threads, asked for approval, or found nothing to do. Keep it compact but complete:

- Reviewed range/head and concrete PR actions taken: new review comment count and anchors, thread replies, resolved threads, approval prompt/action, or no PR action.
- Per-comment verifier subagents: one line per thread naming the anchor, disposition, and the verifier's short reason.
- No-manifest mode — Reviewer fleet subagents: one line per spawned reviewer naming its actionable findings count and the substance of what it found, or `none`.
- Manifest mode — Manifest verifiers: one line per Acceptance Criterion and Global Invariant naming its manifest id, PASS/FAIL/BLOCKED, the model used, and the verifier's short finding.
- Holistic coherence pass (no-manifest mode): surviving comments, dedupes/merges, pruned findings with dominant reasons, range-bounding decisions, summary header if any, and truncation notes.

The cycle summary is for the operator transcript or run log only. Do not paste it into PR review bodies, thread replies, or approval text; the only posted summary-like text is the voice-compliant summary header returned by the holistic pass.

**Gotchas.**

- The only path to decision `approve` is the user-confirmed lgtm prompt above. Never submit `approve` automatically anywhere else.
- Never submit decision `request_changes` — this skill does not algorithmically block merges.
- Never add an AI disclosure footer to a comment, summary, or reply. There is no flag for one.
- Never forward PR conversation or bundle context to a reviewer agent. Only the holistic pass may see that context.
- Never re-raise a finding the holistic pass pruned in this run.
- Never skip thread advancement because the code review range is empty; thread state can change without a new commit.
- In manifest mode, run each `verify.prompt` verbatim and never also run the generic reviewer fleet — the manifest (which `/define` default-injects a `review-code` invariant into) is the single source of truth, and running both reintroduces a second source of truth with duplicate comments.
- In manifest mode, track PASS/FAIL comments by content fingerprint, not comment id — they recur after every push, and re-posting an unchanged FAIL loops `/do`/`babysit-pr` ingestion.

**`--loop`.** Load `references/LOOP.md`.
