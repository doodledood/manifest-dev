# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Quality Gates

Use FEATURE.md table. Emphasize:
- **code-bugs-reviewer** - fix must not introduce new bugs
- **code-coverage-reviewer** - regression test covers the fix

Add: root cause verification (fix addresses cause, not symptom).

## Risks

- **Missing reproduction** - can't verify fix without exact repro steps; probe: what's the sequence to trigger?
- **Environment-specific** - bug only appears under certain conditions; probe: version, OS, config, data state?
- **Band-aid** - symptom suppressed, root cause remains
- **Whack-a-mole** - fix introduces bug elsewhere
- **Incomplete fix** - works for reported case, fails edge cases

## Trade-offs

- Minimal patch vs proper fix
- Single bug vs batch related issues
- Speed vs investigation depth
- Hotfix vs release train
