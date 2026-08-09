# ADR: Group GitHub tickets by sub-issue membership and an effort label

## Status
Accepted

## Area
Ticketing

## Context

The GitHub venue's tracking issue carried, as "its one piece of native mechanics", a list of the open tickets with their edges in priority order, from which a closed ticket's line is deleted at close. The ticket convention forbids derivable state in a front file — "anything a close would stale belongs to the tickets themselves, where it can't rot" — and then carves an exception for exactly this list. The list is hand-maintained: it asserts nothing the issues do not, and a missed deletion stales it.

Separately, efforts had no marker GitHub could filter or enumerate on, so an effort's issues could not be pulled out of a repository's issue list, and a skill answering "what should I work on" had no way to discover which efforts existed.

## Decision

Effort membership is carried by GitHub's native sub-issue relation, with the effort's tracking issue as the parent. Every ticket additionally carries an `effort:<slug>` label and a kind label (`shaped` / `question`); the tracking issue carries an `effort` kind label of its own rather than being identified by the absence of one.

The hand-maintained open list retires, and the convention's front-file carve-out retires with it. The tracking issue reduces to front-file content — destination, priority override, context pointers — plus the child list GitHub maintains, in which closed tickets remain visible as progress rather than having their line deleted.

Because GitHub gives an issue one parent, the sub-issue relation is spent on membership. Dependencies stay where they already are: the canonical `Depends on: #N` line on the blocked ticket, alongside native blocked-by relations where the repository has them, which are a separate mechanism and so cost nothing.

The label's justification is **discovery, not filtering**. Using the parent relation requires already knowing which tracking issue to open, whereas one open-issues query returns labels attached to every ticket and thereby names every effort in play from a cold start.

## Alternatives Considered

- **Keep the hand-maintained open list**: leave the carve-out standing — Rejected: it asserts nothing the issues don't, and every close requires an edit whose omission silently stales the front file.
- **Effort label only, with no tracking issue**: let the label carry grouping alone — Rejected: the front file has to live somewhere, and the native child list supplies per-effort progress for free.
- **Keep sub-issues as an alternate rendering of dependencies**, as previously specified — Rejected: an issue has one parent, and membership has no equally good alternative rendering, while dependencies already have a canonical body line and a separate native relation.
- **Delete a ticket's entry at close, inside the tracker**: mirror the file store's roll-off — Rejected: the roll-off rule protects the open-set read, which `is:open label:effort:<slug>` still satisfies; a progress view is not that read.

## Consequences

### Positive
- Grouping is maintained by GitHub rather than by hand, and cannot go stale at a close.
- Efforts are enumerable from a single open-issues query, with no index to keep.
- Each effort shows its own progress, including finished work.

### Negative
- A long-running effort's child list grows with its closed tickets.
- Two markers — the parent relation and the label — describe one relationship, so hand editing can put them out of step.

## Source
- Session: figure-out on ticketing-skills feedback (2026-08-09)
- Related: 20260806-retire-decision-map-for-ticket-up-and-ticket-store
