# Definition: Land Host Continuation ADR

## 1. Intent & Context
- **Goal:** Land the accepted architecture decision that manifest-dev should align Pi `/do` with the portable main-agent verifier protocol and treat host goal/continuation as an optional outer backstop, then commit and push the ADR branch.
- **Mental Model:** This task records the decision only. It does not implement the Pi runtime simplification. The ADR supersedes prior Pi-runtime verifier-fanout target architecture in principle while keeping independent verifier executions per AC/GI as the artifact-trust mechanism.

## 2. Approach
- **Architecture:** Add one MADR-style ADR under `docs/adr/`; do not modify runtime code or broad docs in this landing slice.
- **Execution Order:** D1 (ADR content) → D2 (archive/verification) → D3 (commit/push)
  - Rationale: The ADR is the durable artifact; verification and archival prove it is landed intentionally; commit/push publishes it.
- **Risk Areas:**
  - [R-1] ADR accidentally frames the decision around a machine-specific goal plugin | Detect: grep for local/plugin-specific terms in the ADR.
  - [R-2] ADR overstates host support by treating Codex as no-continuation or all hosts as continuation-capable | Detect: inspect wording for capability-based framing and Codex `/goal` as an example only when enabled.
  - [R-3] Scope creep into runtime implementation | Detect: git diff includes only ADR/manifest archival files for this slice.
- **Trade-offs:**
  - [T-1] Deterministic Pi runtime enforcement vs portable `/do` + host continuation → Record the portable model as accepted, explicitly naming lost Pi guarantees.

## 3. Global Invariants
- [INV-G1] The landing matches the accepted decision and does not implement runtime changes.
  ```yaml
  verify:
    prompt: |
      Inspect the final diff on the current branch. PASS only if it records the host-continuation `/do` architecture decision as an ADR, archives this manifest, and does not change runtime code, generated distributions, or unrelated docs. FAIL if implementation code changed or the diff goes beyond decision-record landing.
    phase: 1
  ```
- [INV-G2] The ADR is host-capability based and avoids machine-specific goal-plugin framing.
  ```yaml
  verify:
    prompt: |
      Read docs/adr/20260623-use-host-continuation-as-optional-do-backstop.md. PASS only if it frames goal/continuation as a generic host capability, names Codex `/goal` only as an example of a continuation-capable host when enabled, avoids naming any local/private goal plugin or machine-specific setup, and says hosts/configurations without continuation run normal prompt-level `/do` without continuous host enforcement. FAIL with exact quotes otherwise.
    phase: 1
  ```

## 4. Process Guidance
- [PG-1] Keep this landing to the ADR and manifest archival; implementation belongs in a later manifest.
- [PG-2] Commit locally with a conventional commit message and push the branch when verification passes.

## 5. Known Assumptions
- [ASM-1] (auto) ADR-only change does not require plugin or package version bumps. Impact if wrong: add a version bump in a follow-up before release.
- [ASM-2] (auto) Lightweight textual verification is sufficient because no code or generated distribution changes are made. Impact if wrong: run broader checks, though no executable surface changed.

## 6. Deliverables

### Deliverable 1: Superseding host-continuation ADR

**Acceptance Criteria:**
- [AC-1.1] The ADR exists and records the accepted decision.
  ```yaml
  verify:
    prompt: |
      PASS only if docs/adr/20260623-use-host-continuation-as-optional-do-backstop.md exists, has Status Accepted, states it supersedes the target-architecture portions of the older Pi runtime verifier ADRs, and records the decision to align Pi `/do` with portable main-agent verifier protocol plus optional host continuation backstop. Report file path and key quotes.
    phase: 1
  ```
- [AC-1.2] The ADR captures both gains and losses.
  ```yaml
  verify:
    prompt: |
      Read the ADR. PASS only if Consequences include positive gains (reduced Pi runtime complexity/source-surface drift, one conceptual `/do`, continuation-capable hosts can provide stronger continuous execution, independent verifier executions remain the trust mechanism) and negative tradeoffs (loss of Pi deterministic runtime gate inventory/aggregation, more prompt/checker dependence, no continuous enforcement without host capability, need tests/review for skipped gates/weak evidence/phase drift/premature completion). FAIL if either side is missing.
    phase: 1
  ```

### Deliverable 2: Manifest archival and branch landing

**Acceptance Criteria:**
- [AC-2.1] This manifest is archived under `.manifest/` with a descriptive name.
  ```yaml
  verify:
    prompt: |
      PASS only if /Users/aviram.kofman/.manifest-dev/manifests/manifest-20260623T142347Z-auto.md exists and .manifest/host-continuation-do-backstop-2026-06-23.md exists with identical content. FAIL if either path is missing or contents differ.
    phase: 1
  ```
- [AC-2.2] The branch is committed and pushed.
  ```yaml
  verify:
    prompt: |
      PASS only if the current branch is feature/universal-do-continuation-adr, the branch contains a conventional local commit for this ADR landing, `git status --short --branch` is clean relative to tracked/untracked intentional files, and the branch has been pushed to origin. Report branch, commit hash/message, and push target. FAIL if uncommitted files remain or push failed.
    phase: 1
  ```
