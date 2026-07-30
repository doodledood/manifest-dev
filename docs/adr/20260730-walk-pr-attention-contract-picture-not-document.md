# ADR: Walk-pr runs on an attention contract — a picture, not a document

## Status
Accepted

## Context
Walk-pr's canvas mode originally specified a document-shaped artifact: a prose PR primer, per-sub-changeset cards with behavior summaries and verification probes, boundary-view paragraphs, and two-sentence topic headlines, all rationed by progressive disclosure. Built faithfully against a large real PR, that artifact failed with its reviewer twice — "way too much text at once" — even after aggressive collapsing. The design that completed a real review inverted the medium: one persistent spatial system map of the PR, a stepped story animated onto it with short captions, review concerns as pins placed where they live on the map, comment-anywhere on every element, rationale and diffs strictly behind taps, and a single end-of-walk bundle. The reviewer's requirement is attention-shaped: high-level visual orientation first, one idea at a time, and digging only when the reviewer chooses.

## Decision
The binding contract for walk-pr is an attention contract, and it applies to every mode, not only canvas: visual/high-level orientation carries the surface, context stays stable, one idea is active at a time, and text, rationale, code, and diffs appear only on explicit request. In canvas mode the artifact is a picture, not a document — the spine is one persistent PR-specific system map with a stepped story, pins, comment-anywhere, an on-demand diff drawer, and a single completion bundle. A sanitized executable HTML reference (fake system, fake concerns, fake diffs — derived from the successful private artifact but leaking none of its content) ships with the skill as the canonical embodiment of that UX: its interaction shell is the default to preserve, while each PR gets its own bespoke map, visual vocabulary, story, pins, and diffs. The shell adapts or yields when a PR's shape genuinely demands a different picture — judged against the same attention contract, never back toward a document. The artifact is generated once and opened immediately: no agent-side preflight browser verification, screenshot pass, or mid-walk regeneration — the reviewer is the first viewer and starts reviewing at once. Canvas mode drops the separate prose primer; the opening map state and early story steps own all orientation. How the HTML is produced is deliberately unspecified.

## Alternatives Considered
- **Keep the card/document contract with more aggressive progressive disclosure**: Collapsing more of the same text — rejected; tried twice against a real reviewer and failed both times.
- **Visual map as default with cards retained as a fallback contract**: Two full presentation contracts plus a routing judgment per PR — rejected; the trivial-diff activation gate already routes small changes to chat, and a substantial diff always has a drawable structure, so the fallback protects a case that barely exists while keeping a falsified presentation sanctioned.
- **Prose-only spec, no shipped reference artifact**: Rejected; prose interpretation drifts, and with UX as a primary requirement the interaction grammar must be preserved by executable example, not description.
- **Ship a shared generator/schema for producing canvases**: Rejected; a fixed map schema pushes every PR toward the same topology and adds a runtime dependency. Only the resulting HTML matters.
- **Mandatory real-browser verification before handover**: Rejected by the user; the canvas optimizes time-to-first-review, and reliability is carried by the stable reference shell instead.

## Consequences

### Positive
- Future canvases inherit a user-validated review UX instead of re-deriving it from prose.
- ADHD-compatible review by construction: orientation is visual, depth is opt-in, and no unrequested text wall can appear.
- Chat mode and canvas mode share one principle, so the walk feels the same in spirit regardless of medium.
- No generator or runtime dependency; the skill stays portable across harnesses.

### Negative
- The sanitized reference HTML becomes maintained product code; interaction regressions in it ship silently since there is no preflight verification.
- Reviewers who prefer document-first reading get more taps to reach depth.
- Evidence base is one reviewer and one large PR; the contract generalizes by argument, not by measurement.

## Source
- Session: figure-out session reworking `walk-pr/references/CANVAS_MODE.md` (2026-07-30), continuing a handoff from the walk of a large private PR whose approved artifact defined the reference UX.
- Related: 20260730-walk-pr-triages-before-drafting-comments
