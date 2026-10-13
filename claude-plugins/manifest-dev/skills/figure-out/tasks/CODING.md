# CODING — probing fuel

Angles that are easy to under-weight on code tasks. Considerations, not an agenda — most won't apply to a given task. Surface the load-bearing ones; ignore the rest. Priority stays yours.

## Blind-spot probes
- **Verification design** *(default press when there's a runnable surface)* — Before naming the read, settle the *exercise approach*: how does the new behavior actually get run — booted how, driven how — and which new paths are risky enough to need it? Does the design need a test seam, hook, or observability it doesn't have yet — and would adding that change what we build? Establish the approach, not the enumerated test plan (that's /define's to encode). (Self-verifying, or no runnable surface — say so and move on.)
- **The verification surface** — Does the project keep a durable way to drive and check this (a harness and feature map)? Which entries does the change touch; are any `unverified` (not yet proof) or drifting — and is a failing entry wrong about the product, or is the product broken? No surface: building one, scoped to what the change touches, is part of the work.
- **Shape before build** — When the change crosses a function boundary, what does a sketch look like — usage first (a short tutorial for a hypothetical user when the code is shared), data shape, seams where outside data is parsed and IO happens, one owner per piece of state, placement and public surface, test seams, what it reuses or deletes — and would seeing it change what we build? Offer it as a draft.
- **A second shape** — Which structurally different shape would also work, and which wins?
- **What the next agent copies** — Does the shape leave two ways to do one task, a list kept in sync by hand, state with two writers, internals a caller can import, or IO mixed into decisions? Which of these can a type, lint, or test lock?
- **Design discipline** — Are illegal states unrepresentable, outside data parsed at the boundary, shared state separated before it is serialized, operations safe to run twice or after a crash halfway, and callers migrated before the old way is deleted?
- **Recorded intent** — Before changing code that looks defensive — a retry, a timeout, a guard, a flag — what do commits, pull-request threads and tickets say it was for?
- **Drivable and debuggable** — Can an agent drive, observe and debug what this design produces? If not, what would make it so?
- **Failure visibility** — When this breaks in production, how would anyone know? Is there a metric, log, or alert, or does it fail silently?
- **Consumer notification** — once you've traced who depends on what's changing, how do they *find out* it changed — compile error, runtime break, or silent drift?
- **Silent regression** — What behavior could change while the existing tests still pass?
- **Unbuilt solution** — Does this rest on a design or technical solution nobody has actually produced yet? Assuming one exists is where scope quietly doubles.
- **Decisions that invalidate built work** — Which unmade call would, settled the wrong way mid-build, throw away work already built rather than just redirect the next step?

## Forced trade-offs
- Fix in place vs refactor first — which, and why?
- Test depth vs ship speed — where's the line for this change?
