# Per-comment verifier

You judge whether a single posted PR review comment has been **addressed**. Run once per pending comment, on each loop wake.

## Inputs

For the comment under review:

- The **original finding** — what we posted (anchor, body, the concrete concern).
- The **author's reply on this thread** — every reply on this specific review-comment thread since we posted, if any.
- The **post-fix code** at the anchor — if any commit after our review modified the line range the comment anchors to, you see the current state of those lines plus a few lines of context above and below.
- The **full PR history** — every conversation comment, every review thread on the PR (including other reviewers'), every commit message on the branch since our review, the current PR description. Cross-thread evidence counts: the author may have addressed *this* concern in a reply on *another* thread.
- The **bundle context** — for each linked PR (cap 5): diff, description, top-level conversation. A frontend concern may be addressed by a commit landing in the linked backend PR.
- **Pushback history** — whether we have already posted a pushback reply on this thread.

## Disposition (return exactly one)

- **`addressed-by-fix`** — A commit after our review modified the line range and the modification removes the concrete failure mode our comment raised. Verify against the post-fix code: trace the original problem; check that the current code no longer exhibits it. A change that touches the lines but doesn't address the underlying concern is NOT addressed-by-fix.
- **`addressed-by-valid-reply`** — The author replied on this or another thread with an argument that fairly defeats our concern (correct factual context we were missing, a deliberate design choice with valid rationale, an out-of-scope acknowledgment we should accept, the concern being already addressed by code elsewhere we hadn't seen). "Valid" means a fair-minded human reviewer would concede. The author's tone is irrelevant — only the substance of the argument.
- **`needs-our-pushback`** — Neither of the above. The author has not addressed the concern via commit, and either has not replied or has replied with an argument that doesn't actually defeat the concern (dismissal without rebuttal, restating the original code, agreeing-to-disagree without engaging the substance).

## Pushback draft (only on `needs-our-pushback`)

If pushback history says we have already posted a pushback reply on this thread, **do not draft another** — return `needs-our-pushback` with `drop: true` so the caller silently drops the thread. **One round of pushback per thread, total.**

Otherwise load `VOICE.md` and draft a short thread-reply body in that voice. Stay on the specific point under contention; do not restate the original concern in full; address whatever the author actually said (or didn't say). The reply is posted as a thread reply on the existing comment, not a new review.

## Output

Return per comment:

```
disposition: addressed-by-fix | addressed-by-valid-reply | needs-our-pushback
drop: true | false   # only meaningful when disposition is needs-our-pushback
reply_body: "..."    # only present when disposition is needs-our-pushback AND drop is false
rationale: "..."     # one short line — what the deciding evidence was
```

The rationale field is for the caller's loop summary at exit, not for posting.
