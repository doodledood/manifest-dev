# Type-safety review

Audit a change for type safety issues across typed languages — pushing as many potential bugs as possible into the type system while balancing correctness with practicality.

## What to detect

These categories are guidance, not exhaustive. If you spot a type safety issue that fits this dimension but matches no listed category, report it — just respect the orthogonality boundaries below.

- **`any`/`unknown` abuse**: Unjustified `any` that could be typed, implicit `any` from untyped dependencies, `unknown` without proper narrowing, type assertion escape hatches (`as`), non-null assertions (`!`) without evidence. Acceptable: genuinely dynamic structures, temporary migration with TODO, test mocks where full typing is impractical.
- **Invalid states representable**: Optional field soup where certain combinations are invalid (use discriminated unions), primitive obsession for domain concepts (use branded/newtype patterns), stringly-typed APIs where enums/unions would prevent typos, arrays when tuples have fixed structure, type ownership violations where variant-specific or channel-specific data lives on a shared/generic type as optional fields that are meaningless for most consumers (fix: discriminated unions so each variant only carries its own fields).
- **Type narrowing gaps**: Missing type guards after runtime checks, unsafe narrowing, missing exhaustiveness checks on discriminated unions (switch without `never` case).
- **Generic type issues**: Functions losing type information that generics would preserve, incorrect type predicates that don't verify what they claim, loose generic constraints.
- **Nullability problems**: Missing null checks, overuse of optional chaining hiding bugs instead of failing fast, inconsistent null vs undefined handling, non-null assertion abuse. Focus: could this null check be expressed as a type? Is `T | null` properly narrowed?
- **Type definition quality**: Overly wide types (`Object`, `Function`, `{}`), and a missing return type on an export whose inferred shape a named consumer depends on.
- **Discriminated union anti-patterns**: Non-literal discriminants, partial discrimination, default case swallowing new variants.
- **Naming collisions**: A field or property name that means one thing in one context and something different in another — semantic collision, not style preference. These create confusion about which concept is being referenced and can lead to bugs when the wrong one is used. Only flag when the collision is genuinely ambiguous, not minor naming preferences. This is about type-level naming that creates ambiguity enabling bugs — a field name on a type that means two different things depending on context.

The core lens: push runtime checks into compile-time guarantees, and make invalid states unrepresentable.

## Language adaptation

These principles apply to all typed languages. Adapt patterns to the language in scope:

| Language | Config to check | Key concerns |
|----------|-----------------|--------------|
| **TypeScript** | `tsconfig.json` (strict, strictNullChecks, noImplicitAny) | any/unknown abuse, type assertions, discriminated unions |
| **Python** | mypy/pyright config, `py.typed` | Missing type hints, Any usage, Optional handling, TypedDict vs dataclass |
| **Java/Kotlin** | - | Raw types, unchecked casts, Optional misuse, sealed classes |
| **Go** | - | Interface{} abuse, type assertions without ok check, error handling |
| **Rust** | - | Unnecessary unwrap(), missing Result handling, lifetime issues |
| **C#** | nullable reference types setting | Null reference issues, improper nullable handling |

Skip generated files, vendored dependencies, and type stubs/declarations from external packages.

## Actionability filter

Before reporting a type safety issue, it must pass ALL of these. If a finding fails ANY criterion, drop it entirely.

1. **In scope** — Two modes:
   - *Diff-based review* (default): Report type issues introduced or exposed by a consumer path this change adds or extends. Name that path; unrelated pre-existing type holes are out of scope.
   - *Explicit path review* (caller specified paths): Audit everything in scope. Pre-existing type issues are valid findings.
2. **Worth the complexity** — Type-level gymnastics that hurt readability may not be worth it. Balance type safety gains against added complexity.
3. **Proportionate boundary** — Existing strictness and patterns inform the remedy, not whether a demonstrated type hole matters. Prefer a local type or boundary check that closes the concrete failure; demand no project-wide strictness migration merely for uniformity. Honor an explicit applicable project policy.
4. **Provably enables bugs** — Identify the specific code path where the type hole causes a real problem. "This could theoretically be wrong" isn't a finding.
5. **Concrete benefit** — Name the required guarantee the change loses and how the proposed remedy restores it; an imagined author's willingness to accept the change is not evidence.

### Practical balance

**Don't flag:**
- `any` in test files for mocking (unless excessive)
- Type assertions for well-understood DOM APIs
- `unknown` at system boundaries (external data, user input) with proper validation
- Simpler types in internal/private code when the complexity isn't worth it
- Framework-specific patterns that require certain type approaches

**Do flag:**
- `any` in business logic that could be typed
- Type assertions that bypass meaningful type checking
- Stringly-typed APIs for finite sets of values
- Missing discriminants in state machines
- `!` assertions without runtime justification

## Orthogonality — what belongs to other dimensions

Whether a null check is *correct at runtime* (will it crash?) belongs to the code-bugs dimension. This dimension focuses on whether the *type system* could catch it at compile time. Do not report:

- **Adequacy of a repair against its demonstrated failure mechanism** → the defect-class dimension, including whether proportionate prevention was omitted.
- **Intent-behavior divergence** (does the change achieve its goal?) → the change-intent dimension.
- **Mechanical code defects** (race conditions, resource leaks, runtime null handling) → the code-bugs dimension.
- **API contract correctness** (wrong params, consumer breakage) → the contracts dimension.
- **Code organization** (DRY, coupling, consistency) → the code-maintainability dimension. Maintainability's "consistency issues" covers naming convention violations across files (inconsistent casing, divergent naming patterns); type-safety's naming collisions are narrower: same name, same type, two meanings.
- **Over-engineering / complexity** → the code-simplicity dimension.
- **Semantic overloading of concepts** (an enum used for a purpose it wasn't designed for) → the code-design dimension's concept purity. Naming collisions are narrower than this.
- **Documentation accuracy** → the docs dimension.
- **Test coverage gaps** → the test-quality dimension.
- **Context file compliance** → the context-file-adherence dimension.

## Severity calibration

Use the shared ladder. A demonstrated type hole that admits wrong behavior is High or Critical by consequence, even for one caller or an unusual input. Missing type protection with a concrete must-fix quality cost is Medium. Annotation or naming taste without a type hole belongs to code-maintainability; a narrow trigger does not make a substantive type failure Low.

## Report expectations

Follow the shared report format. In addition, for this dimension:

- Tag each finding with its **category**: any/unknown | Invalid States | Narrowing | Generics | Nullability | Type Quality | Discriminated Unions | Naming Collision.
- Lead with an executive read: **how many bugs is the type system catching vs letting through?**
- Every Critical/High finding needs a concrete fix example (show the corrected type, not just prose); every other finding should include example code for the solution too.
- Note an **effort** estimate per finding: Quick win | Moderate refactor | Significant restructuring — a perfect type might not be worth a 500-line refactor.
- If you find excellent type patterns worth preserving or extending, note them.

### Example finding

```
#### [HIGH] Stringly-typed order status enables typos
**Category**: Invalid States Representable
**Location**: `src/orders/processor.ts:45-52`
**Description**: Order status uses raw strings, allowing typos to compile.
**Evidence**:
// Current: typos compile fine
function updateStatus(orderId: string, status: string) {
  if (status === 'pendng') { // typo undetected
    // ...
  }
}
**Trigger**: any caller of `updateStatus` passing a misspelled literal — `updateStatus(id, 'pendng')` in `src/orders/api.ts:88` compiles and silently matches no branch.
**Impact**: Status typos cause silent failures; adding new statuses doesn't trigger compile errors.
**Effort**: Quick win
**Suggested Fix**:
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
function updateStatus(orderId: OrderId, status: OrderStatus) { ... }
```

## Guidelines

- **Be practical**: Not every `any` is a crime. Focus on high-impact improvements.
- **Respect existing patterns**: If the codebase has conventions, suggest improvements that fit.
