# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

CLAUDE.md may specify project-specific preferences.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Bug detection | code-bugs-reviewer | no HIGH/CRITICAL |
| Type safety | type-safety-reviewer | no HIGH/CRITICAL |
| Maintainability | code-maintainability-reviewer | no HIGH/CRITICAL |
| Simplicity | code-simplicity-reviewer | no HIGH/CRITICAL |
| Test coverage | code-coverage-reviewer | no HIGH/CRITICAL |
| Testability | code-testability-reviewer | no HIGH/CRITICAL |
| Documentation | docs-reviewer | no MEDIUM+ |
| Design fitness | code-design-reviewer | no HIGH/CRITICAL |
| CLAUDE.md adherence | claude-md-adherence-reviewer | no HIGH/CRITICAL |

## Project Gates

CLAUDE.md specifies project gates (typecheck, lint, test, format). These become Global Invariants.

## E2E Verification

Before defaulting to manual E2E verification:
- **Test data** - often discoverable; probe: existing test users/accounts? can research via project tools (queries, test fixtures, admin panels)?
- **Environment** - probe: which environment for e2e tests (dev, staging, production read-only)?
- **Automation feasibility** - probe: can tests be scripted? existing health checks or testable endpoints?

Manual only when automated E2E is truly not feasible and user confirms no test data exists.

## Scenario Prompts

- **Silent regression** - behavior changes but tests pass; probe: behaviors not covered by tests?
- **Environment drift** - works locally, fails in CI/prod; probe: env-specific config, secrets, dependencies?
- **Performance cliff** - correct but slow at scale; probe: expected load? hot paths?
- **Security gap** - auth bypass, injection, data exposure; probe: user input? external data? permission checks?
- **Concurrency bug** - race condition, deadlock, lost update; probe: parallel access? shared state?
- **Dependency conflict** - version mismatch, breaking upgrade; probe: pinned versions? transitive deps?
- **Breaking implicit contract** - callers depend on undocumented behavior; probe: who calls this? what do they assume?
- **Error swallowed** - failure silent, no logging, bad state persists; probe: error paths tested? observability?
- **Config mismatch** - feature flags, env vars differ across environments; probe: config parity?
- **Observability blindspot** - works but can't tell when it breaks in prod; probe: metrics? alerts? logs?

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.
