# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Root Cause Verification

Fix must address cause, not symptom. Probe: what's the actual root cause vs. where the error surfaces?

## Risks

- **Environment-specific** - bug only appears under certain conditions; probe: version, OS, config, data state?
- **Incomplete fix** - works for reported case, fails edge cases

## Scenario Prompts

- **Data corruption persists** - bug fixed, bad data still there; probe: need migration/cleanup?
- **Timing-dependent** - bug hides under different conditions; probe: load? timing? data volume?
- **Performance regression** - fix works but slower; probe: acceptable perf impact?
- **Edge case missed** - fix covers reported case, not variants; probe: other inputs that could trigger?
- **Multiple bugs masquerading** - one symptom, multiple causes; probe: is this definitely one bug?
- **Customer communication gap** - bug fixed, customer not informed; probe: who reported? need follow-up?
- **Recurrence likely** - same class of bug will happen again; probe: systemic fix possible?
- **Hotfix vs proper fix** - pressure to ship fast vs fix right; probe: acceptable to patch now, fix later?
- **Scope variation missed** - bug fixed for reported case, not other affected scopes; probe: other configurations, user segments, or contexts where this could manifest differently?

## Trade-offs

- Minimal patch vs proper fix
- Single bug vs batch related issues
- Speed vs investigation depth
- Hotfix vs release train

## Defaults

*Domain best practices for this task type.*

- **Establish reproduction** — Exact repro steps before attempting any fix; verify repro is complete and correct
- **Root cause, not symptoms** — Verify fix addresses root cause, not symptom suppression
- **Regression check** — Identify all callers/dependents of changed code; verify no behavioral regression from the fix
- **Test correctness** — Verify existing tests assert correct behavior, not the buggy behavior
