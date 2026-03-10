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
- **Scope creep** - "while I'm here" expansions; probe: what's explicitly in/out?
- **Vague goal** - "cleaner code" leads to endless churn; probe: what does done look like?

## Scenario Prompts

- **Semantic drift** - behavior subtly changed, tests pass anyway; probe: do tests verify behavior or just no crashes?
- **Lost optimization** - cleaner but slower; probe: was "ugly" code intentionally optimized?
- **Implicit contract broken** - undocumented behavior others relied on; probe: any callers outside this repo?
- **Parallel change conflict** - someone else editing same code; probe: any in-flight work touching this?
- **Rollback impossible** - refactor ships, can't easily undo; probe: incremental? feature-flaggable?
- **Migration stuck halfway** - incremental refactor abandoned mid-way; probe: what's the completion path?
- **Abstraction premature** - new abstraction doesn't fit future needs; probe: confident this is the right shape?
- **Review burden** - change too large to review effectively; probe: can this be split?

## Trade-offs

- Incremental vs big bang
- Perfect structure vs good-enough
- Scope vs time
- Refactor now vs feature first

## Defaults

*Domain best practices for this task type.*

- **Verification plan** — How behavior preservation is verified (existing tests, characterization tests, comparison). Every refactor needs this before starting
- **Identify consumers** — All callers and dependents of refactored code identified; implicit contracts surfaced
- **Assess test coverage** — Coverage adequate for the refactored area; characterization tests written if gaps exist
