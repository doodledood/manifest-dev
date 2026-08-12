# ADR: Tickets follow independently schedulable work units

## Status
Accepted

## Area
Ticketing

## Context

The first Ticket workflow mapped every Manifest Deliverable to a Ticket and offered to emit every decoupled figure-out question separately. That maximized parallel pickup, but real use produced many Question Tickets that were later processed as one effort merely to avoid answering them manually. The store was reflecting units of thought rather than units anyone wanted to assign, prioritize, or close separately.

A Manifest already defines one coherent end-to-end execution contract. Its Deliverable order carries learning and shared invariants that fragment when each Deliverable becomes a separate lifecycle by default.

## Decision

A Ticket represents one independently schedulable lifecycle unit. Work stays together when it shares one outcome and would be assigned, prioritized, blocked, and closed together.

A finished Manifest becomes one Shaped Ticket by default. A caller may explicitly request delegation or parallel pickup, in which case `ticket-up` splits on the Manifest's existing Deliverable boundaries and preserves structural dependencies.

A separate Question Ticket is created only when the question needs independent assignment, priority, blocking, or closure. Related questions sharing one lifecycle are grouped. The same threshold applies to findings discovered during execution; minor observations stay in the source outcome, while substantial separate work can become a follow-up Ticket.

## Alternatives Considered

- **One Ticket per Deliverable by default**: Maximizes parallel delegation. — Rejected as the default because it fragments shared context and creates multiple trigger and lifecycle states for one autonomous run. It remains an explicit mode.
- **One Ticket per question**: Makes every unknown visible. — Rejected because visibility alone does not justify independent scheduling and creates a noisy store.
- **Never split a Manifest**: Preserves coherence absolutely. — Rejected because deliberate delegation remains valuable when Deliverables are genuinely independent vertical slices.

## Consequences

### Positive
- One automated attempt can execute a Manifest as the coherent contract it already is.
- Ticket stores carry less coordination noise.
- Questions and findings become separate work only when separate management has value.

### Negative
- Default Manifest Tickets cannot be claimed or closed per Deliverable.
- Explicit split mode is required to maximize parallel pickup.
- An escalation can keep a whole Manifest Ticket open after some internal Deliverables have landed.

## Source
- Session: unattended Ticket automation design (2026-08-12)
- Narrows: 20260806-retire-decision-map-for-ticket-up-and-ticket-store
- Related: 20260810-shaped-means-the-decision-space-is-closed
