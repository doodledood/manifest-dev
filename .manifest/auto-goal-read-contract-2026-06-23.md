# Definition: Compose /auto Goal with Autonomous Read Contract

## 1. Intent & Context
- **Goal:** Strengthen `/auto` so its single full-chain parent goal explicitly carries the nested `figure-out --autonomous` Read-completion contract, not just the `/do` gate-ledger contract, and make `figure-out --autonomous` supplement weak parent backstops instead of suppressing its own goal whenever any parent exists.
- **Mental Model:** `/auto` should have one parent goal spanning figure-out → define → do. Splitting into sequential child goals is wrong because continuation can stop after the first child. But when a child suppresses its standalone goal under `/auto`, the parent must carry that child’s real completion bar. The Read is the basis for the Manifest; a thin Read can produce a rigorously verified wrong plan.

## 2. Approach
- **Architecture:** Keep one `/auto` full-chain goal. Patch the parent goal text to include autonomous Read anatomy and patch `figure-out --autonomous` suppression to require a parent carrying that Read contract; otherwise supplement. Sync generated distributions and update docs/version/tests.
- **Execution Order:**
  - D1 source prompt changes → D2 docs/dist/version/test sync → D3 verification/commit/push
  - Rationale: source skills are authoritative; generated targets follow.
- **Risk Areas:**
  - [R-1] Accidentally creating two sequential goals instead of one parent goal | Detect: prompt review and tests confirm `/auto` owns one full-chain backstop.
  - [R-2] Parent goal over-bloats or duplicates all of figure-out’s prompt | Detect: prompt review confirms it carries the completion bar, not a second skill body.
  - [R-3] `figure-out --autonomous` supplements too aggressively and creates duplicate goals even when parent is sufficient | Detect: wording says supplement only when visible parent lacks the Read-completion contract; when in doubt still prefer missing-backstop safety.

## 3. Global Invariants
- [INV-G1] Change intent: the diff only strengthens `/auto`’s parent goal composition and `figure-out --autonomous` weak-parent handling, plus required docs/dist/version/tests.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff on the current branch against origin/feature/stronger-do-goal-contract. PASS only if the diff preserves the one-parent-goal /auto architecture, makes that parent goal explicitly carry the autonomous Read-completion contract and the /do gate-ledger contract, makes figure-out --autonomous supplement weak parents rather than blindly suppressing, includes required docs/dist/version/test updates, and avoids unrelated scope creep. PASS only if no LOW-or-higher findings. Report findings with severity and evidence.
    phase: 2
  ```
- [INV-G2] Prompt quality: edited prompt-bearing files pass prompt-engineering calibration.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review edited prompt-bearing files, especially auto/SKILL.md, figure-out/references/autonomous.md, README examples, generated dist copies, and new/updated tests. PASS only if no MEDIUM-or-higher findings. Check that wording closes the real nested-Read gap, stays portable, avoids sequential-goal confusion, avoids prompt bloat, and keeps low-arousal trusted-advisor tone. Report findings with severity and file evidence.
    phase: 2
  ```
- [INV-G3] Project verification commands pass.
  ```yaml
  verify:
    prompt: |
      From the repo root, run relevant checks after implementation: .venv/bin/python -m pytest tests/test_dist_skill_references.py tests/test_dist_install_uninstall.py tests/test_pi_extension_runtime.py; .venv/bin/ruff check claude-plugins/; .venv/bin/black --check claude-plugins/; .venv/bin/mypy. Also run ruff/black on edited Python tests. PASS if available commands pass, or any unavailable command is skipped with evidence. FAIL on available command failures and report command output.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Use prompt-engineering discipline: add only completion-contract language that closes the observed gap; don’t copy the whole figure-out skill into `/auto`.
- [PG-2] Do not create a new branch. Commit and push on `feature/stronger-do-goal-contract`.
- [PG-3] Preserve generated distributions as faithful target-adapted copies of source.

## 5. Known Assumptions
- [ASM-1] (auto) Patch bumps are sufficient: this is a prompt correctness improvement to existing skills, not a new component or schema break. Impact if wrong: version metadata may under-signal compatibility.
- [ASM-2] (auto) Only the core plugin and Pi package versions need bumps; `manifest-dev-tools` source is not changed. Impact if wrong: tools plugin metadata would be stale only if a tools skill changes.

## 6. Deliverables

### Deliverable 1: Source goal contracts

**Acceptance Criteria:**
- [AC-1.1] `/auto` parent goal explicitly composes the autonomous Read contract and the `/do` gate-ledger contract.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS only if /auto still establishes one durable full-chain parent backstop before chaining, and the copy-pasteable contract requires: (1) figure-out names a Read with full autonomous Read anatomy, including load-bearing branches pressed, assumptions surfaced, independent re-derivation run or explicitly unavailable, rival set no longer moving, and evidence/confidence/overturn conditions; (2) /define writes the manifest; (3) /do reports /done with every AC/GI carrying fresh independent verifier PASS evidence in a manifest gate ledger. PASS only if it does not tell /auto to run separate sequential child goals. FAIL with missing or conflicting wording.
    phase: 1
  ```
- [AC-1.2] `figure-out --autonomous` suppresses its standalone goal only when the visible parent carries the Read-completion contract, and supplements weak parents.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md. PASS only if the standalone-backstop suppression rule says to suppress only when the visible broader parent workflow carries the Read-completion contract; when a parent is visible but weak or only says "Read named", it must not replace or narrow the parent into a Read-only goal. PASS only if it says to augment the parent only when the harness can do so without narrowing it; otherwise print or carry the Read-level contract as a local checkpoint and satisfy it before returning to the parent chain. FAIL with missing or conflicting wording.
    phase: 1
  ```

### Deliverable 2: Docs, dist, and regression coverage

**Acceptance Criteria:**
- [AC-2.1] User-facing `/auto` docs/examples describe the full-chain goal as carrying the Read-completion bar, not merely “Read named.”
  ```yaml
  verify:
    prompt: |
      Inspect README.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md, and dist docs changed by this branch. PASS only if /auto unattended guidance describes one full-chain goal whose figure-out phase requires full Read anatomy / load-bearing branches / re-derivation or equivalent, while preserving the /do gate-ledger requirement. FAIL with stale weak examples that only say "Read named" as the figure-out completion bar.
    phase: 1
  ```
- [AC-2.2] Generated distributions match source changes with target-appropriate substitutions.
  ```yaml
  verify:
    prompt: |
      Inspect dist/codex, dist/opencode, and dist/pi copies of auto/SKILL.md and figure-out/references/autonomous.md. PASS only if the source changes appear in all targets, Codex keeps plugin-qualified references where source has them, OpenCode/Pi use target-appropriate bare skill references, Pi prompt aliases remain present, and no generated copy contains stale weak /auto Read-goal wording. FAIL with missing or drifted paths.
    phase: 1
  ```
- [AC-2.3] Regression tests cover the full-chain Read contract and weak-parent supplement behavior.
  ```yaml
  verify:
    prompt: |
      Inspect tests/test_dist_skill_references.py. PASS only if tests assert /auto parent goals across source and dist include the autonomous Read-completion contract (full anatomy, load-bearing branches, independent re-derivation, rival set no longer moving) and assert figure-out autonomous suppression supplements weak parents / "Read named" parents without replacing or narrowing the broader parent into a Read-only goal. FAIL if tests only check generic goal-setting or only the /do gate ledger.
    phase: 1
  ```
- [AC-2.4] Version metadata is bumped consistently for changed surfaces.
  ```yaml
  verify:
    prompt: |
      PASS only if claude-plugins/manifest-dev/.claude-plugin/plugin.json is bumped by patch from 2.16.3 to 2.16.4, repo-root package.json is bumped by patch from 0.12.3 to 0.12.4, generated Codex/OpenCode/Pi package metadata and sync reference examples that mirror those versions are in sync, and manifest-dev-tools remains 0.27.2 unless a tools source file changed. Report each version found.
    phase: 1
  ```

### Deliverable 3: Landed current branch

**Acceptance Criteria:**
- [AC-3.1] This manifest is archived in the repo.
  ```yaml
  verify:
    prompt: |
      PASS only if /Users/aviram.kofman/.manifest-dev/manifests/manifest-20260623T203839Z-auto.md exists and .manifest/auto-goal-read-contract-2026-06-23.md exists with identical content. FAIL if either path is missing or contents differ.
    phase: 1
  ```
- [AC-3.2] The change is committed and pushed on the existing branch.
  ```yaml
  verify:
    prompt: |
      PASS only if the current branch is feature/stronger-do-goal-contract, has a conventional commit after 7a92e1b for the /auto Read-goal contract, working tree is clean, and local HEAD matches origin/feature/stronger-do-goal-contract. Report branch, commit hash/message, and git status --short --branch. FAIL otherwise.
    phase: 2
  ```
