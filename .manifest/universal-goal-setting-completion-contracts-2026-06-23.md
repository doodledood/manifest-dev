# Definition: Universal goal-setting completion contracts across harnesses

## 1. Intent & Context
- **Goal:** Land the accepted figure-out Read: manifest-dev's unattended-run backstops should be expressed as a universal goal-setting capability, not as Claude-specific `/goal` mechanics. If the active harness exposes a durable goal-setting / continuation capability, the model uses it automatically; otherwise it prints the same completion contract for the user to copy into the host's mechanism. Commit locally and wait for the user to push.
- **Mental Model:** The portable source principle is a **goal-setting backstop**: a durable completion contract that carries objective, desired end state, verification signal, important constraints, stop/block condition, and compact progress expectations when useful. Concrete host mechanisms (`/goal`, Pi `start_goal`, etc.) are implementation details, not the shared prompt language. Source prompts, docs, sync references, generated dist, and drift tests must all align so Pi no longer loses the backstop and other targets no longer treat `/goal` as the source principle.

## 2. Approach
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** Edit canonical source prompt/docs under `claude-plugins/manifest-dev/` plus the source-owned `sync-tools` reference files under `.claude/skills/sync-tools/references/`. Regenerate or hand-sync `dist/{codex,opencode,pi}` according to those references. Add/adjust tests that assert the capability-level invariant. Preserve the already-created ADR and glossary update. Commit locally; do not push.
- **Execution Order:**
  - D1 (source prompt/docs + sync-reference wording) → D2 (versioning + dist sync) → D3 (tests/verification + local commit)
  - Rationale: source/reference wording defines the intended generated state; dist and tests follow; commit happens only after verification.
- **Risk Areas:**
  - [R-1] The change merely renames `/goal` but keeps hardcoded host mechanics as the shared rule | Detect: prompt review and grep over source docs for recommended `/goal`-as-principle language.
  - [R-2] Universal language becomes too vague and models stop using available goal-setting tools | Detect: affected skill text explicitly says to use the harness-native goal-setting capability automatically when available and only print fallback text when not.
  - [R-3] Goal examples lose rigor while becoming portable | Detect: examples include durable objective/end state, verification signal, constraints, stop/block condition, and progress expectations where useful.
  - [R-4] Pi dist continues dropping the backstop or mentions no equivalent behavior | Detect: dist/pi affected skill/docs contain universal goal-setting guidance without literal `/goal` as required.
  - [R-5] Dist drift or broad sync fallout | Detect: compare source/dist copies with expected target substitutions and review `git diff --stat` for scope.
  - [R-6] Tests overfit to one phrase or one harness primitive | Detect: drift tests check capability-level invariants, not exact full prose except where exact syntax matters.
- **Trade-offs:**
  - [T-1] Exact host primitive reliability vs universal prompt portability → Prefer universal language because the user explicitly wants same behavior across harnesses without special harness logic; exact primitives can appear only as target examples if a distribution needs them.
  - [T-2] Comprehensive contract fields vs prompt bloat → Prefer a compact contract rubric plus concise examples, not a rigid form every goal must mechanically fill when unnecessary.

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] The change matches the accepted Read and does not scope-creep beyond universal goal-setting language, goal-quality contract upgrades, sync/dist/test alignment, versioning, ADR/context/manifest archival, and the requested local commit.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff on the current branch against origin/main. PASS only if the diff implements the accepted Read: source prompts/docs use universal goal-setting/completion-contract language instead of hardcoding `/goal` as the shared rule; available harness goal-setting is used automatically and copy-paste output is fallback; goal text follows the compact completion-contract rubric; sync references and generated dist align across Pi/Codex/OpenCode; tests guard the invariant; required version bumps and ADR/context/manifest archival are included; and there is no unrelated scope creep. PASS only if no LOW-or-higher findings. Report findings with severity and evidence.
    phase: 2
  ```
- [INV-G2] Edited prompt text passes prompt-engineering gap calibration.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review edited prompt-bearing files: claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md, claude-plugins/manifest-dev/skills/define/SKILL.md, claude-plugins/manifest-dev/skills/auto/SKILL.md, claude-plugins/manifest-dev/skills/do/SKILL.md, affected README/plugin metadata prose, and .claude/skills/sync-tools/references/{pi-cli.md,opencode-cli.md,codex-cli.md if changed}. PASS only if no MEDIUM-or-higher findings. Check especially: portable capability language rather than harness-bound primitives as source rules; no vague fallback that lets models skip goal-setting when a harness capability exists; no rigid checklist/mechanism-as-prescription; no arbitrary hardcoded turn bounds; examples are compact but carry objective/end state/verification/constraints/stop-block/progress where useful; no contradictory target-specific instructions.
    phase: 2
  ```
- [INV-G3] Distribution outputs are synchronized with source and target conversion rules.
  ```yaml
  verify:
    prompt: |
      Inspect source files and corresponding dist copies for affected skills/docs in dist/codex, dist/opencode, and dist/pi. PASS only if dist reflects current source with documented target substitutions: Pi keeps universal goal-setting backstop guidance without a literal `/goal` requirement; Codex/OpenCode keep equivalent universal guidance and may include host syntax/examples only as target-specific examples; no stale "Pi drops the backstop" or "keep `/goal` blocks" split remains; plugin-qualified skill references still follow each target's existing namespace rule. Also confirm `git status --short dist/` reflects only intentional regenerated/synced changes. FAIL with file:line evidence for drift or stale target behavior.
    phase: 1
  ```
- [INV-G4] Versioning is consistent with changed surfaces.
  ```yaml
  verify:
    prompt: |
      Check versions. PASS only if claude-plugins/manifest-dev/.claude-plugin/plugin.json is bumped from 2.15.0 to 2.16.0 (minor for user-visible prompt/distribution behavior), dist/opencode/plugin/package.json mirrors 2.16.0, repo-root package.json and packages/manifest-dev-pi-tools/package.json are bumped in lockstep from 0.11.5 to 0.11.6 because dist/pi shared assets changed, and .claude/skills/sync-tools/references/pi-cli.md's package example matches 0.11.6. PASS only if manifest-dev-tools plugin version remains unchanged unless its plugin files were edited. Report all versions found.
    phase: 1
  ```

## 4. Process Guidance
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] (auto) High-signal prompt updates only: replace old mechanism-specific language rather than adding parallel duplicated rules.
- [PG-2] (auto) Preserve existing effective posture clauses: truth over speed, honest verification, real blockers only, and user-filled stop bounds; convert mechanism framing, not the intent.
- [PG-3] (auto) Edit canonical source under `claude-plugins/manifest-dev/skills/...` for plugin skills. `.claude/skills/sync-tools` is source-owned for sync-tools references; update it directly when changing conversion rules. Do not treat `dist/` as the canonical source.
- [PG-4] (auto) Run targeted tests after edits. Prefer existing repo tests plus focused grep/compare checks over manual inspection alone.
- [PG-5] (auto) Commit locally with a conventional commit message; do not push.

## 5. Known Assumptions
- [ASM-1] (auto) `manifest-dev` plugin gets a minor bump (2.15.0 → 2.16.0) because this changes user-visible unattended-run behavior across skills/docs. Impact if wrong: version level can be adjusted before commit.
- [ASM-2] (auto) Pi package versions get a patch bump (0.11.5 → 0.11.6) because dist/pi shared skill assets change but Pi runtime TypeScript behavior does not. Impact if wrong: semver level can be adjusted; lockstep remains required.
- [ASM-3] (auto) `manifest-dev-tools` plugin version does not change because `sync-tools` is source-owned outside the plugin payload and no manifest-dev-tools plugin skill is edited. Impact if wrong: a missing plugin bump is easy to add.
- [ASM-4] (auto) The existing `Stop after N turns if it stalls` placeholder remains acceptable as a user-filled stop bound, but examples should also mention compact progress/checkpoint expectations when useful. Impact if wrong: prompt review may request tighter wording.
- [ASM-5] (auto) Fully automated sync-tools is a skill procedure rather than a script; if no runnable generator exists, manually synchronize affected dist files according to the reference rules and verify with tests/grep. Impact if wrong: sync drift is caught by INV-G3/tests.

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: Universal source prompt/docs and sync-reference wording

**Acceptance Criteria:**
- [AC-1.1] Affected source skills use universal goal-setting language with automatic harness-native use and manual copy-paste fallback.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md, define/SKILL.md, auto/SKILL.md, and do/SKILL.md. PASS only if each affected unattended-run/backstop section states the portable behavior: set a durable completion goal using the active harness's goal-setting/continuation capability when available; otherwise print a copy-pasteable completion contract for the user. PASS only if `/goal` is not presented as the shared mechanism/principle in these source skill files. PASS only if figure-out under `/auto` still suppresses nested goal-setting only when the wrapping entrypoint clearly owns it. Report exact quotes.
    phase: 1
  ```
- [AC-1.2] Goal examples/instructions follow the completion-contract quality rubric without becoming a rigid checklist.
  ```yaml
  verify:
    prompt: |
      Inspect the goal/backstop examples and explanatory prose in the affected source skills. PASS only if the guidance says a good unattended goal is a compact completion contract with durable objective, desired end state, verification signal, important constraints, stop/block condition, and compact progress/checkpoint expectations when useful. PASS only if the concrete examples retain domain-appropriate rigor: figure-out Read full anatomy + independent re-derivation/rival stability; define/do all AC/GI PASS + done reported; auto full chain complete; honest verification/truth over speed; real blockers only; user-filled stall bound. FAIL if the rubric is absent, examples are vague, or a hardcoded numeric bound appears.
    phase: 1
  ```
- [AC-1.3] Source docs and plugin metadata no longer present `/goal` as the sole recommended mechanism.
  ```yaml
  verify:
    prompt: |
      Inspect README.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md, and claude-plugins/manifest-dev/.claude-plugin/plugin.json. PASS only if user-facing docs describe a harness-native goal-setting / continuation backstop at the capability level, with copy-paste fallback where appropriate, and no recommended prose says the universal way is specifically to wrap in `/goal`. Target-specific examples may mention syntax only if clearly framed as an example for hosts that use it. Report exact quotes.
    phase: 1
  ```
- [AC-1.4] Sync-tool references encode the universal behavior and remove the stale Pi-drop/OpenCode-keep split.
  ```yaml
  verify:
    prompt: |
      Read .claude/skills/sync-tools/references/pi-cli.md and opencode-cli.md, and codex-cli.md if changed. PASS only if the references say goal-setting backstop guidance is preserved/adapted as a universal capability across targets; Pi no longer says to drop the unattended backstop because it lacks `/goal`; OpenCode no longer says to keep `/goal` blocks as the principle; any target-specific syntax is framed as target adaptation/example only. Report exact quotes.
    phase: 1
  ```

### Deliverable 2: Versioning and generated distributions

**Acceptance Criteria:**
- [AC-2.1] Version files are bumped consistently.
  ```yaml
  verify:
    prompt: |
      Same as INV-G4. PASS only if manifest-dev plugin is 2.16.0, dist/opencode plugin is 2.16.0, Pi packages are 0.11.6 in lockstep, pi-cli.md example is 0.11.6, and manifest-dev-tools plugin is unchanged unless its plugin payload changed. Report versions.
    phase: 1
  ```
- [AC-2.2] `dist/` affected skill/docs copies reflect the source and target rules.
  ```yaml
  verify:
    prompt: |
      Same as INV-G3. Additionally compare the affected source skill files with their Codex/OpenCode/Pi counterparts allowing only documented target substitutions (namespace stripping, session-line rules, and target syntax examples). PASS if no affected dist copy carries stale `/goal`-only or Pi-drop behavior. Report discrepancies.
    phase: 1
  ```
- [AC-2.3] Existing distribution/reference tests cover the new invariant or a new drift guard is added.
  ```yaml
  verify:
    prompt: |
      Inspect tests/. PASS only if a test or targeted scripted check asserts the goal-setting invariant across source and dist: source uses universal goal-setting language, Pi dist preserves the backstop without literal `/goal` dependency, and Codex/OpenCode do not regress to stale target-only wording. The guard should not overfit to one full paragraph. Report the test name or scripted command.
    phase: 1
  ```

### Deliverable 3: Verification, manifest archival, and local commit

**Acceptance Criteria:**
- [AC-3.1] Targeted verification passes.
  ```yaml
  verify:
    prompt: |
      Run useful local checks for this change. At minimum: pytest tests/test_dist_skill_references.py; targeted grep checks for stale "Pi has no `/goal` ... drop" / "keep the `/goal` blocks" split; and the repo pre-PR command if feasible: ruff check --fix claude-plugins/ && black claude-plugins/ && mypy. PASS only if checks pass or any failure is unrelated and documented with evidence. Report commands and exit status.
    phase: 1
  ```
- [AC-3.2] The manifest is written at the exact requested path and archived into `.manifest/`.
  ```yaml
  verify:
    prompt: |
      PASS only if /Users/aviram.kofman/.manifest-dev/manifests/manifest-20260623T103501Z-auto.md exists and an archival copy exists under .manifest/ with a descriptive kebab-case filename. FAIL if either is missing. Report paths.
    phase: 1
  ```
- [AC-3.3] A local commit exists and nothing was pushed.
  ```yaml
  verify:
    prompt: |
      PASS only if the branch contains a local commit with a conventional commit message for this work, working tree is clean, and no push was performed by this run. Report branch, commit hash/message, and `git status --short --branch`.
    phase: 1
  ```
