# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Interview Focus

Surface what the general flow won't:
- **Reproduction steps** - exact sequence to trigger; without this, can't verify fix
- **Expected vs actual** - the delta defines the fix
- **Environment** - version, OS, config, data state
- **Error artifacts** - logs, stack traces, screenshots
- **Recent changes** - commits, deploys before bug appeared
- **Impact/workarounds** - urgency and scope

## Quality Gates

Use FEATURE.md table. Emphasize:
- **code-bugs-reviewer** - fix must not introduce new bugs
- **code-coverage-reviewer** - regression test covers the fix

Add: root cause verification (fix addresses cause, not symptom).

## Risks

- **Band-aid** - symptom suppressed, root cause remains
- **Whack-a-mole** - fix introduces bug elsewhere
- **Incomplete fix** - works for reported case, fails edge cases
- **Missing reproduction** - can't verify fix without repro steps

## Trade-offs

- Minimal patch vs proper fix
- Single bug vs batch related issues
- Speed vs investigation depth
- Hotfix vs release train
