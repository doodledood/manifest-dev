# BUG — probing fuel

Angles that are easy to under-weight on defect work. Considerations, not an agenda. Press the load-bearing ones; priority stays yours. Composes with `CODING.md`.

## Blind-spot probes
- **Mechanism, not shape** — Can you name the specific variable, line, and value at the bug moment, and the sequence that produced it? A pattern name ("it's a race", "stale state") is a shape, not a mechanism — keep tracing until it's concrete.
- **Confirm before deploy** — What local check (log, test, code trace) would prove the cause *before* shipping the fix, rather than shipping to see if it worked?
- **Shared-caller fallout** — If the fix touches a callback, hook, or shared-state API, who else calls it and what do they assume about call order or freshness?
- **Bad data left behind** — Does fixing the code leave corrupted state that still needs migration or cleanup?
- **One symptom, several causes** — Is this definitely a single bug, or could the symptom have more than one cause?

## Forced trade-offs
- Hotfix now vs proper fix — stop the bleeding then fix the mechanism, or fix it right once?
- This instance vs the class — fix this bug, or the pattern that lets it recur?
