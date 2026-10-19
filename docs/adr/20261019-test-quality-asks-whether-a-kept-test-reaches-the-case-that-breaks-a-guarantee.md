# ADR: test-quality asks whether a kept test reaches the case that breaks a guarantee

## Status
Accepted

## Area
Code review

## Decided by
The user

## Context
review-code's test-quality dimension asks whether each test would fail on a contradictory
implementation, and derives the scenarios that should exist from input boundaries, branches, error
triggers, state and transformations. It did not ask about guarantees whose breaking case is an
order of events or a rare input. Such a guarantee — at most one delivery, no lost update — is
usually covered by an example test of one uninterrupted run, which keeps passing when a later
change breaks the guarantee. Race conditions in the code belong to the code-bugs dimension, which
finds a race the code has now; neither dimension asked whether the tests would catch one a later
change brings in.

20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks put that question into
figure-out and define, so a change designed with them plans a check that reaches the case. A
change that skipped that design step — a small Ticket under orchestrate, or any pull request
reviewed without a Manifest — gets only the review. When orchestrate lands work, only the
deterministic gates re-run, so a kept test is what protects a guarantee after the run that made
it.

## Decision
- test-quality considers only a guarantee the change states or evidently relies on, never one
  merely inferable from the code. For such a guarantee that depends on the order of events (two
  writers, a retry, a crash partway through) or claims to hold for every input, it asks whether a
  kept test would fail if a later change broke it. The finding quotes where the change states or relies on it, so reviewers do
  not meet guarantees the author never made.
- Where none would, the finding names three things: the breaking case (the sequence of events or
  the input), a later change that would break the guarantee unseen, and the cheapest kind of check
  that reaches the case, such as a test that drives that sequence, generated inputs or call sequences, or a model of the
  design. Tools appear only as examples. A finding that recommends a technique without naming the
  case is not reported.
- On meaningful logic such a finding is Medium, the same as an untested edge case, so it fails the
  dimension's gate.
- A race the code has now stays with code-bugs; test-quality owns whether the tests would catch the
  guarantee breaking later.

## Alternatives Considered
- **Design time only**: figure-out and define already ask the question — Not chosen: work that
  skips design gets no check, and design sees only the risks anticipated before the code exists.
- **A new review dimension**: keeps the question apart — Not chosen: it would add a gate to every
  coding Manifest for a question that sits at test-quality's boundary with code-bugs.
- **Low severity**: advisory only — Not chosen: the user put confidence above effort, and a finding
  below Medium never fails the gate.

## Consequences

### Positive
- A guarantee no kept test can protect is found on every pull request that runs test-quality,
  with the case and the check that reaches it.

### Negative
- More repair rounds on pull requests where the case is real.
- A finding that names no concrete case would add noise; the rule that it must name one is the
  guard.

## Enforced by
partly — the `test-quality-unreached-guarantee` scenario of `verification/recipes/review-code.md`
drives test-quality on a change whose tests miss the crash-and-resend case; the every-input half is
checked by reading only.

## Source
- Session: figure-out and define on formal verification in manifest-dev's workflow (2026-10-19).
- Related: amends 20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks; see
  also 20261019-define-searches-each-new-manifest-for-a-wrong-result-that-passes-every-gate
