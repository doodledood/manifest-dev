# ADR: Generate a venue reference for an unmapped tracker

## Status
Accepted

## Area
Ticketing

## Context

The convention already accepts any tracker: "When the user names any other tracker, ask for the few details the convention needs mapped — how to create an item, set labels/kind, express dependencies, assign, and close — then apply the same convention through those operations. Record those details beside the venue in `tickets/store-config.md`."

Two things are wrong with that shape. **The row set is short.** It names creation, kind, dependencies, assignment, and closing, and omits what the shipped GitHub mapping also covers: what the open-set query is, what readiness means, how efforts are grouped, and where the front file lives. Readiness is the row whose absence matters most now — a store whose record never says what "takeable" means is exactly the store where claiming (20260810-next-ticket-claims-the-ticket-it-picks) silently coordinates nothing. **And the record's home is wrong**: writing a venue manual inline grows `tickets/store-config.md` into the thing the fixed lookup path exists to keep small.

## Decision

When a project's tracker has no shipped mapping, write one. The session asks what it needs and emits a venue reference beside the store config — `tickets/<venue>-store.md` — covering the same rows the shipped GitHub mapping covers, and `tickets/store-config.md` names the venue and points at it.

Say plainly that no mapping ships for this tracker before writing one, so the user knows the mapping is being authored from their answers rather than shipped and exercised — then write it and get on with the work. An unsupported tracker is a mapping to author, not a request to refuse.

## Alternatives Considered

- **Keep the inline detail list**: the shipped behavior — Rejected: its rows are a strict subset of what a venue needs, and it puts a manual inside a pointer.
- **Refuse trackers we do not ship a mapping for**: files and GitHub only — Rejected: the convention's whole claim is that a venue is a rendering and the contract is venue-neutral; a project already running Jira has a store, and telling it otherwise is the tool arguing with the work.
- **Ship mappings for the common trackers**: author Jira, Linear, and the rest up front — Rejected: each is a surface to maintain and verify against an API this project does not run, while one generated reference reaches every tracker including the ones nobody would have shipped. Not foreclosed — a generated mapping that proves itself in use can be promoted to a shipped one.
- **Let each session re-derive the mapping from the user**: no persisted reference — Rejected: it re-asks in every session, and two sessions can answer differently, which is how a store's readiness rule quietly drifts.

## Consequences

### Positive
- Every venue is recorded in one shape, so a later session reads a Jira store the way it reads a GitHub one.
- `tickets/store-config.md` stays a pointer.
- The rows themselves are the interview: a mapping cannot be recorded while readiness or the open-set query is still blank.

### Negative
- A generated mapping is only as good as the user's description of their tracker, and nothing verifies it against the real thing; a wrong row surfaces as a failed operation mid-run rather than at authoring time.
- One more file in `tickets/` for projects on a custom venue.

## Source
- Session: figure-out on parallel ticket sessions (2026-08-10)
- Related: 20260810-recommend-the-projects-shared-tracker-as-the-ticket-venue, 20260809-locate-the-ticket-store-by-convention-not-configuration, 20260809-group-github-tickets-by-sub-issue-membership-and-effort-label
