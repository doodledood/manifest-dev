# Definition: Pi package distribution target for manifest-dev

## 1. Intent & Context
- **Goal:** Make Pi a first-class manifest-dev distribution/package target in repo source, sync-tools guidance, docs, and tests, without pretending the Pi Harness-level Do runtime is already implemented.
- **Mental Model:** Claude Code plugin files remain the shared prompt/skill source. `sync-tools` generates per-CLI/package distribution assets. Pi differs from OpenCode/Codex because it has a package manager and TypeScript extensions; therefore the Pi target needs a capability model, repo-root package install/update metadata, and explicit boundaries around runtime-owned `/do`.

## 2. Approach
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** Add source-owned Pi package metadata at repo root, teach `sync-tools` about `pi`, add a substantial Pi reference file, generate or scaffold only honest package assets, and update README surfaces with install/update/remove/local-dev guidance.
- **Execution Order:**
  - D1 -> D2 -> D3 -> D4
  - Rationale: establish target contract first, then package shape, then docs, then tests/cleanup.
- **Risk Areas:**
  - [R-1] Overclaiming runtime support | Detect: docs or package metadata say Harness-level Do works before extension code exists.
  - [R-2] Stale or shallow Pi mapping | Detect: `pi-cli.md` lacks package, skill, extension, session, command, prompt, and update semantics.
  - [R-3] Drift from generated-target conventions | Detect: `sync-tools` generic rules conflict with package-native Pi behavior.
- **Trade-offs:**
  - [T-1] Full runtime implementation vs distribution foundation -> Prefer distribution foundation now because the user specifically redirected to `sync-tools`/repo-root install/docs, while Harness-level Do remains a larger follow-up.

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Project gates pass for the changed files.
  ```yaml
  verify:
    prompt: "Run the repo's relevant automated checks for sync-tools/docs distribution changes. At minimum run the focused pytest file covering distribution references and any formatter/linter that applies to touched test code. PASS if they succeed. FAIL with command output summary if any fail. BLOCKED only if the local environment lacks the required test runner and no repo-supported fallback exists."
    agent: "test-quality-reviewer"
  ```
- [INV-G2] No fake Pi Harness-level Do runtime is shipped.
  ```yaml
  verify:
    prompt: "Inspect package metadata, README changes, sync-tools guidance, and generated/scaffolded Pi files. PASS only if they do not claim that Pi Harness-level Do is implemented unless actual runtime extension code exists and is tested. It is acceptable to document Harness-level Do as the intended runtime boundary or future consumer. FAIL if any install/update docs make `/manifest-do`, `/do`, `/done`, or `/escalate` appear fully working on Pi without implementation."
    agent: "change-intent-reviewer"
  ```
- [INV-G3] Prompt/skill edits remain high-signal and non-conflicting.
  ```yaml
  verify:
    prompt: "Review changes to `.claude/skills/sync-tools/SKILL.md` and `.claude/skills/sync-tools/references/pi-cli.md` as prompt/skill work. PASS only if the Pi target instructions close real gaps, avoid contradictory guidance with existing OpenCode/Codex behavior, keep generic rules generic, and place detailed Pi knowledge in the reference file rather than overloading the main skill. FAIL with specific prompt conflicts or bloat."
    agent: "prompt-reviewer"
  ```
- [INV-G4] Docs and terminology are internally consistent.
  ```yaml
  verify:
    prompt: "Review `CONTEXT.md`, ADRs, README files, package metadata, and sync-tools docs for consistent terms: Pi-native Runtime Package, Pi Dist Target, Harness-level Do, Source Surface, and Do/Verify Loop. PASS if terms are used consistently and no README contradicts the ADR/source-surface boundary. FAIL with contradictions or missing load-bearing documentation surfaces."
    agent: "docs-reviewer"
  ```

## 4. Process Guidance
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Run existing focused tests before modifying tests when feasible.
- [PG-2] Read project gates from CLAUDE.md before final verification.
- [PG-3] Document load-bearing assumptions.
- [PG-4] Identify affected consumers: Claude Code users, Pi users, and future `sync-tools` runs.
- [PG-5] Prefer an easy revert path: package metadata and generated-target docs should be additive and easy to remove if Pi APIs change.
- [PG-6] Keep prompt changes high-signal; do not overcorrect with a raw Pi docs dump.

## 5. Known Assumptions
- [ASM-1] (auto) Pi repo-root install should be represented by root `package.json` metadata. | Default: add source-owned package metadata at repo root. | Impact if wrong: Pi install may require a subdirectory package or npm publish shape instead.
- [ASM-2] (auto) Harness-level Do runtime is out of scope for this landing pass. | Default: document/runtime-boundary only, no fake extension. | Impact if wrong: a follow-up manifest should implement the runtime extension before docs claim full Pi workflow parity.
- [ASM-3] (auto) Pi package resources can point at repo-local `dist/pi` assets. | Default: root package metadata references generated Pi asset paths. | Impact if wrong: package manifest will need adjustment after empirical Pi install testing.

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: sync-tools Pi target contract

**Acceptance Criteria:**
- [AC-1.1] `sync-tools` accepts and documents `pi` as a first-class target alongside OpenCode and Codex.
  ```yaml
  verify:
    prompt: "Inspect `.claude/skills/sync-tools/SKILL.md`. PASS if it names `pi` in arguments, output paths, per-target processing, package-native install behavior, output summary, and reference-file routing. FAIL if Pi is missing from any target matrix or if generic installer rules still imply every target uses `install.sh` or `npx skills add`."
    agent: "context-file-adherence-reviewer"
  ```
- [AC-1.2] The Pi reference is a capability model, not only a copy recipe.
  ```yaml
  verify:
    prompt: "Inspect `.claude/skills/sync-tools/references/pi-cli.md`. PASS if it covers Pi package model, install/update/remove/local/dev flows, Agent Skills mapping, command behavior, extensions, resource discovery, prompt resources, sessions/forks, runtime/session orchestration, Claude Code component mapping, exclusions, and known uncertainties. FAIL if it only says where to copy skills or omits Pi-only affordances relevant to Harness-level Do."
    agent: "prompt-reviewer"
  ```
- [AC-1.3] Pi skill inclusion/exclusion policy matches the architecture.
  ```yaml
  verify:
    prompt: "Inspect the Pi reference and any generated package assets. PASS if `figure-out`, `define`, and compatible tools skills are included or planned as compatible skills; `/do`, `/done`, and `/escalate` are excluded as ordinary skills; and `/auto` plus `/babysit-pr` are omitted or marked Pi-wrapper-only until runtime-aware wrappers exist. FAIL if runtime-owned skills are copied as normal Pi skills."
    agent: "change-intent-reviewer"
  ```

### Deliverable 2: repo-root Pi package install surface

**Acceptance Criteria:**
- [AC-2.1] Repo-root package metadata exists for Pi install/update without false runtime claims.
  ```yaml
  verify:
    prompt: "Inspect repo-root package metadata. PASS if it is source-owned, includes Pi package discoverability metadata, references only files that exist or are explicitly generated by sync-tools in this change, and does not expose a non-existent Harness-level Do extension. FAIL if package metadata points at missing mandatory extension files or claims full runtime support."
    agent: "contracts-reviewer"
  ```
- [AC-2.2] Package shape leaves room for generated `dist/pi` assets and future runtime extension source.
  ```yaml
  verify:
    prompt: "Inspect package metadata, directory layout, and sync-tools guidance. PASS if generated Pi assets have a clear path and future hand-written Pi runtime extension code has a clear source-owned location. FAIL if generated output and source-owned runtime files are conflated or overwrite each other."
    agent: "code-design-reviewer"
  ```

### Deliverable 3: docs and README surfaces

**Acceptance Criteria:**
- [AC-3.1] Root README documents Pi install, update, remove, and local-development flows.
  ```yaml
  verify:
    prompt: "Inspect `README.md`. PASS if the multi-CLI section includes Pi with repo-root install, update, remove, and local-development commands, and clearly states current Harness-level Do support status. FAIL if Pi is absent, hard to discover, or overclaims full Do/Verify runtime."
    agent: "docs-reviewer"
  ```
- [AC-3.2] Plugin READMEs and generated-target docs stay aligned.
  ```yaml
  verify:
    prompt: "Inspect `claude-plugins/README.md`, `claude-plugins/manifest-dev/README.md`, `claude-plugins/manifest-dev-tools/README.md`, and any `dist/pi/README.md` created. PASS if relevant README surfaces mention Pi only where useful, link or summarize install/update behavior consistently, and avoid duplicating unstable implementation detail. FAIL if readers get contradictory install/update instructions across docs."
    agent: "docs-reviewer"
  ```
- [AC-3.3] ADR/context capture the source-surface and capability-model decisions.
  ```yaml
  verify:
    prompt: "Inspect `CONTEXT.md` and `docs/adr/20260605-pi-native-runtime-package-source-surface.md`. PASS if they record repo-root Pi install, `sync-tools` Pi capability-model reference, generated-vs-source boundary, and Harness-level Do runtime ownership. FAIL if the durable docs lack these decisions or conflict with README/package metadata."
    agent: "docs-reviewer"
  ```

### Deliverable 4: tests and cleanup

**Acceptance Criteria:**
- [AC-4.1] Focused tests guard the Pi target contract.
  ```yaml
  verify:
    prompt: "Inspect tests. PASS if there are focused automated tests or equivalent static checks proving `sync-tools` declares Pi, the Pi reference exists, runtime-owned skills are excluded as ordinary Pi skills, and README/package docs expose install/update behavior without fake runtime claims. FAIL if no automated guard exists for the new target contract."
    agent: "test-quality-reviewer"
  ```
- [AC-4.2] Working tree changes are intentional and committed.
  ```yaml
  verify:
    prompt: "Inspect git status and the final commit. PASS if only intentional files for this task are changed or added, unrelated pre-existing untracked files are not accidentally committed, and the final commit uses a conventional commit message. FAIL if unrelated files are staged/committed or the commit is missing."
    agent: "operational-readiness-reviewer"
  ```
