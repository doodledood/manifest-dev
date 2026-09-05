# ADR: The invoking run owns design verifier selection

## Status
Accepted

## Area
Design skills

## Context

A design gate required a fresh context even inside explicitly selected self-verification, where launching a verifier is forbidden.

## Decision

A nested design gate uses the invoking run's selected evaluator and records actual provenance. Standalone review of self-authored work prefers a fresh context; unavailable independence is disclosed while the evidence bar remains unchanged.

## Alternatives Considered

- Require independent design gates in every run: makes the supported self mode incompatible with ordinary visual work.
- Drop independence everywhere: loses the standalone reviewer default without resolving a caller policy.

## Consequences

### Positive

- All supported verification modes can evaluate the same artifact contract.

### Negative

- Standalone review can proceed with disclosed weaker provenance when independence is unavailable.

## Source

- Amends 20260901-design-skill-pair-distills-research-eval-deferred
