# REFACTOR Task Guidance

Restructuring without behavior change.

## The Contract

Every refactor must establish:
1. What behavior is preserved (specific, verifiable)
2. How preservation is verified (tests, comparison)

Without both, refactoring is gambling.

## Characterization Tests

If no tests exist, probe: should "write characterization tests" be prerequisite deliverable?

## Risks

- **Behavior regression** - changed behavior disguised as cleanup; probe: what exactly must not change?
- **No verification** - refactoring without tests is hope; probe: how will preservation be verified?
- **Scope creep** - "while I'm here" expansions; probe: what's explicitly in/out?
- **Vague goal** - "cleaner code" leads to endless churn; probe: what does done look like?

## Scenario Prompts

- **Semantic drift** - behavior subtly changed, tests pass anyway; probe: do tests verify behavior or just no crashes?
- **Downstream breakage** - refactored code works, callers break; probe: what depends on this? implicit contracts?
- **Lost optimization** - cleaner but slower; probe: was "ugly" code intentionally optimized?
- **Implicit contract broken** - undocumented behavior others relied on; probe: any callers outside this repo?
- **Test coverage gap** - refactor correct, tests insufficient to catch regression; probe: coverage adequate?
- **Parallel change conflict** - someone else editing same code; probe: any in-flight work touching this?
- **Rollback impossible** - refactor ships, can't easily undo; probe: incremental? feature-flaggable?
- **Migration stuck halfway** - incremental refactor abandoned mid-way; probe: what's the completion path?
- **Abstraction premature** - new abstraction doesn't fit future needs; probe: confident this is the right shape?
- **Scope creep** - "while I'm here" expands endlessly; probe: what's explicitly in/out of scope?
- **Characterization gap** - no tests to capture current behavior; probe: need to write tests first?
- **Review burden** - change too large to review effectively; probe: can this be split?

## Trade-offs

- Incremental vs big bang
- Perfect structure vs good-enough
- Scope vs time
- Refactor now vs feature first
