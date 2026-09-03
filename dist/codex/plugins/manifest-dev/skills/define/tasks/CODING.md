# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

The project context file (the always-loaded instruction file the harness reads for this project, resolved by detection rather than assumed by name) may specify project-specific preferences.

### Base Gates (always applicable)

Each gate is a **dimension** of the `review-code` skill (one ref per dimension, loaded on demand). Two tiers by dimension role. **Defect-finding dimensions** (every LOW finding is signal — a real divergence, defect, contract mismatch, or type hole): `no LOW+`. **Advisory dimensions** (LOW findings are usually taste-level — could-be-better, not is-broken): `no MEDIUM+`. The split is structural, not per-finding — it reflects what each dimension is built to detect. The advisory tier is the tier eligible for `/define`'s bearer-test omission valve (`define/SKILL.md` → *The omission valve*); defect-finding dimensions always encode.

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
| Context-file adherence | context-file-adherence | no MEDIUM+ |

### Conditional Gates (when applicable)

| Aspect | Dimension | Threshold | Condition |
|--------|-----------|-----------|-----------|
| Contract correctness | contracts | no LOW+ | When code calls external/internal APIs, changes public interfaces, crosses service boundaries, or changes durable data contracts (API/event payloads, database schema/table-field semantics, exports, analytics feeds) |
| Type safety | type-safety | no LOW+ | When using typed languages (TypeScript, Python with type hints, Java/Kotlin, Go, Rust, C#) |

**Encoding:** each dimension gate's body tells `/do`'s selected evaluator to **activate** the `review-code` skill for the dimension — e.g. *"Done when the review-code skill, activated with dimension=code-bugs, reports nothing at or above that dimension's threshold."* Name the dimension and stop: `review-code` owns every threshold in its own table, and a bar copied into a gate is a second statement that can contradict the skill the gate activates. The thresholds in the table above orient the author, not the gate. Do not tell the evaluator to spawn another agent; a nested spawn drops the gate's PASS/FAIL/BLOCKED contract. See `define/SKILL.md` → "Encoding specialized gates".

**Kind:** every dimension gate is a **Judgment Gate** — a reviewer's verdict over an open finding space, not a command outcome — so each declares the judgment kind, which is what tells `/do` how the gate re-verifies. The defect-finding dimensions above run alongside the project's mechanical gates below (typecheck, lint, test, format), which are Deterministic Gates — and an overlay task file may add a defect-finding dimension, as `BUG.md` adds `defect-class`. The advisory dimensions above are the whole-change quality sweep, and `/do` already spends their one full look once the mechanical and defect-finding gates are settled — no gate has to ask for that.

## Project Gates

The project context file specifies project gates (typecheck, lint, test, format). These become Global Invariants.

## E2E Verification

**E2E encoding — route by scope, not blanket INV-G**: don't enumerate every e2e case as its own INV-G. Match the encoding to what you want independently fix-targeted:

- **Single-deliverable behavioral check** (the new path of one Deliverable, run end-to-end) → a **deliverable AC** on that Deliverable, not a Global Invariant. It accepts that deliverable's behavior; it isn't a property spanning the whole manifest.
- **Genuinely cross-cutting e2e** (a scenario that spans multiple Deliverables) → an **INV-G***, specifying the scenario and expected outcome.
- **Comprehensive edge-case matrix** → **test code under the existing project test-run gate**, not enumerated as manifest criteria.

Principle: **manifest criteria are for what you want independently fix-targeted; the suite is for breadth.** Encode a scenario as its own criterion when an isolated PASS/FAIL gives precise repair targeting; otherwise let the suite carry it. Don't turn the manifest into a test-case list.

**E2E cost**: e2e runs are slow and often deploy-dependent, so re-running one costs far more than a round of repairs. Say that in the gate's own body — how long a run takes, and what it depends on — since that is what tells `/do` to spend the evaluation on a settled state rather than one a repair is about to move. A manual e2e is the expensive extreme and says so the same way; only use manual when automated e2e is truly not feasible and the user confirms no test data exists.

## Defaults

*Domain best practices for this task type.*

- **Run existing tests before modifying test files** — Verify current test state before changing tests; prevents masking pre-existing failures
- **Read project gates from the project context file** — Discover project-specific commands (typecheck, lint, test, format) before implementation
- **Agree test seams before authoring tests** — Settle which public boundaries tests exercise before writing them, and assert behavior through those interfaces rather than internals; a test that breaks under refactor without a behavior change sits at the wrong seam
- **Vertical slices, not bulk test-first** — One test, minimal implementation, repeat; writing all tests up front verifies imagined behavior and commits to test structure before the implementation has taught anything

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.
