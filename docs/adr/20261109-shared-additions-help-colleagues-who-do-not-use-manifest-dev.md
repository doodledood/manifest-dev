# ADR: Shared additions help colleagues who do not use manifest-dev, not only stay out of their way

## Status
Accepted

## Area
Positioning

## Decided by
The user

## Context
The North Star's *Each piece stands alone* principle said: "Shared additions remain plain files
and instructions, so colleagues who do not use manifest-dev keep working as before." It came from
20261015-projects-drive-themselves-as-far-as-each-user-climbs, whose *Never* boundary says what a
user adds to a shared repository "stops no colleague who does not use it from working as they
did." Both state a floor: an addition must not get in a colleague's way.

The owner holds a stronger line. What manifest-dev leaves in a shared project, such as decision
records, the verification harness and the guidance a project keeps for its agents, should be of use
to colleagues who never run it, and to their agents. The owner reports that decision records
and the verification harness, created through manifest-dev runs, were used by colleagues on a
team where most people do not run manifest-dev. The stronger line came up in a figure-out session
about project-owned guidance that steers design, product and architecture work before execution.
That guidance is meant to help every agent on a team, not only manifest-dev's own runs. With only
the floor written, a run would judge such an addition only by whether it gets in the way.

The decision sits inside the North Star's *Purpose*, which names developers "inside a codebase
where most colleagues do not use manifest-dev."

## Decision
The *Each piece stands alone* sentence becomes: "Shared additions remain plain files and
instructions that help colleagues who do not use manifest-dev, and their agents, and never stop
them working as before." The floor stays. The principle now also says what a shared addition is
for.

## Alternatives Considered
- **Leave the floor alone**: not chosen. A shared addition would be judged only by whether it gets
  in a colleague's way, not by whether a colleague's agent can use it.
- **A Taste entry**: not chosen. The owner holds this even when it costs more, which makes it a
  principle, and the North Star is a principle's home. A Taste copy would be a second, weaker copy,
  as 20261102-an-addition-that-costs-every-run-earns-its-place-by-evidence found for the cost line.
- **A line in a product guidance file**: not chosen. A principle the owner holds lives in the North
  Star, and other files cite it rather than restate it.

## Consequences

### Positive
- A shared addition is judged by whether a colleague and their agent can use it without
  manifest-dev, as well as by whether it stays out of their way.

### Negative
- An addition that only manifest-dev's own runs can read needs a reason to live in shared files.

## Enforced by
none — a North Star position informs and never binds.

## Source
- Session: a figure-out session, 2026-11-09 (log kept locally).
- Related: amends 20261015-projects-drive-themselves-as-far-as-each-user-climbs; see also 20261023-projects-advance-toward-assigned-outcomes-within-delegated-authority
