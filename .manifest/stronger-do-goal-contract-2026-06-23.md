# Definition: Stronger /do Goal Completion Contract

## 1. Intent & Context
- **Goal:** Strengthen manifest-dev's unattended `/do` goal/backstop wording so a continuation checker can audit whether verification is actually complete: every Manifest Acceptance Criterion and Global Invariant must be enumerated in a gate ledger with fresh independent PASS evidence before `/done`.
- **Mental Model:** `/do` remains a portable prompt-level workflow. The goal is an outer liveness/completion backstop, not a Pi-specific runtime verifier scheduler. The improvement is prompt-level: make the completion contract evidence-shaped enough that "all done" without a complete, fresh verifier ledger is visibly non-terminal.

## 2. Approach
- **Architecture:** Update the source skills that establish unattended goals (`do`, `auto`, `babysit-pr`) and sync generated distributions/docs. Keep the existing accepted boundary: main agent runs verifier fanout; host continuation audits completion when available.
- **Execution Order:**
  - D1 source skill prompt edits → D2 docs/dist/versioning → D3 verification/land
  - Rationale: generated distributions and README examples should follow source prompt wording, not lead it.
- **Risk Areas:**
  - [R-1] Over-prescribing a runtime implementation instead of a goal contract | Detect: prompt review or architecture grep finds Pi/runtime scheduler language.
  - [R-2] Parent workflows keep weaker goals while suppressing `/do`'s standalone goal | Detect: `auto` and `babysit-pr` goal contracts explicitly carry the gate-ledger/fresh-PASS requirement.
  - [R-3] Dist or version drift | Detect: sync outputs and version checks.
- **Trade-offs:**
  - [T-1] Restore deterministic Pi runtime verifier vs strengthen portable goal contract → Prefer strengthen portable goal contract, because ADR 20260623 accepted host continuation as optional outer backstop and removed Pi-specific verifier runtime.
  - [T-2] Minimal goal phrase vs gate-ledger contract → Prefer gate-ledger contract, because the real failure mode is unverifiable summary claims; a ledger gives the checker concrete evidence to audit.

## 3. Global Invariants
- [INV-G1] Change intent: the branch diff implements only the stronger auditable-goal contract and required sync/version/docs updates.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff on the current branch against origin/main. PASS only if the diff strengthens unattended /do completion checking with a gate ledger / fresh independent PASS evidence contract, updates parent goals that suppress /do's standalone goal, preserves the prompt-level /do plus optional host-continuation architecture, includes required docs/dist/version updates, and avoids unrelated scope creep. PASS only if no LOW-or-higher findings. Report findings with severity and evidence.
    phase: 2
  ```
- [INV-G2] Prompt quality: edited prompt-bearing files pass prompt-engineering calibration.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review all edited prompt-bearing files, especially do/SKILL.md, auto/SKILL.md, babysit-pr/SKILL.md, README examples, and generated dist copies. PASS only if no MEDIUM-or-higher findings. Check that the wording closes the real gap (auditable completion), avoids over-prescriptive runtime mechanics, keeps low-arousal trusted-advisor tone, and does not add redundant or conflicting instructions. Report findings with severity and file evidence.
    phase: 2
  ```
- [INV-G3] Architecture boundary: no live source/docs claim Pi owns deterministic verifier scheduling or done gating.
  ```yaml
  verify:
    prompt: |
      Inspect live source, README docs, package metadata, tests, and dist files changed by this branch, excluding historical .manifest files and superseded ADR bodies unless newly edited. PASS only if the change preserves this boundary: /do is prompt-level and runs independent verifier executions; host goal/continuation is optional outer completion/liveness backstop; Pi does not own a package-specific runtime verifier scheduler, verdict aggregator, or code-level done gate. FAIL with file:line evidence for stale or newly introduced contradictory claims.
    phase: 1
  ```
- [INV-G4] Project verification commands pass.
  ```yaml
  verify:
    prompt: |
      From the repo root, run relevant checks after implementation: .venv/bin/python -m pytest tests/test_dist_skill_references.py tests/test_dist_install_uninstall.py tests/test_pi_extension_runtime.py; .venv/bin/ruff check claude-plugins/; .venv/bin/black --check claude-plugins/; .venv/bin/mypy. PASS if available commands pass, or any unavailable command is skipped with evidence. FAIL on available command failures and report command output.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Use the prompt-engineering discipline: add only wording that closes the observed gap, and prune/avoid restating natural behavior.
- [PG-2] Keep the architecture portable. The goal/backstop can require evidence and a ledger; it must not become a host-specific implementation protocol.
- [PG-3] Update generated distributions through the sync tooling or an equivalent faithful sync; do not hand-edit dist in ways that drift from source.

## 5. Known Assumptions
- [ASM-1] (auto) Patch version bumps are sufficient: the change improves existing skills and docs without adding a new component or breaking schema. Impact if wrong: release metadata under- or over-signals compatibility.
- [ASM-2] (auto) The relevant distribution sync is all targets because source skill changes affect multiple CLIs and Pi package assets. Impact if wrong: one host ships stale goal wording.

## 6. Deliverables

### Deliverable 1: Source skill goal contracts

**Acceptance Criteria:**
- [AC-1.1] `/do` standalone unattended launch requires an auditable gate ledger and fresh PASS evidence before completion.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/do/SKILL.md. PASS only if the Unattended launch section requires the manifest-completion contract to include a gate ledger after reading the manifest, covering every Acceptance Criterion and Global Invariant id, phase, verify.prompt source, latest independent verifier verdict, evidence, and freshness relative to the last relevant change. PASS only if completion requires every listed gate to have fresh PASS evidence and /done reported, and treats unverified, FAIL, stale, BLOCKED/actionable, or escalation-pending gates as non-terminal. PASS only if it says affected gates become stale after implementation changes and rejects self-attestation / "looks done" / summary claims in place of verifier output. FAIL with missing clauses.
    phase: 1
  ```
- [AC-1.2] `/auto` parent unattended goal carries the same `/do` gate-ledger/fresh-PASS requirement.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS only if the standalone full-chain goal/backstop still spans figure-out -> define -> do, and explicitly requires the /do phase to satisfy a manifest gate ledger with fresh independent PASS evidence for every AC/GI before /done. PASS only if it remains clear that /auto owns the parent backstop and nested /do should not set a competing narrower goal. FAIL with missing or conflicting wording.
    phase: 1
  ```
- [AC-1.3] `/babysit-pr` parent unattended goal carries the same manifest gate-ledger/fresh-PASS requirement.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md. PASS only if the standalone PR-tend backstop spans manifest discovery/synthesis and /do, still targets PR mergeable/pending/blocker states, never presses merge, and explicitly requires the /do phase to maintain a manifest gate ledger with fresh independent PASS evidence for every AC/GI before completion. PASS only if nested /do goal suppression remains coherent. FAIL with missing or conflicting wording.
    phase: 1
  ```

### Deliverable 2: Docs, generated distributions, and version metadata

**Acceptance Criteria:**
- [AC-2.1] User-facing goal examples/docs describe the stronger auditable completion contract.
  ```yaml
  verify:
    prompt: |
      Inspect README.md and dist/pi/README.md. PASS only if the recommended /do unattended goal text tells users to require a manifest gate ledger or equivalent enumeration of every AC/GI with fresh independent PASS evidence, no self-attestation/summary substitution, and no completion while any gate is unverified/FAIL/stale/BLOCKED-actionable/escalation-pending. PASS only if the prose still distinguishes /do verification from optional host continuation. FAIL with stale or weak examples.
    phase: 1
  ```
- [AC-2.2] Generated distributions match the source skill changes.
  ```yaml
  verify:
    prompt: |
      Inspect dist/opencode, dist/codex, and dist/pi copies of the changed skills/docs. PASS only if source changes to do, auto, and babysit-pr appear in the generated target copies with target-appropriate namespacing substitutions, Pi prompt aliases remain present, component namespace metadata remains coherent, and no generated target contains stale weaker goal wording where the source was strengthened. FAIL with missing or drifted paths.
    phase: 1
  ```
- [AC-2.3] Version metadata is bumped consistently for changed surfaces.
  ```yaml
  verify:
    prompt: |
      PASS only if claude-plugins/manifest-dev/.claude-plugin/plugin.json is bumped by patch from 2.16.2 to 2.16.3, claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json is bumped by patch from 0.27.1 to 0.27.2, repo-root package.json is bumped by patch from 0.12.2 to 0.12.3, generated Codex/OpenCode/Pi package metadata and sync reference examples that mirror those versions are in sync, and no unrelated major/minor bump appears. Report each version found.
    phase: 1
  ```

### Deliverable 3: Landed branch

**Acceptance Criteria:**
- [AC-3.1] This manifest is archived in the repo.
  ```yaml
  verify:
    prompt: |
      PASS only if /Users/aviram.kofman/.manifest-dev/manifests/manifest-20260623T195805Z-auto.md exists and .manifest/stronger-do-goal-contract-2026-06-23.md exists with identical content. FAIL if either path is missing or contents differ.
    phase: 1
  ```
- [AC-3.2] The change is committed and pushed on a new branch.
  ```yaml
  verify:
    prompt: |
      PASS only if the current branch is not main, has a conventional commit for the stronger /do goal contract, working tree is clean, and local HEAD matches origin/<current-branch>. Report branch, commit hash/message, and git status --short --branch. FAIL otherwise.
    phase: 2
  ```
