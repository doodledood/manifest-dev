# ADR: next-ticket claims the ticket it picks

## Status
Accepted

## Area
Ticketing

## Context

`next-ticket` ends by offering rather than writing: "**Then offer, don't act.** Offer to claim it for the user (write `Claimed by:`, assign the issue) ... Picking is this skill's whole job; working it is the user's call." The reasoning was that a read should leave no state behind — an unwanted claim is something the user has to undo.

That holds for one worker and fails for several. The convention's readiness predicate already excludes claimed tickets — "open, unclaimed, and every ticket it depends on is done" — so mutual exclusion is fully modelled and only the write is missing. Without it, several sessions asking "what's next" against the same store all derive the same answer, because nothing any of them did changed what the others read. Parallel pickup was an accepted property of the ticket store from the start (20260806 records "Parallel pickup forfeits part of the single-executor learning chain; only structural dependency edges carry ordering"), and it is unreachable while a pick leaves no trace.

The undo cost that motivated the offer is real but small, and asymmetric against what it protects: releasing a claim is one edit, while two workers building the same ticket wastes both.

## Decision

`next-ticket` writes the claim as part of naming the pick — a `Claimed by:` line in a file store, the assignee in a tracker — and reports it as done rather than offering it. What remains an offer is the *work*: executing a shaped ticket, opening a figure-out session for a question ticket, and releasing the claim when this was not the ticket the user wanted.

Claiming is unconditional across venues. Where the venue cannot make the claim visible to other workers, it still records intent for the next reader of that checkout; the skill states what the claim does and does not coordinate rather than implying an exclusion the venue cannot provide.

## Alternatives Considered

- **Keep the offer**: the shipped behavior — Rejected: an offer is a question, and a session with nobody watching never answers it, so parallel and autonomous pickup both collapse into every session picking the same ticket.
- **Claim only when told the session is one of several**: a flag or parallel mode — Rejected: it makes the correct behavior conditional on the caller knowing to ask for it, and the unconditional form is already right for a single worker, where a claim is simply what "I am working this" means.
- **Add a reservation distinct from the claim**: a short-lived lock taken at pick time and converted to a claim when work starts — Rejected: two states where one exists, and the convention's claim already carries exactly this meaning.

## Consequences

### Positive
- Several sessions reading one shared store name different tickets, with no coordination beyond the store itself.
- An autonomous session's pick holds without anyone answering a prompt.

### Negative
- A session that dies mid-ticket leaves a claim nobody released. Recovery stays manual: the convention's tidy pass, and this skill's existing surfacing of claims that look abandoned.
- Someone who ran `next-ticket` only to look now has state to undo.

### Accepted risk
- Two sessions starting within the same pick window can both read a ticket as unclaimed and both claim it — the window is the whole pick, not the write. No reservation protocol is added: collisions are rare in practice, and the cost of one is bounded and visible.

## Source
- Session: figure-out on parallel ticket sessions (2026-08-10)
- Related: 20260806-retire-decision-map-for-ticket-up-and-ticket-store, 20260809-next-ticket-derives-its-pick-instead-of-asking, 20260810-recommend-the-projects-shared-tracker-as-the-ticket-venue
