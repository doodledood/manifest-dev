# UI Task Guidance

User-visible interface work: screens, pages, components, styling, visual output. Composes onto `CODING.md`, alongside FEATURE/BUG/REFACTOR as relevant.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Rendered-result review | no MEDIUM+ — the evaluator opens the rendered interface — screenshots of every changed screen, or the running app — and judges layout, alignment, spacing, typography, visual consistency with the surrounding product, acceptable taste (composition, whitespace, color harmony, no boilerplate feel), and fidelity to any references, mocks, or reaction-pinned criteria the manifest carries |
| State coverage | no MEDIUM+ — every changed screen is rendered and reviewed in the states its data produces (empty, loading, error, long and realistic content) and the viewports it targets |

**Rendered evidence is the floor for both**: a verdict formed from reading components, styles, or markup alone is not an evaluation of these gates — the interface must actually be rendered. When the surface cannot be rendered, the verdict is **BLOCKED** rather than a silent fall-back to code inspection, so the unmet review stays visible and routed instead of hidden. Both are judgment gates over the rendered artifact.

## Defaults

*Domain best practices for this task type.*

- **Screenshot as you build** — Render and look at each changed screen during development, not only at review time; a layout defect caught mid-build costs a tweak, one caught at the gate costs a repair round
- **Develop against realistic content** — Real-length text, real data shapes, non-square images; placeholder-sized content hides the truncation, wrapping, and spacing defects the review will find
- **Keep pinned references in view** — Where the user reacted to a mock, reference, or option during definition, keep that artifact at hand while implementing rather than reconstructing it from memory
