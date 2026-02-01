# FEATURE Task Guidance

New functionality: features, APIs, enhancements.

## Quality Gates

Surface which matter for this task. Check CLAUDE.md for project-specific preferences.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Bug detection | code-bugs-reviewer | no HIGH/CRITICAL |
| Type safety | type-safety-reviewer | no HIGH/CRITICAL |
| Maintainability | code-maintainability-reviewer | no HIGH/CRITICAL |
| Simplicity | code-simplicity-reviewer | no HIGH/CRITICAL |
| Test coverage | code-coverage-reviewer | no HIGH/CRITICAL |
| Testability | code-testability-reviewer | no HIGH/CRITICAL |
| Documentation | docs-reviewer | no MEDIUM+ |
| CLAUDE.md adherence | claude-md-adherence-reviewer | no HIGH/CRITICAL |

## Project Gates

Extract from CLAUDE.md: typecheck, lint, test, format commands. These become Global Invariants.

## E2E Verification

Probe for testable endpoints, health checks, test data. If actionable, encode as Global Invariant.

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.

## Risks

- **Scope creep** - feature expands beyond original intent
- **Breaking consumers** - changes to API, DB schema, config break downstream; probe: who consumes this?
- **Missing edge cases** - happy path works, edge cases crash
- **Security blind spot** - auth, user data, external input not reviewed
- **Silent production failure** - works in dev, no observability in prod

## Trade-offs

- Scope vs time
- Flexibility vs simplicity
- Feature completeness vs ship date
- New abstraction vs inline solution
