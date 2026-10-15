# ADR: Ask-first marks cost, not slowness

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
20261014-one-verification-harness-per-project gave ask-first four reasons: money or quota, long
run time, load on shared environments, and effects outside the repository. Long run time was
defined against "the project's usual test run". That mixes up slow and costly. A slow check
that costs nothing then waits for a person, so it runs less and hides creep. And because the
threshold is relative to the usual test run, a suite that slows down raises its own bar.

For the owner, the real boundary is limits, budgets and cost. This repository's eval suites
cost money the owner has no budget for, so they must not run without asking. Whether a check
is fast or slow is something the agent should be aware of, not a rule: lint takes seconds and
can run after every edit, and a long suite runs before done.

## Decision
Ask-first marks a recipe whose run costs money or quota, loads shared systems or other teams,
or has effects outside the repository. Run time alone is not a reason. An ask-first recipe runs
only with a person's agreement, which the project's setting, the user in the session, or a
Manifest can carry. Every other check is free: the agent runs it as often as it is useful,
judging from the durations the evidence shows. There are no speed tiers or cadence rules.

## Alternatives Considered
- **Keep long run time as a reason**: a person's yes for slowness does not scale to many agents,
  and slow free checks would run less, which hides creep.
- **Cadence tiers (every edit, once per change, when a person agrees)**: more rules than the
  owner wants. Awareness of duration lets the agent judge.

## Consequences

### Positive
- Slow free checks run without waiting for anyone.
- Ask-first stays rare, so agents can verify most work on their own.

### Negative
- A project that wants a person to approve a merely slow suite has to say so in its own rules.

## Enforced by
partly — `tests/test_verify.py` holds that an ask-first recipe is refused without `--yes`.
Whether a mark's reason is cost stays judgment.

## Source
- Session: figure-out investigation of the verification harness's control, speed and
  confidence, 2026-10-15.
- Related: amends 20261014-one-verification-harness-per-project
