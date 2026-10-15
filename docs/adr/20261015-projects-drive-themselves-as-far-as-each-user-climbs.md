# ADR: Projects drive themselves as far as each user climbs, and manifest-dev fits inside teams that do not use it

## Status
Accepted

## Area
North Star

## Decided by
The user

## Context
The North Star pictured one quality-first developer at the keyboard of a solo or small-team
project, giving an agent one complex task at a time. The product had moved past that picture:
Tickets carry an Auto grant, unattended runs take one Ticket end to end and ticket up the
follow-ups they find, an escalation mark holds a Ticket for a person, and verification speed
now binds so that many agents working at once are not held up. Nothing in the North Star named
where that leads, and nothing said the workflow fits a team where most people do not use it.
A position changes only by the owner's ruling.

## Decision
- The direction is a project that drives itself wherever it can: agents take work from the
  Ticket store, finish it and ticket up what they find, and people step in only where a run is
  blocked or needs their judgment, taste or authority. *Winning* extends its destination to
  this; its number is unchanged.
- Adoption is an autonomy ladder: one skill on its own, one piece of work understood, defined
  and verified, a project that keeps its direction, vocabulary, decisions and checks, a shared
  queue of work, and unattended runs that take work from that queue. Each level works without
  the ones above it and without anyone else on the team. *How they arrive* says so.
- *Who it's for* widens from solo or small-team developers to developers in a team of any size,
  including existing codebases where most colleagues do not use manifest-dev.
- The *Promise* gains a part for the top of the ladder: as far up as the user chooses to go,
  the project moves forward on its own and asks them only for judgment, taste or authority.
- *Never* gains a boundary: requiring anyone else to adopt it. What a user adds to a shared
  repository reads as plain files and plain instructions, and stops no colleague who does not
  use it from working as they did.
- *What this rests on* gains the hypothesis that gates carrying evidence can stand in for a
  person reviewing each change, wherever no one's judgment, taste or authority is needed.
- *Open* gains what the owner left unruled: which count tracks the self-driving part of
  winning, whether the cost boundary becomes cost per unit of merged value at scale, what keeps
  a self-feeding queue from growing on low-value work, and whether manifest-dev ships the
  orchestrator or stays the protocol any orchestrator drives.

## Alternatives Considered
- **Make the self-driving system the product's identity**: it would read as a requirement to
  adopt every level, which contradicts the standalone shape and excludes a user who works alone
  inside a team that does not use the workflow.
- **Keep the North Star at one task and one person, and let the ticket workflows speak for
  themselves**: sessions anchoring on the North Star would keep weighing work against a picture
  the product has left, and the divergence would stay invisible because no single session
  contradicts it.

## Consequences

### Positive
- A session weighs work against where the project is going, including unattended runs, without
  treating any level as required.
- The open questions that decide the self-driving part are written down with what would settle
  them.

### Negative
- The Promise grows by a part no project has yet met at volume.
- What setup writes into a shared context file has not yet been checked against the new Never.

## Enforced by
none — positions the owner ruled; the North Star informs and never binds.

## Source
- Session: discussion of whether the North Star still matched the owner's direction, held while
  adding a help skill.
- Related: amends 20261013-the-promise-includes-a-codebase-that-gets-easier-to-change
- Related: amends 20260821-positioning-drops-the-conversion-funnel
- Related: amends 20260821-winning-is-our-own-projects-running-the-full-loop
- Related: 20261015-verification-speed-binds-like-cost-second-to-quality
