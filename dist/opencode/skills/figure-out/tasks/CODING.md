# CODING — probing fuel

Angles that are easy to under-weight on code tasks. Considerations, not an agenda — most won't apply to a given task. Surface the load-bearing ones; ignore the rest. Priority stays yours.

## Blind-spot probes
- **Verification design** *(default press when there's a runnable surface)* — Before naming the read, settle the *exercise approach*: how does the new behavior actually get run — booted how, driven how — and which new paths are risky enough to need it? Does the design need a test seam, hook, or observability it doesn't have yet — and would adding that change what we build? Establish the approach, not the enumerated test plan (that's /define's to encode). (Self-verifying, or no runnable surface — say so and move on.)
- **Failure visibility** — When this breaks in production, how would anyone know? Is there a metric, log, or alert, or does it fail silently?
- **Consumer notification** — once you've traced who depends on what's changing, how do they *find out* it changed — compile error, runtime break, or silent drift?
- **Silent regression** — What behavior could change while the existing tests still pass?

## Forced trade-offs
- Fix in place vs refactor first — which, and why?
- Test depth vs ship speed — where's the line for this change?
