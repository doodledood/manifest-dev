# Code-testability review

Audit the change for testability friction — code where important logic is difficult to verify in isolation because it requires excessive mocking, is entangled with IO, or depends on non-deterministic inputs — and suggest ways to reduce that friction.

This dimension audits whether code is **designed** to be testable, not whether tests exist or are good — that is the test-quality dimension. Keep the line sharp: testability = design that makes testing hard; test-quality = the tests themselves.

## What makes code hard to test

Code becomes hard to test when you can't verify its behavior without complex setup. The primary indicators:

1. **High mock count** — Needing disproportionately many mocks relative to the function's complexity and codebase norms.
2. **Logic buried in IO** — Business rules that can only be exercised by calling databases/APIs.
3. **Non-deterministic inputs** — Behavior depends on current time, random values, or external state.
4. **Unrelated dependencies required** — Can't test the code without mocking components irrelevant to the behavior being verified.

| Test Friction | Consequence |
|---------------|-------------|
| High mock count | Tests break on refactors, edge case testing requires repetitive setup |
| Logic buried in IO | Edge cases don't get tested → bugs ship |
| Non-deterministic | Tests are flaky or require complex freezing/seeding |
| Tight coupling | Tests are slow, brittle, and test more than they should |

## Detection categories

**Be comprehensive in analysis, precise in reporting.** Examine every file in scope against every applicable category — do not cut corners or skip areas. Only report findings that meet the high-confidence bar in the Actionability Filter. Thoroughness in looking; discipline in reporting.

These categories are guidance, not exhaustive. If you identify a testability issue that fits this dimension but doesn't match a listed category, report it — just respect the Out of Scope boundaries to maintain orthogonality.

**High test friction (Critical/High severity)**
- **Core logic requiring many mocks** — Important business logic (pricing, validation, permissions, eligibility) that can't be tested without mocking multiple external services. Each edge case needs all mocks set up.
- **IO in loops** — Database/API calls inside iteration, forcing mock setup per iteration.
- **Deep mock chains** — Mocks returning mocks, creating brittle test setup even with few top-level dependencies.

**Moderate test friction (Medium severity)**
- **Constructor IO** — Classes that connect to services or fetch data in constructors, preventing simple instantiation.
- **Hidden singleton dependencies** — Functions that import and use global instances, requiring global mock setup.
- **Non-deterministic inputs** — Logic depending on current time, random values, or real timers (note: complex control flow itself is a simplicity concern; here the concern is non-determinism).
- **Side effects mixed with return values** — Functions that both return a value and mutate external state, requiring tests to verify both.

**Low test friction (often acceptable)**
- Logging statements (usually side-effect free).
- 1–2 mocks for orchestration/controller code (expected to have some IO).
- Framework-required patterns (React hooks, middleware chains have inherent IO patterns).

## Codebase adaptation

Before flagging issues, observe existing project patterns:

- **Testing philosophy**: Does the project favor unit tests with mocks, integration tests, or end-to-end? Calibrate expectations accordingly.
- **Dependency injection**: If the project uses a DI framework (Nest.js, Spring, etc.), multiple constructor parameters may be idiomatic. Focus on whether important logic is testable, not raw dependency count.
- **Mocking conventions**: Note the project's mocking approach. Recommend solutions compatible with existing patterns.
- **Language idioms**: Adapt recommendations to the language's testing conventions.
- **Existing similar code**: If similar code elsewhere follows a testable pattern, reference it. If the codebase consistently uses a less-testable pattern, note friction but acknowledge the consistency tradeoff.

## Actionability filter

Before reporting an issue, it must pass ALL criteria. **If it fails ANY, drop it entirely.** Only report issues you are CERTAIN about.

1. **In scope** — Only report issues in changed/specified code. (Note: tests are expected to have mocks — skip test files.)
2. **Significant friction** — Not just normal orchestration-level mocking.
3. **Important logic** — Business rules that matter if they break (pricing, auth, validation).
4. **Concrete benefit** — You can articulate exactly how testing becomes easier.
5. **High confidence** — You are CERTAIN this is a testability issue, not a guess.

## Out of scope (orthogonality boundaries)

Do NOT report on (owned by other dimensions):
- **Intent-behavior divergence** (does the change achieve its goal?) → the change-intent dimension
- **Code duplication** (DRY violations) → the code-maintainability dimension
- **Over-engineering** (premature abstraction) → the code-simplicity dimension
- **Type safety** (any abuse, invalid states) → the type-safety dimension
- **Test coverage gaps** (missing tests, weak assertions, the tests themselves) → the test-quality dimension
- **Mechanical code defects** (race conditions, resource leaks) → the code-bugs dimension
- **API contract correctness** (wrong params, consumer breakage) → the contracts dimension
- **Documentation** (stale comments) → the docs dimension
- **Context file compliance** → the context-file-adherence dimension

**Key distinction from test-quality:** this dimension owns the *design that makes testing hard* (mock friction, IO-buried logic, non-determinism, tight coupling). The test-quality dimension owns the *tests themselves* (coverage gaps, assertion quality). Focus exclusively on whether code is **designed** to be testable, not whether tests exist or how good they are.

## Severity calibration (this dimension)

Severity = **importance of the logic** × **amount of test friction relative to codebase norms**.

- **Critical**: Core business logic (pricing, permissions, validation) requiring significantly more mocks than comparable code in the codebase. Functions where edge cases are important but practically untestable. IO inside loops with data-dependent iteration count.
- **High**: Important logic requiring notably more test setup than similar functions. Business rules buried after multiple IO operations with no extractable pure function. Constructor IO in frequently-instantiated classes (unless a DI framework makes this trivial).
- **Medium**: Logic that could be extracted but test friction is moderate. Time/date dependencies in business logic. Hidden singleton dependencies that complicate test setup.
- **Low**: Minor test friction in non-critical code. Could be slightly more testable but acceptable as-is.

**Calibration check**: Critical issues should be rare. If you're flagging multiple Critical items, verify each truly has important logic that's practically untestable. Consider what's normal for this codebase.

## Report expectations (this dimension)

Beyond the shared report format, each finding should carry:
- **Test friction**: number of mocks required and what they are.
- **Logic at risk**: what business rules/behavior is hard to test.
- **Why this matters**: concrete explanation of the testing difficulty and its consequence for THIS code.
- **Suggestion**: how to reduce test friction. **Prefer extracting pure functions** as the primary recommendation — a pure function takes the data it needs as parameters and can be tested exhaustively with simple inputs while a thin shell fetches data and calls it. Alternatives: passing dependencies as parameters, leveraging the project's DI patterns, or accepting the friction with rationale if the tradeoff is reasonable.

Example finding:

```
#### [HIGH] Discount calculation requires many mocks to test
**Location**: `src/services/order-service.ts:45-78`
**Test friction**: 3 mocks (db.orders, db.customers, db.promotions)
**Logic at risk**: Discount stacking rules (premium tier + promo + bulk discount)

**Why this matters**: Discount edge cases (premium customer with promo code on large order)
are important to verify but require setting up all 3 mocks correctly for each test case.
This makes thorough testing tedious, so edge cases likely won't be covered.

**Suggestion**: Extract the discount calculation into a pure function that takes the
data it needs as parameters. The pure function can be tested exhaustively with simple
inputs. The shell function fetches data and calls the pure function.
```

When no issues clear the bar, that is a valid, positive outcome — the code in scope has acceptable testability, with business logic already testable in isolation or test friction proportionate to complexity. Do not fabricate issues to fill the report.

## Guidelines

- **Ground issues in impact**: explain WHY the friction matters for THIS code.
- **Suggest, don't mandate**: offer ways to improve; acknowledge when tradeoffs are acceptable.
- **Prefer pure functions**: when suggesting improvements, favor extracting pure functions; acknowledge alternatives that fit the project's patterns.
- **Adapt to the codebase**: what's excessive in one project may be normal in another. Calibrate to local norms.
- **Shell code gets a pass**: controller/orchestration code is expected to do IO — focus on whether important logic is extractable.
- **Every Critical/High issue must explain why the logic is important to test.**
- Statistics must match detailed findings.

## Handling ambiguity

- If you can't tell whether logic is important enough to matter when it breaks, lean toward not reporting.
- If the friction is proportionate to the code's genuine complexity, it isn't a finding.
- **The bar for reporting is certainty, not suspicion.** An empty report is better than one with false positives.
