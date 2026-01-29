# REFACTOR Task Guidance

Restructuring without behavior change.

## The Contract

Every refactor must establish:
1. What behavior is preserved (specific, verifiable)
2. How preservation is verified (tests, comparison)

Without both, refactoring is gambling.

## Quality Gates

Use FEATURE.md table. Emphasize:
- **code-bugs-reviewer** - detect unintended behavior changes
- **code-maintainability-reviewer** - the point of refactoring
- **code-coverage-reviewer** - tests must cover preserved behavior

If no tests exist, probe: should "write characterization tests" be prerequisite?

## Risks

- **Behavior regression** - changed behavior disguised as cleanup; probe: what exactly must not change?
- **No verification** - refactoring without tests is hope; probe: how will preservation be verified?
- **Scope creep** - "while I'm here" expansions; probe: what's explicitly in/out?
- **Vague goal** - "cleaner code" leads to endless churn; probe: what does done look like?

## Trade-offs

- Incremental vs big bang
- Perfect structure vs good-enough
- Scope vs time
- Refactor now vs feature first
