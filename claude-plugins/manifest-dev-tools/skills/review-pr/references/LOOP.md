# --loop mode

Bypass the approval gate entirely — initial post and every rerun run autonomously. The user kicks off /review-pr --loop and walks away.

## Initial post + watch

Run the default pipeline on the full PR (resolve inputs -> fleet -> holistic pass -> submit `comment` review), but skip the approval gate. Record the reviewed head as `last-reviewed-sha`. After posting, wait between checks with escalating intervals (~15 min -> 2 hours). If the harness delivers PR activity events that wake the session, subscribe so a commit push or thread reply resolves the wait early; otherwise blocking `sleep`. At the end of each round, advance the verifier.

## Per-comment verifier (each wake)

For every comment we posted that is still pending (not yet judged resolved), spawn one verifier subagent. The subagent receives:

- The **original finding** — what we posted (anchor, body, the concrete concern).
- The **author's reply on this thread** — every reply on this specific review-comment thread since we posted, if any.
- The **post-fix code** at the anchor — if any commit after our review modified the line range, the current state of those lines plus a few lines of context above and below.
- The **full PR history** — every conversation comment, every review thread on the PR (including other reviewers'), every commit message on the branch since our review, the current PR description. Cross-thread evidence counts: the author may have addressed *this* concern in a reply on *another* thread.
- The **bundle context** — for each linked PR (≤5): diff, description, top-level conversation. A frontend concern may be addressed by a commit landing in the linked backend PR.
- The **voice profile** from SKILL.md — for drafting replies.
- The **thread history** — every prior reply we posted on this thread, so the verifier can continue the thread without repeating itself.

The subagent returns exactly one disposition:

- **`addressed-by-fix`** — A commit after our review modified the relevant code AND the modification removes the concrete failure mode our comment raised. Verify against the post-fix code: trace the original problem; check that the current code no longer exhibits it. Lines touched without addressing the underlying concern do NOT qualify. **Resolve the thread.** Straightforward code fixes do not need a reply unless there was active discussion to answer.
- **`addressed-by-valid-reply`** — The author replied (on this or another thread) with an argument that fairly defeats our concern: correct factual context we missed, a deliberate owner trade-off, a valid out-of-scope boundary, or the concern being already addressed by code elsewhere we hadn't seen. "Valid" means a fair-minded human reviewer would concede. Tone is irrelevant. **Draft a short concession/acknowledgment reply, post it, then resolve the thread.**
- **`false-positive-or-stale`** — Our comment was wrong, stale, or based on context the current PR history disproves. **Draft a brief correction that owns the miss, post it, then resolve the thread.**
- **`needs-our-pushback`** — The author replied or changed code, but the concrete concern remains. Draft a short thread reply in the SKILL.md voice profile, post it on the existing thread, and keep the thread pending.
- **`still-pending`** — No relevant new author reply and no relevant code change since the last wake. Keep the thread pending without posting a duplicate reply.

## Thread closure

Keep the thread active until a terminal disposition: fixed in code, fairly rebutted, explicit owner trade-off or out-of-scope boundary, or our own false-positive/stale correction. There is no one-round pushback limit. Push back again when a new author reply or code change still fails to address the concern, but do not post the same pushback again without new signal.

Stay on the specific point under contention; don't restate the original concern in full; address whatever the author actually said or changed. Replies are posted as thread replies on the existing comment, **not** a new review.

After acting on this wake's dispositions, if any comments remain pending, advance to the next wait interval and wait again.

## Success path: incremental rerun

When every comment we posted has a terminal disposition, compare the current head to `last-reviewed-sha`.

- If the head is unchanged, the latest reviewed head is clean. Run the SKILL.md lgtm prompt and exit according to that answer.
- If the head changed, rerun review on the accumulated range `last-reviewed-sha..current-head`. If one commit landed, that range is naturally one commit. If multiple commits landed, review the full range together; do not iterate commit-by-commit.

For incremental reruns, select narrow reviewers from the incremental diff, not from the whole PR. Spawn only reviewers whose lenses are relevant to that range. The holistic pass still receives full PR history, current PR context, bundle context, and the manifest when present, but it may only surface findings introduced or exposed by `last-reviewed-sha..current-head`. If the incremental review posts comments, update `last-reviewed-sha` to `current-head` and reset to the shortest wait interval. If it returns clean, update `last-reviewed-sha` to `current-head` and follow the clean-rerun terminus.

## Termini (first to fire wins)

1. Clean rerun returns no surviving findings → run the SKILL.md lgtm prompt. Approve → submit `approve` review with body `Looks good to me.`, exit. Decline → exit silent.
2. **24h wall-clock backstop** from initial post.
3. The longest wait interval (~2h) elapses with comments still pending and no new PR activity.

On (2) or (3): silent unsubscribe from PR activity if subscribed + chat summary to the user (latest reviewed head, current head, which comments remain unaddressed, which dispositions were applied). **Never post a bump comment on the PR** — the cap is "I'm done watching," not "I escalate."
