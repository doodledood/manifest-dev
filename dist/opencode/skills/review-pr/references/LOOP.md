# --loop mode

`--loop` is scheduling around the SKILL.md one-shot pass, not a separate review brain.

Bypass interactive approval prompts. Run one full one-shot pass immediately: advance our existing threads, review the relevant range, post comments/replies/resolutions, and record what happened from GitHub state. Then watch for PR activity or wait with backoff and run the same one-shot pass again.

## Watch Cadence

After each pass, wait between checks with escalating intervals (~15 min -> 2 hours). If the harness exposes PR activity wakeups, subscribe so a commit push or thread reply resolves the wait early; otherwise use blocking `sleep`. Each wake runs the SKILL.md one-shot pass from scratch, deriving current head, our prior reviewed head, pending threads, and author replies from GitHub state.

## Success Path

Exit when a one-shot pass reports:

- all threads we authored or replied to are terminal,
- the current head has no unreviewed range since our latest review,
- the latest one-shot review produced no surviving findings.

Exit clean without posting an approval. `--loop` bypasses interactive approval prompts; an approval review requires an explicit operator request outside the loop.

## Termini

First to fire wins:

1. Clean one-shot pass on the latest head.
2. **24h wall-clock backstop** from initial post.
3. The longest wait interval (~2h) elapses with our comments still pending and no new PR activity.

On (2) or (3): silent unsubscribe from PR activity if subscribed + chat summary to the user (latest reviewed head, current head, which comments remain unaddressed, which dispositions were applied). **Never post a bump comment on the PR** — the cap is "I'm done watching," not "I escalate."
