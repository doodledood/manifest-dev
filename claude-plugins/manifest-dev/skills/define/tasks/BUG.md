# BUG Task Guidance

Task-specific guidance for bug fix deliverables: defect resolution, regression fixes, error handling corrections.

## Bug-Specific Interview Probes

Surface these dimensions that the general /define flow won't naturally cover:

- **Reproduction steps**: Exact sequence to trigger the bug. Without this, verification is impossible. Probe until steps are concrete and repeatable.
- **Expected vs actual**: What should happen? What happens instead? The delta defines the fix.
- **Environment specificity**: Version, OS, browser, config, data state. Bugs often only reproduce under specific conditions.
- **Error artifacts**: Logs, stack traces, error messages, screenshots. These narrow root cause investigation.
- **Recent changes**: What changed before the bug appeared? Commits, deploys, config changes. Bisect candidates.
- **Impact and workarounds**: Who's affected? How severely? Any temporary workarounds? Informs fix urgency and scope.
- **Related symptoms**: Other issues that might share the same root cause? Batch opportunities.

## Bug Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Regression prevention | code-bugs-reviewer | Fix doesn't introduce new bugs; no HIGH/CRITICAL |
| Root cause addressed | general-purpose | Fix addresses cause, not just symptom |
| Test coverage | code-coverage-reviewer | Regression test covers the fix |

**Encoding**: Add selected gates as Global Invariants with subagent verification:
```yaml
verify:
  method: subagent
  agent: [agent-name-from-table]
  prompt: "Review bug fix for [quality aspect]"
```

## Project Gates

Same as CODING.md—extract verifiable commands (typecheck, lint, test) from project configuration. Critical for bugs: existing tests must still pass.

## Bug-Specific Risks

These are bug fix failure modes the general pre-mortem won't surface:

- **Band-aid**: Symptom suppressed, root cause remains—bug will resurface or mutate
- **Whack-a-mole**: Fix introduces new bug elsewhere in the system
- **Incomplete fix**: Works for reported case, fails for related edge cases
- **Scope creep**: "While I'm here" refactoring that introduces risk without addressing the bug
- **Missing reproduction**: Fix applied without confirming bug was reproducible—can't verify it's actually fixed

## Bug-Specific Trade-offs

- **Minimal patch vs. proper fix**: Quick targeted change vs. addressing underlying design issue
- **Single bug vs. batch**: Fix this one vs. address related issues with same root cause
- **Speed vs. investigation depth**: Ship fast vs. understand root cause fully
- **Hotfix vs. release train**: Emergency deploy vs. wait for normal release cycle

## Bug-Specific AC Patterns

**Verification**
- "Bug no longer reproducible using original reproduction steps"
- "Regression test added that fails before fix, passes after"
- "Related edge cases [list] verified not affected"

**Root Cause**
- "Root cause identified and documented in commit/PR"
- "Fix addresses root cause, not symptom"
- "If band-aid chosen: tech debt ticket created for proper fix"

**Regression Safety**
- "Existing test suite passes"
- "No new warnings or errors introduced"
- "Functionality adjacent to fix verified unchanged"

## Bug-Specific Process Guidance Patterns

Encode relevant items as PG-*:

- "Reproduce bug locally before attempting fix—confirm reproduction steps work"
- "Write failing test BEFORE implementing fix (TDD for bugs)"
- "Keep fix minimal—resist urge to refactor unrelated code"
- "If root cause unclear after reasonable investigation, document uncertainty and ship minimal fix"
