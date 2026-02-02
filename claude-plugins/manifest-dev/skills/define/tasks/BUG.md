# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Root Cause Verification

Fix must address cause, not symptom. Probe: what's the actual root cause vs. where the error surfaces?

## Risks

- **Missing reproduction** - can't verify fix without exact repro steps; probe: what's the sequence to trigger?
- **Environment-specific** - bug only appears under certain conditions; probe: version, OS, config, data state?
- **Band-aid** - symptom suppressed, root cause remains
- **Whack-a-mole** - fix introduces bug elsewhere
- **Incomplete fix** - works for reported case, fails edge cases

## Scenario Prompts

Consider these failure scenarios when probing:

- **Regression elsewhere** - fix works but breaks unrelated code that depended on buggy behavior; probe: what else calls this code?
- **Lurking root cause** - symptom fixed but underlying issue remains; probe: why did this bug exist in the first place?
- **Data corruption already happened** - bug fixed but bad data persists; probe: do we need migration or cleanup?

## Trade-offs

- Minimal patch vs proper fix
- Single bug vs batch related issues
- Speed vs investigation depth
- Hotfix vs release train
