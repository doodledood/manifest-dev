# CODING — probing fuel

Angles that are easy to under-weight on code tasks. Considerations, not an agenda — most won't apply to a given task. Surface the load-bearing ones; ignore the rest. Priority stays yours.

## Blind-spot probes
- **Verification design** — How will we know this works? Does the design need a test seam, hook, or observability it doesn't have yet — and would adding that change what we build? (If it's self-verifying, say so and move on.)
- **Failure visibility** — When this breaks in production, how would anyone know? Is there a metric, log, or alert, or does it fail silently?
- **Consumer blast radius** — Who depends on what's changing, and how do they find out it changed?
- **Silent regression** — What behavior could change while the existing tests still pass?

## Forced trade-offs
- Fix in place vs refactor first — which, and why?
- Test depth vs ship speed — where's the line for this change?
