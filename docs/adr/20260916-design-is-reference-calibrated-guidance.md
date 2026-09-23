# ADR: Design is reference-calibrated guidance; the evaluator owns review machinery

## Status
Superseded by 20260924-design-starts-from-the-person-and-their-moment

## Area
Design skills

## Context

The experimental `design-v2` skill supplies compact, audience-centered art direction through curated examples. Its reference-use wording allowed agents to read annotations without seeing the examples, while its audience instruction did not require that understanding to shape visual choices. Those gaps are corrected by requiring visual study before composing and a concise brief connecting the audience to color, hierarchy, density and pacing. Quick explainers make the central relationship visible rather than leaving readers to assemble it from prose.

The owner selected this skill to replace `design`, not remain an alternative beside it. The old `design` also owned a builder procedure, three conditional standards references and an HTML checker. `review-design` depends on those references and checker, so deleting the old directory without relocating them would break evaluation.

## Decision

Promote the verified prompt and five example catalogs to `design`, remove the `design-v2` entrypoint, and retire the old builder prompt. `design` supplies design judgment; the invoking workflow creates or changes the artifact. `review-design` remains the evaluator.

Move the existing access, information-fidelity and continuity references and the checker unchanged into `review-design`. Its loading table owns those conditional standards. It can also consult `design` for audience-centered art direction, beneath explicit requirements and the established design system; a profile preference is not a conformance requirement. The lightweight design skill has no evaluator dependency.

Adapt callers to request design guidance rather than delegate implementation. Prototype fidelity and lifecycle stay with the calling workflow instead of a mode on the retired builder. Keep the curated URLs and concise descriptions of concrete elements; do not bundle third-party snapshots or put inspection-session status in shipped guidance. Descriptions direct visual study rather than replace it.

This is a breaking behavioral replacement and removal of an invocation name, reflected in major core-plugin and Pi package versions. Internal checker consumers move to its evaluator-owned path. No compatibility wrapper retains the retired skill.

## Alternatives Considered

- **Keep both skills:** preserves the old invocation behavior but leaves users choosing between competing design defaults instead of making the selected replacement authoritative.
- **Keep the old references and checker inside the new design directory:** avoids path updates but makes a standalone guidance skill carry evaluation machinery it does not use. Moving them to their consumer gives each file a clear owner.
- **Delete the review machinery too:** produces a smaller package by breaking an existing evaluator and losing its access and fidelity checks. That is not part of replacing the design guidance.
- **Merge the old builder procedure into the replacement:** retains its responsibilities but defeats the chosen guidance-only boundary and reintroduces the load the replacement avoids.

## Consequences

### Positive

- One design entrypoint requires audience-grounded choices and direct reference study.
- Evaluation keeps its existing standards and checker without loading them into ordinary design guidance.
- Caller responsibilities and prototype scope are explicit rather than inherited from a removed builder mode.

### Negative

- Users of `design-v2` must invoke `design`; consumers of the old checker path must update.
- Live references can change or disappear. Annotations preserve the selected lesson but cannot reproduce an unavailable visual or interaction.
- Structural checks and focused behavioral exercises do not establish general visual-quality or audience-comprehension improvement. Comparative effectiveness remains unestablished.

## Source

- Amends 20260915-design-keeps-experience-goals-and-conditional-constraints: replaces the builder with reference-calibrated guidance; conditional constraints remain with evaluation.
- Amends 20260901-design-skill-pair-distills-research-eval-deferred: guidance and evaluation replace the doer/evaluator ownership; evaluation deferral stands.
- Amends 20260901-design-derives-structure-from-a-written-task-model: a concise audience-grounded brief replaces the builder's task-model contract; the evaluator still recovers task context and co-visibility.
- Amends 20260901-deliberation-renders-run-the-design-skill-at-prototype-weight: prototype lifecycle belongs to callers rather than a design mode.
- Amends 20260902-design-chooses-an-encoding-per-claim-figures-are-information-not-decoration: quick visual explanation remains explicit; the fidelity reference and checker move to the evaluator.
- Amends 20260905-design-defaults-to-purpose-led-visual-ambition: audience-centered art direction and the selected profile replace the builder's universal ambition contract; evaluator findings still need task consequences.
- Amends 20260905-design-obligations-follow-the-medium-and-task: evaluation retains its medium-specific standards at evaluator-owned paths.
