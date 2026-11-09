# Code-maintainability review

Audit the change for maintainability: code organization, DRY violations, coupling, cohesion, consistency, dead code, and architectural boundaries.

## What this dimension covers

These categories are guidance, not exhaustive. If you spot a maintainability issue that fits this dimension but matches no listed category, report it — just respect the orthogonality boundaries so this dimension stays distinct from its neighbors.

- **DRY violations**: Duplicate functions, copy-pasted logic blocks, redundant type definitions, repeated validation patterns, and similar code that should be abstracted.
- **Structural complexity**: Mixed concerns in single units (e.g., HTTP handling + business logic + persistence in one file).
- **Conditional accretion / spaghetti growth**: New ad-hoc branches, one-off flags, nullable modes, or scattered feature checks inserted into unrelated flows. Report only when the finding names a concrete cleaner owner (state model, policy object, dispatcher, helper, or module) and why leaving the branching in place makes future changes easier to miss.
- **Large-file decomposition triggers**: When a diff pushes a non-generated source file from below roughly 1000 lines to above roughly 1000 lines, inspect whether the added code forms separable concerns. Crossing the threshold is not itself a finding; report only when the finding identifies separable concerns the diff introduced and decomposition would materially reduce coupling, scan cost, or change amplification.
- **Dead code**: Unused functions, unreferenced imports, orphaned exports, commented-out code blocks, unreachable branches, and vestigial parameters.
- **Consistency issues**: Inconsistent error handling patterns, mixed API styles, naming convention violations, and divergent approaches to similar problems.
- **Concept & Contract Drift**: The same domain concept represented in multiple incompatible ways across modules/layers (different names, shapes, formats, or conventions), leading to glue code, brittle invariants, and hard-to-change systems. Look for: duplicated serialization/formatting/normalization logic across components, multiple names/structures for the same artifact across layers without a clear mapping boundary, "parity drift" between producer/consumer subsystems that should share contracts, and similar-looking identifiers with unclear semantics (e.g., `XText` vs `XDocs` vs `XPayload`).
- **Boundary Leakage**: Internal details bleeding across architectural boundaries (domain ↔ persistence, core logic ↔ presentation/formatting, app ↔ framework), making changes risky and testing harder. Includes "stringly-typed" plumbing (passing serialized data through multiple layers instead of keeping structured data until the I/O boundary) and runtime content-based invariants used to compensate for weak contracts.
- **Migration Debt**: Temporary compatibility bridges (dual fields, deprecated formats, transitional wrappers) without a clear removal plan that tend to become permanent.
- **Coupling issues**: Circular dependencies between modules, god objects that know too much, feature envy (methods using more of another class's data than their own), tight coupling that makes isolated testing impossible.
- **Cohesion problems** — the test: "can you give this a clear, accurate name?":
  - **Module**: Handles unrelated concerns, shotgun surgery, divergent change.
  - **Function**: Name is vague (`processData`), compound (`validateAndSave`), or doesn't match behavior — it's doing too much.
  - **Type**: Accumulates unrelated properties (god type), or property doesn't belong conceptually.
- **Global mutable state**: Static/global mutable state shared across modules creates hidden coupling and makes behavior unpredictable (testability-specific concerns belong to the code-testability dimension).
- **Temporal coupling & hidden contracts**: Hidden dependencies on execution order not enforced by types or visible in signatures. The test: "Could a caller know this dependency exists by looking at the function signature?" Includes methods that must be called in order, initialization assumed but not enforced, and code relying on side effects instead of explicit data flow.
- **Common anti-patterns**: Data clumps (parameter groups that always appear together), long parameter lists.
- **Linter/Type suppression abuse**: `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# type: ignore`, `// nolint`, `#pragma warning disable`. These should be rare, justified, and documented. Red flags: no explanation comment, suppressing errors in new code, broad rule disables without specific rule, multiple suppressions in same function.
- **Extensibility risk**: Responsibilities at the wrong abstraction level that create "forgettability risk" when the pattern extends. The test: if someone adds another similar component, will they naturally do the right thing, or must they remember to manually replicate behavior?
- **Contract surface**: When behavior is fundamentally a contract (serialization formats, schemas, message shapes), there should be a single source of truth. Flag "change amplification" where a small contract change requires edits across many files.

## Out of scope (belongs to other dimensions)

Do NOT report on these — they belong elsewhere:

- **Adequacy of a repair against its demonstrated failure mechanism** → the defect-class dimension, including whether proportionate prevention was omitted.
- **Intent-behavior divergence** (does the change achieve its goal?) → the change-intent dimension.
- **Over-engineering / YAGNI** → the code-simplicity dimension.
- **Cognitive complexity** → the code-simplicity dimension.
- **Unnecessary indirection** → the code-simplicity dimension.
- **Premature optimization** → the code-simplicity dimension.
- **Testability design patterns** → the code-testability dimension.
- **Type safety holes** — a type weakness that names a trigger → the type-safety dimension. Type *style* consistency stays here under Consistency: interface-versus-type-alias divergence, over-annotation of obvious types, and discriminant naming that is merely inconsistent across the codebase.
- **Documentation accuracy** → the docs dimension.
- **Mechanical code defects** (race conditions, resource leaks, null handling) → the code-bugs dimension.
- **API contract correctness** (wrong params, consumer breakage) → the contracts dimension.
- **Test coverage gaps** → the test-quality dimension.
- **Comment value / prose AI-tells in comments and doc files** (this dimension owns dead-code identification; value-of-comment lives with the prose auditor) → the prose-value dimension.
- **Context file compliance** → the context-file-adherence dimension.
- **Design fitness** (reinvented wheels, code vs configuration boundary, under-engineering, interface foresight, concept misuse/overloading) → the code-design dimension.

## Scope notes specific to this dimension

For deleted files in the diff: skip reviewing deleted file contents, but search for imports/references to the deleted file paths across the codebase and report any remaining references as potential orphaned code.

High-churn files deserve extra scrutiny since issues there have outsized impact. Files that always change together with files outside scope may indicate coupling — note it in the report's `Summary`.

## Actionability filter

Before reporting an issue, it must pass ALL of these. **If a finding fails ANY criterion, drop it entirely.** A finding names the problem and its cause: "this might be a problem" is not sufficient; "this WILL cause X problem because Y" is required.

1. **In scope** — Two modes:
   - **Diff-based review** (default, no paths specified): ONLY report issues introduced or meaningfully worsened by this change. "Meaningfully worsened" means the change added significant new duplication to a pre-existing issue, added a new instance of an already-problematic pattern (e.g., third copy of duplicate code), or changed a single-file fix into a multi-file change. Also include an existing obligation this change newly relies on or extends when its concrete future-change burden is evidenced. Unrelated pre-existing debt stays out of scope.
   - **Explicit path review** (caller specified files/directories): Audit everything in scope. Pre-existing issues are valid findings since a full review of those paths was requested.
2. **Worth the churn** — Compare the concrete burden on subsequent work with added concepts, coupling, migration risk and coordination cost. Removing independent obligations can justify added lines; fewer lines alone establish no benefit.
3. **Fits the work** — Existing patterns are context, not a quality ceiling. A different abstraction earns its place by reducing the evidenced maintenance burden enough to justify its complexity; its absence alone is not a finding. Honor deliberate applicable project policy.
4. **Substantiated tradeoff** — Evaluate the reason for duplication or another burden against its actual benefit (such as test isolation or avoiding coupling). Repetition establishes prevalence, not justification; an author's rationale is evidence, while explicit owner requirements bind.
5. **Concrete impact** — "Could be cleaner" isn't a finding. Articulate specific consequences: "Will cause shotgun surgery when X changes" or "Makes testing Y impossible." Style-consistency findings under Consistency are the exception to this bar and to the lead-in's "this WILL cause X problem" bar: name the divergence and the surfaces it splits across, and state the impact as reader cost — the scan or learning tax a divergent form imposes on someone working across both — and land at Low. Mere consistency nits are Low; a substantive failure is graded by its demonstrated consequence under the shared ladder.
6. **Grade the consequence** — Use the concrete future-change burden below, not the author's willingness to defer it. Explicit task limits constrain the remedy, not the evidence or severity.

## Context adaptation

Before applying rules rigidly, consider:

- **Project maturity**: Greenfield projects can aim for ideal; legacy systems need pragmatic incremental improvement.
- **Language idioms**: What's a code smell in Java may be idiomatic in Python (e.g., duck typing vs interfaces).
- **Team conventions**: Existing patterns, even if suboptimal, may be intentional trade-offs — flag but don't assume they're errors.
- **Domain complexity**: Some domains (finance, healthcare) justify extra validation/abstraction that would be over-engineering elsewhere.

## Severity calibration

Use the shared ladder. Duplication, mixed concerns, incompatible representations, boundary leakage, circular dependencies, hidden state, inconsistent APIs, migration debt and scattered special cases earn Medium when the finding names the future change they make materially harder and a concrete improvement. A demonstrated correctness, safety or promise failure is High or Critical; grade that consequence rather than the pattern alone. Polish and nits are Low, including style, naming and structural nits.

## Gotchas and false positives

- **Read full files before flagging.** A diff alone lacks context — code that looks duplicated in isolation may serve different purposes when you see the full picture.
- **Be specific and actionable**: include code snippets and a concrete, implementable fix suggestion for every issue.
- **Account for project conventions** from the project context file and existing patterns.
- **Common false positives to avoid**:
  - Test file duplication (test setup repetition is often intentional for isolation).
  - Type definitions that mirror API contracts (not duplication — documentation).
  - Similar-but-different code serving distinct business rules.
  - Intentional denormalization for performance.

## Dimension-specific report expectations

Use the shared report format. In addition, this dimension expects:

- A **Category** tag on each finding, drawn from: DRY | Structural Complexity | Dead Code | Consistency | Coupling | Cohesion | Anti-pattern | Suppression | Boundary | Contract Drift | Extensibility Risk.
- An **Effort** estimate on each finding:
  - **Quick win**: single file, no API changes.
  - **Moderate refactor**: few files, backward compatible.
  - **Significant restructuring**: architectural change, may require coordination.
- A short **Summary Statistics** section: total issues by category, total by severity, and the top 3 priority fixes.

### Worked finding examples

Each example fills the shared report format and adds this dimension's **Category** and **Effort**.

````
### Finding #1: Duplicate validation logic
- **Location**: `src/handlers/order.ts:45-52`, `src/handlers/payment.ts:38-45`
- **Severity**: Medium
- **Category**: DRY
- **Description**: Nearly identical input validation for user IDs exists in both handlers:
  ```typescript
  // order.ts:45-52
  if (!userId || typeof userId !== 'string' || userId.length < 5) {
    throw new ValidationError('Invalid user ID');
  }

  // payment.ts:38-45
  if (!userId || typeof userId !== 'string' || userId.length < 5) {
    throw new ValidationError('Invalid userId');
  }
  ```
- **Acceptance basis**: Concrete quality cost: one validation rule is kept in two places.
- **Impact**: Bug fixes or validation changes must be applied in multiple places; easy to miss one
- **Effort**: Quick win
- **Recommended fix**: Parse the ID once where the request enters, as `parseUserId(raw: unknown): UserId`, returning a branded `UserId` or throwing `ValidationError`, and take `UserId` in both handlers, so a value that skipped the check cannot reach them
````

````
### Finding #2: Analytics calls embedded in individual processors
- **Location**: `src/processors/OrderProcessor.ts:89`, `src/processors/RefundProcessor.ts:67`, `src/processors/ReturnProcessor.ts:73`
- **Severity**: Medium
- **Category**: Extensibility Risk
- **Description**: Each processor manually fires analytics events. Adding a new processor requires remembering to add the analytics call—nothing enforces it.
  ```typescript
  // OrderProcessor.ts:89
  class OrderProcessor {
    process(order: Order) {
      // ... business logic ...
      analytics.track('order_processed', { orderId: order.id });
    }
  }

  // RefundProcessor.ts:67 - same pattern
  // ReturnProcessor.ts:73 - same pattern
  ```
- **Acceptance basis**: Concrete quality cost: every new processor must repeat a call nothing enforces.
- **Impact**: New processors will silently lack analytics unless developers remember to add them. Already have 3 processors with manual calls—pattern will continue.
- **Effort**: Moderate refactor
- **Recommended fix**: Move analytics to the orchestration layer (e.g., `ProcessorRunner`) or use a decorator/wrapper:
  ```typescript
  class ProcessorRunner {
    run(processor: Processor, input: Input) {
      const result = processor.process(input);
      analytics.track(`${processor.name}_processed`, { id: input.id });
      return result;
    }
  }
  ```
````

## Pre-output checklist

Before delivering: scope was clearly established (asked if unclear, or reported BLOCKED with no one to ask); every issue has an actionable fix suggestion; no duplicate issues reported under different names; summary statistics match the detailed findings.
