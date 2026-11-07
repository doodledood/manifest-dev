---
name: review-pr-thread-verify
description: 'Called by review-pr for each review thread it authored that is unresolved or that someone else resolved: judges from the thread, the author''s replies, and the current code whether the original concern is addressed, stale, or still standing, and returns exactly one disposition with a drafted reply where one is needed. Not for direct use.'
user-invocable: false
---

# review-pr-thread-verify

Decide what has happened to one review finding since we posted it. The caller hands over everything; this skill judges and returns, and never posts, resolves, or edits anything itself.

**Receives.** The original finding (its anchor, body, the commit or head SHA it was reviewed at, and the concrete concern it raised); whether the thread is resolved, and by whom; every author reply on the thread since our last message, plus every prior reply we posted there; the current code at the anchor with nearby context, and any commits since the original review that touched the relevant range; the full PR history (all comments, review threads, commit messages, the current PR description, our prior review and comment bodies); bundle context for each linked PR (diff, description, top-level conversation); for judgment threads, the relevant project direction, decisions and prior recommendation with its grounds; and the caller's voice profile — its rules for how a posted comment reads — to apply to any reply drafted here.

**Judges.** Read the concrete concern first and hold it fixed: the question is whether *that* failure mode is gone, conceded, disproven, or still live — not whether the thread has been discussed. A code change counts only when it touches the relevant range and removes the failure mode; a reply counts only when a fair-minded human reviewer would concede it. Push back only on new signal — a new author reply, a code change, or someone else resolving the thread — and stay on the specific point under contention; never repeat an argument already made on the thread. A resolution is not a fix: when someone else resolved the thread and neither a fix nor a reply answers the concern, it still stands.

For a judgment finding, apply `../review-pr-judgment/SKILL.md` → *What answers a concern*.
A settled trade-off is not necessarily a refuted concern or a favorable recommendation. Return
the current recommendation and its grounds alongside the discussion's disposition; an
acknowledgment preserves a remaining disagreement without repeating the argument.

**Returns exactly one disposition:**

- `addressed-by-fix` — A commit after our review modified the relevant code and removes the concrete failure mode. Straightforward code fixes need no reply unless there was active discussion to answer; draft one only then.
- `addressed-by-valid-reply` — The author replied on this or another thread with an argument a fair-minded human reviewer would concede: correct factual context, an informed trade-off accepted by the applicable authority, a valid out-of-scope boundary, or code elsewhere already covering the concern. Draft a short concession or acknowledgment.
- `false-positive-or-stale` — Our comment was wrong, stale, or is disproven by current PR history. Draft a brief correction that owns the miss.
- `needs-our-pushback` — The author replied, changed code, or someone else resolved the thread, but the concrete concern remains. Draft a short reply for the existing thread on that specific point.
- `still-pending` — The thread is unresolved, with no relevant new author reply and no relevant code change since our last look. Draft nothing.

**Return shape.** The disposition name, one short reason (the evidence: the commit, the reply, or the absence of either), and the drafted reply text when the disposition calls for one, written in the supplied voice profile. For judgment, also return the current recommendation, its grounds and whether the discussion is settled.
