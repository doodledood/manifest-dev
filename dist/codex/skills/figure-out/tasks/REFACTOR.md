# REFACTOR — probing fuel

Angles that are easy to under-weight when restructuring without behavior change. Considerations, not an agenda. Press the load-bearing ones; priority stays yours. Composes with `CODING.md`.

## Blind-spot probes
- **Behavior contract** — Exactly what behavior must NOT change, and how is that preservation verified — existing tests, characterization tests, before/after comparison?
- **Characterization gap** — If no tests cover the area being restructured, are characterization tests a prerequisite before touching it?
- **Done definition** — "Cleaner" is unbounded. What does done look like for this refactor?
- **Lost intent** — Could the "ugly" code being cleaned up be ugly on purpose — an optimization or an edge-case workaround?
- **Reviewability** — Is the change small enough to review with confidence, or does it need splitting?

## Forced trade-offs
- Incremental vs big-bang — can this land in safe, reviewable chunks, or must it go at once?
- Refactor now vs feature first — does the feature actually depend on this cleanup?
