# ADR: next-ticket derives its pick instead of asking

## Status
Accepted

## Area
Ticketing

## Context

`next-ticket` resolved a multi-effort store by asking — "Multiple efforts with stores → ask which". In use that is the wrong move: the user typed the skill's name precisely to be told what to work on, and answering a question with a question hands the work back.

The obstacle is narrower than it looks. Of the convention's four priority terms, urgent compares across efforts by definition, unblocking is a count, and cheap is a count. Only impact does not compare: it is measured against the front file's destination, and destinations are per-effort, so there is no common yardstick.

Discovery is not the obstacle. Both venues already enumerate: `tickets/*/` is the list in a file store, and in GitHub a single open-issues query returns the tickets with their effort labels attached. Only efforts with open tickets need naming, and those arrive with the tickets.

## Decision

A bare `next-ticket` answers without asking.

It starts in the effort already in flight — one holding a claimed or recently closed ticket — because finishing beats starting and this requires nothing to be recorded anywhere. With nothing in flight, it ranks across efforts by reading each front file's destination and judging which matters most now, then applies the normal priority rule inside that effort. It reports which effort it chose and why, so one word of correction redirects it.

No index of efforts is kept, and no ordering of efforts is stored. A store that wants a stable order may state one in its store config; absent that line, the pick is derived.

## Alternatives Considered

- **Ask which effort**: the shipped behavior — Rejected: it returns the decision to the user at the moment they asked to be told.
- **Persist an ordering of efforts**: one line ranking them — Rejected as the default: it is hand-maintained state, the class of problem this session set out to remove. Retained as an optional override for anyone who wants reproducibility.
- **Rank on urgent → unblocking → cheap and drop impact**: keep only the terms that compare — Rejected: mechanically reproducible, but it can surface a well-connected ticket inside an effort that no longer matters.

## Consequences

### Positive
- A bare invocation answers, with nothing to configure or maintain.
- Correction costs one word, because the choice is reported with its reason.

### Negative
- Two runs over an unchanged store can name different efforts. Accepted deliberately; the reported reason is what makes it correctable, and a store that cannot tolerate it can state an order.

## Source
- Session: figure-out on ticketing-skills feedback (2026-08-09)
- Related: 20260806-retire-decision-map-for-ticket-up-and-ticket-store
