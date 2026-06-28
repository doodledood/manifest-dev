# Definition: Generalize Figure-Out Status-Quo Purpose Probe

## 1. Intent & Context
- **Goal:** Land a general `figure-out` skill improvement so a Read that implies changing/removing the status quo first tests what purpose the status quo may serve, without overfitting to any one incident, domain, or implementation detail.
- **Mental Model:** The failure mode is general: an investigation can correctly identify that an existing condition contributes to a symptom, then prematurely recommend changing it without first treating the existing condition's purpose as a live rival explanation or trade-off. The fix belongs in core `figure-out` if it is conditional, general, and non-preservationist.

## 2. Approach
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** Add one concise rule to the always-loaded `figure-out` core near the live-rival/disconfirming-probe discipline. Keep task-file probes unchanged unless verification shows the rule is too broad.
- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: update the source skill first, sync derived distributions/metadata second, verify and commit last.
- **Risk Areas:**
  - [R-1] Overfitting to a single observed incident | Detect: wording mentions a specific product domain, implementation detail, tool, artifact path, or one-off mechanism.
  - [R-2] Overcorrecting into status-quo preservation | Detect: wording treats old intent as a veto rather than evidence.
  - [R-3] Distribution drift | Detect: source plugin, local skill symlink target, and generated Pi/OpenCode/Codex outputs disagree after sync.
- **Trade-offs:**
  - [T-1] General core rule vs task-file specificity → Prefer a core rule because the gap applies whenever a Read implies changing/removing an existing state, behavior, constraint, or artifact; keep it conditional to avoid bloat.

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] The change remains general and non-overfit.
  ```yaml
  verify:
    prompt: |
      Review the diff for overfitting. PASS only if the figure-out change is expressed as a general status-quo-purpose rule and does not mention a specific incident, product domain, implementation detail, artifact path, or required evidence-gathering tool. FAIL with exact offending lines if it overfits. BLOCKED only if the diff cannot be inspected.
    phase: 1
  ```

- [INV-G2] Prompt quality holds.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-prompt skill and review the changed figure-out prompt/skill text against prompt-engineering principles. PASS only if there are no MEDIUM-or-higher issues. In particular check: every added line closes the observed gap, the rule is conditional rather than absolute, status-quo intent is evidence not a veto, the wording holds across domains, and no prompt bloat or duplicated rule was introduced. Report findings with severity.
    phase: 2
  ```

- [INV-G3] Change intent is satisfied without unrelated edits.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the change. PASS only if the diff implements the requested general figure-out improvement, includes required manifest-dev metadata/sync updates, and contains no unrelated changes. Report any LOW-or-higher findings with severity.
    phase: 2
  ```

- [INV-G4] Repository checks pass.
  ```yaml
  verify:
    prompt: |
      Inspect the verification evidence from the run. PASS only if the maintainer ran the relevant local repository checks for this prompt/skill distribution change (at minimum sync tooling or an explicit no-op check, plus formatting/lint/type checks when applicable) and the checks passed, or if a check is inapplicable with a concrete reason. FAIL if required verification is missing or failed. BLOCKED only if required tooling is unavailable for reasons outside the repo.
    phase: 3
  ```

## 4. Process Guidance
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] High-signal changes only (auto): every prompt change must address the observed real failure mode. Do not change for style or add broad checklists.
- [PG-2] Calibrate emotional tone (auto): keep wording low-arousal and trusted-advisor-like.
- [PG-3] Prompt-engineering discipline (auto): prefer a small replacement/addition that states what and why, not a prescribed mechanism.
- [PG-4] Publish only when explicitly requested by the user.

## 5. Known Assumptions
- [ASM-1] README updates are not required for a one-line behavioral calibration that does not add/rename/remove a component. | Default: skip README edits unless sync tooling reveals generated docs drift. | Impact if wrong: documentation may omit a subtle behavior change, but component inventory remains accurate.

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: Source skill update

**Acceptance Criteria:**
- [AC-1.1] `figure-out` core includes a concise conditional rule: when a Read implies changing/removing an existing state, behavior, constraint, or artifact, test what purpose the status quo may serve and whether that purpose is still desired.
  ```yaml
  verify:
    prompt: |
      Inspect the changed figure-out source skill. PASS only if the always-loaded core contains a concise conditional status-quo-purpose rule that applies broadly, and if the rule says status-quo intent is evidence to weigh rather than a veto. FAIL with exact missing or problematic text otherwise.
    phase: 1
  ```

### Deliverable 2: Distribution and metadata consistency

**Acceptance Criteria:**
- [AC-2.1] All generated/distributed skill copies and required package/plugin metadata are consistent with the source change.
  ```yaml
  verify:
    prompt: |
      Inspect the repo state and sync evidence. PASS only if source plugin files, local symlinked skill surfaces, and generated distribution outputs that should contain the figure-out skill are consistent after running the project's sync workflow, and relevant package/plugin versions were bumped according to repository policy. FAIL with the inconsistent file list otherwise.
    phase: 2
  ```

### Deliverable 3: Branch publication when requested

**Acceptance Criteria:**
- [AC-3.1] The work is committed on a non-main branch and publication matches explicit user instruction.
  ```yaml
  verify:
    prompt: |
      Inspect git state. PASS only if the current branch is not main/master, the working tree is clean, the latest local commits contain the implemented manifest-dev figure-out prompt change and sync metadata, and any push was performed only after explicit user instruction. FAIL with the branch/status/commit issue otherwise.
    phase: 3
  ```
