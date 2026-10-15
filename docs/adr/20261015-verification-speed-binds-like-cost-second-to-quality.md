# ADR: Verification speed binds like cost, second to quality

## Status
Accepted

## Area
Positioning

## Decided by
The user

## Context
The North Star's Never list makes cost a binding constraint, second to quality
(20260820-cost-is-a-binding-constraint-second-to-quality), and names speed only as
something quality is never traded for. Nothing stated that speed is a requirement in its own
right, and the shipped workflow reflected that. The verification harness treats a long run
only as a reason to ask a person first. `/do` re-runs every deterministic gate in full after
each repair, so one slow check costs its full time in every repair round. And no run measures
how long verification takes, so a slowdown stays invisible until it dominates.

The owner's own projects show the result. A test suite slowed a little with each change
until it became the main bottleneck, and getting it back down took a dedicated effort, more
than once. This repository shows the same shape: its property suite takes 94 s run serially,
mostly spent waiting, and about 30 s with four workers, with identical results.

The owner wants to run many agents at once on a project. At that scale the round time of each
run bounds throughput, and the verification step is most of a round. This sits inside the
Diagnosis rather than against it: speed here makes establishing what done means cheap enough
to repeat on every round, and it is never bought by doing less of it.

## Decision
Verification speed is a binding constraint, like cost and second to quality. A run's
verification rounds must stay fast enough that many agents working at once are not held up by
them. Quality stays the deciding axis: a check that runs faster by proving less is not faster,
and nothing trades proof away for time. The North Star's Never entry gains this line. How the
verification harness and the workflow skills hold speed is a separate decision.

## Alternatives Considered
- **Leave speed unstated**: a suite slows a little with each change and nobody notices, until
  a dedicated clean-up is needed. That has already happened more than once.
- **Make speed co-primary with quality**: rejected. A fast check that proves less defeats the
  point of checking, and the promise is output trustworthy enough to ship.
- **State it only in the verification harness's reference**: setup-project and `/do` would
  hold it, but figure-out and define weigh scope and priority against the North Star. Speed
  would be weighed in some calls and not in others.

## Consequences

### Positive
- Scoping and design calls in every session weigh how long a change makes each verification
  round, not only whether the check passes.
- The harness design can treat run time as a requirement with its own measurement, not a cost
  noticed late.

### Negative
- One more constraint to weigh beside quality and cost.
- A run could argue for a weaker check in the name of speed. The rule that speed is second to
  quality is the guard, and a reviewer has to hold it.

## Enforced by
none — a North Star position informs and never binds. The checks that hold verification speed
belong to the verification harness and the gates a Manifest carries.

## Source
- Session: figure-out investigation of the verification harness's control, speed and
  confidence, 2026-10-15.
- Related: amends 20260820-cost-is-a-binding-constraint-second-to-quality
