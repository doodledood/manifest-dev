# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Quality Gates

No additional quality gates beyond CODING.md base.

## Risks

- **Environment-specific** - bug only appears under certain conditions (version, OS, config, data state, timing, load); probe: reproduction conditions?
- **Incomplete fix** - works for reported case, fails edge cases

## Scenario Prompts

- **Data corruption persists** - bug fixed, bad data still there; probe: need migration/cleanup?
- **Performance regression** - fix works but slower; probe: acceptable perf impact?
- **Edge case missed** - fix covers reported case, not variants; probe: other inputs, configurations, user segments, or contexts that could trigger?
- **Multiple bugs masquerading** - one symptom, multiple causes; probe: is this definitely one bug?
- **Hotfix vs proper fix** - pressure to ship fast vs fix right; probe: acceptable to patch now, fix later?

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
- **Systemic fix assessment** — Identify the class of bug; probe whether a pattern fix prevents recurrence
