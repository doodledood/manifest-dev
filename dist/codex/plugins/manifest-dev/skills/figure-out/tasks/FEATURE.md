# FEATURE — probing fuel

Angles that are easy to under-weight on new functionality. Considerations, not an agenda — most won't apply. Press the load-bearing ones; priority stays yours. Composes with `CODING.md`.

## Blind-spot probes
- **Verification design** — How will we confirm the feature does what it promises across its real use cases, not just the happy path? Does the design need a seam or fixture to make that checkable — and does that reshape what we build? (If self-verifying, say so.)
- **Partial failure** — What state is left behind if it fails halfway through?
- **Consumer awareness** — Downstream consumers of any changed interface: who are they, and how do they learn it changed?
- **Orphaned resources** — Does this create data or state that grows unbounded with no cleanup path?
- **Rollback** — If this ships and goes wrong, how is it reversed — flag, migration rollback, manual revert?

## Forced trade-offs
- Graceful degradation vs fail-fast — when this breaks, should the surrounding functionality keep working or stop loudly?
- New abstraction vs inline — is the generality earned yet, or is one call site speculating?
