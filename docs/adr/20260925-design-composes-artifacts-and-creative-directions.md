# ADR: Design composes artifact guidance and creative directions

## Status
Accepted

## Area
Design skills

## Context

The short design prompt grounds choices in the person, moment, and subject. It leaves concrete art direction to the model. Reusable direction-specific guidance can preserve a strong creative intent, such as cinematic awe, while artifact guidance supplies the composition and interaction priorities of the work.

A direction and an artifact answer different questions. A cinematic landing page and a cinematic presentation share an emotional intent but have different reading and interaction patterns. Separate standalone skills for their combinations would repeat the brief and multiply maintenance.

## Decision

Keep one design entrypoint and add two reference collections, each with a concise index and individual guides. Artifact guides describe how people use the work. Creative directions describe the intended feeling and concrete visual choices that support it. Whole-app guidance belongs with artifacts and can compose with guides for individual screens.

The entrypoint owns brief completion, precedence, selective loading, and composition. New compositions and substantial redesigns use the indexes to read only relevant guides. Narrow refinements retain their scope. Explicit creative choices remain choices; the references do not reopen them.

Both collections are non-exhaustive and composable. A blend has a coherent center rather than accumulating every guide's instructions. The subject supplies palette, typography, and visual material. The guides do not require external example-site study or prescribe implementation, verification, or delivery. Platform-specific guides are outside this change.

## Alternatives Considered

- **Standalone skills for each direction:** make invocation explicit but duplicate the brief and fragment guidance for combinations.
- **One reference containing every guide:** reduces file count but loads unrelated material whenever one approach is needed.
- **Keep only the short prompt:** preserves minimal context but omits reusable, concrete creative guidance.
- **Restore example-site catalogs:** reintroduces the shared-style and mandatory browsing costs recorded in the preceding decision.

## Consequences

### Positive

- Named directions remain strong without imposing their associated artifact assumptions.
- One entrypoint can compose guidance for pages, apps, documents, presentations, and graphics.
- Small indexes keep irrelevant guidance out of a design run.

### Negative

- Selection adds a reference-reading step and remains a judgment call.
- The collections need editorial care to remain distinct and concise.
- General visual-quality improvement is unmeasured; structural checks and brief-level exercises establish narrower properties.

## Source

- Amends 20260924-design-starts-from-the-person-and-their-moment: artifact use is modeled explicitly beneath the person-and-moment foundation; required external catalogs remain retired.
- Related: 20260703-progressive-disclosure-triggers-live-in-loading-layer
