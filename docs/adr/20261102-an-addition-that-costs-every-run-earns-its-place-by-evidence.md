# ADR: An addition that costs every run earns its place by evidence

## Status
Accepted

## Area
Positioning

## Decided by
The user

## Context
The North Star holds that quality decides and that cost and speed bind second to it
(20260820-cost-is-a-binding-constraint-second-to-quality,
20261015-verification-speed-binds-like-cost-second-to-quality). That line says what must never
happen — quality bought away for cost or time. It does not say what an addition owes before it
ships, and the gap shows on additions that run on every use: another agent, a review pass, a
gate. Each is easy to justify by the quality it might add, and each charges every user, on every
run, in tokens and in waiting.

The figure-out seat pass showed it. It added a second fresh context to every read a person will
see, about a third more cost per read, and on one-prompt cases its verdicts moved by no more than
run-to-run noise (`claude-plugins/manifest-dev/evals/README.md`, *Is a seat look worth its
cost — 2026-11-02*). Nothing in the evidence reported cost: drives recorded verdicts and not what
each arm spent, so the question was raised by the owner, not by the evidence. By contrast,
define's journeys gate added one evaluator call and named four real defects the existing gate
missed on the same fixture, a gain shown for its cost.

A workflow that spends without limit on checks that might help is not used: it outruns the
user's budget or makes them wait, and its quality reaches no one.

## Decision
The North Star's *Quality decides* principle gains one sentence: "Anything that adds cost or wait
to every run — another agent, a review pass, a gate — earns its place by a gain shown on
evidence, not by the quality it might add." Quality still decides; this says what deciding on
quality requires of something that costs every run.

## Alternatives Considered
- **A Taste entry stating the same principle**: rejected. It would be a second copy of a ruled
  position, and a weaker one, since a Taste entry is weighed against other calls while a ruled
  principle is not.
- **Leave the principle as it was**: rejected. The seat pass was built on the quality it might
  add, and no session weighed its cost until the owner asked.

## Consequences

### Positive
- A proposed agent, pass or gate is judged by its shown gain against what it adds to each run.
- Before-and-after evidence carries each arm's cost and wall time: `scripts/drive-skill.sh`
  records both in every drive's summary and asks that they be reported beside each verdict.

### Negative
- An addition whose gain shows only in conditions no case reproduces waits until a case does.

## Enforced by
none — a North Star position informs and never binds. The drive summary's cost and wall time
(`tests/test_drive_scripts.py`, `test_a_drive_summary_carries_the_sessions_cost_and_wall_time`)
make the evidence the principle asks for visible.

## Source
- Related: amends 20260820-cost-is-a-binding-constraint-second-to-quality
