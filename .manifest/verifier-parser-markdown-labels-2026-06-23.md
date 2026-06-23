# Definition: Pi Verifier Parser Markdown Label Tolerance

## 1. Intent & Context
- **Goal:** Fix manifest-dev's Pi runtime verifier-output parser so semantically valid reports with harmless Markdown label styling parse correctly instead of blocking a gate as unparseable.
- **Mental Model:** The verifier contract remains `VERDICT` / `EVIDENCE` / `DETAILS`. The runtime parser is authoritative for converting child Pi JSON subprocess text into gate results. This task makes label recognition tolerant of Markdown emphasis around required labels while preserving strict verdict values and avoiding prose inference.
- **Repos:** [manifest-dev: /Users/aviram.kofman/Documents/Projects/manifest-dev]

## 2. Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** Localized parser/runtime robustness fix in `pi/extensions/manifest-dev-runtime.ts`; regression coverage in `tests/pi_extension_runtime.test.mjs`; Pi package patch-version metadata kept in lockstep per repo guidance.
- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: Reproduce and fix parser behavior first, encode strictness/regression boundaries second, then update packaging metadata and run verification.
- **Risk Areas:**
  - [R-1] Parser becomes too permissive and infers verdicts from ordinary prose | Detect: tests and review must show verdict labels are still required and values remain only PASS/FAIL/BLOCKED.
  - [R-2] Evidence/details parsing loses useful report content when labels are bold or details include a descriptor | Detect: regression tests use minimized captured report shapes with `**EVIDENCE:**` and `**DETAILS — what passed:**`.
  - [R-3] Runtime package metadata drifts after changing Pi runtime code | Detect: version gate checks root package, tools package, and sync-tools Pi reference example.
- **Trade-offs:**
  - [T-1] Parser robustness vs prompt tightening → Prefer parser robustness because captured verifier outputs satisfied the semantic contract and only Markdown label styling broke parsing.
  - [T-2] Localized fix vs broad parser rewrite → Prefer a localized label parser helper; broaden only around explicit labels/Markdown wrapping, not natural-language inference.

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Targeted Pi runtime checks pass.
  ```yaml
  verify:
    prompt: |
      In repo /Users/aviram.kofman/Documents/Projects/manifest-dev, run the targeted Pi runtime verification for this parser change: `node --experimental-strip-types --check pi/extensions/manifest-dev-runtime.ts`, `node --experimental-strip-types --test tests/pi_extension_runtime.test.mjs`, and `.venv/bin/python -m pytest tests/test_pi_extension_runtime.py -q` if the virtualenv exists. PASS only if all runnable targeted checks pass. FAIL on any failing runnable check. BLOCKED only if Node is unavailable or the local environment lacks a required tool with no reasonable static fallback.
    phase: 1
  ```

- [INV-G2] Parser contract remains strict while accepting Markdown label wrappers.
  ```yaml
  verify:
    prompt: |
      Inspect `pi/extensions/manifest-dev-runtime.ts` and parser tests. PASS only if the verifier parser requires an explicit VERDICT label, accepts only PASS/FAIL/BLOCKED verdict values, accepts harmless Markdown emphasis around report labels/values such as `**VERDICT: PASS**` and `**VERDICT:** PASS`, and does not infer verdicts from prose like "looks good" or non-contract values like `PASSED`. FAIL if the parser accepts unlabeled prose, broadens verdict values, or only fixes prompts instead of runtime parsing.
    phase: 1
  ```

- [INV-G3] Pi package version metadata is bumped consistently for the runtime change.
  ```yaml
  verify:
    prompt: |
      Inspect root `package.json`, `packages/manifest-dev-pi-tools/package.json`, and `.claude/skills/sync-tools/references/pi-cli.md`. PASS only if the Pi package patch version increased from 0.11.4, both package.json files are in lockstep, and the pi-cli reference example matches the new version. FAIL on any mismatch or missing bump.
    phase: 1
  ```

- [INV-G4] Code-bugs review finds no LOW-or-higher mechanical defects in the changed parser/runtime and tests.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=code-bugs and review the changed files for this parser fix. PASS only if there are no LOW-or-higher mechanical defects. Report findings with severity.
    phase: 2
  ```

- [INV-G5] Contracts review finds no LOW-or-higher verifier-output contract mismatch.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=contracts and review the changed parser contract, regression tests, and version metadata. PASS only if there are no LOW-or-higher contract findings, especially around accepted report labels, verdict values, and blocked fallback behavior. Report findings with severity.
    phase: 2
  ```

- [INV-G6] Test-quality review finds no MEDIUM-or-higher regression coverage gaps.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=test-quality and review the added/updated tests for this parser fix. PASS only if there are no MEDIUM-or-higher test-quality findings. The tests must exercise both captured Markdown-bold report shapes and strict rejection boundaries. Report findings with severity.
    phase: 2
  ```

- [INV-G7] Type-safety review finds no LOW-or-higher typed-runtime issues.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=type-safety and review the TypeScript runtime/test changes. PASS only if there are no LOW-or-higher type-safety findings. Report findings with severity.
    phase: 2
  ```

- [INV-G8] Context adherence review finds no MEDIUM-or-higher deviation from repo instructions.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=context-file-adherence and review this change against `/Users/aviram.kofman/Documents/Projects/manifest-dev/AGENTS.md`, `CLAUDE.md`, and the user task. PASS only if there are no MEDIUM-or-higher context-adherence findings. Report findings with severity.
    phase: 2
  ```

## 4. Process Guidance
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Establish reproduction before fixing: use the captured/minimized `**VERDICT: PASS**` report shape against the current parser.
- [PG-2] Change source-owned manifest-dev runtime files, not the installed/generated copy under `~/.pi/agent/git/.../dist/pi/skills/`.
- [PG-3] Do not make prompt tightening the primary fix; runtime parser robustness is the requested fix.
- [PG-4] Preserve allowed verdict values exactly: PASS, FAIL, BLOCKED.
- [PG-5] Do not implement broader investigation suggestions or user-level `AGENTS.md` changes.

## 5. Known Assumptions
- [ASM-1] (auto) The right branch base is current `main` after `git pull --ff-only`; the user will push later. Impact if wrong: the commit may need to be rebased before push.
- [ASM-2] (auto) A patch bump from `0.11.4` to `0.11.5` is the correct version level for a Pi runtime bug fix. Impact if wrong: version metadata can be adjusted without changing parser logic.
- [ASM-3] (auto) Updating source package metadata/reference is sufficient; generated/installed dist copies should not be edited for this parser-only runtime fix. Impact if wrong: a later sync-tools run may be needed.

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: Flexible verifier report label parser

**Acceptance Criteria:**
- [AC-1.1] The parser accepts plain verifier reports and Markdown-emphasized verdict labels for all three valid verdicts.
  ```yaml
  verify:
    prompt: |
      Inspect `parseVerifierReport` and tests in `/Users/aviram.kofman/Documents/Projects/manifest-dev`. PASS only if parser behavior covers plain `VERDICT: PASS|FAIL|BLOCKED`, `**VERDICT: PASS**`, `**VERDICT:** PASS`, and equivalent Markdown emphasis around the verdict value while still returning the canonical verdict. FAIL if any valid verdict value is missing from coverage.
    phase: 1
  ```

- [AC-1.2] The parser accepts Markdown-emphasized `EVIDENCE` and `DETAILS` labels, including a details descriptor like `**DETAILS — what passed:**`.
  ```yaml
  verify:
    prompt: |
      Inspect `parseVerifierReport` and regression tests. PASS only if reports with `**EVIDENCE:**` followed by bullet evidence and `**DETAILS:**` or `**DETAILS — what passed:**` followed by multiline details produce useful `evidence` and `details` fields rather than empty fields. FAIL if only the verdict line is fixed while bold evidence/details labels remain unparsed.
    phase: 1
  ```

### Deliverable 2: Strictness and blocked fallback preserved

**Acceptance Criteria:**
- [AC-2.1] The parser does not infer verdicts from prose or non-contract values.
  ```yaml
  verify:
    prompt: |
      Inspect tests and parser implementation. PASS only if there are explicit regression tests showing missing-label prose remains unparseable and non-contract values such as `PASSED` are rejected, and the implementation's verdict extraction requires a label line plus PASS/FAIL/BLOCKED. FAIL if the parser accepts prose summaries or broadens verdict values.
    phase: 1
  ```

- [AC-2.2] Completed verifier records without a parseable verdict still route to the existing BLOCKED/unparseable-verdict result.
  ```yaml
  verify:
    prompt: |
      Inspect `toGateVerificationResult` tests and implementation. PASS only if completed verifier output without a parseable verdict still produces verdict BLOCKED with evidence explaining the missing parseable VERDICT line, while Markdown-bold valid verdict reports now produce their actual verdict. FAIL if missing-verdict fallback is removed or downgraded.
    phase: 1
  ```

### Deliverable 3: Regression coverage and package metadata

**Acceptance Criteria:**
- [AC-3.1] Regression tests use minimized captured report shapes for the observed failures.
  ```yaml
  verify:
    prompt: |
      Inspect `tests/pi_extension_runtime.test.mjs`. PASS only if tests include minimized raw outputs matching the captured failure shapes: one with `**VERDICT: PASS**`, `**EVIDENCE:**`, and `**DETAILS — what passed:**`, and one with `**VERDICT: PASS**`, `**EVIDENCE:**`, and `**DETAILS:**`. FAIL if tests only cover artificial plain-label reports.
    phase: 1
  ```

- [AC-3.2] Pi runtime package version metadata reflects the bug fix.
  ```yaml
  verify:
    prompt: |
      Inspect version metadata. PASS only if root `package.json`, `packages/manifest-dev-pi-tools/package.json`, and `.claude/skills/sync-tools/references/pi-cli.md` all use the same bumped patch version for the Pi runtime package after this change. FAIL on mismatch.
    phase: 1
  ```
