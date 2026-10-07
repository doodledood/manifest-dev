# ADR: Design exposes optional instruments with bounded evidence

## Status
Accepted

## Area
Design skills

## Context

Design guidance selects composition and interaction choices from the person, moment and subject. Some design questions benefit from repeatable observations: whether required facts are visible together, which label is near a referent, what happens after a failed save, or how declared values map to chart marks. A mandatory numerical score would treat unlike tasks as equivalent and reward shortcuts such as hiding content or deleting necessary qualifications.

The existing evaluator owns normative standards and review checks. Consultation during design needs a separate boundary: a measurement may inform a trade-off without becoming a requirement or declaring the artifact finished.

## Decision

Keep the current guidance and add a selectively loaded instrument catalog inside the standalone design skill. Ship input-only local analysis scripts with the skill, including explicit dependencies, input shapes, localized observations and coverage limits. The invoking agent obtains images, HTML, text or structured observations with its environment's available tools. Rendering, capture, interaction, simulations and document export stay outside the shipped instruments; the development harness owns its browser adapter. Source HTML provides source inventories, not computed layout or executed behavior. The caller chooses instruments by question; using none or rejecting an improved number remains legitimate. Explicit requirements and the existing design system retain precedence.

Separate supplied observations, declarations, agent-obtained scenario evidence and actual audience evidence. Do not supply a universal aesthetic/UX score, required suite, pass threshold or fixed optimization loop. Keep normative evaluation with `review-design`; consultation scripts do not certify conformance or quality.

Keep metric development beside a reproducible evaluation harness, outside ordinary prompt load. Preserve baseline/refinement outcomes, known-fact checks, misleading shortcuts, independent transfer cases and unfavorable results. Constructed validity and model inspection do not establish human UX improvement or causal prompt effectiveness. A generated comparison gallery lets a reviewer judge matched alternatives before revealing their measurements and identities.

## Alternatives Considered

- **Mandatory instrument suite:** makes consultation repeatable but invents applicability and turns descriptions into conformance requirements.
- **Composite quality score:** eases automated optimization while hiding trade-offs, incomplete coverage and metric gaming.
- **Bundled browser acquisition:** convenient for local web evaluations but couples consultation to a browser installation and owns tasks better left to the invoking agent. Retain it only in the development harness.
- **Prose alone:** keeps dependencies minimal but leaves repeated geometric and behavioral questions to manual inspection.
- **Bundle every research model:** expands capability at the cost of distinct model stacks and unsupported equivalence claims. Authentic learned importance and feature-congestion adapters can be added when their inputs, dependencies and validity earn them a place.

## Consequences

### Positive

- Models can consult repeatable evidence without surrendering design discretion.
- Instruments work in an isolated skill installation and report missing capability rather than returning an empty success.
- Development failures remain reproducible and visible to reviewers.

### Negative

- JSON/text analysis needs Node; source HTML also needs Python, and native image decoding needs Pillow. Browser and PDF dependencies belong only to development capture.
- Exact geometry, clipping, type, paint and interaction observations must be obtained by the caller when the question requires them.
- Meaning, optical fit, taste and audience outcomes still require appropriate judgment or measurement.
- Native hosts, assistive announcements, physical devices and unusual paint remain explicit coverage limits.

## Source

- Amends 20260924-design-starts-from-the-person-and-their-moment: preserves its art-direction foundation and adds optional evidence consultation.
- Amends 20260925-design-composes-artifacts-and-creative-directions: adds a selectively loaded instrument collection without changing artifact/direction selection.
- Related: 20260905-the-invoking-run-owns-design-verifier-selection
- Related: 20260927-design-names-the-defaults-to-avoid
