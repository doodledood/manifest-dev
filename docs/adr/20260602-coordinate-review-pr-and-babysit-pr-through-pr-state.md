# ADR: Coordinate review-pr and babysit-pr through PR state

## Status
Accepted

## Context

`review-pr` and `babysit-pr` both operate on pull requests, but from opposite sides of the collaboration. `review-pr` is reviewer-side: it inspects a PR, advances its own prior threads, and posts comments a human reviewer would stand behind. `babysit-pr` is author-side: it tends an existing PR through CI, review threads, description sync, and mergeability without pressing merge.

The design question is whether these two skills should coordinate through a direct private protocol, or whether they should run independently and converge through durable PR state. The motivating product shape is an async pair: one actor applies quality pressure, the other keeps the PR moving toward green and mergeable.

## Decision

`review-pr` and `babysit-pr` are companion PR actors that coordinate only through GitHub PR state and, for author-side work, the Manifest. There is no direct hidden queue, session-memory dependency, or private protocol between them.

`review-pr` owns reviewer-side behavior: review range selection, prior-thread advancement, comment posting, and optional human-confirmed approval. It does not become the author-side lifecycle owner.

`babysit-pr` owns author-side lifecycle behavior: CI/review/thread/description/mergeability tending, running the manifest workflow when needed, applying fixes when it has normal author authority, and escalating when the PR needs human judgment or permissions. It never merges, never force-pushes, and never pushes to a base branch.

The shared substrate is the PR itself: commits, checks, comments, review threads, review requests, approvals, and description. The Manifest is the author-side acceptance contract when `babysit-pr` needs one. This makes the pair replayable in CI and safe to run asynchronously.

## Alternatives Considered

- **Direct coordination protocol between `review-pr` and `babysit-pr`**: rejected because hidden state would make runs brittle, non-replayable, and hard to resume in CI. GitHub already provides the durable shared state both actors need.
- **Fold babysitting into `/auto --babysit` and leave `/babysit-pr` as a command printer**: rejected because `babysit-pr` is the user-facing author-side companion to `review-pr`, not just a wrapper that tells the operator to run another command. It should actually run the lifecycle machinery.
- **Treat `review-pr` as a source of approval for `babysit-pr`**: rejected. If both skills run under the same GitHub identity, `review-pr` can be a critic/commenter but not an independent approver for branch-protection semantics. Human or repository policy remains the approval authority.

## Consequences

### Positive

- The two skills can run concurrently or on independent schedules without shared session memory.
- CI usage becomes straightforward: each run reconstructs state from GitHub and the manifest, then advances what it owns.
- The actor boundary is clear: review pressure belongs to `review-pr`; author-side lifecycle tending belongs to `babysit-pr`.
- The model scales to async workflows where reviewers, CI, bots, and the babysitter all make progress through normal PR artifacts.

### Negative

- Coordination latency is bounded by GitHub state refresh and polling cadence, not immediate in-process handoff.
- Some useful cross-actor context may need to be expressed as PR comments, commits, description updates, or manifest amendments rather than hidden memory.
- Same-identity runs cannot provide true independent approval, even if `review-pr` reports clean.

## Source

- Session: `/figure-out --with-docs` session on 2026-06-02.
- Related: `20260518-verifier-fail-hints-are-directives`
