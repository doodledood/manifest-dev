# CODING Task Guidance

Base guidance for all code-change tasks (features, bugs, refactors).

## Quality Gates

The project context file (the always-loaded instruction file the harness reads for this project, resolved by detection rather than assumed by name) may specify project-specific preferences.

### Base Gates (always applicable)

Each row names a quality to assess through a **dimension** of `review-code` (one reference per dimension, loaded on demand). Express the claim for the work's supported use and useful life. Roles control applicability and omission: only advisory dimensions are eligible for `/define`'s bearer-test omission valve (`define/SKILL.md` → *The omission valve*); defect-finding coverage always remains.

| Aspect | Dimension | Quality owed |
|--------|-----------|-----------|
| Intent analysis | change-intent | The change fulfills the accepted purpose and obligations |
| Mechanical bug detection | code-bugs | Supported inputs and reachable states produce correct behavior |
| Operational readiness | operational-readiness | The change can be run, observed and recovered under its operating conditions |
| Maintainability | code-maintainability | Expected maintenance does not incur unjustified coordination, hidden assumptions or change risk |
| Simplicity | code-simplicity | Complexity has a present purpose proportionate to the burden it removes |
| Test quality | test-quality | Checks distinguish required behavior from plausible wrong results using independent expectations |
| Testability | code-testability | The real behavior can be exercised and observed at suitable boundaries |
| Documentation | docs | Affected users and maintainers have accurate instructions they need |
| Design fitness | code-design | Responsibilities and interfaces support current use and evidenced changes without disproportionate coupling |
| Prose value | prose-value | Written material gives its intended reader useful information without obscuring it |
| Context-file adherence | context-file-adherence | Applicable documented project obligations hold |

### Conditional Gates (when applicable)

| Aspect | Dimension | Quality owed | Condition |
|--------|-----------|-----------|-----------|
| Contract correctness | contracts | Producers and consumers satisfy their actual interface and data obligations | When code calls external/internal APIs, changes public interfaces, crosses service boundaries, or changes durable data contracts (API/event payloads, database schema/table-field semantics, exports, analytics feeds) |
| Type safety | type-safety | Types and boundary checks preserve required guarantees without unchecked escape paths | When using typed languages (TypeScript, Python with type hints, Java/Kotlin, Go, Rust, C#) |

**Encoding:** claims state the relevant qualities, grounded in this work. Evidence activates
`review-code` for each applicable dimension with the claims it assesses, as
`define/SKILL.md` → *Specialized gates activate a skill* says. Coverage stays broad even when
several dimensions share one claim. Preserve a deliberately required review policy with its source.

**Kind:** these quality claims are **Judgment Gates**, assessed from concrete findings and evidence rather than a command outcome. The defect-finding dimensions run alongside the project's mechanical gates below (typecheck, lint, test, format), which are Deterministic Gates. An overlay may add a dimension, as `BUG.md` adds `defect-class`.

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
- **Agree test seams before authoring tests** — Settle which public boundaries tests exercise before writing them, and where each expected value comes from independently of the code under test, and assert behavior through those interfaces rather than internals; a test that breaks under refactor without a behavior change sits at the wrong seam. Where correctness depends on the order of events or holds for every input, ask whether example tests can reach the case that breaks; where they cannot, use the cheapest check that can — generated inputs or call sequences on the real code, then a model checker for an order-dependent design (such as TLA+ or Alloy), then a verifier on the code where the language has one (such as Kani for Rust), and a proof only where no bound is enough — and keep it as a recipe or a test like any other
- **Vertical slices, not bulk test-first** — One test, minimal implementation, repeat; writing all tests up front verifies imagined behavior and commits to test structure before the implementation has taught anything
- **Use what is already provided** — Before building, look for what the framework, the codebase, generated clients and schemas and the API's documentation (including what it deprecates) already provide or require; use it, or record why not
- **Earn each module's depth** — Give each new module a small interface over real work and one job it can be named for; add no pass-through layer, and no option, abstraction or cache without a case that exists today
- **Sketch the shape before implementing** — For a change that crosses a function boundary, sketch it first — how callers use it, including that the call with only required arguments is safe, the data shape, which layer owns each decision and what belongs in configuration (and which source overrides which) or off the request path, seams where outside data is parsed and IO happens, one owner per piece of state, placement and public surface, test seams, what it deletes — then sketch one structurally different shape and keep the better. Ground likely changes in current callers, change history or known direction; hide the decisions that vary behind small interfaces where that reduces what the next maintainer must understand, remember or edit enough to repay the added complexity. Sound existing structure needs no redesign. Where the design's correctness depends on the order of events — concurrency, retries, crash recovery, several writers — model it in scratch and check the model before building, and turn what it finds into design decisions and gates
- **Screen for what the next agent copies** — Check the shape for two ways to do one task, a list kept in sync by hand, state with two writers, internals a caller can import, IO mixed into decisions, a call order or ambient input the signature hides, and one name carrying two meanings; where one remains, add the type, lint or test that locks the better shape
- **Hold the design discipline** — Replace branches spread across files with one structure (a state machine, a registry, a union), make illegal states unrepresentable, parse outside data at the boundary, separate shared state before serializing it, make operations safe to run twice, concurrently or after a crash halfway, and migrate callers before deleting the old way
- **Read the intent before removing or adding a guard** — Before changing code that looks defensive — a retry, a timeout, a guard, a flag — read what commits, pull-request threads and tickets say it was for; before adding one where a crash surfaced, check whether the state that crashed is legitimate, since a guard that turns a crash from an illegal state into silent wrong data is the wrong fix
- **Make failure visible and the result drivable** — For each new failure mode, name how someone would know (a metric, log or alert), and make what the change produces something an agent can drive, observe and debug
- **Name what could regress silently** — Before implementing, name the behavior that could change while existing tests still pass, and cover it
- **Reshape, don't patch** — Surface any departure from the sketch instead of absorbing it. When the same workaround appears at unrelated call sites, or types need casts or other escape hatches to compile, the shape is wrong: reshape it rather than patching around it
- **Trust the check before relying on it** — Before a check's PASS counts for the change — a harness recipe, or a test, script or checklist step in the project's own form — confirm it would mean something for the paths the change touches: one scenario runs from cold and its evidence survives cleanup, a health check tells a usable instance from one that merely answers, each run gets its own instance and data, the run exercises the real path, what the change touches can be started in a known state, observed and stopped through the harness or the project's own scripts, failed evidence carries what locates the cause, and the check was seen failing on a scratch break of what it proves (a throwaway change that makes the checked behavior wrong), each job judged by its counterpart for that check (`../../setup-project/references/VERIFICATION_HARNESS.md` → *Fit to trust*); where it does not, repairing it is part of the work
- **Build the lever** — When work isn't trivial, build the script, codemod or generator that does it or proves it, so a reviewer can rerun it instead of trusting hand edits

## Multi-Repo

When spanning repos: per-repo project gates differ, cross-repo contracts need verification, scope reviewers to changed files per repo.
