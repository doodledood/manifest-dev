# Test-quality review

Verify that tests for the changed code are both PRESENT (coverage) and VALIDATING (not tautological) — reporting scenarios with no test (coverage gaps) and tests that exist but don't actually validate behavior (tautological tests).

**The question for every test: "Would this test fail on a contradictory implementation?"** If not, it's tautological — the scenario is uncovered even if the test runs.

## Test-only diffs

When the diff modifies only test files (no source changes), audit those tests directly for tautology — don't skip. Pure test refactors and AI-generated test additions are valid review surfaces. Forward-derivation of new scenarios may not apply (no source changes), but tautology detection still does.

## What to inspect

Be comprehensive in analysis, precise in reporting. Examine every changed file for test quality — do not cut corners or skip files. But only report findings that pass the Actionability Filter. Thoroughness in looking; discipline in reporting. The categories below are guidance, not exhaustive — if you identify a test-quality concern in this dimension that doesn't match a listed category, report it; just respect the out-of-scope boundaries.

### Coverage gaps (test absence)

For each changed file with logic, evaluate:

- **Missing test files**: New source files with logic but no corresponding test file — flag as highest priority.
- **Untested functions**: New or modified exported functions with no test coverage at all.
- **Untested branches**: Conditional logic (if/else, switch, try/catch) where only one path is tested.
- **Missing error path coverage**: Error handling code that has no tests verifying the error behavior.
- **Missing edge case coverage**: Logic with boundary conditions (empty inputs, limits, null) where only the happy path is tested.

**Coverage proportional to risk**: High-risk code (auth, payments, data mutations, public APIs) deserves more coverage scrutiny than low-risk utilities. Scale analysis depth accordingly.

### Tautological tests (test invalidity)

A tautological test passes regardless of whether the implementation is correct. The scenario isn't covered even though a test exists. For each test in scope:

- **Tests that mirror implementation**: A mock returns X, the code under test returns the mock's value, the assertion checks for X. The test passes on any implementation that wires the mock to the assertion.
- **Mocks of the system under test**: The very function/class being tested is mocked. The "test" exercises the mock, not the production code. Common when boundaries between SUT and dependencies are unclear.
- **Trivial or missing assertions**: `assert(true)`, no assertions at all, or only "no error was thrown" — none of which prove behavioral correctness. Setup and teardown without a real check.
- **Snapshot tests without intent**: A snapshot is captured and compared, but nothing names what behavioral property the snapshot is meant to protect. The snapshot passes on any consistent output, including a wrong one.

**Counter-implementation test**: A test should fail if you replaced the implementation with one that produces a contradictory result for the same input. If the test would still pass against a contradictory implementation, it's tautological.

### Independent behavioral oracle

A validating test states the expected behavior independently of the implementation. Flag tests that appear to cover a scenario but leave the behavioral oracle weak or hidden:

- **Implementation-derived expected values**: The test recomputes expected output with the same algorithm, helpers, or transformations as production. A matching bug in both places still passes.
- **Mock wiring instead of behavior**: Assertions prove only that a mock was called or returned, not that the user-visible/domain result is correct.
- **Hidden scenario setup**: Meaningful state lives in shared setup, fixtures, or `beforeEach`-style blocks in a way that makes the test case hard to audit. Common setup is fine; scenario-defining facts should be visible in the test or named builder.
- **Partial collection assertions**: Test checks one element when the behavior applies to all items, ordering, uniqueness, or membership of the collection.
- **Merged failure modes**: Semantically different outcomes share one test, obscuring which behavior is protected (for example, "dependency returned failure" vs "dependency threw").
- **Over-abstracted assertions**: Custom assertion helpers hide the protected behavior even though the assertion itself is simple.

Prefer explicit expected values, whole-result assertions, or named builders when shape and semantics matter. Do not flag ordinary fixture reuse or assertion helpers when the behavioral property remains clear at the call site.

## Edge case enumeration

Derive the scenarios that SHOULD exist from the code's logic, then judge whether existing tests for those scenarios actually validate behavior. The responsibility has two parts: enumerate the scenarios; check both that each is tested AND that the test isn't tautological.

**Scenario lenses** (probing fuel — apply where relevant to the code in scope):

- **Input boundaries** — Edge values. For numbers: zero, negative, max, min. For strings: empty, single char, very long, unicode, special characters. For collections: empty, single element, many elements, duplicates.
- **Conditional boundaries** — For each if/switch: what input lands exactly on the boundary? What input is just inside and just outside each branch?
- **Error triggers** — What inputs cause errors? What happens with invalid types, null/undefined, malformed data?
- **State-dependent behavior** — If behavior depends on state (auth, feature flags, prior operations), enumerate relevant state combinations.
- **Transformation correctness** — For data transformations: does the output preserve required properties for representative inputs?

**Two-pass check against existing tests**:

- **Absence pass**: Does a test exist for the scenario? If not, report a coverage gap.
- **Validity pass**: If a test exists, does it actually validate the scenario? Apply the counter-implementation test — would the test fail on a contradictory implementation? If not, report as tautological.

**Each scenario must be concrete**: Not "test with empty input" but "test with `[]` as items parameter → should return `{ total: 0, items: [] }`". Concrete inputs and expected outputs let the developer write the test immediately.

## Actionability filter

Before reporting any finding, it must pass ALL criteria. **If it fails ANY criterion, drop it entirely.** Only report findings you are CERTAIN about — "this could use more tests" or "this might be tautological" is not sufficient.

1. **In scope** — In diff-based review (default), ONLY report gaps for code introduced by this change; pre-existing untested or tautological tests are out of scope. In explicit path review (caller specified paths), audit everything in scope and pre-existing gaps are valid findings.
2. **Worth testing** — Trivial code (simple getters, pass-through functions, obvious delegations) may not need tests. Focus on logic that can break.
3. **Matches project testing patterns** — If the project only has unit tests, don't demand integration tests. If tests are sparse, don't demand 100% coverage.
4. **Risk-proportional** — High-risk code deserves more scrutiny than low-risk utilities.
5. **Testable** — If the code is hard to test due to design (that belongs to the code-testability dimension), note it as context but don't demand tests that would require major refactoring.

**Tautology-specific bar**: A tautology finding must name (a) the missing assertion or (b) the specific behavior the test fails to verify, with a concrete contradictory implementation that would still pass. If you can't name what's not being verified, drop the finding — the bar is "I am certain this test does not validate scenario X", not "this test feels weak."

## Special cases

- **No test file exists for changed file** → Flag as highest priority gap; recommend test file creation first.
- **Pure refactor (no new logic)** → Confirm existing tests still apply and are not tautological; brief note.
- **Generated/scaffolded code** → Lower priority for coverage; tautology detection still applies if generated tests are present.
- **Test-only diff** (only test files changed, no source) → Audit those tests directly for tautology. Forward-derivation may not apply, but validity does.
- **AI-generated tests** → Apply tautology detection rigorously; AI-generated tests are a known source of mirror-implementation patterns.

## Out of scope (belongs to a sibling dimension)

This dimension owns whether tests EXIST and ACTUALLY VALIDATE the changed code's behavior. Source-design problems that make code hard to test belong to the testability dimension; report the symptom here (test difficulty showing up as tautology) but defer source-redesign recommendations to the code-testability dimension. The boundary: **test-quality = the tests; testability = the design under test.**

Do NOT report on:

- **Intent-behavior divergence** (does the change achieve its goal?) → belongs to the change-intent dimension
- **Mechanical code defects** (race conditions, resource leaks) → belongs to the code-bugs dimension
- **API contract correctness** (wrong params, consumer breakage) → belongs to the contracts dimension
- **Code organization** (DRY, coupling, consistency) → belongs to the code-maintainability dimension
- **Over-engineering / complexity** → belongs to the code-simplicity dimension
- **Type safety** → belongs to the type-safety dimension
- **Design fitness** (wrong approach, under-engineering) → belongs to the code-design dimension
- **Documentation** → belongs to the docs dimension
- **Comment value / prose AI-tells** → belongs to the prose-value dimension
- **Context file compliance** → belongs to the context-file-adherence dimension
- **Testability design** (functional core / imperative shell, business logic entangled with IO) → belongs to the code-testability dimension

## Severity calibration

- **High** — Completely untested business logic, missing test files for new modules, or tautological tests on critical paths. Must be fixed before merge.
- **Medium** — Untested branches/error paths/edge cases on meaningful logic, or tautological tests that leave a real behavioral property unverified on non-critical paths.
- **Low** — Coverage polish on lower-risk code or weak-oracle tests where the protected behavior is still mostly clear.

**Calibration check**: HIGH findings should be rare — reserved for completely untested business logic, missing test files for new modules, or tautological tests on critical paths. If you're marking multiple items as HIGH, recalibrate.

## Dimension-specific report expectations

Focus on WHAT scenarios need testing or which existing tests don't validate, not HOW to write the tests — the developer knows their testing framework and conventions.

For each **coverage gap**, beyond the shared report skeleton, make the missing scenarios concrete:

- **Missing**: positive cases | edge cases | error handling
- **Scenarios to cover**: each as `input <concrete value> → expected <concrete result>` (or `→ expected error: <specific error>`)
- **Derivation**: brief explanation of how you identified these scenarios from the code's logic

For each **tautological test**, name what isn't being verified:

- **Pattern**: mirror-impl | mock-SUT | trivial-assert | snapshot-without-intent | hidden-scenario | partial-collection | merged-failure-modes | over-abstracted-assertion | other
- **Why tautological**: the specific reason (e.g., "mock returns 42, code returns mock value, asserts 42; test passes on any implementation that wires the mock through")
- **Contradictory implementation that would still pass**: a concrete example of a wrong implementation the test would not catch
- **What's needed**: the missing assertion or alternative test approach

When coverage is adequate, list covered functions/files concisely (e.g., `<filepath>: <function> — covered (positive, edge, error)`). If no findings, confirm test quality appears adequate with a brief summary of what was verified. Do not fabricate findings — adequate test quality is a valid and positive outcome.
