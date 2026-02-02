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

- **Regression elsewhere** - fix breaks code depending on buggy behavior; probe: what else calls this?
- **Lurking root cause** - symptom fixed, cause remains; probe: why did this bug exist?
- **Data corruption persists** - bug fixed, bad data still there; probe: need migration/cleanup?
- **Wrong reproduction** - incomplete repro leads to wrong diagnosis; probe: exact steps to trigger?
- **Timing-dependent** - bug hides under different conditions; probe: load? timing? data volume?
- **Performance regression** - fix works but slower; probe: acceptable perf impact?
- **Edge case missed** - fix covers reported case, not variants; probe: other inputs that could trigger?
- **Multiple bugs masquerading** - one symptom, multiple causes; probe: is this definitely one bug?
- **Fix correct, tests wrong** - tests pass because they encoded bug; probe: do tests verify correct behavior?
- **Customer communication gap** - bug fixed, customer not informed; probe: who reported? need follow-up?
- **Recurrence likely** - same class of bug will happen again; probe: systemic fix possible?
- **Hotfix vs proper fix** - pressure to ship fast vs fix right; probe: acceptable to patch now, fix later?

## Trade-offs

- Minimal patch vs proper fix
- Single bug vs batch related issues
- Speed vs investigation depth
- Hotfix vs release train
