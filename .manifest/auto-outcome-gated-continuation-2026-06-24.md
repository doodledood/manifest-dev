# Definition: Outcome-Gated Auto Continuation Contracts

## 1. Intent & Context
- **Goal:** Update manifest-dev's autonomous continuation guidance so full-chain `/auto` success is judged by durable final outcome evidence, while standalone `figure-out --autonomous` still completes on a full-anatomy Read.
- **Mental Model:** A figure-out **Read** buys process trust and is the deliverable only for standalone figure-out. In `/auto`, the Read is an upstream phase checkpoint that feeds `/define`; terminal success is the artifact-trust path: manifest written, `/do` reports `/done`, and every Manifest gate has fresh independent PASS evidence.

## 2. Approach
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** Update source prompt surfaces first (`auto`, `figure-out` autonomous), then user-facing docs and ADR context, then sync generated distributions from source.
- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: Prompt source is canonical; docs and generated distributions should follow source language.
- **Risk Areas:**
  - [R-1] Weakening figure-out autonomous rigor | Detect: source and docs still preserve standalone `figure-out --autonomous` full-anatomy Read completion.
  - [R-2] Leaving contradictory goal examples | Detect: grep for stale `/auto` wording that makes Read naming the terminal full-chain success condition.
  - [R-3] Distribution drift | Detect: run sync tooling after source changes and include generated updates.
- **Trade-offs:**
  - [T-1] Process compliance vs final outcome auditability → Prefer final outcome auditability for terminal goals because host checkers and manifest gates should validate durable artifacts; keep process compliance as checkpoints unless the process artifact is the deliverable.

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Prompt-quality gate: changed prompt/skill language should be calibrated, non-contradictory, and not overfit to one anecdote.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-prompt skill. Review this change's prompt/skill surfaces for prompt quality, focusing on whether goal-setting rules are clear, non-contradictory, edge-calibrated, and no more prescriptive than needed. PASS only if there are no MEDIUM-or-higher findings. Report any findings with severity and evidence.
    phase: 2
  ```

- [INV-G2] Change-intent gate: the diff should implement the intended boundary without broad unrelated churn.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff. PASS only if the changes directly implement outcome-gated `/auto` continuation contracts while preserving standalone `figure-out --autonomous` Read rigor, with no LOW-or-higher unrelated intent drift. Report findings with severity and evidence.
    phase: 2
  ```

- [INV-G3] Sync/version gate: generated distributions and version metadata reflect changed plugin/package surfaces.
  ```yaml
  verify:
    prompt: |
      Inspect the repository after implementation. PASS only if source prompt changes under claude-plugins/ are propagated to generated dist targets where applicable, plugin/package versions were bumped according to repo rules, and no generated target retains stale contradictory `/auto` goal language. Use git diff and grep evidence. Report FAIL with exact stale files or version omissions.
    phase: 2
  ```

## 4. Process Guidance
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Keep the change right-sized: replace the failing goal boundary; do not redesign figure-out, `/define`, `/do`, or host continuation generally.
- [PG-2] Preserve standalone `figure-out --autonomous` rigor; only demote Read anatomy from terminal `/auto` success to a phase checkpoint.
- [PG-3] Use source-owned plugin files as canonical, then run sync tooling for `dist/` rather than hand-editing generated files when possible.
- [PG-4] Commit locally on a new branch; do not push.

## 5. Known Assumptions
- [ASM-1] A patch version bump is sufficient for the manifest-dev plugin and Pi package. | Default: patch bump | Impact if wrong: release metadata may need a minor bump instead.
- [ASM-2] The 2026-06-23 universal goal-setting ADR should be superseded/clarified by a new ADR rather than edited in place. | Default: new ADR | Impact if wrong: ADR history may be too noisy, but immutability is preserved.

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: Source prompt contract update

**Acceptance Criteria:**
- [AC-1.1] `/auto` unattended-launch language defines terminal full-chain completion around manifest creation plus `/do` gate-ledger PASS evidence and `/done`; figure-out Read anatomy is framed as an if-invoked phase checkpoint, not a post-hoc terminal failure after `/do` PASS.
  ```yaml
  verify:
    prompt: |
      Inspect claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS only if the unattended-launch guidance and copy-paste contract make `/auto` terminal completion depend on manifest written + `/do` `/done` + every AC/GI fresh independent PASS evidence, while treating full-anatomy figure-out Read as a required phase checkpoint when figure-out runs rather than the final success criterion. FAIL if wording still says the full chain runs "until figure-out names a Read" as the primary terminal condition.
    phase: 1
  ```

- [AC-1.2] `figure-out --autonomous` source preserves standalone Read completion while allowing parent `/auto` contracts to carry the Read bar as a checkpoint inside a broader outcome-gated chain.
  ```yaml
  verify:
    prompt: |
      Inspect claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md. PASS only if the standalone autonomous figure-out backstop still completes on a named full-anatomy Read, and the suppression/parent-workflow language permits broader `/auto`-style contracts that own continuation through final artifact evidence while carrying the Read contract as a phase checkpoint. FAIL if standalone Read rigor is weakened or if parent contracts must treat Read naming as the final chain success condition.
    phase: 1
  ```

### Deliverable 2: Documentation and decision record alignment

**Acceptance Criteria:**
- [AC-2.1] User-facing docs explain the general rule: terminal goals/gates use auditable outcomes/artifacts; process rigor is a checkpoint or Process Guidance unless the process artifact itself is the deliverable.
  ```yaml
  verify:
    prompt: |
      Inspect README.md and claude-plugins/manifest-dev/README.md. PASS only if `/auto` continuation examples and prose align with outcome-gated terminal completion, preserve Read checkpoint language, and include or clearly imply the general rule separating outcome/artifact completion from process checkpoints. FAIL if stale docs still frame Read naming as the terminal full-chain success condition.
    phase: 1
  ```

- [AC-2.2] ADR history records the changed boundary without rewriting accepted history in place.
  ```yaml
  verify:
    prompt: |
      Inspect docs/adr/. PASS only if a new ADR or equivalent accepted decision record clarifies/supersedes the prior universal goal-setting wording about `/auto`, preserving the standalone figure-out completion condition while making full-chain `/auto` terminal success outcome-gated. FAIL if the old ADR is edited to silently change history or if no decision record captures the boundary shift.
    phase: 1
  ```

### Deliverable 3: Distribution sync, verification, and commit

**Acceptance Criteria:**
- [AC-3.1] Generated distributions and version metadata are synchronized with source changes.
  ```yaml
  verify:
    prompt: |
      Inspect git diff, dist/, claude-plugins/manifest-dev/.claude-plugin/plugin.json, package.json, and sync metadata. PASS only if generated target files reflect source prompt/doc changes where applicable and required versions are bumped consistently. FAIL with exact omissions.
    phase: 2
  ```

- [AC-3.2] The work is committed locally on a new branch and not pushed.
  ```yaml
  verify:
    prompt: |
      Inspect git branch, git status, and recent git log. PASS only if the current branch is not main, the changes are committed with a conventional commit, the working tree is clean except for no unrelated leftovers, and no push was performed. FAIL with evidence if uncommitted changes remain or branch/commit state is wrong.
    phase: 3
  ```
