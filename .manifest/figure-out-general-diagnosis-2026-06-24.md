# Definition: Generalize figure-out diagnosis probes

## 1. Intent & Context
- **Goal:** Land a right-sized prompt/skill update that teaches `figure-out` general-purpose diagnosis lessons from the RCA session without encoding staging/prod or Nexus-specific details, on a new branch with a local commit only.
- **Mental Model:** The missed behavior was not generic truth-seeking — core `figure-out` already carries that. The gap is diagnosis-shaped probe fuel and autonomous completion wording: locating where a symptom appears is not enough; for comparative or layer-crossing diagnosis the agent must explain why this case differs or earn underdetermination by running/blocking discriminating probes. Goal/backstop contracts should be detailed enough for a fresh continuation checker to enforce the real completion bar; every word earns its place, but brevity is not the objective.
- **Repos:** `manifest-dev`: `/Users/aviram.kofman/Documents/Projects/manifest-dev`

## 2. Approach
- **Architecture:** Patch source-owned skill files under `claude-plugins/manifest-dev/skills/figure-out/`; regenerate generated dist targets with `sync-tools`; bump source-owned package/plugin versions required by repo conventions; commit locally on `fix/figure-out-general-diagnosis` without pushing.
- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: source prompt wording must settle before generated distributions and version metadata can be synchronized, and commit happens only after verification.
- **Risk Areas:**
  - [R-1] Overfit RCA wording | Detect: prompt-quality review flags staging/prod/Nexus/provider-specific or tech-only language in the general-purpose surfaces.
  - [R-2] Prompt bloat | Detect: prompt-quality review flags checklist-y, prescriptive, or redundant wording.
  - [R-3] Distribution drift | Detect: generated dist copies match source after sync and metadata versions are consistent.
- **Trade-offs:**
  - [T-1] Specific RCA checklist vs general probe fuel → Prefer general probe fuel because `figure-out` is a general-purpose thinking skill.

## 3. Global Invariants
- [INV-G1] The change remains general-purpose and does not encode the staging/prod/Nexus incident as a special case.
  ```yaml
  verify:
    prompt: |
      Review the final diff in /Users/aviram.kofman/Documents/Projects/manifest-dev. PASS only if the figure-out source prompts express portable diagnosis principles rather than staging/prod, Nexus, OpenAI, provider, gateway, Kubernetes, service-env, or other incident-specific mechanics. It is OK for generated dist files to mirror the same portable wording. FAIL with exact file/line evidence if any general-purpose skill surface overfits to the original incident.
    phase: 1
  ```

- [INV-G2] Prompt quality stays calibrated.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill and review the changed source prompt files under claude-plugins/manifest-dev/skills/figure-out/. PASS only if there are no MEDIUM-or-higher prompt-quality findings. Pay special attention to prompt-engineering principles: every added line closes the observed gap, no broad checklist bloat, no prescriptive HOW where a principle suffices, no contradiction with existing figure-out discipline, and progressive disclosure remains correct.
    phase: 1
  ```

- [INV-G3] Source, generated distributions, and versions are synchronized.
  ```yaml
  verify:
    prompt: |
      Inspect /Users/aviram.kofman/Documents/Projects/manifest-dev. PASS only if: (1) generated dist copies for figure-out match the source figure-out changes after running sync tooling; (2) claude-plugins/manifest-dev/.claude-plugin/plugin.json has an appropriate patch version bump for changed plugin prompts; (3) repo-root package.json and .claude/skills/sync-tools/references/pi-cli.md agree on the Pi package version if dist/pi changed; and (4) git status contains no unexpected unsynced generated artifacts. FAIL with exact mismatches.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] (auto) Edit source files, not generated dist files; use sync tooling to update dist.
- [PG-2] (auto) Keep probe additions compact, but make goal/backstop contracts detailed enough to be auditable. Do not optimize goals for brevity when more specificity prevents premature completion.
- [PG-3] (auto) Commit locally with a conventional commit; do not push.

## 5. Known Assumptions
- [ASM-1] Patch-level version bumps are sufficient. Default: bump `manifest-dev` and Pi package by one patch version. Impact if wrong: release metadata could understate a prompt behavior change.
- [ASM-2] No README update is required. Default: changed behavior is internal skill calibration, not a new component or user-facing command. Impact if wrong: docs may omit a subtle behavior refinement.

## 6. Deliverables

### Deliverable 1: Source prompt changes

**Acceptance Criteria:**
- [AC-1.1] `DIAGNOSIS.md` includes compact, general-purpose probes for comparative diagnosis, evidence layer/source attribution, locus-vs-cause, and controlled contrast when passive evidence is confounded.
  ```yaml
  verify:
    prompt: |
      Inspect claude-plugins/manifest-dev/skills/figure-out/tasks/DIAGNOSIS.md. PASS only if it includes compact general-purpose probe fuel covering: comparative diagnosis (X vs Y, before/after, cohort/context differences), layer/source attribution of evidence, locus-vs-cause distinction, and a controlled contrast/replay/intervention trade-off when passive observations are sparse/mixed/confounded. FAIL if these ideas are absent, too verbose, or framed as tech-only/staging-only instructions.
    phase: 1
  ```

- [AC-1.2] `autonomous.md` backstop uses detailed, general-purpose diagnosis wording.
  ```yaml
  verify:
    prompt: |
      Inspect claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md. PASS only if the autonomous Read-completion contract no longer says “layer-localized” or “mechanism-splitting probes” and instead states a detailed general-purpose completion bar: full Read anatomy, explicit Evidence Ledger / assumption separation, independent re-derivation or explicit unavailability, no mere localization for diagnosis, concrete mechanism for diagnosis (including why this case differs for comparative questions), and earned underdetermination by naming surviving explanations plus feasible distinguishing probes that were run or blocked. FAIL if the wording is weaker, duplicative, incident-specific, or optimized for brevity at the expense of auditability.
    phase: 1
  ```

- [AC-1.3] `/auto` parent backstop carries the detailed autonomous Read bar it suppresses in child `figure-out --autonomous`.
  ```yaml
  verify:
    prompt: |
      Inspect claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS only if the full-chain goal includes the same detailed autonomous Read bar needed when figure-out's standalone backstop is suppressed: full Read anatomy, evidence/assumption separation, independent re-derivation or explicit unavailability, rival-set convergence, confidence/evidence/overturn conditions, and the diagnosis-specific no-mere-localization / concrete-mechanism-or-earned-underdetermination rule. FAIL if /auto carries only a terse or weaker Read contract.
    phase: 1
  ```

### Deliverable 2: Distribution and version sync

**Acceptance Criteria:**
- [AC-2.1] Multi-CLI distributions are regenerated from source and include the same figure-out prompt changes.
  ```yaml
  verify:
    prompt: |
      Compare source figure-out files with dist/opencode, dist/codex, and dist/pi generated counterparts where those files exist. PASS only if the diagnosis/autonomous wording changes are present consistently in all generated targets and sync metadata has been updated by the sync process. FAIL with exact missing targets or stale metadata.
    phase: 2
  ```

- [AC-2.2] Version metadata is bumped consistently.
  ```yaml
  verify:
    prompt: |
      Inspect claude-plugins/manifest-dev/.claude-plugin/plugin.json, package.json, and .claude/skills/sync-tools/references/pi-cli.md. PASS only if manifest-dev plugin version is bumped by an appropriate patch increment, repo-root Pi package version is bumped by an appropriate patch increment because dist/pi changed, and the pi-cli.md package manifest example matches package.json. FAIL with exact mismatches.
    phase: 2
  ```

### Deliverable 3: Local-only commit

**Acceptance Criteria:**
- [AC-3.1] Work is committed locally on a new branch and not pushed.
  ```yaml
  verify:
    prompt: |
      Inspect git state in /Users/aviram.kofman/Documents/Projects/manifest-dev. PASS only if the current branch is not main, there is a local commit containing the verified changes, working tree is clean, and the branch has not been pushed/upstreamed. FAIL if on main, uncommitted changes remain, no commit exists, or an upstream/push is detected.
    phase: 3
  ```
