---
name: review-pr-holistic
description: 'Called by review-pr after its reviewer fleet and judgment pass return: consolidates their findings against the PR''s history into the set of comments worth posting — pruning what the PR already covers, merging duplicates, subordinating defects under premise questions, bounding to the reviewed range, and rewriting every body in the caller''s voice. Not for direct use.'
user-invocable: false
---

# review-pr-holistic

Turn a pile of findings into the comments a careful reviewer would actually post. This skill edits and consolidates; it generates nothing new and posts nothing itself.

**Receives.** Fleet findings — severity-graded defect findings from the reviewer dimensions, already stripped of Low severity by the caller — and judgment findings — a distinct non-severity class, each `{ trigger, concrete evidence, author-facing question }`, already synthesized to one question per root; the PR history (all comments and threads on the PR, including ours from any prior pass, the author's recent commit messages on the branch, the PR description); bundle context for each linked PR (diff, description, top-level conversation — no inline review comments from linked PRs); the manifest if present; the reviewed range for this invocation — the code the fleet's defect findings are bounded to; the caller's voice profile — its rules for how a posted comment reads; and any truncation the caller did, to carry forward.

**Does, in this order:**

- **Prunes** any finding already covered on the PR: a prior comment (ours from a previous run or another reviewer's), a concession or rebuttal on an existing thread, anything contradicted by the manifest, a commit message, or the PR description, or anything that would pile on an active thread.
- **Dedupes** across reviewers: merge near-duplicates into one comment when they raise the same underlying concern.
- **Premise-subsumption.** When a judgment finding questions the necessity or existence of a surface, subordinate the fleet's findings on that same surface under the premise question — drop the low-value ones, and fold any that survive beneath it ("if you keep X: also a, b") rather than listing them as independent peers. Never hard-delete a severe independent defect: the judgment finding is non-blocking, so a defect that matters even if the surface stays is still surfaced on its own.
- **Bounds** surfaced defect findings to issues introduced or exposed by the reviewed range, unless the range is the full PR diff — which covers a first review and a repeat review of an unchanged head alike. This keys on the range, never on whether we have reviewed before: bounding a repeat pass to the delta since our last review would have it read the whole PR and then surface nothing. Judgment findings are exempt: they are whole-PR by construction and stay exempt from the drop-Low step too — they surface whenever their evidence fired and the PR does not already cover the point.
- **Anchors** each surviving finding to exactly one of inline file:line (default), file-level (a whole-file concern), or PR-level (cross-cutting, no specific anchor).
- **Rewrites** every comment body and any drafted reply in the supplied voice profile.
- **Omits a summary header by default** — adds one only when there is a real overall take the per-comment list misses (one short sentence, voice-compliant, no boilerplate).

**Returns.** The comments to post (anchor plus voice-compliant body), the summary header text if any, truncation notes, and a brief dropped-findings tally with the dominant reasons.
