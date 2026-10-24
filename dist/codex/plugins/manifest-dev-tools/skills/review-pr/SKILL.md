---
name: review-pr
description: 'Autonomous PR review that posts high-signal, human-voiced comments under your account. Use when reviewing someone else''s PR or your own manifest-driven PR, when you want a precision-tuned review you can walk away from, or when the user asks to review a PR, post a PR review, autoreview, loop review, or watch a PR.'
argument-hint: '[pr-url] [--manifest <path>] [--bundle <urls>] [--loop]'
user-invocable: true
---

High-signal autonomous PR review posted under your account. A review you'd put your name on — precision over coverage.

**Inputs.** `pr-url` from the arg or the current branch's upstream PR. `--manifest <path>` switches the skill into **manifest mode**: it skips the generic reviewer fleet and verifies *only* the manifest's contract — it does not merely ground the fleet against author intent. Only in that mode, load `references/MANIFEST_MODE.md` for the verification mechanics; without `--manifest`, that reference is never read and review runs the generic `review-code` fleet. The skill does not auto-discover a manifest from any folder convention. `--bundle <urls>` plus PR-description linked-PR parsing (`Depends on #N`, `Stack:`, `Co-changes:`, GitHub PR URLs) provides cross-PR context for coupled changes. Resolve the PR, current head SHA, our prior GitHub reviews/comments/replies, open review threads, author commits, PR description, and linked-PR context before deciding what to do.

**Review organization.** Run the required inspections in this session or delegate them to separate contexts when useful; related work may share a context. Another context can help with independent judgment, separable work, or substantial reading. Without that capability, work inline. Placement does not change the required coverage, skill standards, or result for each thread, dimension, and gate. Honor an explicit request for independent review, and report the context actually used rather than claiming independence from the author when none was present.

**Self-marking.** Posting under your own account means a human reviewer uses the same account, so authorship alone can't tell our automated comments from theirs. Stamp every body this skill posts — new finding comments, thread replies, the summary header, the approval body, and manifest-mode PASS/FAIL — with a trailing hidden marker `<!-- manifest-dev:review-pr -->` — a fixed literal string, byte-identical wherever review-pr runs (don't namespace-rewrite it per distribution, or comments posted by one host stop matching another's); GitHub strips it from the rendered comment but returns it through the API. This marker, not account authorship, is what makes a comment an automated review-pr comment: everywhere this skill says *threads/comments we authored or replied to* (or *our prior* reviews/comments) it means the ones carrying this marker, so an unmarked comment on our account reads as human and is left untouched. Manifest mode extends the marker with the criterion id (`references/MANIFEST_MODE.md`). Judgment-pass findings extend it with a `judgment` token — `<!-- manifest-dev:review-pr judgment -->` — so a prior judgment finding is distinguishable from an ordinary review-pr comment in both modes (the once-per-PR gate keys on this token).

## One-Shot Pass

Every invocation, including non-`--loop`, performs one complete PR-state advance:

1. **Advance our existing threads.** For every unresolved thread we authored or replied to, run the per-thread verification below. Post needed thread replies, resolve terminal threads, and leave genuinely pending threads open.
2. **Verify the change.** **Manifest mode** (`--manifest`): load `references/MANIFEST_MODE.md` and follow it to verify the manifest contract against the PR head — the generic reviewer fleet is skipped entirely. **No-manifest mode:** run the generic reviewer fleet over the review range — determine that range from durable GitHub state: if we have a prior review on this PR and the head has moved since, use that review's commit/head SHA as the lower bound and review `last-reviewed-by-us..current-head`; otherwise review the full PR diff. Later `--loop` wakes use that invocation's checkpoint instead, per `references/LOOP.md`. In **both** modes, include the judgment pass (below) when its once-per-PR generation rule permits it.
3. **Post outcomes.** Submit new surviving findings as a single GitHub review with decision `comment`. Thread replies are posted on their existing threads, not as new review comments. End with the cycle summary below.

Each invocation starts from GitHub state and the current checkout. A `--loop` invocation then checkpoints completed verification for its later wakes, per `references/LOOP.md`; a fresh invocation always verifies again.

**An invocation always verifies the change.** Choosing to run review-pr again is the operator's call — often a risky change worth a second read, under a different model — so a fresh invocation reviews the head even when we already reviewed it and nothing has moved since. There is nothing to pass for this. The review range is then the full PR diff, and the prune below is what keeps the pass to whatever it has new to add: a second read that simply concurs posts nothing.

The unchanged-head skip survives in one place only — a `--loop` wake after that invocation's first pass (`references/LOOP.md`). There nobody re-decided anything, and re-reviewing one commit on every wake is the nag the check exists to prevent. Where a PR carries no prior review of ours, the pass is already a full review of the full diff and nothing about it differs.

## Per-Thread Verification

For every unresolved thread we authored or replied to, invoke the `review-pr-thread-verify` skill. Supply the evidence for that thread:

- The original finding: anchor, body, review commit/head SHA, and concrete concern.
- Every author reply on this thread since our last message, plus every prior reply we posted on this thread.
- Current code at the anchor, with nearby context, and any commits since the original review that touched the relevant range.
- Full PR history: all comments, review threads, commit messages, current PR description, and our prior review/comment bodies.
- Bundle context for each linked PR (≤5): diff, description, top-level conversation.
- The voice profile below, for any reply it drafts.

It returns exactly one disposition, a short reason, and a drafted reply where the disposition calls for one. Act on it: `addressed-by-fix` → resolve the thread, posting the reply only if it drafted one; `addressed-by-valid-reply` → post its concession, then resolve; `false-positive-or-stale` → post its correction, then resolve; `needs-our-pushback` → post its reply on the existing thread and keep it pending; `still-pending` → leave the thread open and post nothing.

**Reviewer fleet.** No-manifest mode only — skipped entirely in manifest mode (`references/MANIFEST_MODE.md`). Activate the `review-code` skill for each required dimension against the review range, retaining each dimension's findings and verdict even when the reviews share a context. Always-on dimensions: `change-intent`, `code-bugs`, `code-design`, `code-maintainability`, `code-simplicity`, `context-file-adherence`. Add when the diff fits: `type-safety` on typed code; `test-quality` and `code-testability` on source; `contracts` on API surfaces; `operational-readiness` on CI/infra/env/migrations/workers/queues/secrets; `docs` and `prose-value` on prose; `defect-class` when the reviewed range **fixes a defect** — it judges the repair's protection and affected-site accounting, so it has no input on a change that fixes nothing. Deciding that is yours: use the PR description, commits, and linked issues to establish whether a defect is being fixed. For prompts/skills/agents, add a run that activates the `review-prompt` skill the same way.

**Evidence and scope.** Keep each dimension focused on its own standard. Use binding requirements, explicit exclusions, and permission limits to judge scope, and give them to defect-class so it can judge authorized remedies. An author's implementation preference is not such a limit. Inspect the code and relevant evidence; the author's explanation or success report does not establish correct behavior. The judgment pass also needs the stated pain and whole-PR context to assess the premise.

**Holistic coherence pass.** After every required inspection has returned, collect their findings (drop Low severity except defect-class findings; keep dimension and severity; judgment findings are a distinct non-severity class, **not** subject to drop-Low). Invoke the `review-pr-holistic` skill. Keep BLOCKED verdicts with their missing evidence or authority in the cycle summary; consolidation cannot turn an incomplete evaluation into a clean result. Supply the retained findings plus:

- PR history: all comments and threads on the PR (including our own from any prior review pass), the author's recent commit messages on the branch, the PR description.
- Bundle context for each linked PR: diff, description, top-level conversation. No inline review comments from linked PRs.
- The reviewed range for this invocation — the code the fleet's defect findings are bounded to.
- The judgment pass's findings, from its whole-PR assessment (below). They are consolidated alongside the fleet's but stay exempt from drop-Low and from reviewed-range bounding — the judgment pass reads the whole PR head itself, so its findings are already whole-PR.
- Any truncation the caller did, carried forward.
- The voice profile below.

It prunes what the PR already covers, dedupes across reviewers, subordinates defect findings beneath a judgment question on the same surface (premise-subsumption), bounds defect findings to the reviewed range, anchors each survivor, and rewrites every body in the voice profile. It returns the comments to post (anchor + voice-compliant body), summary header text if any, truncation notes, and a brief dropped-findings tally with dominant reasons.

**Judgment pass (premise check).** Runs in **both** modes; in manifest mode it wires via `references/MANIFEST_MODE.md`. Activate the `review-pr-judgment` skill as its own assessment before consolidation. It is **wide-context**: fed the PR description, conversation, codebase direction, linked-PR context (diff, description, top-level conversation), and the **full PR-head diff** (`base..head`, the whole PR), so its whole-PR altitude holds even on an incremental/loop pass where the reviewed range is only the latest delta. It asks the whole-PR question of whether the change earns its keep against the pain it solves, only when concrete evidence fires one of its triggers. Its findings are a **distinct non-severity class** (`{trigger, evidence, author-facing question}`). The judgment pass itself **synthesizes one question per root** before returning (so this holds in both modes, independent of the holistic pass). In no-manifest mode those findings then flow into the holistic coherence pass, which dedupes/merges them alongside fleet findings but **exempts them from the drop-Low step** (they surface whenever the evidence-gate fires and the PR does not already cover the point, never bounded to the reviewed range) and applies **premise-subsumption** (the `review-pr-holistic` rule that folds defect findings beneath a premise question on the same surface). They post as author-answerable questions through the same voice, self-marker, and single batched `comment` review; the judgment pass never blocks, never submits `request_changes`, and never auto-approves.

**Once per PR.** Fresh judgment generation runs only when no prior **judgment-marked** finding (`<!-- manifest-dev:review-pr judgment -->`) exists on the PR — read from durable GitHub state, never session memory. So once the pass has posted a question, later passes skip regeneration and never re-nag; the discriminator token is what makes "a prior judgment finding exists" detectable (the base marker alone can't — every review-pr comment carries it). This matches its kind: defect-finding re-runs each round on new commits, but a premise question is answered once by the human, so re-posting it every round would be the nag this pass exists to avoid. Advancing an existing judgment thread (reply/resolve via per-thread verification) is **not** gated by this — only fresh generation is. Two honest bounds: (1) a pass that stays **silent** posts no judgment marker, so on a PR the pass keeps finding sound it may re-run on later rounds — bounded and harmless, since it stays silent (no nag), and the whole-PR read is the same cost the fleet already pays each round; (2) a premise concern introduced by a *late* commit after a question was already posted is not re-caught — most premise issues are visible from the initial PR, and re-scanning every round is the noise.

**Voice.** Each comment is one thought: state the problem, point to evidence inline (file:line, short code excerpt when load-bearing), suggest the fix. Direct, concrete, no softeners.

Never in a posted body, header, or thread reply: severity labels (`[High]`, `⚠️`, `Critical:`); emoji of any kind; em-dash rhetorical flourishes ("It's not just X — it's Y" / "not just A, but B"); softeners ("I think", "I recommend", "It seems", "Perhaps consider"); opener boilerplate ("Great PR!", "Nice change, but..."); "at the location above" / "as mentioned" (always name file:line inline); AI disclosure footer.

Structural defaults: prose, not bullets, for a single suggestion; no markdown headers or bold-the-takeaway when the comment is one thought. Headers and bullets are fine when a comment genuinely covers multiple distinct thoughts or parallel items.

Target voice: *"Empty input skips the null check — `if (input?.value)` at `parser.ts:42` short-circuits before the parse at `parser.ts:47`, so `{}` reaches `parse()` without the guard. Tighten to `if (input?.value != null)`, or move the `parse()` call inside the existing branch."*

**Posting.** When the holistic pass returns comments to post, submit a single GitHub PR review with decision `comment` — all comments batched atomically. In CI or non-interactive contexts, do not wait for approval.

**Zero comments to post.** When the holistic pass returns nothing, every required dimension completed without BLOCKED, and all our existing threads reached terminal disposition, report clean. Otherwise report incomplete with the unresolved evaluation blockers; continue independent review work and do not offer approval. Only after a clean result, in interactive sessions, ask: `"Looks good to me. Post as approval on the PR?"`. Approve → submit decision `approve` with body `Looks good to me.`; decline → take no PR action. In CI or non-interactive contexts, take no approval action.

**Cycle summary.** Every one-shot pass ends with an operator-facing summary, whether it posted comments, resolved threads, asked for approval, or found nothing to do. Keep it compact but complete:

- Review context used, reviewed range/head, and concrete PR actions taken: new review comment count and anchors, thread replies, resolved threads, approval prompt/action, or no PR action.
- Whether this pass re-reviewed a head we had already reviewed or reviewed a new delta, and on a re-review, the split between findings newly surfaced and findings dropped as already covered — the only thing distinguishing a second read that agreed from one that never happened.
- Per-thread verifications: one line per thread naming the anchor, disposition, and the verifier's short reason.
- Reviewer fleet (no-manifest mode): one line per dimension run naming its verdict, actionable findings count and substance, or `none`; for BLOCKED, name the missing evidence or authority. In manifest mode, report per-criterion verifier results instead, per `references/MANIFEST_MODE.md`.
- Holistic coherence pass (no-manifest mode): surviving comments, dedupes/merges, pruned findings with dominant reasons, range-bounding decisions, summary header if any, and truncation notes.
- Judgment pass (no-manifest mode): premise questions posted — count and their roots — or `none`. In manifest mode, report it per `references/MANIFEST_MODE.md`.

The cycle summary is for the operator transcript or run log only. Do not paste it into PR review bodies, thread replies, or approval text; the only posted summary-like text is the voice-compliant summary header returned by the holistic pass.

**Posting boundaries.** Approval requires the explicit user-confirmed path above. Never submit `request_changes`, revive a pruned finding, or relax deduplication to produce output. Advance existing threads even when the code review range is empty.

**`--loop`.** Load `references/LOOP.md`.
