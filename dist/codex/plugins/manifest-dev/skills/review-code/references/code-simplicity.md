# Code-simplicity review

Find code where implementation complexity exceeds problem complexity — over-engineering, premature optimization, and cognitive burden that make code harder to understand than the problem requires.

**The question for every piece of code: "Is this harder to understand than it needs to be?"**

## What to inspect

Be comprehensive in analysis, precise in reporting. Examine every file in scope against every applicable category — do not cut corners or skip areas. But only report findings that meet the high-confidence bar in the Actionability Filter. Thoroughness in looking; discipline in reporting.

These categories are guidance, not exhaustive. If you identify a simplicity issue that fits within this dimension's domain but doesn't match a listed category, report it — just respect the Out of Scope boundaries to maintain orthogonality with sibling dimensions.

### 1. Over-Engineering

Solutions more complex than the problem demands:

- **Premature abstraction**: Generalizing before concrete use cases justify it (factory for one implementation, plugin system for one plugin)
- **Unnecessary configurability**: Options that never vary in practice
- **Speculative generality**: Code for hypothetical future requirements ("what if we need to...")
- **Missed structural simplification**: A concrete behavior-preserving reframing would delete whole branches, helper layers, modes, or concepts rather than merely polish them. Report only when the simpler shape is visible from the code, preserves behavior, and materially reduces what the reader must hold in their head.

### 2. Premature Optimization

Complexity added for performance without evidence of need:

- **Micro-optimizations**: Bit manipulation, manual loop unrolling, avoiding standard library for "speed" — without profiling data
- **Unnecessary caching**: Memoization without profiled need (cache that never hits)
- **Complex data structures**: Specialized structures without scale justification (trie for 10 items)

### 3. Cognitive Complexity

Code that requires excessive mental effort to understand:

- **Deep nesting**: Nesting deep enough that the reader loses track of context — use early returns and flat structure instead
- **Complex boolean expressions**: Conditions dense enough to require re-reading — extract into named variables
- **Nested ternaries**: Any ternary within a ternary
- **Dense one-liners**: Long chained operations that should be broken into named intermediate steps
- **Long functions**: Functions doing multiple things that could be extracted for clarity

### 4. Clarity Over Cleverness

Code that sacrifices readability for brevity or showing off:

- **Cryptic abbreviations**: Variable/function names that require decoding
- **Magic numbers/strings**: Unexplained literals in non-obvious contexts
- **Implicit behavior**: Side effects or behavior not obvious from the signature (note: if the hidden side effect causes *incorrect behavior*, that belongs to the code-bugs dimension; this dimension focuses on *comprehension*)

### 5. Unnecessary Indirection

Layers that add complexity without value. Focus on **local indirection within a module** — cross-module abstraction layers are maintainability's concern.

- **Pass-through wrappers**: Functions that just call another function with no added logic
- **Over-abstracted utilities**: Wrapping standard operations that are already clear

## Actionability filter

Before reporting an issue, it must pass ALL of these criteria. **If it fails ANY criterion, drop it entirely.** Only report complexity you are CERTAIN is unnecessary — "this might be over-engineered" is not sufficient; "this abstraction serves no purpose and could be replaced with X" is required.

1. **In scope** — Two modes:
   - **Diff-based review** (default): ONLY report simplicity issues introduced by this change. Pre-existing complexity is strictly out of scope.
   - **Explicit path review** (caller specified paths): Audit everything in scope. Pre-existing complexity is valid to report.
2. **Actually unnecessary** — The complexity must provide no value. If there's a legitimate reason (scale, requirements, constraints), it's not over-engineering. Check comments and context for justification before flagging.
3. **Simpler alternative exists** — You must describe a concrete simpler approach that would work. "This is complex" without a better alternative is not actionable.
4. **Worth the simplification** — Trivial complexity (an extra variable, one level of nesting) isn't worth flagging. Focus on complexity that meaningfully increases cognitive load.
5. **Matches codebase context** — A startup MVP can be simpler than enterprise software. A one-off script can be simpler than a shared library. Consider scale, maturity, team size, domain, and performance requirements before flagging.

When looking for simplifications, prefer changes that delete concepts over changes that just rearrange complexity. Do not report speculative "there might be a better design" feedback; the simpler flow must be concrete enough that the author could implement it from the review.

## Out of scope (belongs to a sibling dimension)

Do NOT report on:

- **Intent-behavior divergence** (does the change achieve its goal?) → belongs to the change-intent dimension
- **DRY violations** (duplicate code) → belongs to the code-maintainability dimension
- **Dead code** (unused functions) → belongs to the code-maintainability dimension
- **Coupling/cohesion** (module dependencies) → belongs to the code-maintainability dimension
- **Consistency issues** (mixed patterns across codebase) → belongs to the code-maintainability dimension
- **Mechanical code defects** (race conditions, resource leaks, null handling) → belongs to the code-bugs dimension
- **API contract correctness** (wrong params, consumer breakage) → belongs to the contracts dimension
- **Type safety** (any/unknown, invalid states) → belongs to the type-safety dimension
- **Documentation accuracy** → belongs to the docs dimension
- **Test coverage gaps** → belongs to the test-quality dimension
- **Context file compliance** → belongs to the context-file-adherence dimension

**Key distinction from maintainability:**

- **Maintainability** asks: "Is this well-organized for future changes?" (DRY, coupling, cohesion, consistency, dead code)
- **Simplicity** asks: "Is this harder to understand than the problem requires?" (over-engineering, cognitive complexity, cleverness)

**Rule of thumb:** If the issue is about **duplication, dependencies, or consistency across files**, it's maintainability. If the issue is about **whether this specific code is more complex than needed**, it's simplicity.

## Severity calibration

**High**: Complexity that significantly impedes understanding and maintenance

- Abstraction layers with single implementation and no planned alternatives
- A visible behavior-preserving simplification would remove multiple branches, modes, or helper layers from core logic
- Deep nesting in core logic paths that loses context
- Complex optimization without profiling evidence in hot paths
- Multiple indirection layers that obscure simple operations
- Extensive configurability used with single configuration

**Medium**: Complexity that adds friction but doesn't severely impede understanding

- Moderate over-abstraction (could be simpler but isn't egregious)
- A concrete local reframing would collapse repeated branches or helper indirection in one module
- Nested ternaries or moderately complex boolean expressions
- Unnecessary caching or memoization in non-critical paths
- Somewhat cryptic naming that requires context to understand

**Low**: Minor simplification opportunities

- Single unnecessary wrapper functions
- Slightly verbose approaches that could be more concise
- Magic numbers in semi-obvious contexts
- Minor naming improvements

**Calibration check**: High severity should be reserved for complexity that actively harms comprehension. If you're marking many issues as High, recalibrate — most simplicity issues are Medium or Low.

## Dimension-specific report fields

Beyond the shared report skeleton, each finding for this dimension should make the simpler shape explicit:

- **Category**: Over-Engineering | Missed Structural Simplification | Premature Optimization | Cognitive Complexity | Clarity | Unnecessary Indirection
- **Impact**: how this complexity hinders understanding
- **Effort**: Quick win (localized change, single file) | Moderate refactor (may affect a few files, backward compatible) | Significant restructuring (may require design discussion)
- **Simpler Alternative**: a concrete code example of the simpler approach the author could implement directly

The executive summary for this dimension answers: **Is the code complexity proportional to the problem complexity?**

If no issues pass the filter, the PASS report should state which files/changes were reviewed and affirm that solutions match the problems they solve — clean code with appropriate complexity is a valid and positive outcome. Do not fabricate issues to fill the report.
