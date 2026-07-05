# ADR: Use CI one-shot cadence for babysit-pr

## Status
Accepted

## Context

`babysit-pr` is expected to run both interactively and in CI. Interactive runs can reasonably keep tending a PR until it becomes mergeable or hits a real blocker. CI runs have different economics: keeping a runner alive while waiting for reviewers, checks, or bot scanners burns minutes, risks workflow timeouts, and makes concurrency cancellation harder.

At the same time, CI babysitting should be useful. On trusted same-repo PRs with explicit write authority, it should be able to auto-fix, test, commit, and push. On untrusted or unwritable PR heads, it should report actionable blockers instead of mutating state it cannot safely own.

## Decision

`babysit-pr --ci` uses a one-shot cadence: reconstruct PR state and grounding, execute every immediately actionable lifecycle step, then exit. When only wait-shaped blockers remain, it reports a pending wait state and does not execute long sleeps.

CI one-shot mode may mutate the PR only when the head is trusted and writable:

- The runner has normal push permission to the PR head branch.
- The head branch is not a protected/base branch.
- The PR is not an untrusted fork path with privileged secrets.
- The local checkout matches the current PR head SHA before fixing.
- The push is a normal fast-forward branch update; force-push is forbidden.

Interactive babysitting can still use the normal `/do` loop and execute wait/reinvoke directives. CI mode changes cadence, not merge authority: the target remains mergeable, not merged.

## Alternatives Considered

- **Long-running CI babysit loop**: rejected because it wastes runner minutes on external waits, is more likely to time out, and makes overlapping workflow runs harder to reason about.
- **CI comments/status only, never auto-fix**: rejected because trusted same-repo CI with explicit write authority should be able to do the useful author-side work automatically.
- **Separate CI-only babysit skill**: rejected because the grounding and lifecycle rules are the same; only cadence and mutation authority differ.

## Consequences

### Positive

- CI babysitting is event-driven and replayable: pull request events, check events, scheduled workflows, or manual dispatch can each advance state once.
- Trusted same-repo PRs can still receive automatic fixes, commits, and pushes.
- Untrusted or unwritable PRs degrade safely to comments, summaries, or escalation.
- Runner time is spent on work, not sleeping.

### Negative

- Wait resolution depends on a future trigger; without check/review/schedule events, progress can pause.
- `/do` needs a caller overlay for no-wait contexts so wait directives do not automatically sleep.
- Users may need CI concurrency controls to avoid overlapping fixer runs on the same PR.

## Source

- Related: `20260602-coordinate-review-pr-and-babysit-pr-through-pr-state`
- Related: `20260602-make-babysit-pr-manifest-aware-but-manifest-optional`
