# ADR: Split the tech-design task profile by workflow role

## Status
Accepted

## Context
manifest-dev maintains parallel task-file sets for different phases. figure-out task files provide probing fuel for reaching shared understanding; /define task files provide encoder data that becomes Manifest gates and Process Guidance. Technical design documents sit across that boundary: the document's audience, layering, source-absorption policy, visual strategy, and taste criteria are part of the understanding that must exist before a Manifest is encoded, while the final document still needs /define-time gates for standalone readability, decision coverage, image quality, and source fidelity.

A single task profile must support two entry paths. In the full workflow, figure-out should surface the document-shaping questions before /define. In standalone /define, the Manifest gates still need enough parameterization to force missing inputs into the interview rather than silently defaulting them.

## Decision
Split the tech-design task profile across both task sets by workflow role:

- Add `figure-out/tasks/TECH_DESIGN.md` for document-authoring probing fuel. It surfaces audience layering, reference/source role, visual policy, taste pinning, asset placement, and ownership/estimate questions as non-natural probes.
- Add `define/tasks/TECH_DESIGN.md` for encoder data only. It contributes Quality Gates for audience layering, decisions coverage, image review, and content-frozen fidelity, plus Defaults for generated-image label checks and the two gate-less placement/ownership probes.
- Do not introduce a new `## Interview Probes` content type in /define task files. Standalone /define is handled by parameterized gates: a dual-persona gate cannot be encoded without personas, and a decisions-coverage gate cannot be encoded without the source list and citation/absorption policy.

## Alternatives Considered
- **Single /define-side file carrying probes and gates**: Rejected — it would make /define responsible for understanding questions that belong upstream in figure-out, weakening the existing phase boundary.
- **Duplicate the same probes in both task sets**: Rejected — duplication invites drift and teaches both phases to ask the same questions for different reasons. /define should encode missing gate parameters, not re-run figure-out's probing agenda.
- **Add a generic writing/document probe base to figure-out**: Rejected for now — the observed gap is specific to technical design documents with source records, visuals, and audience layering. A broader document taxonomy can be added when multiple document-shaped gaps justify it.

## Consequences

### Positive
- The full workflow surfaces audience, taste, and source-policy criteria while understanding is still being formed.
- /define remains an encoder: its task files stay limited to Quality Gates and Defaults.
- Standalone /define still works because the gates expose the parameters it must ask for.
- The split aligns with the existing parallel task-file architecture instead of creating a new content type.

### Negative
- A tech-design change touches two task files and two routing tables, which is more maintenance than a single profile.
- The gates-pull-questions pattern relies on /define honoring parameterized gates during its interview; if that weakens, explicit define-side probe guidance may need to be revisited.
- A future generic document-probing base may make part of the figure-out file redundant.

## Source
- Related: 20260604-figure-out-owns-domain-probing-via-mirrored-task-files
- Related: 20260606-figure-out-process-trust-vs-define-do-artifact-trust
