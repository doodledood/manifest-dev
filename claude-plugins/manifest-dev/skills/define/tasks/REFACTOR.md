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

Consider these failure scenarios when probing:

- **Semantic drift** - behavior subtly changed but tests pass because they're also wrong; probe: do tests verify behavior or just lack of crashes?
- **Downstream breakage** - refactored code works but callers break; probe: what depends on this? Any implicit contracts?
- **Lost optimization** - cleaner code but performance regressed; probe: was there a reason for the "ugly" code?

## Trade-offs

- Incremental vs big bang
- Perfect structure vs good-enough
- Scope vs time
- Refactor now vs feature first
