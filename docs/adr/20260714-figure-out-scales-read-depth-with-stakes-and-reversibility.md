# ADR: figure-out scales read depth with stakes and reversibility, not fog alone

## Status
Accepted

## Context

`figure-out`'s investigative depth has a single dial: "All of this scales with the fog actually present" (`## Naming the read`). That is epistemic proportionality only. Senior-practitioner judgment adds a consequence axis — the one-way-door/two-way-door instinct: a read whose consequences are costly or impossible to unwind gets scouted harder even when fog looks light, while a cheap-to-reverse call can be named earlier at an honestly lower confidence, because further investigation costs more than being wrong would.

Because the fog-scaling sentence explicitly occupies the proportionality slot, models do not graft the stakes axis on by themselves. The change carries a real hazard: carelessly worded, "cheap to reverse → earlier read" becomes the sentence a motivated model cites to skip an inconvenient crumb or discount its claimed confidence — an attack on the skill's core quality-over-speed ethos.

## Decision

Extend the scaling sentence in `## Naming the read` so the depth dial takes two inputs — the fog actually present, and what rides on the read (how costly or hard to unwind acting on it would be) — with the closing "discipline bites where..." clause extended to match.

Binding guards in the wording:

- **Stakes move effort, never confidence semantics.** The high-stakes side prescribes wider scouting of no-crumb fog before naming — it never demands or fabricates a confidence floor. The cheap-to-reverse side permits an earlier read only "at the lower confidence the remaining fog imposes": confidence stays coupled to unresolved fog exactly as the evidence discipline demands.
- **Crumb closure stays absolute.** An open crumb closes before any read, at every stake — stated explicitly so reversibility cannot be cited as a crumb waiver.
- **Symmetric ceremony guard.** The earlier-read permission for reversible calls is legitimized as honest work, so quality-over-speed is not misread as always-maximal depth; the retained "not as ceremony" clause keeps stakes from ratcheting everything to maximum.
- **Domain-neutral subject.** "Acting on the read" covers a code migration, a public commitment, an org decision, or a published claim — reads that are diagnoses rather than decisions included.

## Alternatives Considered

- **No change; rely on models knowing the one-way/two-way-door concept:** Rejected — the existing fog-only scaling line anchors proportionality to a single axis; a stated rule crowds out an unstated instinct.
- **A separate stakes-assessment step or mechanism:** Rejected — a new mechanism invites ceremony; the gap is one missing input on an existing dial, so the fix belongs at the dial.
- **Also annotating the scouting sentence earlier in the paragraph:** Deferred — one canonical locus; duplication invites drift. Revisit only if the single edit proves too quiet in practice.

## Consequences

### Positive
- Investigation effort allocates the way senior judgment allocates it: consequence-weighted, in both directions.
- The two failure modes the wording was designed against — crumb-skipping under a reversibility excuse, and confidence inflation on reversible calls — are foreclosed in the text itself rather than left to interpretation.

### Negative
- Reversibility is itself a judgment the model can misassess (data written, trust spent, options foreclosed all masquerade as reversible); the wording installs the dial but cannot calibrate it. Watch sessions before adding a "reversibility is a claim" clause.
- In unattended runs the stakes input may be unknowable and gets set by assumption; existing flagged-assumption discipline covers it, with high-stakes as the conservative default implied by the ethos rather than stated.

## Source
- Grounding: textual analysis of the spine (single-axis scaling at the fog sentence), corroborated by an independent re-derivation from evidence with the conclusion withheld, which converged on the same placement and produced the crumb and confidence guards adopted here.
- Related: 20260714-figure-out-keeps-do-nothing-in-the-option-set
- Related: 20260714-figure-out-roots-crux-tree-above-solution-shaped-topics
