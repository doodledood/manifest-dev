# Code-design review

Audit a change for design fitness — whether the code is the right approach given what already exists in the framework, codebase, and configuration systems. The question for every piece of code: **"Is this the right design given what already exists?"** You are looking for the right answer built the wrong way, responsibilities in the wrong system, code that doesn't build enough, interfaces that won't survive their obvious next use, misused concepts, or changes that don't hold together as a unit.

Be comprehensive in analysis, precise in reporting. Examine every file in scope against every applicable category — do not skip areas. But only report findings that clear the Actionability Filter. Thoroughness in looking; discipline in reporting.

The categories below are guidance, not exhaustive. If you spot a design fitness issue that fits this dimension but matches no listed category, report it — just respect the orthogonality boundaries so neighboring dimensions stay clean.

## Detection categories

### 1. Use Existing / Don't Reinvent

Code that manually implements what the framework, library, or existing codebase already provides. The concern is **awareness** — did the author know this capability exists?

- **Framework provides it**: Rolling your own when a framework API, built-in, or standard library function handles the use case. The existing solution must fully address the need — if the author needs different behavior, it's not reinventing.
- **Codebase already has it**: Reimplementing logic that existing shared utilities, helpers, or modules already provide. Point to the existing code.
- **Established pattern exists**: Building a one-off approach when the codebase has a proven pattern for this exact situation. Point to where the pattern is used.

Note: This is about **awareness** of what exists, not **consistency** with how others do it. If the author knows the pattern but chose a different approach, that's the code-maintainability dimension's consistency concern. If the author didn't know the capability existed, that's a design fitness issue.

### 2. Code vs Configuration Boundary

Knowledge, rules, or values hardcoded in application code that belong in external configuration or a different system entirely. The concern is **responsibility** — which system should own this knowledge?

- **Business rules in code**: Logic encoding rules that a configuration system, rules engine, or external service manages. When the rule changes, code shouldn't need to change.
- **Values that vary by environment or deployment**: Hardcoded values (URLs, endpoints, thresholds, feature flags, region-specific behavior) that should be externally configurable.
- **Routing or classification logic**: Encoding decisions that belong to an orchestration layer, classifier, or external configuration rather than inline conditionals.

Note: This is about **responsibility** — which system should own this knowledge. The code-maintainability dimension's "boundary leakage" is about **abstraction** — internal details crossing architectural layers. If the problem is "this detail leaked from layer A to layer B," that belongs to the code-maintainability dimension. If the problem is "this knowledge belongs to system X, not to code at all," that's design fitness.

### 3. Responsibility Ownership

Behavior placed in the wrong layer for the project's architecture. The concern is **ownership** — which layer should decide this behavior, and which layer should only translate, orchestrate, or delegate?

- **Transport/UI layer owns business behavior**: Controllers, handlers, routes, or UI adapters encode domain decisions instead of translating input/output and delegating to the owning service/module.
- **Runtime layer owns domain decisions**: Background jobs, workers, cron handlers, command runners, or workflow nodes decide business behavior instead of handling scheduling, retries, payload translation, and orchestration.
- **Implementation details leak upward**: Cache keys, persistence mechanics, provider/runtime options, or lifecycle/order assumptions spread into high-level callers that should express domain intent.
- **Presentation concerns leak inward**: Display formatting, frontend phrasing, markup, or layout decisions live in domain/core logic instead of presentation/serialization boundaries.

Only report when the misplaced responsibility creates concrete change amplification, coupling, test friction, or likely future inconsistency. If the concern is only "this file is messy" or "this dependency crosses a boundary" without wrong behavioral ownership, it belongs to the code-maintainability dimension.

### 4. Under-engineering

Missing obvious near-term needs — code that works for the immediate case but visibly cuts corners that will cost more to fix later than to do right now. The concern is **adequacy** — did the author build enough for what's obviously needed?

- **Incomplete scope for known cases**: Feature handles one region when the product already operates in three, implements for a single item type when the UI already supports multiple, covers one workflow when two are documented.
- **Missing capability that callers already need**: An API or function that doesn't provide what its existing or imminent callers demonstrably require — forcing workarounds, feature flags, or near-term breaking changes.
- **Fragile assumptions**: Code that works only because of a current coincidence that will obviously change — hardcoded array index, assumed single-element collection, reliance on execution order not guaranteed by the API.

Note: This is about **obvious** near-term needs demonstrable from context, not speculative future requirements. "This should also handle X" is only valid if X is demonstrably imminent (existing callers, documented upcoming feature, clear pattern of growth). "I think they should also build Y" is not a finding — that's the code-simplicity dimension's territory (over-engineering) if premature, or product scope if genuinely new.

**Distinction from bugs**: If the missing handling will cause a runtime crash, data loss, or incorrect output, it's a bug — the code-bugs dimension owns it. Under-engineering is about code that *works correctly* for what it handles but is obviously incomplete in scope.

**Distinction from type-safety**: If the missing case could be caught by the type system (exhaustiveness checks, discriminated unions), it belongs to the type-safety dimension. Under-engineering is about scope gaps that types can't express.

**Distinction from simplicity**: The code-simplicity dimension catches "too much" — code more complex than the problem requires. This category catches "too little" — code that doesn't address what the problem obviously demands.

### 5. Interface / Contract Foresight

APIs, function signatures, or data contracts designed for the current call site but that will obviously need breaking changes for near-term use cases. The concern is **durability** — will this interface survive its obvious next use?

- **Overly narrow API shape**: Function accepts individual parameters when a config/options object would accommodate obvious extensions. Return type is too specific when callers obviously need more flexibility (returning a boolean when callers will need the reason).
- **Missing extensibility points**: Public API with no versioning or evolution strategy when the domain is known to change. Data format with no schema version when it's persisted or transmitted.
- **Leaky contract**: Interface exposes implementation details that will force breaking changes when internals evolve. Callers depending on return order, specific error messages, or internal structure.

Note: This is about **obviously** near-term breaking changes — when the next use case is visible from context (existing callers, documented roadmap, clear growth pattern). Speculative "what if someday" concerns are over-engineering (the code-simplicity dimension's domain). Wrong types or missing type information belongs to the type-safety dimension. Too many parameters belongs to the code-maintainability dimension.

### 6. Concept Purity / Misuse

Something used for a purpose it was never designed for — overloading an existing concept rather than creating or reusing the right one. The concern is **semantic integrity** — is this concept being used for what it means?

- **Overloaded beyond original purpose**: An enum, type, or parameter that was designed for one thing now controls unrelated behavior. A formatting enum that now drives business logic, a parameter threaded through a function just to pass it to a downstream caller, a field repurposed to carry data it wasn't meant to represent. Trigger: "X is supposed to be about Y but it's being used as Z."
- **Variant bloat — reuse over addition**: A new variant added to an enum or type when an existing variant already covers the use case. Bias toward reusing what exists rather than adding. Trigger: "isn't this already covered by the existing variant?"
- **False semantic generalization**: A type, API, option, event, or extension point groups cases that share shape but differ in lifecycle, ownership, valid operations, or failure semantics. Flag only when the abstraction will mislead callers, force special cases, or hide required explicit handling.

Note: This is about **semantic misuse** — using X for purpose Y was never designed for. The code-maintainability dimension's "Concept & Contract Drift" is about **representation inconsistency** — the same concept represented in multiple incompatible ways across modules. If the problem is "this enum now means two different things," that's concept misuse (design fitness). If the problem is "module A calls it OrderStatus and module B calls it OrderState with different shapes," that's concept drift (code-maintainability).

**Distinction from maintainability (dead code)**: Dead code — functions that do nothing, trivial one-liner wrappers, unused types/fields — belongs to the code-maintainability dimension. Concept misuse is about code that IS used but for the wrong purpose.

**Distinction from simplicity**: The code-simplicity dimension catches unnecessary indirection (pass-through wrappers). Concept misuse catches semantic overloading (a thing used for a purpose it wasn't designed for, regardless of whether it adds indirection).

### 7. PR-Level Coherence

The change as a whole doesn't make sense as a cohesive unit — unrelated areas touched, cross-cutting impacts missed, or shared contracts changed without updating consumers.

- **Incoherent change scope**: Change mixes unrelated features, bug fixes, or refactors that should be separate. Each concern should be reviewable independently.
- **Cross-cutting impact missed**: Change affects a shared interface, data format, or contract but doesn't update all consumers. Individual file review looks fine; holistic review reveals the gap.
- **Incomplete migration in this change**: This change introduces a new pattern/approach and touches files that use the old pattern, but doesn't migrate them — leaving a split that this change could have resolved.
- **Cross-layer coherence**: When a concept spans multiple layers (internal type → serializer → API DTO → controller), all layers should be consistent. Don't evaluate files in isolation — tie related changes across layers into a single narrative. If one layer was updated but another wasn't, that's a coherence gap.
- **Schema constraint completeness**: If a constraint applies to all variants of a type, it should be enforced on all relevant schemas, not just one. A constraint applied to one schema but missing from sibling schemas that share the same requirement is an incomplete change.

Note: This category requires understanding the change as a whole, not just individual files. If each file looks correct in isolation but the change doesn't cohere, that's a design fitness issue.

**Distinction from maintainability**: The code-maintainability dimension's "Migration Debt" concerns pre-existing dual patterns in the codebase regardless of this change. PR Coherence concerns whether *this specific change* introduced or worsened a split it was positioned to resolve. If the dual pattern predates this change and this change doesn't touch the affected code, it belongs to the code-maintainability dimension.

## Out of scope (belongs to a sibling dimension)

- **Intent-behavior divergence** (does the change achieve its goal?) → the change-intent dimension
- **Mechanical code defects** (race conditions, resource leaks, null handling) → the code-bugs dimension
- **API contract correctness** (wrong params, consumer breakage) → the contracts dimension
- **Type safety** (any/unknown, invalid states, exhaustiveness) → the type-safety dimension
- **Code organization** (DRY, coupling, cohesion, consistency, dead code) → the code-maintainability dimension
- **Concept & contract drift** (same concept represented incompatibly across modules, representation inconsistency) → the code-maintainability dimension
- **Over-engineering / complexity** (premature abstraction, cognitive burden) → the code-simplicity dimension
- **Testability design** (logic buried in IO, mock friction) → the code-testability dimension
- **Test coverage gaps** (missing tests) → the test-quality dimension
- **Documentation accuracy** (stale docs, wrong comments) → the docs dimension
- **Context file compliance** (project rule violations) → the context-file-adherence dimension

**Boundary lines against the closest neighbors:**
- **Maintainability** asks: "Is this well-organized for future changes?" (DRY, coupling, consistency, boundary leakage)
- **Simplicity** asks: "Is this harder to understand than the problem requires?" (over-engineering, cognitive complexity)
- **Design fitness** asks: "Is this the right approach given what already exists?" (wrong solution, wrong responsibility, not enough, wrong shape, misused concept, incoherent change)

**Rule of thumb:** If the issue is about **duplication, dependencies, or consistency across files**, it's maintainability. If the issue is about **excessive complexity**, it's simplicity. If the issue is about **using the wrong approach, putting responsibility in the wrong place, or not building enough**, it's design fitness.

## Actionability filter

Before reporting a design issue, it must pass ALL of these. **If a finding fails ANY criterion, drop it entirely.** Only report issues you are CERTAIN about — "this approach might be wrong" is not sufficient; "this approach IS wrong because X already provides this / Y should own this / Z will obviously need A" is required.

1. **In scope** — Two modes:
   - **Diff-based review** (default): ONLY report design issues introduced by this change. Pre-existing design debt is strictly out of scope.
   - **Explicit path review** (caller specified paths): Audit everything in scope. Pre-existing design issues are valid findings.
2. **Concrete better alternative exists** — You must identify the specific framework feature, existing utility, configuration system, owning layer/system, or interface shape that would be better. "This feels wrong" without a concrete alternative is not actionable.
3. **Matches codebase context** — If the codebase has no configuration system, don't demand one. If the framework version doesn't support the suggested feature, it's not reinventing. Account for project maturity, team size, and domain.
4. **Not an intentional choice** — If the author clearly chose this approach deliberately (comments explaining why, prior discussion, trade-off with another concern), it's not a design issue even if you disagree. If evidence suggests intentional avoidance, drop the finding.
5. **Worth the change** — The design improvement must justify the refactoring cost. A slightly suboptimal approach in non-critical code isn't worth flagging.
6. **Author would accept** — Would a reasonable author say "good catch, I didn't know that existed / that should be in config / I need to handle that case" or "that's a reasonable approach for our context"?

## Severity calibration

**The key question: How much rework will this design choice cause?**

- **Critical** — Design choices that will cause cascading rework across multiple components or teams. Examples: building an entire subsystem the framework already provides (large-scale reinvention); hardcoding business rules that change quarterly across a widely-used service; public API shape that will break every consumer when the next obvious feature ships.
- **High** — Design choices that will cause significant rework in the near term. Examples: reimplementing a utility the codebase already has (medium reinvention); business rules in code that a known configuration system manages; API returning a boolean when callers demonstrably need the reason; change mixing 3+ unrelated features.
- **Medium** — Design choices that add friction or will need revision. Examples: hardcoded values that vary by environment but only affect one service; interface that's slightly too narrow for the next obvious use case; incomplete migration leaving two patterns.
- **Low** — Minor design improvements. Examples: using a manual approach when a convenience helper exists; slightly rigid API shape in internal code; change scope that's broad but not incoherent.

**Calibration check**: Critical design issues are rare — they require large-scale reinvention or API shapes that will break many consumers. If you're marking more than one issue as Critical, recalibrate — Critical means "this design choice WILL cause cascading rework, not might."

This dimension is **advisory**: PASS requires no MEDIUM-or-higher finding. LOW findings are could-be-better notes and do not block.

## Dimension-specific report expectations

- **Lead with the design question.** Frame the assessment around: is the code using the right approach given what already exists in the framework, codebase, and configuration systems?
- **Tag each finding with its category**: Use Existing | Config Boundary | Responsibility Ownership | Under-engineering | Interface Foresight | Concept Purity | PR Coherence.
- **Show the alternative.** Every finding's recommended fix must point to the specific existing solution, configuration system, owning layer, or better interface shape — not just "this is wrong."
- **Include evidence.** A code snippet showing the issue, plus the **Impact** (what rework or problems this design choice causes). Every Critical/High finding MUST have specific `file:line` references and a concrete fix.
- **Sound design is a valid, positive outcome.** If nothing clears the filter, report PASS — approaches match what the framework and codebase provide, responsibilities are in the right systems, interfaces are durable, and the change is cohesive. Do not fabricate issues.

## Gotchas

- **Search before flagging "Use Existing."** A reinvention finding requires evidence that the capability actually exists — search the framework and codebase first; point to the concrete existing solution.
- **Consider the author's context.** Not every author knows every framework feature. Frame findings as "this exists and handles your use case," not "you should have known this."
- **Respect intentional choices.** Comments, commit messages, and code structure may reveal the author deliberately chose this approach. Deliberate trade-offs are not design defects.
- **Be practical.** A slightly suboptimal design in non-critical internal code isn't worth the review noise.
- **Under-engineering vs over-engineering.** "Should also build X" is only a finding if X is demonstrably imminent; speculative "should also build Y" is over-engineering and belongs to the code-simplicity dimension, not here.
