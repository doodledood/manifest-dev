# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

CLAUDE.md may specify project-specific preferences.

### Base Gates (always applicable)

Defect-finding agents: every finding at Low severity or above fails the gate (`no LOW+`). Quality/advisory agents: findings at Medium or above fail the gate (`no MEDIUM+`) — their Low findings are acceptable trade-offs.

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
| CLAUDE.md adherence | context-file-adherence-reviewer | no MEDIUM+ |

### Conditional Gates (when applicable)

| Aspect | Agent | Threshold | Condition |
|--------|-------|-----------|-----------|
| Contract correctness | contracts-reviewer | no LOW+ | When code calls external/internal APIs, changes public interfaces, or crosses service boundaries |
| Type safety | type-safety-reviewer | no LOW+ | When using typed languages (TypeScript, Python with type hints, Java/Kotlin, Go, Rust, C#) |

## Project Gates

CLAUDE.md specifies project gates (typecheck, lint, test, format). These become Global Invariants.

## E2E Verification

**E2E encoding**: E2E verification encodes as Global Invariants (INV-G*), not as deliverable ACs or separate deliverables. Each e2e test case gets its own INV-G*, specifying the scenario and expected outcome.

**E2E phasing**: E2e tests are slow and often deploy-dependent — assign them a later phase than fast automated checks. Manual e2e goes in an even later phase. Only use manual when automated E2E is truly not feasible and user confirms no test data exists.

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
- **E2E test data missing** - no test users/accounts discoverable; probe: existing test fixtures? admin panels? can research via project tools?
- **E2E environment unclear** - which environment for e2e tests; probe: dev, staging, production read-only?
- **E2E automation infeasible** - can tests be scripted; probe: existing health checks or testable endpoints?

## Risks

- **Scope underestimation** - change touches more files/systems than expected; probe: what's the blast radius?
- **Test gap** - changed code has no test coverage; probe: what tests exist for this area?
- **Implicit dependency** - code relies on undocumented behavior or ordering; probe: what assumptions does this code make?

## Trade-offs

- Fix in place vs refactor first
- Test depth vs implementation speed
- Minimal change vs thorough cleanup
- Performance vs readability

## Defaults

*Domain best practices for this task type.*

- **Run existing tests before modifying test files** — Verify current test state before changing tests; prevents masking pre-existing failures
- **Read project gates from CLAUDE.md** — Discover project-specific commands (typecheck, lint, test, format) before implementation

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.
