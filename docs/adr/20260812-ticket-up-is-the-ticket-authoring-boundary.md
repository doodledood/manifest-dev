# ADR: ticket-up is the single Ticket-authoring boundary

## Status
Accepted

## Area
Ticketing

## Context

`ticket-up` originally accepted only a finished Manifest. Figure-out wrote Question Tickets directly, and an automated Ticket run needed a way to record separate follow-up work. Letting each caller author venue items itself would duplicate the Ticket convention, store configuration, labels, effort membership, dependency mapping, deduplication, and Auto judgment across prompts.

The source material differs, but the authoring obligation does not: every Ticket must become one self-sufficient work packet rendered through the same configured venue.

## Decision

`ticket-up` is the single Ticket-authoring boundary. It accepts a finished Manifest, a direct work request, an independently managed question, or findings linked to a source Ticket.

Callers supply the work and relationship context. `ticket-up` decides the convention-compliant unit and kind, deduplicates against the open store, applies type and Auto rules, preserves effort and structural dependencies, and renders the result through the venue reference. Other skills invoke `ticket-up`; they do not write follow-up or Question Tickets directly.

## Alternatives Considered

- **Keep Manifest-only ticket-up and add a separate follow-up skill**: Gives each source a narrow prompt. — Rejected because both skills would own the same convention and venue mutations.
- **Let every caller write Tickets directly**: Avoids another skill invocation. — Rejected because authoring rules would drift and no single boundary could enforce deduplication or grant propagation.
- **Move Ticket authoring into define**: Gives Manifests a native store output. — Rejected because direct questions and execution findings do not originate in define, and venue mutation remains a separate concern.

## Consequences

### Positive
- Ticket shape, grant logic, and venue rendering have one source of truth.
- New callers can create Tickets without learning tracker-specific operations.
- Follow-up deduplication and source linkage apply consistently.

### Negative
- `ticket-up` supports several input shapes and must distinguish them clearly.
- A caller that already has tracker access still delegates the write through another skill boundary.

## Source
- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260806-retire-decision-map-for-ticket-up-and-ticket-store, 20260810-generate-a-venue-reference-for-an-unmapped-tracker
