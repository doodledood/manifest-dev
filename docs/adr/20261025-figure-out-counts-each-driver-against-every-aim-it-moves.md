# ADR: figure-out's decision probes count each driver against every aim it moves

## Status
Accepted

## Area
Task guidance

## Decided by
The user

## Context

figure-out presses one branch at a time, parent before child. In a decision, that order also
fences factors off: a factor judged under one aim is not carried to another aim it moves.

In an observed session on how to vote, the user said the economy mattered most and took
security first. figure-out marked the parties' settlement and annexation positions as a low
weight under security, then judged the economy on the tax and housing platforms alone. It never
counted what settlement building and annexation cost the economy until the user raised it.

In-session simulations of that conversation and of a product choice, graded blind by two
graders per batch (two replies per variant; not eval-suite results):

- Vote case: with no drivers line, no reply counted the economic effects of the settlement
  positions (0 of 6); with a drivers line, in each placement tried, every reply did (8 of 8).
  With the line in `tasks/DECISION.md`, 2 of 2.
- Product case (support's warning that users would not find how to connect data, against the
  activation goal of connecting data): with a drivers line, 8 of 8 linked the two; without, 3 of
  4.
- Small decision (`64`): the line in `DECISION.md` passed the repository's rubric in 1 of 2
  replies, against 2 of 2 for the same prompt without it; a line in `SKILL.md`'s spine made small
  asks about as heavy.

## Decision

Add a *Drivers across branches* probe to `figure-out/tasks/DECISION.md`, before *States of the
world*: before judging options against one aim, ask what drives that aim — second-order effects
and factors the session filed under another branch included — how each option reaches it,
roughly how large each effect is next to the others, and count each factor against every aim it
moves. `DECISION.md` now carries 14 blind-spot probes. `86-decision-driver-in-another-branch`
is its eval case.

## Alternatives Considered

- **A causal-model line in `SKILL.md`'s spine**: fixed the vote case 2 of 2 and reaches every
  topic — rejected because it made small asks heavier, needed a depth-by-stakes line beside it to
  offset that, and no tested code or design case showed the miss it would add.
- **A "who else must say yes" probe** (whose agreement, capacity or rules an option needs): no
  gain in simulation, at the first turn or the second — not added.
- **Wording that walks how a vote becomes policy** (seats, threshold, coalition): no gain —
  not added. That gap stays open.

## Consequences

### Positive
- Decision reads count a factor once per aim it moves, including factors met earlier under
  another branch.

### Negative
- The probe loads only with `DECISION.md`; a fenced-off factor in a code, design or diagnosis
  inquiry gets no prompt.
- On a small decision the probe can add analysis the choice does not need.

## Enforced by
partly — `86-decision-driver-in-another-branch/counts-the-driver-from-another-branch` in the figure-out eval suite; whether a factor reaches an aim stays judgment

## Revisit when
A session or eval case shows figure-out fencing a factor off between branches in code, design or diagnosis work, where `DECISION.md` does not load — read in figure-out logs and the suite README's results.

## Source
- Session: a figure-out investigation and `/auto` run on figure-out's question quality, 2026-10-25; simulation batches and blind keys kept outside the repository.
- Related: 20261019-figure-out-probes-decisions-and-plans-under-uncertain-futures
- Related: 20261025-figure-out-re-derives-only-reads-that-are-costly-to-get-wrong
