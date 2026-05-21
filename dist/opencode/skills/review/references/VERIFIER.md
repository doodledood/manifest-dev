# Per-comment verifier

## Inputs

- **Original finding** — what we posted (anchor, body, the concrete concern).
- **Author's reply on this thread** — every reply on this specific review-comment thread since we posted, if any.
- **Post-fix code** at the anchor — if any commit after our review modified the line range, the current state of those lines plus a few lines of context above and below.
- **Full PR history** — every conversation comment, every review thread (including other reviewers'), every commit message on the branch since our review, the current PR description. Cross-thread evidence counts.
- **Bundle context** — for each linked PR (cap 5): diff, description, top-level conversation. A frontend concern may be addressed by a backend-PR commit.
- **Pushback history** — whether we have already posted a pushback reply on this thread.

## Disposition (return exactly one)

- **`addressed-by-fix`** — A commit after our review modified the line range AND the modification removes the concrete failure mode our comment raised. Verify against the post-fix code; trace the original problem; check it no longer fires. Lines touched without addressing the underlying concern do NOT qualify.
- **`addressed-by-valid-reply`** — The author replied (on this or another thread) with an argument that fairly defeats our concern: correct factual context we missed, a deliberate design choice with valid rationale, an out-of-scope acknowledgment to accept, or the concern being already addressed by code elsewhere we hadn't seen. "Valid" means a fair-minded human reviewer would concede. Tone is irrelevant.
- **`needs-our-pushback`** — Neither of the above. The author hasn't addressed the concern via commit and either hasn't replied or has replied with an argument that doesn't defeat the concern (dismissal without rebuttal, restating the code, agreeing-to-disagree without engaging substance).

## Drafting (on `needs-our-pushback`)

If pushback history says we already posted a pushback reply on this thread, **do not draft another** — return with `drop: true` so the caller silently drops the thread. **One round per thread, total.**

Otherwise load `VOICE.md` and draft a short thread-reply body in that voice. Stay on the specific point under contention; don't restate the original concern in full; address whatever the author actually said (or didn't say).

## Output

```
disposition: addressed-by-fix | addressed-by-valid-reply | needs-our-pushback
drop: true | false
reply_body: "..."
rationale: "..."
```
