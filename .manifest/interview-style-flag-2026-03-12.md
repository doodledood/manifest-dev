# Definition: Interview Style Flag for /define

## 1. Intent & Context
- **Goal:** Add `--interview <level>` flag to /define that controls how much the agent asks the user during the interview, from fully autonomous to the current thorough default.
- **Mental Model:** Interview style is a "who decides" slider. All protocols still run at every level — the difference is whether the agent asks the user or picks the recommended option itself. Thorough = user decides everything (current behavior). Minimal = user decides scope/constraints/high-impact items. Autonomous = agent decides everything, presents manifest for approval. Style is dynamic — set via flag but can shift if the user explicitly requests more (or less) probing mid-interview.

## 2. Approach

- **Architecture:** Modify SKILL.md to:
  1. Parse `--interview <level>` from `$ARGUMENTS` (same pattern as /do's `--mode`)
  2. Add an Interview Style section defining three levels via principles
  3. Fold existing fast-track signal into autonomous level
  4. Keep all existing interview logic intact — add conditional behavior around AskUserQuestion usage

- **Execution Order:**
  - D1 (SKILL.md changes) → D2 (version bump + READMEs)
  - Rationale: Core feature first, then metadata updates that depend on the feature being finalized.

- **Risk Areas:**
  - [R-1] Thorough default regression — change inadvertently alters the default interview behavior | Detect: diff review shows no changes to existing logic when `--interview` is omitted or set to `thorough`
  - [R-2] Composition conflict with complexity triage — interview style interacts badly with Simple/Standard/Complex triage | Detect: both mechanisms have clear, non-overlapping scopes
  - [R-3] Context rot from prompt length — SKILL.md is already very long; additions risk middle-context loss | Detect: additions are concise, use principles not exhaustive rules
  - [R-4] Fast-track removal creates gap — folding fast-track into autonomous might remove mid-interview escape capability | Detect: autonomous handles the "just build it" use case completely

- **Trade-offs:**
  - [T-1] Specificity vs brevity → Prefer principles per level (not exhaustive rules), keep additions concise to manage prompt length
  - [T-2] New mechanism vs extending existing → Prefer new `--interview` flag rather than overloading `--mode` (which controls verification, not interview)

## 3. Global Invariants (The Constitution)

- [INV-G1] Default behavior unchanged: When `--interview` is omitted or set to `thorough`, /define must behave identically to the current implementation | Verify: diff review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Compare the SKILL.md changes. Verify that when --interview is not specified or is 'thorough', no existing behavior is altered. Check: argument parsing defaults, interview flow, AskUserQuestion usage, protocol execution, complexity triage, convergence criteria, manifest-verifier loop — all unchanged for the default path."
  ```

- [INV-G2] No manifest schema changes: The output manifest format must be identical regardless of interview style — no new fields, no structural changes | Verify: schema comparison
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read the manifest schema section in SKILL.md. Verify the schema has no new fields related to interview style. The interview style must only affect the discovery log, not the manifest output."
  ```

- [INV-G3] All protocols still execute at every interview level: Domain Grounding, Outside View, Pre-Mortem, Backcasting, Adversarial Self-Review must still run (per complexity triage) regardless of interview style — only the questioning threshold changes | Verify: prompt review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read the interview style section in SKILL.md. Verify that all interview protocols (Domain Grounding, Outside View, Pre-Mortem, Backcasting, Adversarial Self-Review) are stated to run at every interview level. The style must only affect whether findings are presented to the user or auto-decided."
  ```

- [INV-G4] Prompt clarity — no ambiguous instructions, no vague language, no implicit expectations | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the interview style additions to SKILL.md for clarity issues: ambiguous instructions, vague language, implicit expectations. Focus on the new section and any modified existing sections."
  ```

- [INV-G5] No prompt anti-patterns — no prescriptive HOW, arbitrary limits, capability instructions, weak language | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the interview style additions to SKILL.md for anti-patterns: prescriptive HOW language, arbitrary limits, capability instructions ('use grep'), weak language ('try to', 'maybe'). Focus on additions only."
  ```

- [INV-G6] No conflicts with existing rules — new interview style instructions must not contradict existing constraints (complexity triage, confirm-before-encoding, convergence criteria, etc.) | Verify: conflict check
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Check the full SKILL.md for contradictions between the new interview style section and existing sections. Specifically check: complexity triage, confirm-before-encoding, convergence criteria, fast-track signal (should be removed/folded), AskUserQuestion constraint, resolvable task file handling."
  ```

- [INV-G7] Information density — additions earn their place, no redundancy | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the interview style additions for information density. Every sentence should earn its place. Check for redundancy with existing SKILL.md content."
  ```

- [INV-G8] Project gates pass — lint, format, typecheck | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ruff check --fix claude-plugins/ && black claude-plugins/ && mypy"
  ```

- [INV-G9] No breaking changes to plugin consumers — /do and /verify must not need any changes | Verify: diff review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Check that no changes were made to /do's SKILL.md, /verify's SKILL.md, or BUDGET_MODES.md. Interview style is a /define-only concern."
  ```

- [INV-G10] CLAUDE.md adherence — follows all project conventions (kebab-case, version bumping, README sync) | Verify: reviewer
  ```yaml
  verify:
    method: subagent
    agent: context-file-adherence-reviewer
  ```

- [INV-G11] Invocation fit — `--interview` parsing matches actual invocation patterns (flag position in args, interaction with task description text) | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Check that the --interview flag parsing in SKILL.md matches how users actually invoke /define. Verify the flag can appear before or after the task description, and that the task description isn't confused with the flag value."
  ```

- [INV-G12] Complexity fit — interview style additions are proportional to the task, not over-engineered | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Assess whether the interview style additions to SKILL.md are right-sized. The feature adds a three-level flag — the prompt additions should be proportional. Flag over-engineering: excessive edge case handling, redundant explanations, unnecessary subsections."
  ```

- [INV-G13] Edge case coverage — prompt handles boundary conditions for `--interview` (invalid values, dynamic style shifts, interaction with user feedback on manifest) | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Check the interview style section for edge case coverage. Verify it addresses: (1) invalid --interview values, (2) user requesting more probing mid-interview (dynamic shift), (3) manifest rejection in autonomous mode, (4) minimal interview on a simple task (doesn't collapse to nothing useful)."
  ```

- [INV-G14] Structure — interview style rules are surfaced prominently, not buried in middle of the prompt | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Check where the interview style section is placed in SKILL.md. It should be surfaced prominently (near argument parsing or interview flow sections), not buried in the middle where context rot could cause it to be missed."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Document load-bearing assumptions — identify what must remain true for the feature to work; surface invisible dependencies
- [PG-2] Keep interview style additions concise — use principles not exhaustive rules per level, to manage prompt length and context rot risk
- [PG-3] Follow existing patterns — argument parsing should mirror /do's `--mode` pattern for consistency

## 5. Known Assumptions

- [ASM-1] Three levels are sufficient (minimal, autonomous, thorough) | Default: three levels | Impact if wrong: would need to add/remove levels later, but the principle-based approach makes this easy to adjust
- [ASM-2] Auto-decided items tracked as Known Assumptions AND with inline "(auto)" annotation on INV/AC items | Default: both tracking methods | Impact if wrong: one tracking method may be redundant, but no harm
- [ASM-3] Invalid `--interview` value should error and halt (same as /do's `--mode`) | Default: error on invalid | Impact if wrong: could silently default instead, but explicit errors are safer
- [ASM-4] Interview style is orthogonal to execution mode (`--mode`) — they control different things and don't interact | Default: no interaction | Impact if wrong: would need cross-cutting logic
- [ASM-5] CODING.md quality gates (bug detection, type safety, etc.) are not applicable — this task changes prompt files (SKILL.md), plugin.json, and READMEs, but no executable code | Default: skip CODING gates | Impact if wrong: if hooks or code files need changes, would need to add these gates

## 6. Deliverables (The Work)

### Deliverable 1: SKILL.md Interview Style Feature

**Acceptance Criteria:**

- [AC-1.1] SKILL.md parses `--interview <level>` from `$ARGUMENTS` with three valid values: `minimal`, `autonomous`, `thorough` | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md. Verify it contains argument parsing logic for --interview flag with exactly three valid values: minimal, autonomous, thorough. Verify invalid values produce an error. Verify the default is thorough."
  ```

- [AC-1.2] Interview style section defines principles for each level that control AskUserQuestion usage threshold | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md's interview style section. Verify each level (minimal, autonomous, thorough) has a clear principle defining when to use AskUserQuestion vs auto-decide. Thorough = ask everything (current behavior). Minimal = ask scope, constraints, high-impact items. Autonomous = never ask, present final manifest for approval."
  ```

- [AC-1.3] Auto-decided items are encoded normally AND listed in Known Assumptions with reasoning | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md. Verify it instructs that when interview style causes an item to be auto-decided (agent picks recommended option instead of asking), the item is: (1) encoded as a normal INV/AC/PG with an '(auto)' annotation, and (2) also listed in the Known Assumptions section."
  ```

- [AC-1.4] Existing fast-track signal is folded into autonomous level — no duplicate mechanism | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md. Verify: (1) the old fast-track signal section ('If the user signals just build it...') is removed or replaced with a reference to autonomous interview style, and (2) autonomous level handles the 'just build it' use case. There should be one mechanism, not two."
  ```

- [AC-1.5] Interview style is logged in the discovery log file, not in the manifest | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md. Verify the interview style is recorded in the discovery log (define-discovery-*.md) but NOT added as a field in the manifest schema."
  ```

- [AC-1.6] Complexity triage remains orthogonal — both mechanisms have clear, non-overlapping scopes | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md. Verify that complexity triage (Simple/Standard/Complex) and interview style (minimal/autonomous/thorough) are described as orthogonal. Complexity determines which protocols run; interview style determines who decides within those protocols."
  ```

- [AC-1.7] Dynamic style shifting — prompt addresses user explicitly requesting more/less probing mid-interview (style adapts rather than being rigidly locked) | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md. Verify it describes interview style as dynamic — set via flag but responsive to user signals mid-interview. If a user on autonomous explicitly asks questions or probes, the agent should engage. If a user on thorough signals 'enough', the agent should compress."
  ```

- [AC-1.8] Autonomous manifest rejection — prompt addresses what happens when an autonomous manifest is rejected by user or verifier (agent auto-resolves concerns without switching to interactive mode) | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read SKILL.md. Verify it addresses autonomous manifest rejection: the agent should auto-resolve verifier or user concerns while staying in autonomous mode (not switching to thorough), unless the user explicitly asks for more interaction."
  ```

### Deliverable 2: Version Bump and README Updates

**Acceptance Criteria:**

- [AC-2.1] Plugin version bumped (minor) in plugin.json | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "cat claude-plugins/manifest-dev/.claude-plugin/plugin.json | grep '\"version\"'"
  ```

- [AC-2.2] READMEs updated per sync checklist — root README.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md mention interview style flag | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Check README.md, claude-plugins/README.md, and claude-plugins/manifest-dev/README.md. Verify each mentions the --interview flag feature for /define with the three levels (minimal, autonomous, thorough). The mention should be accurate and consistent with the SKILL.md implementation."
  ```
