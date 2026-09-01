# UI Task Guidance

User-visible artifact work of any genre — anything a person will see and judge rather than call. Composes onto `CODING.md` when the artifact is code, alongside FEATURE/BUG/REFACTOR as relevant; applies on its own when the deliverable is a non-code visual artifact.

## Quality Gates

| Aspect | Skill | Threshold |
|--------|-------|-----------|
| Design quality | `review-design` | no MEDIUM+ |
| Reference fidelity | — | Faithful to any mocks, references, or reaction-pinned criteria the manifest carries |

The design gate encodes as a gate body that activates the `review-design` skill under `/do`'s selected evaluator. Name the skill, the artifact surface, and the genre where the manifest knows it, and stop — the skill owns the threshold (the bar in the table above orients the author rather than being copied into the gate), loads the design standards it shares with the `design` skill, and covers register fit, functional state coverage (empty, loading, error, happy path), composition and hierarchy, craft consistency, copy, and viewport behavior inside that one gate; they do not need gates of their own. It is a Judgment Gate, which is what tells `/do` how it re-verifies.

**Rendered evidence is the floor**: `review-design` renders and exercises the artifact or returns BLOCKED rather than judging from source, so an unrenderable surface stays visible and routed instead of silently passing on code inspection. A manifest whose artifact needs a build step, fixture data, or a running service to render names it in the gate body so the evaluator can reach a verdict.

Pinned mocks, references, and reaction-pinned criteria land on the fidelity gate, per the pinning rules in `SKILL.md`.

## Defaults

*Domain best practices for this task type.*

- **Build with the design skill** — Invoke the `manifest-dev:design` skill when creating or restyling the artifact; it front-loads the purpose/register decision, the token system, and the floor checklist the gate will later judge
- **Screenshot as you build** — Render and look at each changed surface during development, not only at review time; a layout defect caught mid-build costs a tweak, one caught at the gate costs a repair round
- **Develop against realistic content** — Real-length text, real data shapes, non-square images; placeholder-sized content hides the truncation, wrapping, and spacing defects the review will find
- **Keep pinned references in view** — Where the user reacted to a mock, reference, or option during definition, keep that artifact at hand while implementing rather than reconstructing it from memory
