# ADR: Deliverables are exercisable slices, ordered by uncertainty

## Status
Accepted

## Context

`/define` carried detailed guidance on how to *verify* a Deliverable — thirteen `review-code` dimensions, two severity tiers, phase ordering, verifier-prompt discipline, an encoding pattern for every gate — and no guidance at all on how to *cut* one. The manifest schema's only statement about decomposition was an ordering annotation: "ordered by dependency then importance."

That left the highest-leverage judgment in the workflow unspecified. `docs/LLM_CODING_CAPABILITIES.md` identifies task size and specification quality as the primary determinants of agent success, ahead of model capability, and identifies attempting an entire feature in one pass as a characteristic failure. The step that fixes task size had no guidance; the step that checks the result had a great deal.

The gap also undermines the acceptance model itself. A Deliverable cut along an implementation layer — "the data model", "the endpoints" — has no behavior to run, so the only Acceptance Criteria it can carry are structural: the type exists, the module imports, the code compiles. Existence is the weakest property a gate can assert, and a manifest full of existence gates reproduces exactly the false-completion failure that inline verification exists to prevent. How a Deliverable is cut therefore determines whether its gates mean anything, and nothing in the workflow said so.

`define/tasks/CODING.md` already assumed the resolution without stating it: its E2E routing sends "the new path of one Deliverable, run end-to-end" to a deliverable Acceptance Criterion. That routing presupposes a Deliverable with an end-to-end path, while nothing guaranteed one.

Separately, the ordering annotation encoded the wrong default. Ordering by dependency and importance places the least-proven work wherever the dependency graph happens to put it, which is frequently late. An approach that turns out to be unworkable is cheapest to discover early, while context and remaining budget still allow a change of course.

## Decision

`/define` states how Deliverables are cut and ordered, inline in `SKILL.md` alongside the other encoding-discipline guidance.

A Deliverable is a slice that can be finished on its own and **exercised end-to-end** — put in front of its real use: run, read, or otherwise judged in the situation it is for, not merely inspected as present. The stated reason is the acceptance consequence: this is what allows its Acceptance Criteria to judge behavior rather than existence.

The guidance names three signs a cut is wrong: you cannot say how done it is; the name is generic rather than specific to the work; it is too large to finish soon.

Ordering changes from "dependency then importance" to **least-proven approach first**, with real dependencies still binding and uncertainty ordering what they leave free. The schema annotation is rewritten rather than supplemented.

List order *is* the execution order — stating that is what makes the ordering rule mean anything to `/do`, and it is the foundation the guidance rests on. Position and ID are therefore independent: an amendment inserts a new Deliverable where uncertainty puts it rather than always last, taking a fresh ID without renumbering the others, so `/do`'s gate ledger keeps its stable keys while the uncertainty ordering survives amendment. There is no separate sequencing field. The order is soft in the same sense the Initial Approach is: `/do` may resequence when execution surfaces a real dependency the ordering missed, recording the deviation. The manifest therefore carries a second non-binding element alongside the Initial Approach, and both `/do` and the emitted schema name the pair. Per `20260726-only-gates-bind-process-guidance-is-advisory`, the binding layer is Acceptance Criteria and Global Invariants alone.

Cutting and ordering are recorded as one decision because they answer the same question about the same object. Cutting makes a Deliverable exercisable so its gates judge behavior; ordering decides which exercisable slice runs first so an unworkable approach fails early. Split apart, the ordering rule would have no unit worth ordering — least-proven-first over layer-shaped slices moves the false-completion risk around rather than reducing it — and the cutting rule would leave the sequencing consequence of exercisable slices unstated.

The guidance lives inline rather than in a companion reference because deliverable-cutting applies to every `/define` invocation. Per `20260703-progressive-disclosure-triggers-live-in-loading-layer`, always-needed behavior belongs in the entry prompt; companion references carry mode-specific mechanics reached through a trigger.

`define/tasks/CODING.md` is left unchanged. Once `SKILL.md` requires exercisable slices, that file's E2E routing rests on stated ground, and restating the requirement there would duplicate a rule that now has a single home.

## Alternatives Considered

- **A companion reference under `define/references/`**: keep `SKILL.md` lean and load decomposition guidance on demand — Rejected: there is no trigger to gate it behind. Cutting Deliverables happens on every run, so the reference would load every time while costing an indirection.
- **An Acceptance Criterion that verifies slice quality**: gate each manifest on whether its Deliverables are well cut — Rejected: the manifest's gates verify the work a manifest produces, not the manifest's own construction. A gate checking the shape of the contract it belongs to is circular, and `/define` has no execution phase in which such a gate would run.
- **Encoding the guidance as Process Guidance emitted into each manifest**: have `/define` write slicing rules into every manifest it produces — Rejected: the rules govern the encoder, not the executor. `/do` receives Deliverables already cut and cannot act on advice about cutting them.
- **Keeping dependency-then-importance and adding uncertainty as a tie-break only**: a smaller change to the ordering line — Rejected: it preserves the default that puts unproven work late, which is the behavior the change exists to correct. Uncertainty leads; dependencies constrain.
- **An authoritative `Sequence:` field in the Deliverables section**: let an amendment record a running order that differs from list order, so late-arriving least-proven work could still lead — Rejected: it requires a lifecycle (what the line names, when an entry drops, when the line is deleted), a precedence rule against list order, and a migration story for manifests written before it — three mechanisms whose interactions are the defect surface. The amendment case it exists for is served instead by positional insertion under stable IDs, which needs no lifecycle, no precedence rule, and no migration: the new Deliverable is placed where uncertainty puts it, and its ID is independent of that position.
- **Adding an explicit size or cost ceiling for a Deliverable**: bound how much a single Deliverable may consume — Rejected for now, not on merit: a slice that is genuinely small, central and exercisable is substantially self-bounding, so a separate ceiling may be solving a problem good slicing already solves. Worth revisiting once this guidance has been exercised.

## Consequences

### Positive
- Acceptance Criteria can be written against behavior, because the Deliverables they attach to are runnable by construction.
- `define/tasks/CODING.md`'s E2E routing rests on a stated requirement rather than an unstated assumption.
- An unworkable approach surfaces early enough to change course rather than at the end of a run.
- The three wrong-cut signs give a concrete test, so "is this well cut?" is answerable rather than a matter of feel.

### Negative
- `SKILL.md` grows, and it loads on every `/define` invocation. The cost is accepted because decomposition applies universally; the ordering line was rewritten rather than added to keep the net growth proportionate.
- Uncertainty-first ordering can conflict with a reader's expectation that execution order follows dependencies. The guidance states that real dependencies still bind, but the two rules must now be reconciled per manifest rather than read off the dependency graph.
- Requiring exercisability may push against work that is genuinely infrastructural, where the honest slice has no user-visible path. Such cases must be cut so that something can still be run against them, which is more demanding than cutting by layer.

## Source
- Related: [20260703-progressive-disclosure-triggers-live-in-loading-layer](20260703-progressive-disclosure-triggers-live-in-loading-layer.md)
- Related: [20260709-process-guidance-is-binding-but-unverified](20260709-process-guidance-is-binding-but-unverified.md)
