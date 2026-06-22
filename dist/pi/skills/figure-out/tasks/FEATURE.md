# FEATURE — probing fuel

Angles that are easy to under-weight on new functionality. Considerations, not an agenda — most won't apply. Press the load-bearing ones; priority stays yours. Composes with `CODING.md`.

## Blind-spot probes
- **Beyond the happy path** *(default press when there's a runnable surface)* — Sharpens the base's verification-design probe: is the feature *exercised* — run end-to-end against its real use cases — or only inspected as present in the diff? Settle which new paths get driven, not just the demo flow. Approach, not the enumerated plan.
- **Partial failure** — What state is left behind if it fails halfway through?
- **Orphaned resources** — Does this create data or state that grows unbounded with no cleanup path?
- **Rollback** — If this ships and goes wrong, how is it reversed — flag, migration rollback, manual revert?

## Forced trade-offs
- Graceful degradation vs fail-fast — when this breaks, should the surrounding functionality keep working or stop loudly?
- New abstraction vs inline — is the generality earned yet, or is one call site speculating?
