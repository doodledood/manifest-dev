# BUG — probing fuel

Angles that are easy to under-weight when fixing a known defect. Considerations, not an agenda. Press the load-bearing ones; priority stays yours. Composes with `CODING.md`; diagnosis-phase angles (tracing the mechanism, multiple causes) live in `DIAGNOSIS.md`.

## Blind-spot probes
- **Confirm before deploy** — What local check (log, test, code trace) proves the diagnosed cause is actually fixed *before* shipping, rather than shipping to see if it worked?
- **Shared-caller fallout** — If the fix touches a callback, hook, or shared-state API, who else calls it and what do they assume about call order or freshness?
- **Bad data left behind** — Does fixing the code leave corrupted state that still needs migration or cleanup?

## Forced trade-offs
- Hotfix now vs proper fix — stop the bleeding then fix the mechanism, or fix it right once?
- This instance vs the class — fix this bug, or the pattern that lets it recur?
