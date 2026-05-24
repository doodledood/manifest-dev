# --loop mode

Bypass the approval gate entirely — initial post and every rerun run autonomously. The user kicks off /review-pr --loop and walks away.

## Initial post + watch

Run the default pipeline (resolve inputs → fleet → holistic pass → submit `comment` review), but skip the approval gate. After posting, wait between checks with escalating intervals (~15 min → 2 hours). If the harness delivers PR activity events that wake the session, subscribe so a commit push or thread reply resolves the wait early; otherwise blocking `sleep`. At the end of each round, advance the verifier.

## Per-comment verifier (each wake)

For every comment we posted that is still pending (not yet judged resolved), spawn one verifier subagent. The subagent receives:

- The **original finding** — what we posted (anchor, body, the concrete concern).
- The **author's reply on this thread** — every reply on this specific review-comment thread since we posted, if any.
- The **post-fix code** at the anchor — if any commit after our review modified the line range, the current state of those lines plus a few lines of context above and below.
- The **full PR history** — every conversation comment, every review thread on the PR (including other reviewers'), every commit message on the branch since our review, the current PR description. Cross-thread evidence counts: the author may have addressed *this* concern in a reply on *another* thread.
- The **bundle context** — for each linked PR (≤5): diff, description, top-level conversation. A frontend concern may be addressed by a commit landing in the linked backend PR.
- The **voice profile** from SKILL.md — for drafting replies.
- The **pushback history** — whether we have already posted a pushback reply on this thread.

The subagent returns exactly one disposition:

- **`addressed-by-fix`** — A commit after our review modified the line range AND the modification removes the concrete failure mode our comment raised. Verify against the post-fix code: trace the original problem; check that the current code no longer exhibits it. Lines touched without addressing the underlying concern do NOT qualify. **Mark the comment resolved.**
- **`addressed-by-valid-reply`** — The author replied (on this or another thread) with an argument that fairly defeats our concern: correct factual context we missed, a deliberate design choice with valid rationale, an out-of-scope acknowledgment to accept, or the concern being already addressed by code elsewhere we hadn't seen. "Valid" means a fair-minded human reviewer would concede. Tone is irrelevant. **Mark the comment resolved.**
- **`needs-our-pushback`** — Neither of the above. The author hasn't addressed the concern via commit and either hasn't replied or has replied with an argument that doesn't defeat the concern (dismissal without rebuttal, restating the code, agreeing-to-disagree without engaging substance). **If `drop: false`, post the drafted reply on the existing thread; if `drop: true`, silently drop the thread.**

## Pushback drafting and the one-round rule

If pushback history says we have already posted a pushback reply on this thread, the verifier returns with `drop: true`. **One round of pushback per thread, total** — no comment wars.

Otherwise the verifier drafts a short thread-reply body in the SKILL.md voice profile. Stay on the specific point under contention; don't restate the original concern in full; address whatever the author actually said (or didn't say). The reply is posted as a thread reply on the existing comment, **not** a new review.

After acting on this wake's dispositions, if any comments remain pending, advance to the next wait interval and wait again.

## Success path: rerun on full resolution

When every comment is resolved (by fix, valid reply, or one-round pushback that ended in a drop), rerun the full pipeline (default mode in SKILL.md) on the new PR state. Reset to the shortest wait interval for the new cycle.

## Termini (first to fire wins)

1. Clean rerun returns no surviving findings → run the SKILL.md lgtm prompt. Approve → submit `approve` review with body `Looks good to me.`, exit. Decline → exit silent.
2. **3 cycles total** (initial post + 2 reruns).
3. **24h wall-clock backstop** from initial post.
4. The longest wait interval (~2h) elapses with comments still pending.

On (2), (3), or (4): silent unsubscribe from PR activity if subscribed + chat summary to the user (which cycles completed, which comments remain unaddressed, which dispositions were applied). **Never post a bump comment on the PR** — the cap is "I'm done watching," not "I escalate."
