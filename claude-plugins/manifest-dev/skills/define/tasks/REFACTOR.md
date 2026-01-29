# REFACTOR Task Guidance

Task-specific guidance for restructuring: code reorganization, pattern changes, architecture shifts—without behavior change.

## The Refactor Contract

**Behavior must not change.** This is the defining constraint. Every refactor interview must establish:
1. What behavior is being preserved (the contract)
2. How preservation will be verified (the gate)

Without both, refactoring is gambling.

## Refactor-Specific Interview Probes

Surface these dimensions that the general /define flow won't naturally cover:

- **Preserved behavior**: What exact behavior must remain unchanged? Be specific—"the API" is too vague, "GET /users returns same response shape" is verifiable.
- **Verification method**: How will you prove behavior is preserved? Existing tests? New characterization tests? Manual comparison? If no tests exist, this is a red flag—probe whether writing tests first is in scope.
- **Scope boundaries**: What's in scope for restructuring? What's explicitly out of scope? Refactors expand easily—define the fence.
- **Success criteria**: What does "done" look like? Cleaner structure? Better performance? Easier testing? Vague goals lead to endless refactoring.
- **Incremental strategy**: One big change or series of small changes? Each approach has different risk profiles.

## Quality Gates

Use FEATURE.md quality gates table. For refactors, emphasize:
- **code-bugs-reviewer**: Critical—must detect unintended behavior changes
- **code-maintainability-reviewer**: The point of refactoring—should show improvement
- **code-coverage-reviewer**: Tests must cover preserved behavior

**Critical gate**: If no tests verify the preserved behavior, probe whether "write characterization tests" should be a prerequisite deliverable.

## Project Gates

Same as FEATURE.md. For refactors, passing tests is THE critical gate—proof behavior is preserved.

## Refactor-Specific Risks

These are refactor failure modes the general pre-mortem won't surface:

- **Behavior regression**: The #1 risk. Changed behavior disguised as "cleanup"
- **Scope creep**: "While I'm here" expansions that introduce risk without clear value
- **No verification**: Refactoring without tests is hope-driven development
- **Refactor for its own sake**: No clear goal, just "cleaner code"—leads to endless churn
- **Big bang**: Large refactor that's hard to review, hard to revert, hard to bisect

## Refactor-Specific Trade-offs

- **Incremental vs big bang**: Small safe PRs vs one complete restructure
- **Perfect structure vs good-enough**: Ideal architecture vs pragmatic improvement
- **Scope vs time**: Comprehensive refactor vs focused high-value changes
- **Refactor now vs feature first**: Clean up before or after the feature lands

## Refactor-Specific AC Patterns

**Preservation**
- "All existing tests pass without modification"
- "API contract unchanged: [specific endpoints/signatures]"
- "Characterization tests added before refactor, pass after"

**Structural Goals**
- "Module X extracted from monolith Y"
- "Pattern Z applied consistently across [scope]"
- "Coupling between A and B reduced: [metric or description]"

**Verification**
- "Diff reviewed for unintended behavior changes"
- "No new warnings or errors introduced"
- "Performance baseline maintained: [metric]"

## Refactor-Specific Process Guidance Patterns

Encode relevant items as PG-*:

- "If no tests cover the behavior being preserved, write characterization tests BEFORE refactoring"
- "Make structural changes in separate commits from any behavior changes"
- "When in doubt about scope, smaller is safer—additional refactoring can follow"
- "If refactor goal is vague ('clean up'), clarify specific structural outcome before starting"
