# Code-maintainability review

Audit the change for maintainability: code organization, DRY violations, coupling, cohesion, consistency, dead code, and architectural boundaries. Advisory dimension — PASS requires no MEDIUM-or-higher findings.

## What this dimension covers

**Be comprehensive in analysis, precise in reporting.** Examine every file in scope against every applicable category — do not cut corners or skip areas. But only report findings that clear the Actionability Filter below. Thoroughness in looking; discipline in reporting.

These categories are guidance, not exhaustive. If you spot a maintainability issue that fits this dimension but matches no listed category, report it — just respect the orthogonality boundaries so this dimension stays distinct from its neighbors.

- **DRY violations**: Duplicate functions, copy-pasted logic blocks, redundant type definitions, repeated validation patterns, and similar code that should be abstracted.
- **Structural complexity**: Mixed concerns in single units (e.g., HTTP handling + business logic + persistence in one file).
- **Conditional accretion / spaghetti growth**: New ad-hoc branches, one-off flags, nullable modes, or scattered feature checks inserted into unrelated flows. Report only when the branching has a concrete cleaner owner (state model, policy object, dispatcher, helper, or module) and makes future changes easier to miss.
- **Large-file decomposition triggers**: When a diff pushes a non-generated source file from below roughly 1000 lines to above roughly 1000 lines, inspect whether the added code forms separable concerns. Crossing the threshold is not itself a finding; report only when decomposition would materially reduce coupling, scan cost, or change amplification.
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

- **Intent-behavior divergence** (does the change achieve its goal?) → the change-intent dimension.
- **Over-engineering / YAGNI** → the code-simplicity dimension.
- **Cognitive complexity** → the code-simplicity dimension.
- **Unnecessary indirection** → the code-simplicity dimension.
- **Premature optimization** → the code-simplicity dimension.
- **Testability design patterns** → the code-testability dimension.
- **Type safety issues** → the type-safety dimension.
- **Documentation accuracy** → the docs dimension.
- **Mechanical code defects** (race conditions, resource leaks, null handling) → the code-bugs dimension.
- **API contract correctness** (wrong params, consumer breakage) → the contracts dimension.
- **Test coverage gaps** → the test-quality dimension.
- **Comment value / prose AI-tells in comments and doc files** (this dimension owns dead-code identification; value-of-comment lives with the prose auditor) → the prose-value dimension.
- **Context file compliance** → the context-file-adherence dimension.
- **Design fitness** (reinvented wheels, code vs configuration boundary, under-engineering, interface foresight, concept misuse/overloading) → the code-design dimension.

## Scope notes specific to this dimension

For deleted files in the diff: skip reviewing deleted file contents, but search for imports/references to the deleted file paths across the codebase and report any remaining references as potential orphaned code.

Cross-file analysis should only examine files directly connected to the scoped changes: files that the changed files import from, and files that import from the changed files. Do not traverse further (no imports-of-imports). Issues outside scope go in a brief "Related Concerns" note, not deep analysis.

High-churn files deserve extra scrutiny since issues there have outsized impact. Files that always change together with files outside scope may indicate coupling — note in "Related Concerns".

## Actionability filter

Before reporting an issue, it must pass ALL of these. **If a finding fails ANY criterion, drop it entirely.** Only report issues you are CERTAIN about — "this might be a problem" is not sufficient; "this WILL cause X problem because Y" is required.

1. **In scope** — Two modes:
   - **Diff-based review** (default, no paths specified): ONLY report issues introduced or meaningfully worsened by this change. "Meaningfully worsened" means the change added significant new duplication to a pre-existing issue, added a new instance of an already-problematic pattern (e.g., third copy of duplicate code), or changed a single-file fix into a multi-file change. Pre-existing tech debt is strictly out of scope.
   - **Explicit path review** (caller specified files/directories): Audit everything in scope. Pre-existing issues are valid findings since a full review of those paths was requested.
2. **Worth the churn** — Fix value must clearly exceed refactor cost. A refactor is worth it when the lines of problematic code eliminated substantially outweigh the lines added for the new abstraction plus modified call sites.
3. **Matches codebase patterns** — Don't demand abstractions absent elsewhere. If the codebase doesn't use dependency injection, don't flag its absence.
4. **Not an intentional tradeoff** — Some duplication is intentional (test isolation, avoiding coupling). If identical patterns exist in multiple other places in the codebase, assume it's an intentional convention.
5. **Concrete impact** — "Could be cleaner" isn't a finding. Articulate specific consequences: "Will cause shotgun surgery when X changes" or "Makes testing Y impossible."
6. **Author would prioritize** — Given limited time, would a reasonable author fix this before shipping, or defer it? If defer, it's Low severity at best.

For conditional accretion, the finding must name the cleaner owner for the logic and why leaving the branch in place creates forgettability risk. For large-file growth, line count alone is never enough; the finding must identify separable concerns introduced by the diff and why extracting them would reduce review or future-change risk.

## Context adaptation

Before applying rules rigidly, consider:

- **Project maturity**: Greenfield projects can aim for ideal; legacy systems need pragmatic incremental improvement.
- **Language idioms**: What's a code smell in Java may be idiomatic in Python (e.g., duck typing vs interfaces).
- **Team conventions**: Existing patterns, even if suboptimal, may be intentional trade-offs — flag but don't assume they're errors.
- **Domain complexity**: Some domains (finance, healthcare) justify extra validation/abstraction that would be over-engineering elsewhere.

## Severity calibration

The shared severity ladder applies; this dimension refines it as follows.

**Critical** — matching one or more of these patterns (exhaustive for Critical):

- Exact code duplication across multiple files.
- Dead code that misleads developers.
- Severely mixed concerns that prevent testing.
- Completely inconsistent error handling that hides failures.
- 2+ incompatible representations of the same concept across layers that require compensating runtime checks or special-case glue code.
- Boundary leakage that couples unrelated layers and forces changes in multiple subsystems for one feature.
- Circular dependencies between modules (A→B→C→A) that prevent isolated testing and deployment.
- Global mutable state accessed from 2+ modules (creates hidden coupling).

**High** — significantly impacts maintainability, should be addressed soon:

- Near-duplicate logic with minor variations.
- Abstraction layers that increase coupling without enabling reuse.
- Indirection that violates architectural boundaries.
- Inconsistent API patterns within the same module.
- Inconsistent naming/shapes for the same concept across modules causing repeated mapping/translation code.
- Migration debt (dual paths, deprecated wrappers) without a concrete removal plan.
- Low module cohesion: single file handling concerns from multiple core architectural layers (HTTP/transport, business/domain logic, data access/persistence, external service integration). Supporting concerns (logging, configuration, error handling) don't count as separate layers when mixed with one core layer.
- Low function cohesion: function name doesn't match behavior (misleading), or function does multiple distinct operations that could be separate functions.
- Low type cohesion: type spanning unrelated domains, or property that clearly belongs to a different concept (e.g., `billingAddress` on `AuthToken`).
- Special-case branching scattered through a shared or already-busy flow when the logic has a clear owning abstraction, creating forgettability risk for the next similar case.
- A diff pushes a non-generated source file past roughly 1000 lines and the added code contains separable concerns whose extraction would materially improve cohesion or reviewability.
- Long parameter lists without parameter object.
- Unexplained `@ts-ignore`/`eslint-disable` in new code — likely hiding a real bug.
- Extensibility risk where 2+ sibling components already exist and each manually implements the same cross-cutting behavior — evidence the concern belongs at a higher level.
- Hidden contract in main API paths: function fetches external state instead of receiving it as a parameter, hiding the dependency from callers.

**Medium** — degrades code quality but doesn't cause immediate problems:

- Minor duplication that could be extracted.
- Small consistency deviations.
- Suppression comments without explanation (add comment explaining why).
- Broad `eslint-disable` without specific rule (should target specific rule).
- Minor boundary violations (one layer leaking into another).
- Extensibility risk in new code: cross-cutting concern placed in a specific implementation where the pattern is likely to be extended.
- New local branch/mode accretion that makes a function harder to extend safely, but the cleaner owner is limited to one module.
- Function with compound name (`validateAndSave`, `fetchAndTransform`) that could be split.
- Hidden contract in internal/helper code: function relies on external state or execution order not visible in signature.
- Type growing beyond its original purpose (new property doesn't quite fit but isn't egregious).

**Low** — minor polish:

- Stylistic inconsistencies.
- Minor naming improvements.
- Unused imports or variables.
- Well-documented suppressions that could potentially be removed with refactoring.

**Calibration check**: Maintainability reviews should rarely have Critical issues. If you're marking more than two issues as Critical in a single review, double-check each against the explicit Critical patterns above — if it doesn't match one of those patterns, it's High at most.

## Gotchas and false positives

- **Read full files before flagging.** A diff alone lacks context — code that looks duplicated in isolation may serve different purposes when you see the full picture.
- **Be specific and actionable**: always reference exact file paths, line numbers, and code snippets; every issue needs a concrete, implementable fix suggestion.
- **Account for project conventions** from CLAUDE.md files and existing patterns.
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

A clean review is a valid outcome — do not fabricate issues to fill the report.

### Worked finding examples

```
#### [HIGH] Duplicate validation logic
**Category**: DRY
**Location**: `src/handlers/order.ts:45-52`, `src/handlers/payment.ts:38-45`
**Description**: Nearly identical input validation for user IDs exists in both handlers
**Evidence**:
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
**Impact**: Bug fixes or validation changes must be applied in multiple places; easy to miss one
**Effort**: Quick win
**Suggested Fix**: Extract to a shared validation module as `validateUserId(id: string): void`
```

```
#### [HIGH] Analytics calls embedded in individual processors
**Category**: Extensibility Risk
**Location**: `src/processors/OrderProcessor.ts:89`, `src/processors/RefundProcessor.ts:67`, `src/processors/ReturnProcessor.ts:73`
**Description**: Each processor manually fires analytics events. Adding a new processor requires remembering to add the analytics call—nothing enforces it.
**Evidence**:
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
**Impact**: New processors will silently lack analytics unless developers remember to add them. Already have 3 processors with manual calls—pattern will continue.
**Effort**: Moderate refactor
**Suggested Fix**: Move analytics to the orchestration layer (e.g., `ProcessorRunner`) or use a decorator/wrapper:
```typescript
class ProcessorRunner {
  run(processor: Processor, input: Input) {
    const result = processor.process(input);
    analytics.track(`${processor.name}_processed`, { id: input.id });
    return result;
  }
}
```
```

```
#### [HIGH] Function name doesn't match behavior
**Category**: Cohesion
**Location**: `src/services/user.ts:145`
**Description**: `getUser()` creates a user if not found, but the name implies read-only retrieval. Callers expecting idempotent read behavior will cause unintended user creation.
**Evidence**:
```typescript
async function getUser(email: string): Promise<User> {
  const existing = await db.users.findByEmail(email);
  if (existing) return existing;
  // Surprise! This "get" function creates users
  return await db.users.create({ email, createdAt: new Date() });
}
```
**Impact**: Callers will misuse this function. Someone checking "does user exist?" by calling getUser will accidentally create users. The name lies about the contract.
**Effort**: Quick win
**Suggested Fix**: Either rename to `getOrCreateUser()` or split into `getUser()` (returns null if not found) and `ensureUser()` (creates if needed).
```

```
#### [HIGH] Type accumulates unrelated concerns
**Category**: Cohesion
**Location**: `src/types/User.ts:1-45`
**Description**: `User` type has grown to include authentication, profile, preferences, billing, and audit fields—5 distinct concerns in one type.
**Evidence**:
```typescript
interface User {
  // Identity (ok)
  id: string;
  email: string;
  // Auth (separate concern)
  passwordHash: string;
  mfaSecret: string;
  sessions: Session[];
  // Profile (separate concern)
  displayName: string;
  avatarUrl: string;
  bio: string;
  // Preferences (separate concern)
  theme: 'light' | 'dark';
  notifications: NotificationSettings;
  // Billing (separate concern)
  stripeCustomerId: string;
  subscriptionTier: string;
  // Audit (separate concern)
  createdAt: Date;
  lastLoginAt: Date;
}
```
**Impact**: Every feature touching any user aspect must load/pass the entire User. Changes to billing affect auth code. Type is hard to understand and evolve.
**Effort**: Moderate refactor
**Suggested Fix**: Decompose into focused types: `UserIdentity`, `UserAuth`, `UserProfile`, `UserPreferences`, `UserBilling`. Core `User` composes or references these.
```

## Pre-output checklist

Before delivering: scope was clearly established (asked if unclear); every Critical/High issue has specific file:line references; every issue has an actionable fix suggestion; no duplicate issues reported under different names; summary statistics match the detailed findings.
