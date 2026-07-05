# ADR: figure-out reads ship an Evidence Ledger and earn their terminals; the independent re-derivation pass is un-deferred

## Status
Accepted

## Context

A fresh trust-gap pass over figure-out (post the 2026-06-06 hardening) found five residual gaps: **epistemic blur** (verified observation, inference, and recall voiced identically), **shapeless reads** (no required confidence / evidence / overturn conditions on the deliverable), **confirmation-shaped probing** (support accumulates for the leader instead of probes that split rivals), **staleness** (turn-3 claims recited at turn 40 in a verified voice, including post-compaction), and **self-grading at convergence** (nothing independent ever re-derives the read — worst under `--autonomous`).

The 2026-06-06 ADR deferred the independent fresh-context pass on machinery cost. That costing predates the Evidence Ledger: once reads ship their evidence, the pass needs no new machinery.

A late operator constraint shaped the non-convergence clause: models reach for "unclear" as a lazy escape; underdetermined must not be a cheap exit.

## Decision

Adopt an evidence-ledger trust core in the spine, mode-general:

1. **Tiered claim discipline** — epistemic status is always voiced (verified / inferred / assumed); concrete provenance (file:line, command output, URL, quoted statement) is required only for load-bearing claims — the ones the read will rest on. No per-sentence citation bureaucracy.
2. **Read anatomy** (principle, not template) — the named read ships: conclusion, confidence, the Evidence Ledger it rests on, and what would overturn it (for judgment-driven reads, the trade-off boundary). Assumptions ride in the ledger as `assumed` entries — which `/define` can encode as `ASM-*`. With no evidence claims, it collapses to conclusion + reasoning + confidence.
3. **Status decay** — "verified" is not permanent: when a claim's basis is no longer trustworthy (files changed, long session, compaction swallowed the evidence), it drops to inferred/assumed until re-anchored; the read-time ledger check forces re-verification of decayed pillars.
4. **Discriminating probes** (folded into the existing rival-set line) — while rivals remain live, prefer the probe that splits them or kills the leader over accumulating support; the read earns commitment by surviving its best disconfirming test.
5. **Earned non-convergence** — never manufacture a winner, but "underdetermined" must be earned, not declared: every runnable discriminating probe has been run and sits in the ledger, and the set still won't move. Unrun probes mean keep pressing. No routing of ambiguity to `/define` — the existing "read implies work → offer /define" line is the only handoff.
6. **Independent re-derivation, un-deferred** — at convergence, when the read is load-bearing and no human adversary will audit it (which captures `--autonomous` without naming it), or on request: a fresh context that has not seen the conclusion receives the question plus the ledger's evidence and derives its own read. Divergence is a live rival the register must absorb; persistent divergence is the mechanical non-convergence signal. Cheap version only — re-derive from gathered evidence, no new collection (it may flag "evidence underdetermines; you'd need X"). Phrased harness-agnostic (any isolated fresh context); where no isolation exists, skip with disclosure ("read is self-graded").

## Alternatives Considered

- **Provenance on every claim**: Rejected — bureaucratic turns, buries signal; fails at the light end of the skill's range.
- **Fixed read template**: Rejected — forces ledger theater onto pure judgment calls; principle-with-named-elements scales.
- **Keep the independent pass deferred**: Rejected — the deferral was costed before the ledger existed; the ledger removes the machinery the 06-06 ADR was avoiding.
- **Full re-investigation / multi-frame fan-out at convergence**: Rejected (again) — becomes a research engine / second `/do`.
- **Non-convergence as a simple terminal**: Rejected — hands the model a lazy escape; both terminals now cost the same currency (discriminating evidence exhausted).

## Consequences

### Positive
- Reads are auditable: the human adversary (and `/define` downstream) can check evidence, not just reasoning.
- The autonomous self-grading hole closes mechanically rather than by self-assessment; the 06-06 ADR's deferred residual is built.
- "Underdetermined — here's what would decide it" enters the vocabulary without becoming an exit ramp.

### Negative
- Spine weight increases; ledger upkeep and the re-derivation pass cost tokens (accepted: quality-first per CUSTOMER.md).
- The cheap re-derivation checks evidence→conclusion fit only; evidence-gathering blind spots remain partially open.

## Source
- Related: PR #189.
- Related: 20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass (un-defers its deferred independent pass; its inline-rigor decision stands); 20260606-figure-out-process-trust-vs-define-do-artifact-trust (process-trust boundary unchanged); 20260611-figure-out-spine-owns-epistemics-mode-refs-thin
