# REFACTOR Task Guidance

Restructuring without behavior change.

## The Contract

Every refactor must establish:
1. What behavior is preserved (specific, verifiable)
2. How preservation is verified (tests, comparison)

Without both, refactoring is gambling.

## Interview Focus

- **Preserved behavior** - what exactly must not change
- **Verification method** - existing tests? characterization tests? If no tests, red flag
- **Scope boundaries** - what's in/out; refactors expand easily
- **Success criteria** - what "done" looks like; vague goals → endless refactoring

## Quality Gates

Use FEATURE.md table. Emphasize:
- **code-bugs-reviewer** - detect unintended behavior changes
- **code-maintainability-reviewer** - the point of refactoring
- **code-coverage-reviewer** - tests must cover preserved behavior

If no tests exist, probe: should "write characterization tests" be prerequisite?

## Risks

- **Behavior regression** - #1 risk; changed behavior disguised as cleanup
- **Scope creep** - "while I'm here" expansions
- **No verification** - refactoring without tests is hope
- **Vague goal** - "cleaner code" leads to endless churn

## Trade-offs

- Incremental vs big bang
- Perfect structure vs good-enough
- Scope vs time
- Refactor now vs feature first
