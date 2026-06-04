# Definition: figure-out domain probing via mirrored probe task files

## 1. Intent & Context
- **Goal:** Re-home domain probing fuel in figure-out's own per-domain probe task files so non-natural angles (verification chief among them) enter the model's awareness during understanding — without turning figure-out into a checklist-ticker. define keeps formalizing; figure-out keeps probing.
- **Mental Model:** The 1.0.0 over-slim evicted probing fuel from define's task files and declared probing "figure-out's job" but never gave figure-out the fuel or a mechanism. Fix per ADR `docs/adr/20260604-figure-out-owns-domain-probing-via-mirrored-task-files.md`: figure-out gets its own probe task files (mirroring define's taxonomy) with a **split, self-contained index**; define's task files keep Quality Gates + Defaults. Probes are **awareness, not a script** — loaded always when a domain matches, pressed only by the model's judgment.

## 2. Approach
- **Architecture:** New `claude-plugins/manifest-dev/skills/figure-out/tasks/` probe set + figure-out's own task-type index + a SKILL.md consumption line; reconcile stale docs (CLAUDE.md, define/tasks/README.md) to the two-parallel-sets model; mirror via symlinks, dist-sync, version bump; drive PR #172 to mergeable.
- **Execution Order:**
  - D1 (probe files + figure-out index) → D2 (SKILL.md consumption) → D3 (doc reconciliation) → D4 (plumbing: symlinks, dist, version, READMEs) → lifecycle
  - Rationale: content before the loader that points at it; docs before plumbing; plumbing before lifecycle.
- **Risk Areas:**
  - [R-1] Checklist-ticker regression — probes consumed as an agenda, not awareness | Detect: prompt-reviewer + INV-G4 read the consumption framing and file headers.
  - [R-2] figure-out coupled to define (index cross-reference) | Detect: grep figure-out files for define/tasks paths; INV-G4.
  - [R-3] Old checklists re-imported wholesale / natural probes kept | Detect: AC-1.2 non-natural-only inspection.
- **Trade-offs:**
  - [T-1] DRY (single shared index) vs self-containment → Prefer self-containment: figure-out is the standalone primary entry point; split index per skill (ADR-locked).
  - [T-2] Probe coverage breadth vs ritual-compliance risk → Prefer short, non-natural-only files (4–6 items/section) so structure itself discourages list-walking.

## 3. Global Invariants

- [INV-G1] Every changed or new prompt/skill/probe file passes prompt-review at no MEDIUM+.
  ```yaml
  verify:
    prompt: "Review every prompt-bearing file changed on this branch vs origin/main (figure-out SKILL.md, the new figure-out/tasks/*.md probe files and their index, plus any reworded define/tasks/README.md). Goal: prompt quality per the prompt-engineering gap-calibration discipline — trust the model, add only lines that close a real gap, no prescriptive HOW, no ritual/checklist framing, low-arousal tone. The probe files must read as optional context-dependent awareness, NOT an agenda the model must work through. Use the prompt-reviewer agent if available; else evaluate against the PROMPTING quality-gate table in tasks/PROMPTING.md. PASS if no finding at MEDIUM or above; FAIL listing each MEDIUM+ finding with file and line; BLOCKED if the diff cannot be read."
    agent: prompt-reviewer
    phase: 1
  ```
- [INV-G2] The change does what this manifest intends, with no behavioral divergence.
  ```yaml
  verify:
    prompt: "Adversarially analyze the branch diff vs origin/main against the stated intent: figure-out gains its own probe task files + self-contained index + a load-always/press-by-judgment consumption instruction; define's task files and docs are reconciled to the two-parallel-sets model. Confirm no unintended behavioral change to define, /do, or other skills. PASS if intent is achieved with no divergence; FAIL listing each divergence (file, line, what diverges); BLOCKED if undeterminable. Use change-intent-reviewer if available."
    agent: change-intent-reviewer
    phase: 1
  ```
- [INV-G3] Project gate clean: `ruff check --fix claude-plugins/ && black claude-plugins/ && mypy` exits 0.
  ```yaml
  verify:
    prompt: "Run `ruff check --fix claude-plugins/ && black claude-plugins/ && mypy` from the repo root. PASS if the combined command exits 0 (markdown-only changes should be no-ops for these tools); FAIL with the failing tool's output; BLOCKED if tooling is not installed."
    phase: 1
  ```
- [INV-G4] figure-out stays standalone and general: no figure-out file references define's task-type index, define/tasks paths, or requires define to function; with no domain match, figure-out falls back to pure general probing.
  ```yaml
  verify:
    prompt: "Inspect every file under the figure-out skill directory (claude-plugins/manifest-dev/skills/figure-out/ and its symlinked .claude counterpart). Goal: confirm figure-out is self-contained. FAIL if any figure-out file references define's index, reads from define/tasks/, or otherwise makes figure-out depend on define to detect a task type or load probes. Also confirm the SKILL.md consumption instruction explicitly degrades to general probing when no domain matches, and frames probes as awareness/suggestions (not a required checklist). PASS only if self-contained AND graceful-degradation AND awareness-framing all hold; FAIL listing each violation with file:line; BLOCKED if files are unreadable."
    phase: 1
  ```

## 4. Process Guidance
- [PG-1] Apply prompt-engineering discipline throughout: trust the model, add only gap-closing lines, non-natural probes only. Don't re-import the pre-strip checklists wholesale.
- [PG-2] Source probe raw material from the pre-strip files at git ref `17043f9~1` (`define/tasks/{CODING,FEATURE,BUG,REFACTOR}.md` `## Risks` / `## Scenario Prompts` / `## Trade-offs`), filtering to non-natural angles only.
- [PG-3] Edit the `claude-plugins/` side of every symlinked file; never edit through `.claude/`.
- [PG-4] Keep probe files terse — 4–6 items per section; a short list resists ritual completion.

## 5. Known Assumptions
- [ASM-1] Task type is PROMPTING, not CODING (no executable code changes) | Default: PROMPTING gates only (prompt-reviewer, change-intent) + project gate | Impact if wrong: missing code reviewer gates.
- [ASM-2] Ship probe files for CODING, FEATURE, BUG, REFACTOR now; add PROMPTING and RESEARCH probe files only if a genuine non-natural angle exists for them; skip WRITING/BLOG/DOCUMENT/PR_LIFECYCLE | Default: code domains first | Impact if wrong: a domain lacks probe fuel until a later pass (acceptable — files are additive).
- [ASM-3] figure-out's task-type index lives in `figure-out/tasks/README.md` (mirroring define's location pattern) and is referenced from SKILL.md | Default: own README index | Impact if wrong: index placement differs, no behavioral change.
- [ASM-4] "Land it" includes driving PR #172 to mergeable via github-pr-lifecycle (origin is github.com) | Default: include lifecycle gate (phase 2) | Impact if wrong: PR left un-tended.
- [ASM-5] Version bump is minor (new capability) per CLAUDE.md versioning | Default: minor | Impact if wrong: wrong semver step.

## 6. Deliverables

### Deliverable 1: figure-out probe task files + self-contained index

**Acceptance Criteria:**
- [AC-1.1] A new `claude-plugins/manifest-dev/skills/figure-out/tasks/` directory exists with per-domain probe files for at least CODING, FEATURE, BUG, REFACTOR. Each file has: a terse header framing probes as context-dependent suggestions (awareness, not an agenda; most won't apply; priority stays with the model), a `## Blind-spot probes` section (question-shaped angles), and a `## Forced trade-offs` section.
  ```yaml
  verify:
    prompt: "List claude-plugins/manifest-dev/skills/figure-out/tasks/ and read each probe file. PASS if CODING.md, FEATURE.md, BUG.md, REFACTOR.md all exist AND each contains a suggestions/awareness-framing header, a '## Blind-spot probes' section with question-shaped items, and a '## Forced trade-offs' section. FAIL listing each missing file or section; BLOCKED if the directory is absent."
    phase: 1
  ```
- [AC-1.2] Probe content is non-natural-only and verification is first-class. Natural probes (scope-creep/out-of-scope, performance-vs-readability, minimal-change-vs-cleanup) are absent; non-natural angles are present (verification design, failure visibility/observability, consumer blast radius, cleanup/orphaned resources, rollback/undo; BUG "mechanism not shape"; REFACTOR behavior-contract + characterization tests). CODING.md and FEATURE.md each carry a first-class, design-shaping verification probe ("how will we know this works; does the design need a seam/observability it lacks; if self-verifying, say so").
  ```yaml
  verify:
    prompt: "Read the figure-out probe files. Goal: confirm non-natural-only selection and first-class verification. FAIL if any clearly-natural probe a competent model raises unprompted is present (e.g. generic 'what's out of scope', 'performance vs readability', 'minimal change vs cleanup'). FAIL if CODING.md or FEATURE.md lacks a design-shaping verification probe that asks how the change will be verified and whether the design needs a seam/observability to allow it. Spot-check that retained probes match the non-natural set (verification, observability/failure-visibility, consumer blast radius, cleanup, rollback; BUG mechanism-not-shape; REFACTOR behavior-contract+characterization). PASS only if non-natural-only AND verification-first-class hold; FAIL listing offending items with file:line."
    phase: 1
  ```
- [AC-1.3] figure-out's task-type detection index is inlined directly in `figure-out/SKILL.md` (the domain→probe-file mapping), self-contained, with no reference to define's index or define/tasks paths.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS if it inlines the domain→probe-file mapping (indicators → CODING/FEATURE/BUG/REFACTOR.md, with CODING as the composable base) directly in the SKILL.md body AND contains no reference to define's index, define/tasks/, or any path outside the figure-out skill. FAIL if the mapping is missing from SKILL.md or references define; cite the offending line."
    phase: 1
  ```
- [AC-1.4] No separate `tasks/README.md` index file remains under either skill — the index lives inline in each SKILL.md.
  ```yaml
  verify:
    prompt: "Confirm neither claude-plugins/manifest-dev/skills/figure-out/tasks/README.md nor claude-plugins/manifest-dev/skills/define/tasks/README.md exists (both deleted), and confirm no dist copy remains (dist/{opencode,codex}/skills/{figure-out,define}/tasks/README.md absent). PASS if all four paths are absent; FAIL listing any that still exist."
    phase: 2
  ```

### Deliverable 2: figure-out consumption instruction

**Acceptance Criteria:**
- [AC-2.1] `figure-out/SKILL.md` instructs: when the topic maps to a known domain, load that probe file (always — to put angles in view), then continue normal branch-walking folding in only what's load-bearing; framed as awareness not a script (don't walk the list, no probe is required); degrades to general probing when no domain matches. figure-out remains lean and general (no bloat, no coding-only narrowing of its frame).
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS if it contains an instruction that (a) loads the matching domain probe file when the topic maps to a known domain, (b) frames probes as awareness/suggestions the model presses by its own judgment — explicitly not a checklist to walk or required questions, and (c) falls back to general probing when no domain matches. FAIL if any of (a)/(b)/(c) is missing, or if the addition narrows figure-out to coding-only or bloats the general frame. Quote the added text."
    phase: 1
  ```

### Deliverable 3: documentation reconciliation

**Acceptance Criteria:**
- [AC-3.1] `CLAUDE.md` and `CONTEXT.md` describe the two-parallel-sets model (figure-out task files carry probes; define task files carry Quality Gates + Defaults) with no stale claim that define's task files carry probes for /define's interview; and the "each skill owns its own index" wording reflects that the index now lives inline in each SKILL.md, not in a separate `tasks/README.md`.
  ```yaml
  verify:
    prompt: "Read the task-file section of CLAUDE.md and the Task File entry/relationship in CONTEXT.md. PASS if both: (a) describe figure-out's task files as probe carriers and define's as Quality-Gates+Defaults carriers, with no surviving claim that define's task files carry probes for define's interview; and (b) any reference to where each skill's task-type index lives points to the SKILL.md inline location, not a separate tasks/README.md index file. FAIL quoting any stale passage (including a dangling 'tasks/README.md' index reference)."
    phase: 1
  ```
- [AC-3.2] `define/tasks/README.md` is deleted; its content (Domains detection table, Composition rules, Task-file content-types, encode-timing guidance) plus the two-parallel-sets reconciliation now live inline in `define/SKILL.md`, and define detects task type / loads its task files from SKILL.md guidance rather than a separate README.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md and confirm claude-plugins/manifest-dev/skills/define/tasks/README.md no longer exists. PASS if: (a) define/tasks/README.md is absent; (b) define/SKILL.md now carries the inlined task-file guidance — domain detection table (or equivalent mapping), composition rules, and content-types; (c) it states the two-parallel-sets model (define task files = Quality Gates + Defaults; figure-out owns its own probe files) with no dangling 'task files don't carry probing fuel / no home' claim; (d) define no longer instructs loading a now-deleted tasks/README.md. FAIL quoting the offending text or naming the missing piece."
    phase: 1
  ```

### Deliverable 4: plumbing (symlinks, dist, version, READMEs)

**Acceptance Criteria:**
- [AC-4.1] The new figure-out `tasks/` probe files are reachable through the `.claude/` symlink path exactly as other figure-out skill files are (per repo symlink convention).
  ```yaml
  verify:
    prompt: "Confirm the figure-out probe files are reachable via .claude (e.g. .claude/skills/figure-out/tasks/CODING.md resolves through the symlink to claude-plugins/manifest-dev/skills/figure-out/tasks/CODING.md, consistent with how figure-out/SKILL.md is linked). PASS if reachable and consistent with the existing link convention; FAIL describing the inconsistency."
    phase: 1
  ```
- [AC-4.2] dist packages are regenerated so the new probe files and SKILL.md change appear in the OpenCode/Codex distributions (via the sync-tools skill).
  ```yaml
  verify:
    prompt: "After dist sync, confirm dist/ reflects the figure-out probe files and the SKILL.md consumption change for the generated distributions (OpenCode, Codex). PASS if the new content is present in dist/; FAIL listing what's missing; BLOCKED if the sync tooling could not run."
    phase: 2
  ```
- [AC-4.3] The manifest-dev plugin version is bumped (minor) in `.claude-plugin/plugin.json`, and READMEs are updated per the CLAUDE.md sync checklist for the new probe-file surface.
  ```yaml
  verify:
    prompt: "Check claude-plugins/manifest-dev/.claude-plugin/plugin.json version was bumped by a minor increment vs origin/main. Check that READMEs (root README.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md) mention figure-out's probe task files where component surfaces are listed, per the CLAUDE.md README sync checklist. PASS if version bumped minor AND READMEs updated where required; FAIL listing what's missing."
    phase: 1
  ```

### Deliverable 5: land PR #172

**Acceptance Criteria:**
- [AC-5.1] PR #172 is driven to a mergeable state (not merged).
  ```yaml
  verify:
    agent: github-pr-lifecycle
    prompt: |
      PR: https://github.com/doodledood/manifest-dev/pull/172
      Branch: claude/figure-out-verification-prompt-xLvFW

      Steering: Baseline. Drive to mergeable and stop — do not press merge. Ensure the branch is pushed with all committed work, CI (if any registered) is green, the PR description reflects the final change, and there are no unresolved blocking review threads. This repo currently has no registered CI checks; absence of checks is not a blocker.
    phase: 2
  ```
