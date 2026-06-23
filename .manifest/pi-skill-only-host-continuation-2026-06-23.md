# Definition: Pi Skill-Only Host-Continuation Simplification

## 1. Intent & Context
- **Goal:** Implement the accepted host-continuation ADR by making Pi a skill-only manifest-dev package: full workflow skills plus prompt-template aliases (`/do`, `/auto`, `/babysit-pr`), with no manifest-dev TypeScript extension, no deterministic Pi runtime verifier fanout, and no runtime done/escalation gate.
- **Mental Model:** The trust mechanism remains independent verifier executions per AC/GI gate. The Pi package now looks much closer to Codex/OpenCode: skills own behavior, prompt aliases provide slash UX, and any host goal/continuation capability is an optional outer backstop. Without a continuation capability, `/do` still runs prompt-level but has no automatic cross-turn enforcement.

## 2. Approach
- **Architecture:** Remove Pi TypeScript extension code and the tools subpackage. Include all workflow skills in `dist/pi/skills`, including `do`, `done`, `escalate`, `auto`, and `babysit-pr`. Add prompt templates in `dist/pi/prompts` for `/do`, `/auto`, and `/babysit-pr`. Update package metadata, docs, sync reference, tests, and versions.
- **Execution Order:** D1 (package/skills/prompts) → D2 (docs/reference/tests/versioning) → D3 (verification/archive/commit/push)
- **Risk Areas:**
  - [R-1] Stale Pi runtime code or tests still imply deterministic verifier fanout | Detect: deleted extension dirs/tests and grep for runtime symbols.
  - [R-2] Pi loses `/do` UX | Detect: prompt templates exist and package metadata loads `dist/pi/prompts`.
  - [R-3] `babysit-pr` no longer gets a wrapper-owned goal/backstop | Detect: source and dist `babysit-pr` skill include standalone unattended goal-setting guidance.
  - [R-4] Docs overclaim runtime guarantees | Detect: live docs say skill-only/prompt-level plus optional continuation.
  - [R-5] Versioning misses source plugin behavior change | Detect: Pi package bumped to 0.12.0; manifest-dev-tools plugin bumped for `babysit-pr` prompt change.
- **Trade-offs:**
  - [T-1] Bare `/do` extension command vs prompt-template alias → Prefer prompt templates because they preserve UX without a TypeScript source surface.

## 3. Global Invariants
- [INV-G1] The implementation matches the accepted ADR and no unrelated scope is introduced.
  ```yaml
  verify:
    prompt: |
      Activate the review-code skill with dimension=change-intent and review the full diff on the current branch against origin/main. PASS only if the diff implements the host-continuation Pi simplification: Pi is skill-only plus prompt aliases; no Pi TypeScript extension/runtime verifier fanout/done gate remains; host continuation is optional and capability-based; independent verifier executions per AC/GI remain the trust mechanism; docs/dist/tests/versioning align; and no unrelated scope creep appears. PASS only if no LOW-or-higher findings. Report findings with severity and evidence.
    phase: 2
  ```
- [INV-G2] Edited prompt text passes prompt-engineering calibration.
  ```yaml
  verify:
    prompt: |
      Activate the review-prompt skill. Review edited prompt-bearing files, especially babysit-pr/SKILL.md, README.md, dist/pi/README.md, and .claude/skills/sync-tools/references/pi-cli.md. PASS only if no MEDIUM-or-higher findings. Check: portable capability language; no machine-specific goal-plugin dependency; no contradiction between skill-only Pi and runtime-owned wording; `babysit-pr` standalone goal/backstop is clear but not over-prescriptive; fallback without continuation remains explicit.
    phase: 2
  ```
- [INV-G3] No stale live Pi runtime verifier claims remain.
  ```yaml
  verify:
    prompt: |
      Inspect live source/docs/tests/dist (excluding historical .manifest files and superseded ADR bodies unless newly edited). PASS only if there are no current claims that Pi owns JSON subprocess verifier fanout, runtime manifest gate parsing, runtime verdict aggregation, runtime done/escalation gate, verifier concurrency flags, or wait-pending runtime-token routing. Negative tests may construct forbidden strings only as assertions, not as product claims. FAIL with file:line evidence for stale live claims.
    phase: 1
  ```
- [INV-G4] Project verification commands pass.
  ```yaml
  verify:
    prompt: |
      Run relevant checks from the repo root after implementation. At minimum: .venv/bin/python -m pytest tests/test_pi_extension_runtime.py tests/test_dist_skill_references.py tests/test_dist_install_uninstall.py; .venv/bin/ruff check claude-plugins/; .venv/bin/black --check claude-plugins/; .venv/bin/mypy. Run node tests only if any Node runtime tests remain. PASS if available commands pass, or any unavailable command is skipped with evidence. FAIL on available command failures.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] (auto) Prefer deletion over compatibility scaffolding. Do not leave dead extension exports or runtime files.
- [PG-2] (auto) Keep `/do`, `/auto`, and `/babysit-pr` UX through prompt templates, not TypeScript commands.
- [PG-3] (auto) Do not make any specific continuation plugin mandatory; link a Pi-compatible provider as an optional recommendation only.
- [PG-4] (auto) Commit with a conventional message and push when all gates pass.

## 5. Known Assumptions
- [ASM-1] (auto) Pi package version bumps from 0.11.6 to 0.12.0 because runtime/package behavior changes while still pre-1.0. Impact if wrong: adjust version before release.
- [ASM-2] (auto) `manifest-dev-tools` plugin bumps from 0.26.0 to 0.27.0 because `babysit-pr` gains standalone unattended goal/backstop behavior. Impact if wrong: version bump can be revised before release.
- [ASM-3] (auto) `manifest-dev` core plugin version stays 2.16.0 because no core source skill changed. Impact if wrong: add bump and regenerate target versions.
- [ASM-4] (auto) Prompt templates are sufficient for bare `/do`, `/auto`, and `/babysit-pr` aliases in Pi. Impact if wrong: a future extension could restore aliases without verifier runtime.

## 6. Deliverables

### Deliverable 1: Skill-only Pi package surface

**Acceptance Criteria:**
- [AC-1.1] Pi package metadata loads only skills and prompt templates.
  ```yaml
  verify:
    prompt: |
      Inspect package.json. PASS only if version is 0.12.0, `pi.skills` is [`./dist/pi/skills`], `pi.prompts` is [`./dist/pi/prompts`], and there is no `pi.extensions`, workspace tools package, runtime export, or Pi peer dependency required only for extension code. FAIL with exact stale fields.
    phase: 1
  ```
- [AC-1.2] Pi extension/runtime code and extension-only tests are removed.
  ```yaml
  verify:
    prompt: |
      PASS only if `pi/extensions/`, `packages/manifest-dev-pi-tools/`, and Node extension tests for Pi runtime/flag ownership/tools runtime are absent, and no live test imports those paths. FAIL with paths/imports if any remain.
    phase: 1
  ```
- [AC-1.3] Pi dist includes full workflow skills and prompt aliases.
  ```yaml
  verify:
    prompt: |
      Inspect dist/pi. PASS only if `dist/pi/skills` contains all core and tools workflow skills including auto, do, done, escalate, and babysit-pr; `dist/pi/prompts` contains do.md, auto.md, and babysit-pr.md; each prompt expands to `Use the <skill> skill with: $ARGUMENTS`; and component-namespaces.json records skills, prompts, and no runtime commands/tools. FAIL with missing or stale entries.
    phase: 1
  ```

### Deliverable 2: Prompt/docs/reference/version alignment

**Acceptance Criteria:**
- [AC-2.1] `babysit-pr` owns its standalone unattended backstop.
  ```yaml
  verify:
    prompt: |
      Inspect source and dist copies of `babysit-pr/SKILL.md`. PASS only if each has an Unattended launch section that establishes a durable goal-setting/continuation backstop when available, prints/carries a fallback when not, spans manifest discovery/synthesis and `/do`, includes PR mergeable/pending/blocker completion, honest AC/GI verification, wait-only CI pending behavior, never-merge constraint, and compact progress checkpoints. FAIL if source/dist drift or wrapper-only assumptions remain.
    phase: 1
  ```
- [AC-2.2] Live docs/reference describe skill-only Pi consistently and suggest optional Pi continuation provider.
  ```yaml
  verify:
    prompt: |
      Inspect README.md, CONTEXT.md, dist/pi/README.md, dist/pi/.sync-meta.json, dist/pi/component-namespaces.json, and .claude/skills/sync-tools/{SKILL.md,references/pi-cli.md}. PASS only if they describe Pi as skills plus prompt aliases with no TypeScript extension, explain host continuation as optional and fallback as prompt-level/no continuous enforcement, and dist/pi/README suggests the doodledood/pi-plugins goal-controller package link as one possible continuation provider without making it mandatory. FAIL with stale runtime or missing recommendation quotes.
    phase: 1
  ```
- [AC-2.3] Versioning is consistent.
  ```yaml
  verify:
    prompt: |
      PASS only if package.json is 0.12.0, claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json is 0.27.0, dist/codex/plugins/manifest-dev-tools/.codex-plugin/plugin.json is 0.27.0, .claude/skills/sync-tools/references/pi-cli.md example uses 0.12.0, and manifest-dev core plugin remains 2.16.0. Report versions.
    phase: 1
  ```
- [AC-2.4] Tests assert the new skill-only boundary.
  ```yaml
  verify:
    prompt: |
      Inspect tests/test_pi_extension_runtime.py and tests/test_dist_skill_references.py. PASS only if tests cover skill-only package metadata, prompt aliases, full Pi skill set, absence of extensions/runtime fanout claims, and no stale extension-runtime tests remain. FAIL if tests still require Pi TypeScript extension behavior.
    phase: 1
  ```

### Deliverable 3: Verification, archival, commit, and push

**Acceptance Criteria:**
- [AC-3.1] Targeted verification passes.
  ```yaml
  verify:
    prompt: |
      Same as INV-G4. Report commands, exit status, and any skips with evidence.
    phase: 2
  ```
- [AC-3.2] This manifest is archived under `.manifest/` with a descriptive name.
  ```yaml
  verify:
    prompt: |
      PASS only if /Users/aviram.kofman/.manifest-dev/manifests/manifest-20260623T143329Z-auto.md exists and .manifest/pi-skill-only-host-continuation-2026-06-23.md exists with identical content. FAIL if either path is missing or contents differ.
    phase: 1
  ```
- [AC-3.3] Branch is committed and pushed.
  ```yaml
  verify:
    prompt: |
      PASS only if the current branch contains a conventional commit for the full skill-only simplification, working tree is clean, and the branch is pushed to origin with local HEAD matching remote HEAD. Report branch, commit hash/message, and `git status --short --branch`.
    phase: 1
  ```
