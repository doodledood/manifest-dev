# CODING Task Guidance

Task-specific guidance for code deliverables: features, APIs, fixes, refactors, tests.

## Code Quality Gates

Surface which quality aspects matter. Mark recommended defaults based on task context.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Bug detection | code-bugs-reviewer | no HIGH/CRITICAL |
| Type safety | type-safety-reviewer | no HIGH/CRITICAL |
| Maintainability | code-maintainability-reviewer | no HIGH/CRITICAL |
| Simplicity | code-simplicity-reviewer | no HIGH/CRITICAL |
| Test coverage | code-coverage-reviewer | no HIGH/CRITICAL |
| Testability | code-testability-reviewer | no HIGH/CRITICAL |
| Documentation | docs-reviewer | no MEDIUM+ (max severity is MEDIUM) |
| CLAUDE.md adherence | claude-md-adherence-reviewer | no HIGH/CRITICAL |

**Filter through project preferences**: CLAUDE.md is auto-loaded into context—check it for quality gate preferences. Users may have disabled certain default gates (e.g., "skip documentation checks") or added custom ones (e.g., "always run security scan"). Exclude disabled gates from the selection, and include any custom gates the user has defined.

**Encoding**: Add selected quality gates as Global Invariants with subagent verification:
```yaml
verify:
  method: subagent
  agent: [agent-name-from-table]
  prompt: "Review for [quality aspect] issues in the changed files"
```

## Project Gates

Extract verifiable commands from project configuration (typecheck, lint, test, format). Add as Global Invariants with bash verification:
```yaml
verify:
  method: bash
  command: "[command from CLAUDE.md]"
```

## E2E Verification

Probe for testable endpoints, health checks, test data. If actionable, encode as Global Invariant with bash verification.

## Coding-Specific AC Patterns

**Functional**
- "API endpoint X returns Y when Z"
- "Clicking [element] triggers [behavior]"
- "Function handles [edge case] by [behavior]"

**Non-Functional**
- "Response time < Nms"
- "Memory usage stays below X"
- "All handlers follow [Pattern] pattern"

**Process**
- "Changelog entry added"
- "Migration script included"
- "README updated with new usage"
