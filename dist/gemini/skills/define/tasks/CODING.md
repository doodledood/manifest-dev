# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

GEMINI.md may specify project-specific preferences.

### Base Gates (always applicable)

Defect-finding agents use `no LOW+` — every verified defect is worth fixing. Quality/advisory agents use `no MEDIUM+` — their Low findings are acceptable trade-offs.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Intent analysis | change-intent-reviewer | no LOW+ |
| Mechanical bug detection | code-bugs-reviewer | no LOW+ |
| Maintainability | code-maintainability-reviewer | no MEDIUM+ |
| Simplicity | code-simplicity-reviewer | no MEDIUM+ |
| Test coverage | code-coverage-reviewer | no MEDIUM+ |
| Testability | code-testability-reviewer | no MEDIUM+ |
| Documentation | docs-reviewer | no MEDIUM+ |
| Design fitness | code-design-reviewer | no MEDIUM+ |
| GEMINI.md adherence | context-file-adherence-reviewer | no MEDIUM+ |

### Conditional Gates (when applicable)

| Aspect | Agent | Threshold | Condition |
|--------|-------|-----------|-----------|
| Contract correctness | contracts-reviewer | no LOW+ | When code calls external/internal APIs, changes public interfaces, or crosses service boundaries |
| Type safety | type-safety-reviewer | no LOW+ | When using typed languages (TypeScript, Python with type hints, Java/Kotlin, Go, Rust, C#) |

## Project Gates

GEMINI.md specifies project gates (typecheck, lint, test, format). These become Global Invariants.

## E2E Verification

E2E verification encodes as Global Invariants (INV-G*), not as deliverable ACs or separate deliverables. E2E verifies the system works end-to-end — it's a constitutional constraint, not per-deliverable success criteria.

Each e2e test case gets its own INV-G*. Together, the set of e2e invariants represents the complete e2e testing plan (e.g., INV-G5: login flow, INV-G6: order creation, INV-G7: checkout flow).

E2e tests are slow and often deploy-dependent — assign them a later phase than fast automated checks (lint, tests, code review agents). Manual e2e should be in an even later phase (human-dependent, slowest iteration). Only use manual when automated E2E is truly not feasible and user confirms no test data exists.

Before encoding e2e invariants, probe:
- **Test data** - often discoverable; probe: existing test users/accounts? can research via project tools (queries, test fixtures, admin panels)?
- **Environment** - probe: which environment for e2e tests (dev, staging, production read-only)?
- **Automation feasibility** - probe: can tests be scripted? existing health checks or testable endpoints?

When probing yields actionable findings, encode each test case as an INV-G*. Each should specify the scenario and expected outcome (e.g., "INV-G5: E2E login flow — POST /auth/login returns 200 with valid credentials on staging").

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
