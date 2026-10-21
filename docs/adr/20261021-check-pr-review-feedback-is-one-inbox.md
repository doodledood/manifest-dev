# ADR: check-pr's third gate is the review-feedback inbox

## Status
Accepted

## Area
PR lifecycle

## Decided by
The user

## Context
`check-pr` reported a pull request ready once every open review thread was addressed. A
reviewer who put asks in a `CHANGES_REQUESTED` or `COMMENTED` review body, or in a top-level
PR comment, never failed that gate. After the threads cleared, Mergeable failed on
`CHANGES_REQUESTED` and emitted `re-request-review` while those asks were still open.
`review-pr` already writes summary headers and PR-level findings into that hole, so the
author-side companion could talk past itself. Issue #360 named the hole. This sits inside
the North Star's Purpose: agents that tend a pull request need the inspection to see the
asks a reviewer actually left.

## Decision
`check-pr`'s third canonical gate is **Review feedback addressed** — one inbox, not a
thread-only gate plus a sibling. The inbox is open review threads, non-empty bodies of each
author's latest submitted `CHANGES_REQUESTED` or `COMMENTED` review, inbound human top-level
PR comments, and comments stamped `<!-- manifest-dev:review-pr -->`. Empty, pending,
dismissed, and superseded reviews are out; `APPROVED` bodies are out; unthreaded GitHub-App
IssueComments are out.

A thread is addressed when it is resolved, replied to, or addressed by a follow-up commit on
the current head. A review body or top-level comment is addressed when the PR author has
later replied on the Conversation, the review is dismissed, or a newer submitted review from
the same reviewer supersedes it. A follow-up commit does not address a body or comment.

`reply` / `reply-and-resolve` still name a review-thread GraphQL ID. Unthreaded items FAIL as
prose findings that name every outstanding item. No new vocabulary token. The synthesized
lifecycle Subject in `define/tasks/PR_LIFECYCLE.md` enumerates the same inbox.

## Alternatives Considered
- **A sixth "Comments addressed" gate**: keeps thread tokens and unthreaded prose on
  separate Suggested lines — Rejected: two gates for one author-side job, and a minor
  version for a coverage hole; mixed FAILs use prose Suggested that names every outstanding
  item, with thread ids in Context.
- **"Since the last head" as the body's addressing signal**: quieter after every push —
  Rejected: thread-fixing commits would clear the motivating body without answering it.
- **Include non-empty `APPROVED` bodies**: catches approve-with-nits in the summary —
  Rejected: nags on LGTM; approval is Mergeable's problem.
- **Surface unthreaded GitHub-App IssueComments**: closes App-only asks —
  Rejected: status-comment loops in a stateless inspector; bot nits that arrive as threads
  still hit the gate.
- **A `comment <id>` / overloaded `reply` token**: literal dispatch for Conversation
  replies — Rejected: ADR 20260518, new scenarios use prose.

## Consequences

### Positive
- A `CHANGES_REQUESTED` body or a top-level ask fails the same gate as an open thread.
- `review-pr` summary headers and PR-level findings become visible to the author-side
  inspector without a private protocol.
- The vocabulary stays six tokens; Codex, Cursor, OpenCode and Pi all read the same source
  gate (Codex via the existing dist copy).

### Negative
- Mixed thread-plus-body FAILs lose a bare `reply PRRT_…` Suggested line; the caller reads
  prose that still names the thread id.
- Approve-with-nits-only-in-the-summary, and App asks that never become threads, stay
  invisible.

## Enforced by
partly — `tests/test_check_pr_feedback_gate.py` — fails if gate 3 loses review bodies or
top-level comments, if `reply` / `reply-and-resolve` drop the review-thread GraphQL ID
requirement, if an `APPROVED` body or unthreaded GitHub-App IssueComment is required as
outstanding, or if `define/tasks/PR_LIFECYCLE.md`'s lifecycle Subject no longer names review
bodies and top-level comments; that Suggested is prose naming every outstanding unthreaded
item, and that `/do` acts on that prose, stay judgment.

## Source
- Session: unattended `/auto` on https://github.com/doodledood/manifest-dev/issues/360
- Related: See also 20260518-verifier-fail-hints-are-directives, 20260602-coordinate-review-pr-and-babysit-pr-through-pr-state, 20260602-deliberate-on-pr-review-comments-at-the-caller, 20260622-mark-review-pr-comments-with-hidden-marker
