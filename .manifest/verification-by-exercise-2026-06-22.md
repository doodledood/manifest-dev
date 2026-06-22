# Definition: Verification-by-exercise — task-file encoding

## 1. Intent & Context
- **Goal:** Make "actually run the new behavior" a default expectation in manifest-dev's workflow, by (a) elevating the verification-design angle to a default press in figure-out's feature/code probes, (b) adding an additive default "exercise" gate to /define's FEATURE task file, and (c) refining /define's CODING E2E encoding rule from blunt "every case → INV-G" to scope-driven granularity. Prompt/guidance-only change to task files — no new skills, no plan-file, no manifest-as-test-list.
- **Mental Model:** Two surfaces compose. figure-out (understanding) reflexively establishes the *exercise approach* — booted how, risky new paths, test seam present or needed — but NOT the enumerated plan. /define (encoding) turns that approach into gates: an exercise gate alongside the existing inspect gates, with AC-vs-INV chosen by scope. The existing project test-run gate owns breadth; manifest criteria are for what you want independently fix-targeted.

## 2. Approach
*Initial direction, not rigid plan.*

- **Architecture:** Four task-file edits (markdown), a plugin version bump, README/dist sync. All edits land on the `claude-plugins/manifest-dev/` source files; `.claude/` paths resolve to the same files via symlink. dist/ is regenerated, not hand-edited.
- **Execution Order:**
  - D1 (figure-out probes) → D2 (/define FEATURE gate) → D3 (/define CODING rule) → D4 (version + READMEs + dist regen)
  - Rationale: content edits first so the sync/regen in D4 captures all of them; version bump and dist regen are the closing housekeeping.
- **Risk Areas:**
  - [R-1] Over-reach in figure-out probes — turning an awareness probe into a planning agenda, breaking the understanding→encoding boundary. | Detect: change-intent / review-prompt flags scope creep; probe files should stay terse "angles," not steps.
  - [R-2] FEATURE exercise gate worded as a hard always-on requirement, failing pure-logic/library changes with no runnable surface. | Detect: gate text must carry the conditional-but-default + BLOCKED-when-unbootable shape.
  - [R-3] dist/ drift — task files changed but dist/ regen skipped, leaving Codex/Pi/OpenCode copies stale. | Detect: post-regen `git status` shows dist/ updated; clean diff after a second regen.
- **Trade-offs:**
  - [T-1] Reflex vs cost → Prefer making exercise a *default-when-runnable* expectation (cheap smoke) over a heavy always-comprehensive gate, because comprehensive E2E is too expensive to default and breadth belongs in the suite.
  - [T-2] figure-out scope → Prefer figure-out establishing *approach only* over producing the full test plan, because the enumerated plan is /define's encoding job and the project guards that boundary.

## 3. Global Invariants

- [INV-G1] Changed task-file guidance is high-quality prompt text (clear, no conflicts, terse, no prescriptive-HOW creep, edges hold).
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review ONLY the changed task files in this diff:
      claude-plugins/manifest-dev/skills/figure-out/tasks/{FEATURE,CODING}.md and
      claude-plugins/manifest-dev/skills/define/tasks/{FEATURE,CODING}.md (git diff origin/main...HEAD).
      Judge them as guidance prompts: the figure-out probe edits must read as terse awareness angles (not a step-by-step
      planning agenda), and the /define edits must read as clean encoder data (Quality Gate rows / encoding rules).
      PASS only if no MEDIUM-or-higher findings. If review-prompt is unavailable, report BLOCKED.
    phase: 1
  ```
- [INV-G2] The change does exactly what the manifest intends — no scope drift, no unrelated edits, no contradiction with the established Read.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the change
      (git diff origin/main...HEAD). The intended change is THREE things only: (1) elevate verification-design
      from optional probe to default-press for runnable surfaces in figure-out's FEATURE.md/CODING.md probes
      (approach only, not full plans); (2) ADD an additive, conditional-but-default "exercise the new behavior"
      Quality Gate to /define's FEATURE.md — alongside, not replacing, the existing inspect gates; (3) refine
      /define's CODING.md E2E rule to scope-driven granularity (single-deliverable→AC, cross-cutting→INV-G,
      broad matrix→suite). PASS only if no LOW-or-higher findings (the diff matches this intent and nothing else
      material). Report findings with severity.
    phase: 1
  ```
- [INV-G3] Repo conventions honored: edits on `claude-plugins/` source (not `.claude/` copies), manifest-dev plugin version bumped (minor), READMEs synced per the CLAUDE.md checklist where components/capability changed.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=context-file-adherence and review the change
      (git diff origin/main...HEAD) against CLAUDE.md. Confirm: (a) task-file edits are to claude-plugins/manifest-dev/
      paths, not duplicated direct edits of .claude/ targets; (b) claude-plugins/manifest-dev/.claude-plugin/plugin.json
      version is bumped by a minor increment from 2.12.0; (c) README sync checklist applied as needed (these are
      guidance-content changes within existing task files — no new/renamed/removed components — so READMEs may legitimately
      need no change; flag only a genuine omission). PASS only if no MEDIUM-or-higher findings.
    phase: 1
  ```
- [INV-G4] Lint, format, and typecheck pass.
  ```yaml
  verify:
    prompt: |
      Run: ruff check claude-plugins/ && black --check claude-plugins/ && mypy
      PASS only if all three exit clean. On failure, report the failing command and output. BLOCKED if a tool
      is not installed/available.
    phase: 2
  ```
- [INV-G5] dist/ is regenerated and in sync with the changed source task files (no stale Codex/Pi/OpenCode copies).
  ```yaml
  verify:
    prompt: |
      Verify dist/ reflects the source task-file changes. The figure-out tasks/FEATURE.md and tasks/CODING.md and the
      define tasks/FEATURE.md and tasks/CODING.md changes that propagate into dist/ must be present in the corresponding
      dist/ copies (e.g. dist/codex/plugins/manifest-dev/, dist/pi/, dist/opencode/ as applicable). Method: run the
      manifest-dev:sync-tools regeneration, then `git status --porcelain dist/` — PASS if, after the executor's own
      regen, a fresh regen produces NO further dist/ changes (i.e. dist/ is already in sync). FAIL if a fresh regen
      mutates dist/ (means the executor left it stale). BLOCKED if sync-tools cannot run.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Edit the `claude-plugins/manifest-dev/` versions; the `.claude/` paths are symlinks to the same files. Do not duplicate edits.
- [PG-2] Keep figure-out probe files terse — angles/awareness phrased as the question that opens a branch, not instructions for how to do the work. Strengthen the existing "Verification design" / "Beyond the happy path" hooks; do not add a planning agenda.
- [PG-3] The new FEATURE exercise gate is additive — leave Requirements traceability / Behavior completeness / Error experience rows intact and unworded-over.
- [PG-4] Run existing tooling before committing; regenerate dist via sync-tools rather than hand-editing dist/ files.
- [PG-5] Commit on branch `claude/manifest-dev-verification-bgpkum`; push and open a PR when gates pass.

## 5. Known Assumptions
- [ASM-1] (auto) Domain encoded as PROMPTING (task-file/guidance prompt edits), not CODING — no executable code changes. | Default: PROMPTING gates (review-prompt + change-intent + context-file-adherence). | Impact if wrong: a code-quality dimension might be under-applied, but the diff is markdown + a version-string bump.
- [ASM-2] (auto) Minor version bump (2.12.0 → 2.13.0) per CLAUDE.md "new features" tier — task-file capability change. | Default: 2.13.0. | Impact if wrong: wrong semver tier; trivially corrected.
- [ASM-3] (auto) READMEs likely need no change (no component added/renamed/removed; capability lives inside existing task files). | Default: update only if a genuine reference goes stale. | Impact if wrong: a README sentence drifts; low blast radius.
- [ASM-4] (auto) Pi package version (`package.json`) NOT bumped — change is shared task-file guidance, not Pi runtime code or Pi-distributed assets. | Default: leave package.json untouched. | Impact if wrong: a stale Pi package version; correctable.

## 6. Deliverables

### Deliverable 1: figure-out probes default-press verification-design
Strengthen `claude-plugins/manifest-dev/skills/figure-out/tasks/FEATURE.md` and `.../CODING.md` so the verification/exercise angle is a default press before naming a read on a runnable surface — approach only, not a plan.

**Acceptance Criteria:**
- [AC-1.1] CODING.md probe's "Verification design" and FEATURE.md probe's "Beyond the happy path" are elevated from one optional angle among many to a default press for changes with a runnable surface, establishing the *exercise approach* (booted how, risky new paths, test seam present/needed) while staying terse awareness — not a step-by-step planning agenda, and not the enumerated test plan.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/tasks/FEATURE.md and tasks/CODING.md (and the diff,
      git diff origin/main...HEAD). PASS only if ALL hold: (1) the verification-design / beyond-the-happy-path angle
      is now framed as a default press for runnable-surface changes (e.g. "by default, before naming the read" or
      equivalent), not merely one optional probe; (2) it asks for the exercise APPROACH (how the surface is booted /
      driven, which new paths are risky, whether a test seam exists or must be built) — NOT a full enumerated test
      plan; (3) the files remain terse awareness angles phrased as questions, not procedural steps (no planning agenda).
      FAIL if exercise is still just-one-angle, if it prescribes producing the full plan, or if the probe became a
      step list. Report findings with severity.
    phase: 1
  ```

### Deliverable 2: /define FEATURE adds the additive exercise gate
Add a default Quality Gate to `claude-plugins/manifest-dev/skills/define/tasks/FEATURE.md` requiring the new behavior to be exercised, sitting alongside the existing inspect gates.

**Acceptance Criteria:**
- [AC-2.1] A new Quality Gate row/entry requires the new behavior to be *exercised* (run the new path, assert the outcome) rather than only confirmed present in the diff; it is additive (the three existing inspect-gate rows remain verbatim); conditional-but-default (fires when a runnable surface exists, auto-skips for pure-logic/library changes with no bootable surface); modality-agnostic (a new integration test that boots+drives the new path is the canonical satisfier, live verifier drive is the fallback); and returns BLOCKED when the surface cannot be booted rather than silently falling back to inspection.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/define/tasks/FEATURE.md (and the diff). PASS only if ALL hold:
      (1) a NEW Quality Gate exists whose verb is exercise/run-and-assert-outcome, distinct from "implemented/present";
      (2) the three existing rows (Requirements traceability, Behavior completeness, Error experience) are unchanged
      (additive, not reworded/replaced); (3) the new gate is explicitly conditional-but-default — default-on when a
      runnable surface exists, skipped when there is none; (4) it states integration-test-that-boots-the-new-path as
      canonical satisfier with live drive as fallback; (5) it specifies BLOCKED (not silent inspection) when the surface
      can't be booted. FAIL if any are missing or if an existing row was reworded. Report findings with severity.
    phase: 1
  ```

### Deliverable 3: /define CODING E2E rule → scope-driven granularity
Replace the blunt "each e2e case → INV-G" rule in `claude-plugins/manifest-dev/skills/define/tasks/CODING.md` with scope-driven granularity.

**Acceptance Criteria:**
- [AC-3.1] The E2E Verification section no longer says every e2e case gets its own INV-G; instead it routes by scope: single-deliverable behavioral check → deliverable AC (not INV-G); genuinely cross-cutting e2e spanning deliverables → INV-G; comprehensive edge-case matrix → test code under the existing project test-run gate, not enumerated as manifest criteria — and states the principle that manifest criteria are for what you want independently fix-targeted while the suite carries breadth (don't turn the manifest into a test-case list).
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/define/tasks/CODING.md (and the diff). PASS only if ALL hold:
      (1) the old blanket "each e2e test case gets its own INV-G*" guidance is gone/replaced; (2) the new rule routes by
      SCOPE — single-deliverable behavioral check → deliverable AC; cross-cutting e2e (spans deliverables) → INV-G;
      broad edge-case matrix → test code under the existing test-run gate, not enumerated manifest criteria;
      (3) it states the principle "criteria are for what you want independently fix-targeted; the suite is for breadth /
      don't turn the manifest into a test-case list" (or clear equivalent); (4) E2E phasing guidance (slow/later-phase)
      is preserved. FAIL if the blunt rule remains or scope routing is absent. Report findings with severity.
    phase: 1
  ```

### Deliverable 4: Version bump, README/dist sync
Close out repo housekeeping so the change is shippable.

**Acceptance Criteria:**
- [AC-4.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is bumped one minor step (2.12.0 → 2.13.0).
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/.claude-plugin/plugin.json. PASS only if "version" is "2.13.0" (a single minor
      bump from 2.12.0). FAIL otherwise.
    phase: 1
  ```
- [AC-4.2] dist/ regenerated via sync-tools so downstream CLI copies reflect the source task-file changes; no stale copies remain.
  ```yaml
  verify:
    prompt: |
      Run the manifest-dev:sync-tools regeneration, then `git status --porcelain dist/`. PASS if a fresh regen leaves
      dist/ unchanged (already in sync, reflecting the four edited task files where they propagate). FAIL if the fresh
      regen mutates dist/ (executor left it stale). BLOCKED if sync-tools cannot run.
    phase: 2
  ```
