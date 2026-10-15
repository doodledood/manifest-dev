# ADR: The promise includes a codebase that gets easier to change correctly

## Status
Accepted — amended by [20261015-projects-drive-themselves-as-far-as-each-user-climbs](20261015-projects-drive-themselves-as-far-as-each-user-climbs.md): the bar sentence gains a fourth part, a project that moves forward on its own as far up the autonomy ladder as the user chooses.

## Area
North Star

## Decided by
The user

## Context
The North Star's promise held two halves: output trustworthy enough to ship with minimal review,
and a project that still knows what it is becoming, what is next, and what done means. The
workflow now also turns corrections into checks, pays debt on the path of the next change, and
keeps a verification surface fresh through normal runs, so a codebase it works on is meant to
get easier to change correctly over time. Nothing in the promise said so, and a position changes
only by the owner's ruling.

## Decision
- The Promise's bar sentence gains a third part: "— and find the codebase easier to change
  correctly than when I started."
- *What this rests on* gains the hypothesis that a codebase converges toward one the workflow
  can maintain on its own when every correction becomes a check, debt is paid on the path of the
  next change, and each long-lived artifact keeps a way to verify it that normal runs keep fresh.
  It is unmeasured.

## Alternatives Considered
- **Leave the North Star unchanged until the eval baseline runs**: the convergence goal already
  shapes what the workflow does, so the standing direction would understate it.
- **Add the hypothesis without changing the promise**: the codebase half is something a user
  should hold the project to, not only an assumption it rests on.

## Consequences

### Positive
- A session anchoring on the North Star weighs whether work leaves the codebase easier to change.

### Negative
- The promise grows by a claim no stranger has tested yet.

## Enforced by
none — a position the owner ruled; the North Star informs and never binds.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20260821-positioning-drops-the-conversion-funnel
- Related: 20261013-debt-is-paid-on-the-path-of-work
