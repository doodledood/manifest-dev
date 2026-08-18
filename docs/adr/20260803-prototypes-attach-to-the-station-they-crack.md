# ADR: a prototype attaches to the question it was built to crack, and the reaction lands there

## Status
Deprecated — the canvas this bound to was deleted by 20260818-chat-surface-replaces-the-crux-map-canvas; the surviving principle (a reaction is encoded against the question it answers) lives in define's criteria-pinned-by-reaction rule

## Area
figure-out

## Context

figure-out produces disposable artifacts mid-investigation. `SKILL.md`'s one-shot probe covers the case where a criterion exists but cannot be stated: *"offer to make something concrete to react to — a reference to point at, a quick mock, or a few divergent options."* Scratch mode covers a rougher, session-long mirror of understanding. The distinction between them is already drawn: *"here the artifact leads — it generates a criterion not yet settled — where scratch mirrors understanding already reached."*

Today both arrive through chat, and the reaction goes back through chat as free prose. That works while chat is the only surface. Once a canvas exists as a place the user can work in instead of chat, a produced artifact and its request for reaction become invisible there unless the canvas carries them.

There is a downstream reason the reaction's anchor matters. `/define` treats reactions to concrete artifacts as binding: *"Criteria the user pinned by reacting to something concrete during figure-out — a mock, a reference, a chosen direction — are success criteria, not flavor: encode them as an Acceptance Criterion or Global Invariant."* A reaction that arrives detached from the question it answers loses what makes it encodable, and `SKILL.md` warns that reaction-derived criteria bind execution — *"a stray one becomes a gate."*

## Decision

A prototype attaches to the crux or fog patch it was built to crack, and the user's reaction is captured against that same node.

- **The artifact is listed on its node, not announced in a feed.** A node carrying one says so on the map surface, so the picture itself shows where there is something to open. Several artifacts on one question are listed newest-first, since prototypes supersede each other.
- **The reaction box sits with the list**, so the criterion the reaction names travels back labelled with the question it answers, and remains encodable by `/define` as a gate.
- **Links carry a selectable path alongside them**, because `file://` link behaviour varies by browser and a copyable path always works.
- **Session-long artifacts — scratch, the investigation log — do not attach to a node.** They mirror the whole investigation rather than one question, so they belong in the header, reached through the same detail surface against a session pseudo-node. No new surface is introduced for them.
- **The canvas points at prototypes; it never hosts or becomes one.** The canvas mirrors understanding already reached; a prototype leads, by generating a criterion that does not exist yet. They are opposite kinds of object, and the distinction is the same one `SCRATCH.md` already draws.
- **When the two compete for a turn, the prototype wins.** A prototype produces a criterion the session does not have; a canvas update re-renders what it does. A turn that owes a prototype skips the canvas update.

## Alternatives Considered

- **Keep prototypes in chat only**: Rejected — it defeats the reason the canvas exists. A user working in the artifact would see neither the prototype nor the request to react to it, which is the exact failure mode the canvas was built to remove for turn content.
- **Embed the prototype inside the canvas** (iframe or inline): Rejected on two grounds — `file://` subresource loading is unreliable, and it collapses the mirror/leader distinction, producing the degenerate case of a canvas embedding a canvas.
- **A separate artifacts tray or panel**: Rejected — a new surface for something the existing detail surface already renders, and it would divorce the artifact from the question it exists to answer, which is the part that has to survive.
- **Attach everything to the session header, nothing to nodes**: Rejected — it loses the anchor. An unlabelled reaction is what stops `/define` from encoding it as a gate.

## Consequences

### Positive
- A reaction arrives already attached to the question it answers, which is what makes it encodable as an acceptance gate rather than loose commentary.
- The map shows where produced work lives, so nothing the session built is discoverable only by scrolling chat history.
- Reusing the detail surface for session artifacts adds a capability without adding a surface.

### Negative
- Prototypes now have a required home, so a probe produced for no particular question has nowhere natural to sit — an acceptable pressure, since a probe with no question behind it is suspect anyway.
- Superseded prototypes accumulate on a node across a long session, and nothing prunes them.
- The prototype-beats-canvas priority is stated but unmeasured; if canvas updates start being skipped routinely, the canvas is costing more than it returns and that is the signal to reopen it.

## Source
- Origin: figure-out investigation of how prototypes remain visible and encodable when a canvas is active (2026-08-03).
- Related: 20260803-figure-out-gains-an-optional-canvas
- Related: 20260714-figure-out-challenge-solution-existence-before-design
