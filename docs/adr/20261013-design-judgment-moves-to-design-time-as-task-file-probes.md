# ADR: Design judgment moves to design time as task-file probes and Defaults; review dimensions stay as post-code gates

## Status
Accepted

## Area
Task guidance

## Decided by
The user

## Context
Design knowledge lived only in review-code references: make illegal states unrepresentable, validate at boundaries, give each piece of state one owner, make operations idempotent, keep one way to do a task, derive lists instead of syncing them by hand. Those references run after the code exists. A design found wrong at that point gets local patches, not a new shape: in recorded executions, most repairs of post-code design findings were one-off edits, and few installed a type or structure that would stop the class from recurring.

An agent sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. So the risks worth checking before code are the patterns the next agent will copy. figure-out already has a mechanism to find disagreement before a thing is built: a disposable prototype that is concrete at the joints and thin between them. A sketch of a change's shape is that mechanism applied to code.

## Decision
- figure-out task files carry short probes. When a change crosses a function boundary, a probe asks for a sketch of its shape: how callers use it, the data shape, the seams where outside data is parsed and IO happens, one owner per piece of state, placement and public surface, test seams, and what is reused or deleted. The sketch is figure-out's existing prototyping; no new mechanism or step is added.
- The sketch probe asks for a second, structurally different shape before one is chosen. The first design an agent produces is the one most often accepted unexamined. For shared code or a package, the usage part of the sketch can take the form of a short tutorial for a hypothetical user.
- Red-flag probes ask what the next agent will copy: two ways to do one task, a list kept in sync by hand, state with two writers, internals a caller can import, IO mixed into decisions.
- Red flags exist per task type, not only for code. For documents: a fact restated from code or configuration, the same fact in two documents, mixed modes. For plans: a fix bundled with experiments. For process: a step that depends on someone remembering it.
- define task files carry a matching Default: sketch the shape and screen it against the red flags before implementing a change that crosses a function boundary. Direct requests and unattended runs, which may skip figure-out, still get the step. The Default also carries the signs that a shape is wrong during implementation: a deviation from the sketch is surfaced, not absorbed; the same workaround at unrelated call sites, or types that need casts or other escape hatches to compile, mean the run reshapes instead of patching.
- Probes stay one line each, phrased as questions, and only for angles a capable model skips by default. A pretrained discipline name carries the content in place of restated principle text.
- review-code dimensions stay as post-code gates. Findings that exist only after code exists — defects, test adequacy, documentation drift — stay with them.
- The red-flag list appears in both task-file sets, which stay decoupled. A change to one is made to the other in the same change.

## Alternatives Considered
- **Copy the review references into figure-out**: it adds load on every run and restates text the run can reach itself.
- **A new design step in figure-out's spine**: it duplicates the prototyping mechanism.
- **Move all review before code**: defects, test adequacy, and documentation drift cannot be predicted before the code exists.
- **Drop the advisory review dimensions**: rejected earlier as a quality cut the project will not take.

## Consequences

### Positive
- Disagreement about a change's shape surfaces while changing it costs least.
- Unattended runs screen their own shape before writing code.

### Negative
- The red-flag list is maintained in two task-file sets.
- A Default is advisory, so the define step binds only as Process Guidance.

## Enforced by
none — what a probe asks is judgment; CLAUDE.md names the red-flag lists kept in both task-file sets as pairs to change together.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions; aggregate figures only.
- Related: 20260604-figure-out-owns-domain-probing-via-mirrored-task-files
- Related: 20260826-prototyping-and-scratch-are-one-mechanism
- Related: 20260726-only-gates-bind-process-guidance-is-advisory
