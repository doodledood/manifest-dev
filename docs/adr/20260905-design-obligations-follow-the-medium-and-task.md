# ADR: Design obligations follow the medium and task

## Status
Accepted

## Area
Design skills

## Context

The design pair covers digital artifacts, but several shared rules assume a web page. Visual tokens do not apply to audio-only conversation. A static first view cannot demonstrate an interactive simulation. A screenshot cannot establish workbook formulas, document reading order or service recovery. Meanwhile style defaults and narrow checks can be mistaken for universal requirements.

## Decision

Derive obligations from the task, medium and claimed delivery before applying visual defaults. A compact shared experience reference routes stateful, multi-page and non-web work to the relevant continuity, agency, access and delivery probes. The builder and reviewer use the same applicability boundaries.

Applicable functional and accessibility requirements bind. Style defaults guide creative choices; departures become findings only through the brief, the governing design system or demonstrated user need. Verification uses the actual artifact and reports unavailable evidence. A limited HTML checker provides bounded measurements and review candidates, not conformance certification.

This extends the written task model and shared reference structure. It narrows the static-on-arrival prototype rule to orientation and necessary controls: when interaction or pacing is the subject, that behavior must be available at the fidelity being judged. Purpose-led visual ambition continues for visual work. Source provenance remains outside shipped skill instructions, and comparative effectiveness remains unmeasured.

## Alternatives Considered

- **Keep web rules as the universal default:** smaller instructions, but silently misroutes non-web artifacts and turns preferences into failures.
- **Add a separate skill for every medium:** deeper specialization, but duplicates task, state and access rules. The current need is reliable routing; specialist production guidance can be loaded when required.
- **Create an exhaustive always-loaded manual:** wider detail at the cost of irrelevant instructions and more conflicts. A short conditional reference fits the existing architecture.

## Consequences

### Positive

- New artifact families have an explicit route without being forced into web layouts.
- Builder and reviewer share applicable obligations and evidence limits.
- Creative ambition survives while functional failures remain visible.

### Negative

- Applying a standard or default requires context-sensitive judgment.
- The router is not specialist expertise for every medium.
- Regression fixtures establish specific repairs, not general design-quality improvement.

## Source

- Session: 2026-09-05 design research and skill audit; review-only delivery requested.
- Extends 20260901-design-derives-structure-from-a-written-task-model
- Extends 20260901-design-skill-pair-distills-research-eval-deferred
- Narrows 20260901-deliberation-renders-run-the-design-skill-at-prototype-weight
- Narrows 20260902-design-chooses-an-encoding-per-claim-figures-are-information-not-decoration
- Related: 20260905-design-defaults-to-purpose-led-visual-ambition
