# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

CLAUDE.md may specify project-specific preferences.

### Base Gates (always applicable)

Two tiers by agent role. **Defect-finding agents** (every LOW finding is signal — a real divergence, defect, contract mismatch, or type hole): `no LOW+`. **Advisory agents** (LOW findings are usually taste-level — could-be-better, not is-broken): `no MEDIUM+`. The split is structural, not per-finding — it reflects what each agent is built to detect.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Intent analysis | change-intent-reviewer | no LOW+ |
| Mechanical bug detection | code-bugs-reviewer | no LOW+ |
| Operational readiness | operational-readiness-reviewer | no MEDIUM+ |
| Maintainability | code-maintainability-reviewer | no MEDIUM+ |
| Simplicity | code-simplicity-reviewer | no MEDIUM+ |
| Test quality | test-quality-reviewer | no MEDIUM+ |
| Testability | code-testability-reviewer | no MEDIUM+ |
| Documentation | docs-reviewer | no MEDIUM+ |
| Design fitness | code-design-reviewer | no MEDIUM+ |
| Prose value | prose-value-reviewer | no MEDIUM+ |
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

## Defaults

*Domain best practices for this task type.*

- **Run existing tests before modifying test files** — Verify current test state before changing tests; prevents masking pre-existing failures
- **Read project gates from CLAUDE.md** — Discover project-specific commands (typecheck, lint, test, format) before implementation

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.
