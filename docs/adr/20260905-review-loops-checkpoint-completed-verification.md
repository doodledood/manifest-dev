# ADR: Review loops checkpoint completed verification

## Status
Accepted

## Area
PR lifecycle

## Context

A clean review posts no GitHub review, so durable review metadata cannot record that head as checked. Using only that metadata on later loop wakes can repeat a clean pass or prevent completion.

## Decision

Keep a completed-verification checkpoint within the current invocation, including clean passes. Later wakes use it for range and freshness while refreshing external state. Missing or incomplete checkpoints trigger verification. Fresh explicit invocations still begin from GitHub and verify again. No public checkpoint comment or empty review is posted.

## Alternatives Considered

- Post an empty review after every clean pass: adds public output solely for bookkeeping.
- Use only prior posted review metadata: loses silent verification progress.

## Consequences

### Positive

- A clean pass can finish and an unchanged head need not be repeatedly reviewed.

### Negative

- Checkpoint loss can cause extra verification; it cannot certify an unchecked head.

## Source

- Amends 20260602-coordinate-review-pr-and-babysit-pr-through-pr-state
- Amends 20260816-an-invocation-is-the-signal-to-review-again
