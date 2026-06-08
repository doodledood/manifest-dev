# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

AGENTS.md may specify project-specific preferences.

### Base Gates (always applicable)

Each gate is a **dimension** of the `review-code` skill (one ref per dimension, loaded on demand). Two tiers by dimension role. **Defect-finding dimensions** (every LOW finding is signal — a real divergence, defect, contract mismatch, or type hole): `no LOW+`. **Advisory dimensions** (LOW findings are usually taste-level — could-be-better, not is-broken): `no MEDIUM+`. The split is structural, not per-finding — it reflects what each dimension is built to detect.

| Aspect | Dimension | Threshold |
|--------|-----------|-----------|
| Intent analysis | change-intent | no LOW+ |
| Mechanical bug detection | code-bugs | no LOW+ |
| Operational readiness | operational-readiness | no MEDIUM+ |
| Maintainability | code-maintainability | no MEDIUM+ |
| Simplicity | code-simplicity | no MEDIUM+ |
| Test quality | test-quality | no MEDIUM+ |
| Testability | code-testability | no MEDIUM+ |
| Documentation | docs | no MEDIUM+ |
| Design fitness | code-design | no MEDIUM+ |
| Prose value | prose-value | no MEDIUM+ |
| CLAUDE.md adherence | context-file-adherence | no MEDIUM+ |

### Conditional Gates (when applicable)

| Aspect | Dimension | Threshold | Condition |
|--------|-----------|-----------|-----------|
| Contract correctness | contracts | no LOW+ | When code calls external/internal APIs, changes public interfaces, or crosses service boundaries |
| Type safety | type-safety | no LOW+ | When using typed languages (TypeScript, Python with type hints, Java/Kotlin, Go, Rust, C#) |

**Encoding:** each dimension gate is verified by a general-purpose subagent (there is no `verify.agent` field) whose `verify.prompt` invokes the `manifest-dev:review-code` skill for that dimension at the row's threshold — e.g. *"Spawn a general-purpose review using the manifest-dev review-code skill with dimension=code-bugs against the change. PASS only if no LOW-or-higher findings."* See `define/SKILL.md` → "Encoding gates".

## Project Gates

AGENTS.md specifies project gates (typecheck, lint, test, format). These become Global Invariants.

## E2E Verification

**E2E encoding**: E2E verification encodes as Global Invariants (INV-G*), not as deliverable ACs or separate deliverables. Each e2e test case gets its own INV-G*, specifying the scenario and expected outcome.

**E2E phasing**: E2e tests are slow and often deploy-dependent — assign them a later phase than fast automated checks. Manual e2e goes in an even later phase. Only use manual when automated E2E is truly not feasible and user confirms no test data exists.

## Defaults

*Domain best practices for this task type.*

- **Run existing tests before modifying test files** — Verify current test state before changing tests; prevents masking pre-existing failures
- **Read project gates from AGENTS.md** — Discover project-specific commands (typecheck, lint, test, format) before implementation

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.
