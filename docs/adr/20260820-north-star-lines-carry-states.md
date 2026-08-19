# ADR: North Star lines carry four states, and positions move only on the owner's ruling

## Status
Accepted

## Area
North Star

## Context
A strategy doc read by every session steers wrong the moment a guess reads as settled fact — worse than not steering, because nothing prompts anyone to check a line that looks settled. Three behaviors force an explicit, movable marker that is not the position's own prose: `init-context` seeds fields from a README without inventing, so seeded content must read as unconfirmed; sessions encounter evidence that weakens a stated field and need a way to register it without rewriting the owner's words; and unattended runs must never flip a position on their own.

A first three-state draft (evidence / hypothesis / empty) mislabeled on first use: a deliberate choice ("free, no monetization intended") was marked `evidence`, and a form that calls both a measurement and a ruling "evidence" cannot say which lines new data could ever move.

## Decision
Every North Star line carries one of four states, rendered as a plain provenance line with a date ("— hypothesis: matches ourselves (n=1); no stranger has confirmed it. 2026-08"):

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — the owner decided it; only the owner moves it.
- **empty** — nobody has answered, written always with what would fill it, never bare.

The update rule is one asymmetry: **statuses move on evidence, positions move only on the owner's ruling.** A session whose finding contradicts a stated field surfaces the clash and the owner rules; on a ruling the field updates and the change is remembered in a decision record — the doc states current truth, records remember why it moved. A finding that is merely unclear may lower a status (evidence → hypothesis, with one line naming what would settle it) but never rewrites a position; unattended runs get the same rule with no ruling path at all — they downgrade or flag, never flip. Fog that fits no field goes to Open or stays out of the doc. Updates are event-driven — a session's finding touching a field, carried by figure-out's docs-mode capture beside glossary and ADR offers — never a review cadence; the dated provenance lines in a resident file are what keep staleness visible.

## Alternatives Considered
- **No marking**: rejected — a hypothesis then reads as fact, and init's seeds masquerade as settled truth.
- **Epistemic register carried in the prose itself** ("we believe, untested, that…"): rejected — an evidence-driven downgrade would then edit the owner's sentences, exactly what the asymmetry forbids, and nothing mechanical distinguishes a settled field from a guessed one.
- **Three states without `ruled`**: rejected — mislabeled a ruling as evidence on first use; choices and world-facts decay differently and are moved by different parties.
- **A review cadence**: rejected — this project avoids cadences, and residency already surfaces stale dates in every session; the accepted residual risk is a field no session touches, kept honest by its visible date.

## Consequences

### Positive
- Seeded and guessed content cannot masquerade as settled; empty fields are a visible to-do list that makes the doc self-orchestrating.
- Unattended runs are safe around strategy: the worst they can do is lower confidence.
- The owner's words are never machine-edited; every position change has a ruling and a record behind it.

### Negative
- A marker per line is apparatus every reader meets; the plain provenance-line rendering is the mitigation.
- Statuses themselves can rot if no session touches strategy for months — accepted, with dates visible on every line.

## Source
- Session: figure-out design session, 2026-08-19–20 (investigation log kept locally).
- Related: 20260820-manifest-dev-owns-a-project-north-star
