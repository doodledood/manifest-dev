# ADR: Disposable prototypes may expose behavior

## Status
Accepted

## Area
figure-out

## Context

A non-executed prototype cannot demonstrate interaction or pacing. The design skill requires those properties to be observable when they are the subject of judgment.

## Decision

Permit execution of disposable prototypes outside real project files when behavior is being judged. Simulate data and effects where real actions require separate authority. The boundary is product implementation and external authority, not execution itself.

## Alternatives Considered

- Keep prototypes static: excludes the evidence required for interactive work.
- Implement in the product to demonstrate it: commits to a design before agreement.

## Consequences

### Positive

- The prototype can test the property the user must judge.

### Negative

- The run must keep simulated effects separate from real actions.

## Source

- Amends 20260826-prototyping-and-scratch-are-one-mechanism
