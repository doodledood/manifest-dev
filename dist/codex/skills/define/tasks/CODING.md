# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

AGENTS.md may specify project-specific preferences.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Bug detection | code-bugs-reviewer | no MEDIUM+ |
| Type safety | type-safety-reviewer | no MEDIUM+ |
| Maintainability | code-maintainability-reviewer | no MEDIUM+ |
| Simplicity | code-simplicity-reviewer | no MEDIUM+ |
| Test coverage | code-coverage-reviewer | no MEDIUM+ |
| Testability | code-testability-reviewer | no MEDIUM+ |
| Documentation | docs-reviewer | no MEDIUM+ |
| Design fitness | code-design-reviewer | no MEDIUM+ |
| AGENTS.md adherence | context-file-adherence-reviewer | no MEDIUM+ |

## Project Gates

AGENTS.md specifies project gates (typecheck, lint, test, format). These become Global Invariants.

## E2E Verification

E2E verification encodes as ACs on the relevant deliverable(s), not as a separate deliverable or process guidance. E2E is verification of the work, not work itself.

Before encoding e2e ACs, probe:
- **Test data** - often discoverable; probe: existing test users/accounts? can research via project tools (queries, test fixtures, admin panels)?
- **Environment** - probe: which environment for e2e tests (dev, staging, production read-only)?
- **Automation feasibility** - probe: can tests be scripted? existing health checks or testable endpoints?

When probing yields actionable findings, encode as ACs on the deliverable being verified. Each e2e AC should specify the test scenario and expected outcome (e.g., "AC-1.4: POST /api/orders returns 201 with valid payload on staging").

Manual verification only when automated E2E is truly not feasible and user confirms no test data exists.

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
- **E2E verification gap** - unit gates pass, integration fails; probe: integration points without test coverage? cross-service dependencies?

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.
