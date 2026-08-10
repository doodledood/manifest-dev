# ADR: Retire the decision-map planning shape in favor of ticket-up and a ticket store

## Status
Accepted — venue default narrowed by 20260810-recommend-the-projects-shared-tracker-as-the-ticket-venue

## Area
define / figure-out

## Context

The planning shape shipped as a decision-map: figure-out charted an effort's decisions, define encoded them into a durable map artifact (destination, standing decisions, frontier, fog, rulings) worked over time. Its first real-world use showed the shape serving the wrong half of the problem. Deliberation is serial by nature — parent cruxes resolve before children — so a single deep session tends to settle an effort's decision space in one sitting; the observed map was created with every decision already closed and a frontier holding only small work items, and its standing decisions duplicated ADRs that already existed. Meanwhile the need that motivated a planning shape — decomposing a large, finished understanding into work that several people or agents can execute in parallel, or producing tickets as the deliverable rather than doing the work in-session — had no support: the map convention deliberately kept work items as thin pointers.

## Decision

Retire the decision-map (both PLANNING task files, the map convention reference, and figure-out's map awareness) and serve the work-decomposition need directly with two thin pieces plus one figure-out behavior:

- **ticket-up**: a skill that turns a finished Manifest into one self-sufficient, plain-prose ticket per Deliverable plus explicit structural dependency edges. Knowledge travels (why, scope, binding rules, traps, definition of done); manifest-dev machinery stays behind, so any person or agent can execute a ticket without the toolchain.
- **Ticket store convention**: a venue-neutral contract (kinds, anatomy, lifecycle, claiming, priority) with files-in-repo as the zero-config default, GitHub Issues shipped as a mapped venue, and custom trackers supported from user-supplied details. The `next-ticket` skill answers "what should I work on" as a priority read over any conforming store.
- **figure-out decouple-exit**: when a session's remaining unknowns stop depending on each other, figure-out offers to hand them off as question tickets instead of pressing them serially.

The map's organs dissolve into existing homes: standing decisions were already ADRs; the frontier becomes the store's priority read; fog stays in figure-out logs until statable, then becomes question tickets.

## Alternatives Considered

- **Keep the map, fix only its trigger**: tighten when figure-out offers charting so a one-deliberation effort never gets a map — Rejected: even correctly triggered, the map centers decisions, which are serial and session-sized; the parallelizable, delegable half is work, which the convention deliberately thinned. The trigger was a symptom, not the defect.
- **Do nothing (remove planning, add nothing)**: accept that big efforts run as long figure-out sessions — Rejected: the founding need is real — days-long multiply-compacted sessions, no delegation path, no PM-style ticket output — and unserved by any existing component.
- **Extend /define to emit tickets directly**: fold decomposition into the manifest builder — Rejected: ticket-up's input is a *finished* manifest and its consumers (stores, delegates, other harnesses) differ from define's; a separate thin skill keeps both simple.

## Consequences

### Positive
- Finished understanding can be executed in parallel by agents, teammates, or later sessions, with or without manifest-dev.
- Tickets are implementer-agnostic, so the loop serves a PM-style user whose deliverable is the tickets.
- One less bespoke artifact to steward; decisions live in ADRs, work in tickets.

### Negative
- An effort that genuinely is many long-lived, loosely-coupled decisions worked over time loses its dedicated artifact; if such an effort recurs, this decision should be revisited (the retired convention remains in git history).
- Parallel pickup forfeits part of the single-executor learning chain; only structural dependency edges carry ordering.

## Source
- Manifest: manifest-20260806-181958 (ticket-up + ticket store, planning retirement)
- Related: 20260705-front-figure-out-as-door-define-do-loop-as-house
