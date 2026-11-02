# ADR: The convergence bet counts debt paid on the change that meets it

## Status
Accepted

## Area
Positioning

## Decided by
The user

## Context
The North Star bets that a codebase converges toward one the workflow can maintain on its own
"when every correction becomes a check, debt is paid on the path of the next change, and each
long-lived artifact keeps a way to verify it". The middle clause described a workflow that
recorded what a run met and left it for a later change to pay.

20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges makes `/do` fix
the pre-existing issues its work meets on the change that meets them, related or not, and leave as
debt only what is a project of its own, needs a person, or a project's own rules keep out. Debt is
still paid on the path of later changes, but most of it no longer waits for one. The bet's wording
named a mechanism the workflow no longer leans on first.

## Decision
The bet reads: "A codebase converges toward one the workflow can maintain on its own when every
correction becomes a check, each change pays the debt it meets unless the fix is a project of its
own, and each long-lived artifact keeps a way to verify it that normal runs keep fresh." It stays a
hypothesis: nothing has measured it.

## Alternatives Considered
- **Leave the wording as it was**: rejected. It still reads true, but a later session would read
  "the path of the next change" as the place debt waits, which is the rule
  20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges replaced.

## Consequences

### Positive
- The bet names the mechanism the workflow now uses, so a session weighing a change against it
  reads the current rule.

### Negative
- The *How we know* measure still counts "debt paid on the path of later changes"; it reads as a
  subset of what the bet now names until someone measures it.

## Enforced by
none — a North Star position informs and never binds.

## Source
- Related: 20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges
