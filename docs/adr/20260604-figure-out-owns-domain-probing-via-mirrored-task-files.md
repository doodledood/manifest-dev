# ADR: figure-out owns domain probing via mirrored probe task files

## Status
Accepted

## Context

The experimental → 1.0.0 promotion (commit `17043f9`) over-slimmed the define/figure-out split. It stripped the domain probing fuel (Risks, Scenario Prompts, Trade-offs) out of `define/tasks/*` and declared probing to be figure-out's job (`tasks/README.md`: *"Probing of the conversation is figure-out's job — task files don't carry probing fuel."*). But figure-out was never given any domain probes, nor a mechanism to load them — it probes only with its general "walk every branch" discipline.

The probing fuel was therefore **evicted, not migrated**: the responsibility moved to figure-out while the fuel was deleted from its old home and never re-homed. Non-natural domain probes — how a change will be **verified**, rollback strategy, consumer/blast-radius impact, error experience — now live nowhere actionable, and the model skips them by default. The observed failure that surfaced this: a feature's verification approach was never discussed during understanding, so the design lacked the seams to verify it, forcing post-hoc iteration to add testing affordances.

The documentation also drifted: `CLAUDE.md` still describes the pre-pivot model (task files carry Risks/Scenario/Trade-off probes whose "consumer is /define's interview process"), contradicting both `tasks/README.md` and the actual stripped files.

A decisive constraint: **figure-out is the primary entry point** — sessions usually start in figure-out, not define. So figure-out must be able to probe with domain awareness while running standalone, without depending on define to feed it.

## Decision

Domain probing belongs to figure-out, and figure-out is given the fuel and the mechanism to do it:

- **figure-out gets its own per-domain task files** holding *only* probing fuel (probes / non-natural angles), mirroring define's task-type taxonomy.
- **define keeps its task files** holding Quality Gates and Defaults (encoder data). The two sets are parallel, each scoped to its own consumer.
- **The detection index is split** — each skill carries its own task-type detection index and load call, in the skill itself. figure-out does not reference define's index. This keeps figure-out fully self-contained for standalone use.
- **figure-out detects task type, loads the matching probe file when one exists, and weaves those probes into its branch-walking** — degrading gracefully to general probing when no domain matches (it handles arbitrary topics, not only manifest task types).
- **Probe restoration is calibrated, not exhaustive** — re-home the proven non-natural probes (verification chief among them), not a wholesale restore of the old checklists. This honors the repo's prompt-engineering philosophy: add only what closes a real gap the model misses on its own.

define continues to *formalize* the understanding figure-out reaches; it does not invent verification post-hoc.

## Alternatives Considered

- **Inline-only (a single verification line in figure-out)**: rejected — a band-aid on one symptom; it doesn't scale, and the broader class of non-natural domain probes stays homeless.
- **define-mediated (define injects probe fuel into figure-out at spawn)**: rejected — figure-out is the dominant standalone entry point and cannot depend on define to feed it.
- **One shared task file per type, each skill reads its own section**: rejected — figure-out would pull define's reviewer-gate tables into general thinking sessions and the two skills would be coupled through shared files.
- **Shared single detection index referenced by both skills**: rejected — reintroduces a figure-out → define dependency, breaking standalone figure-out. The split-index duplication cost is accepted as the price of self-containment.
- **Full restore of all pre-pivot probe checklists**: rejected — re-bloats the task files and fights the trust-the-model / add-only-real-gaps discipline.

## Consequences

### Positive

- Probing responsibility and its fuel are finally co-located in figure-out.
- figure-out is self-contained for the dominant workflow (start in figure-out, standalone).
- define stays a lean encoder; verification and similar non-natural angles get a real home, surfaced while the design is still soft enough to absorb the answer.
- Calibrated scope keeps the probe files from re-accreting into the checklists that were rightly slimmed.

### Negative

- Two parallel task-type taxonomies/indexes can drift; adding a domain now touches both skills' task directories. Mitigated by the CLAUDE.md multi-location sync checklist.
- figure-out gains task-type detection machinery — a step away from pure leanness — justified by it being the primary prober.
- The pre-pivot docs (`CLAUDE.md`, `tasks/README.md`) must be reconciled to the new model as part of the change.

## Source

- Related: over-slim root cause in promotion `17043f9`; partial steering restore in `d8ffab7` (#145).
