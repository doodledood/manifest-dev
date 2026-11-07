---
name: review-pr
description: 'Autonomous PR review that posts high-signal, human-voiced comments under your account. Use when reviewing someone else''s PR or your own manifest-driven PR, when you want a precision-tuned review you can walk away from, or when the user asks to review a PR, post a PR review, autoreview, loop review, or watch a PR.'
argument-hint: '[pr-url] [--manifest <path>] [--bundle <urls>] [--loop]'
user-invocable: true
---

High-signal autonomous PR review posted under your account. A review you'd put your name on — precision over coverage.

**Inputs.** `pr-url` from the arg or the current branch's upstream PR. `--manifest <path>` switches the skill into **manifest mode**: it skips the generic reviewer fleet and verifies *only* the manifest's contract — it does not merely ground the fleet against author intent. Only in that mode, load `references/MANIFEST_MODE.md` for the verification mechanics; without `--manifest`, that reference is never read and review runs the generic `review-code` fleet. The skill does not auto-discover a manifest from any folder convention. `--bundle <urls>` plus PR-description linked-PR parsing (`Depends on #N`, `Stack:`, `Co-changes:`, GitHub PR URLs) provides cross-PR context for coupled changes. Resolve the PR, current head SHA, our prior GitHub reviews/comments/replies, open review threads, author commits, PR description, and linked-PR context before deciding what to do.

**Review organization.** Run the required inspections in this session or delegate them to separate contexts when useful; related work may share a context. Another context can help with independent judgment, separable work, or substantial reading. Without that capability, work inline. Placement does not change the required coverage, skill standards, or result for each thread, dimension, and gate. Honor an explicit request for independent review, and report the context actually used rather than claiming independence from the author when none was present.

**Self-marking.** Posting under your own account means a human reviewer uses the same account, so authorship alone can't tell our automated comments from theirs. Stamp every body this skill posts — new finding comments, thread replies, the summary header, the approval body, and manifest-mode PASS/FAIL — with a trailing hidden marker `<!-- manifest-dev:review-pr -->` — a fixed literal string, byte-identical wherever review-pr runs (don't namespace-rewrite it per distribution, or comments posted by one host stop matching another's); GitHub strips it from the rendered comment but returns it through the API. This marker, not account authorship, is what makes a comment an automated review-pr comment: everywhere this skill says *threads/comments we authored or replied to* (or *our prior* reviews/comments) it means the ones carrying this marker, so an unmarked comment on our account reads as human and is left untouched. Manifest mode extends the marker with the criterion id (`references/MANIFEST_MODE.md`). Judgment-pass findings extend it with a `judgment` token — `<!-- manifest-dev:review-pr judgment -->` — so a prior judgment finding is distinguishable from an ordinary review-pr comment in both modes (continuation uses this token to recover prior judgment and avoid repeating it).

## One-Shot Pass

Every invocation, including non-`--loop`, performs one complete PR-state advance:

1. **Advance our existing threads.** For every thread *Per-Thread Verification* covers, run that verification and act on its disposition. Post needed thread replies, resolve terminal threads, reopen a resolved one whose concern still stands, and leave genuinely pending threads open.
2. **Verify the change.** **Manifest mode** (`--manifest`): load `references/MANIFEST_MODE.md` and follow it to verify the manifest contract against the PR head — the generic reviewer fleet is skipped entirely. **No-manifest mode:** run the generic reviewer fleet over the review range (*Review range*, below). In **both** modes, include the judgment pass (below) under its continuation rule.
3. **Post outcomes.** Submit new surviving findings as a single GitHub review with decision `comment`. Thread replies are posted on their existing threads, not as new review comments. End with the cycle summary below.

Each invocation starts from GitHub state and the current checkout.

**An invocation always verifies the change.** Choosing to run review-pr again is the operator's call — often a risky change worth a second read, under a different model — so a fresh invocation reviews the head even when we already reviewed it and nothing has moved since. The review range is then the full PR diff, and the prune below is what keeps the pass to whatever it has new to add: a second read that simply concurs posts nothing.

The one unchanged-head skip is a `--loop` wake after that invocation's first pass (`references/LOOP.md`): there nobody re-decided anything, and re-reviewing one commit on every wake is the nag the check exists to prevent.

**Review range.** The lower bound is the head our latest prior review on this PR recorded in GitHub state; on a `--loop` wake after the invocation's first pass, it is the head of that invocation's latest checkpoint instead. Review `lower-bound..current-head` when the current head has moved past the bound and still descends from it. Otherwise review the full PR diff: with no prior review, at an unchanged head on a fresh invocation, and when a rebase or force-push left a head that no longer descends from the bound, since that range no longer describes the PR's change.

## Per-Thread Verification

This verification covers every unresolved thread we authored or replied to, and every thread opened by our finding that someone other than this account resolved — a resolution says nothing about whether the concern is gone, so it is verified like a reply. A resolved judgment-marked thread is recovered by *Judgment continuation* instead. For each, invoke the `review-pr-thread-verify` skill. Supply the evidence for that thread:

- The original finding: anchor, body, review commit/head SHA, and concrete concern.
- Whether the thread is resolved, and by whom.
- Every author reply on this thread since our last message, plus every prior reply we posted on this thread.
- Current code at the anchor, with nearby context, and any commits since the original review that touched the relevant range.
- Full PR history: all comments, review threads, commit messages, current PR description, and our prior review/comment bodies.
- Bundle context for each linked PR (≤5): diff, description, top-level conversation.
- For a judgment thread, the relevant project direction and decisions, the prior recommendation and the evidence or accepted trade-off it rested on.
- The voice profile below, for any reply it drafts.

It returns exactly one disposition, a short reason, and a drafted reply where the disposition calls for one; for judgment, also the current recommendation and whether the discussion is settled. Preserve that assessment in the cycle summary even after resolving the thread. Act on it:

| Disposition | Unresolved thread | Thread someone else resolved |
|---|---|---|
| `addressed-by-fix` | Resolve it, posting the reply only if one was drafted. | Leave it resolved, posting the reply only if one was drafted. |
| `addressed-by-valid-reply` | Post the concession, then resolve. | Post the concession; leave it resolved. |
| `false-positive-or-stale` | Post the correction, then resolve. | Post the correction; leave it resolved. |
| `needs-our-pushback` | Post the reply; keep it pending. | Reopen it, post the reply; keep it pending. |
| `still-pending` | Leave it open; post nothing. | Not returned: a resolution with no fix and no conceding reply leaves the concern standing. |

Post a drafted reply only when, read fresh just before posting, our latest message on that thread does not already say it — a pass stopped after replying and before resolving, or another invocation, may have posted it — then take the row's remaining step.

**Caller policy.** In no-manifest mode, assess whether the change fulfills its stated purpose
and applicable obligations without demonstrated defects or material quality costs in its
supported use and expected maintenance. Pass those claims to each inspection. Grades describe
the evidence; they are not the default acceptance condition. Publication still selects Medium+
findings by default. An explicit invocation may choose other acceptance or publication policies,
including Low; pass both separately to inspection and consolidation. Manifest mode uses the
Manifest's current claims and required policies instead. A finding omitted from publication
does not thereby become resolved or cease to count against acceptance.

**Reviewer fleet.** No-manifest mode only — skipped entirely in manifest mode (`references/MANIFEST_MODE.md`). Activate the `review-code` skill for each required dimension against the review range, retaining each dimension's findings and verdict even when the reviews share a context. Always-on dimensions: `change-intent`, `code-bugs`, `code-design`, `code-maintainability`, `code-simplicity`, `context-file-adherence`. Add when the diff fits: `type-safety` on typed code; `test-quality` and `code-testability` on source; `contracts` on API surfaces; `operational-readiness` on CI/infra/env/migrations/workers/queues/secrets; `docs` and `prose-value` on prose; `defect-class` when the reviewed range **fixes a defect** — it judges the repair's protection and affected-site accounting, so it has no input on a change that fixes nothing. Deciding that is yours: use the PR description, commits, and linked issues to establish whether a defect is being fixed. For prompts/skills/agents, add a run that activates the `review-prompt` skill the same way.

**Evidence and scope.** Keep each dimension focused on its own standard. Use binding requirements, explicit exclusions, and permission limits to judge scope, and give them to defect-class so it can judge authorized remedies. An author's implementation preference is not such a limit. Inspect the code and relevant evidence; the author's explanation or success report does not establish correct behavior. The judgment pass separately assesses the consequences against the project's purpose, using the inputs below.

**Holistic coherence pass.** After every required inspection has returned, collect their findings. Regrade correctness or safety failures and broken binding promises received as Low from their evidence before applying the caller's chosen policy. Filter only by that publication policy, retaining Low findings when requested; keep dimension and severity. Invoke the `review-pr-holistic` skill. Keep BLOCKED verdicts with their missing evidence or authority in the cycle summary; consolidation cannot turn an incomplete evaluation into a clean result. Supply the retained findings and the chosen caller policy plus:

- PR history: all comments and threads on the PR (including our own from any prior review pass), the author's recent commit messages on the branch, the PR description.
- Bundle context for each linked PR: diff, description, top-level conversation. No inline review comments from linked PRs.
- The reviewed range for this invocation — the code the fleet's defect findings are bounded to.
- The judgment pass's assessment and findings, including settled disagreements, from its whole-PR assessment (below). They are consolidated alongside the fleet's but stay exempt from the caller's severity filter and from reviewed-range bounding — the judgment pass reads the whole PR head itself, so its findings are already whole-PR.
- Any truncation the caller did, carried forward.
- The voice profile below.

It prunes what the PR already covers, dedupes across reviewers, subordinates defect findings beneath a judgment question on the same surface (premise-subsumption), bounds defect findings to the reviewed range, anchors each survivor, and rewrites every body in the voice profile. It returns the comments to post (anchor + voice-compliant body), summary header text if any, truncation notes, a brief dropped-findings tally with dominant reasons, and the judgment assessment for the operator. Pruning a comment does not erase its retained recommendation.

**Judgment pass (project consequences).** Runs in **both** modes; manifest mode wires via
`references/MANIFEST_MODE.md`. Activate the `review-pr-judgment` skill as its own assessment
before consolidation. Retrieve the project's purpose, intended users, goals and applicable
decisions from its available context, documentation and linked discussion, following relevant
pointers. Pass the sources and their reasons, not just a summary of the author's request; name
material gaps. This needs neither a Manifest nor a particular filename or setup workflow.
Supply those inputs with the PR description, conversation, linked-PR context (diff,
description, top-level conversation), the **full PR-head diff** (`base..head`), and recovered
prior judgment and dispositions. The skill owns the assessment and finding shape. In
no-manifest mode its findings and assessment flow through the holistic pass; questions post
through the existing voice, judgment marker and single batched `comment` review.

**Judgment continuation.** Recover prior judgment findings, replies and settled decisions
from durable GitHub state, including resolved judgment-marked threads. A prior marker prevents
repetition, not assessment of new consequences. Compare the current proposal and relevant
evidence with what the prior assessment considered; reassess material changes and previously
unassessed concerns against the whole PR. Continue an existing root on its thread when new
signal warrants it; only a distinct root needs a new comment. Carry unchanged supported
assessments forward, including settled disagreement, without posting them again. A fresh
explicit review may find a new concern at the same head; an unchanged loop wake does not
repeat a completed assessment. Keep the recommendation, grounds, limits and thread disposition
in the invocation checkpoint so silence or resolution cannot become inferred endorsement.

**Voice.** Each comment is one thought: state the problem, point to evidence inline (file:line, short code excerpt when load-bearing), suggest the fix. Direct, concrete, no softeners.

Never in a posted body, header, or thread reply: severity labels (`[High]`, `⚠️`, `Critical:`); emoji of any kind; em-dash rhetorical flourishes ("It's not just X — it's Y" / "not just A, but B"); softeners ("I think", "I recommend", "It seems", "Perhaps consider"); opener boilerplate ("Great PR!", "Nice change, but..."); "at the location above" / "as mentioned" (always name file:line inline); AI disclosure footer.

Structural defaults: prose, not bullets, for a single suggestion; no markdown headers or bold-the-takeaway when the comment is one thought. Headers and bullets are fine when a comment genuinely covers multiple distinct thoughts or parallel items.

Target voice: *"Empty input skips the null check — `if (input?.value)` at `parser.ts:42` short-circuits before the parse at `parser.ts:47`, so `{}` reaches `parse()` without the guard. Tighten to `if (input?.value != null)`, or move the `parse()` call inside the existing branch."*

**Posting.** When the holistic pass returns comments to post, submit a single GitHub PR review with decision `comment` — all comments batched atomically. Just before submitting, re-read the PR's comments carrying our marker and drop any comment whose concern one posted since this pass read the PR already raises, so a second invocation running on the same PR at once does not post the same findings twice; name the drops in the cycle summary. In CI or non-interactive contexts, do not wait for approval.

**Zero comments to post.** Report implementation clean only when its required assessments support acceptance,
no supported implementation failure or material verification uncertainty remains, every required
dimension completed without BLOCKED, and all our defect threads reached terminal disposition.
Report any pending judgment discussion separately; it does not change implementation acceptance. A holistic prune needs an
evidenced disposition; a publication filter alone cannot clear a failure. Otherwise report the
unresolved findings or evidence blockers, continue independent review work and do not offer
approval. Report that implementation acceptance separately from the judgment recommendation: a settled
advisory disagreement does not fail acceptance, but is not an unqualified endorsement. Only
after acceptance, in interactive sessions, offer approval with any retained adverse judgment
or material judgment limit visible in the question. With none, ask: `"Looks good to me. Post as
approval on the PR?"`. Explicit confirmation → submit decision `approve`, preserving any stated
reservation in its body; decline → take no PR action. In CI or non-interactive contexts, take no
approval action.

**Cycle summary.** Every one-shot pass ends with an operator-facing summary, whether it posted comments, resolved threads, asked for approval, or found nothing to do. Keep it compact but complete:

- Review context used, reviewed range/head, and concrete PR actions taken: new review comment count and anchors, thread replies, resolved threads, approval prompt/action, or no PR action.
- Whether this pass re-reviewed a head we had already reviewed or reviewed a new delta, and on a re-review, the split between findings newly surfaced and findings dropped as already covered — the only thing distinguishing a second read that agreed from one that never happened.
- Per-thread verifications: one line per thread naming the anchor, disposition, and the verifier's short reason.
- Reviewer fleet (no-manifest mode): one line per dimension run naming its verdict, actionable findings count and substance, or `none`; for BLOCKED, name the missing evidence or authority. In manifest mode, report per-criterion verifier results instead, per `references/MANIFEST_MODE.md`.
- Holistic coherence pass (no-manifest mode): surviving comments, dedupes/merges, pruned findings with dominant reasons, range-bounding decisions, summary header if any, and truncation notes.
- Judgment pass: recommendation, grounds and material limits; questions posted or continued, or `none`; and any settled disagreement. Distinguish the decision to proceed from reviewer endorsement. Say whether assessed afresh or carried forward and why. This also applies in manifest mode.

The cycle summary is for the operator transcript or run log only. Do not paste it into PR review bodies, thread replies, or approval text; the only posted summary-like text is the voice-compliant summary header returned by the holistic pass.

**Posting boundaries.** Approval requires the explicit user-confirmed path above. Never submit `request_changes`, repost an unchanged pruned finding, or relax deduplication to produce output. Advance existing threads even when the code review range is empty.

**`--loop`.** Load `references/LOOP.md`.
