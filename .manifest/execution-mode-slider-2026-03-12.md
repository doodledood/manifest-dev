# Definition: Execution Mode Slider for /do, /verify, and /define

## 1. Intent & Context
- **Goal:** Add an execution mode slider (`--mode efficient|balanced|thorough`) that controls subagent model routing, quality gate inclusion, parallelism, and verification loop limits across the manifest-dev workflow. Addresses GitHub issue #38 — quota-aware execution during /do.
- **Mental Model:** Mode is an execution policy, not a requirements concern. It controls HOW work is verified, not WHAT gets built. The default (`thorough`) preserves all current behavior unchanged. Users opt in to cheaper modes explicitly. Mode flows through the workflow: manifest `mode:` field → /do reads it (or `--mode` arg overrides) → /do passes to /verify. Implementation is primarily prompt changes to skills, plus one new reference file.

## 2. Approach

- **Architecture:**
  - New `references/BUDGET_MODES.md` file under `skills/do/references/` — single source of truth for all mode routing tables, escalation rules, and per-level behavior.
  - BUDGET_MODES.md uses **Claude-specific model names** (haiku) in the source. Model tier routing (using cheaper models in efficient mode) is a **Claude Code-only feature**. For all other CLIs, sync-tools replaces Claude model names with `inherit` — all tiers use the session model. The parallelism, loop limits, and gate-skipping aspects of budget modes still apply universally.
  - Core skills (`/do`, `/verify`, `/define`) get minimal additions — 2-3 lines each pointing to the reference file when mode != thorough.
  - `/verify` receives mode as `--mode` argument from /do.
  - Manifest schema gets an optional `mode` field at the top level.
  - Skill descriptions updated with `--mode` parameter syntax for model visibility.
  - Sync-tools reference files updated: model tier routing is Claude Code-only, all other CLIs use `inherit` for all tiers.
  - After all changes: run `/sync-tools` to regenerate dist/ for all target CLIs.

- **Execution Order:**
  - D1 (BUDGET_MODES.md reference file) → D2 (/do SKILL.md) → D3 (/verify SKILL.md) → D4 (/define SKILL.md schema) → D5 (docs, README, version) → D6 (sync-tools references) → D7 (run /sync-tools)
  - Rationale: Reference file first (source of truth), then consumers in dependency order. /do depends on reference file. /verify depends on /do's argument passing. /define depends on schema being defined. Docs and sync-tools updates after core feature. Run sync-tools last to regenerate dist/.

- **Risk Areas:**
  - [R-1] Cheapest-tier model criteria-checker inadequacy | Detect: >50% of efficient-mode verification criteria require escalation in a single /do run
  - [R-2] Prompt complexity creep in /do | Detect: /do SKILL.md grows by more than 10 lines due to mode logic
  - [R-3] Regression in default (thorough) behavior | Detect: any test or usage of thorough mode behaves differently than current behavior

- **Trade-offs:**
  - [T-1] Quota savings vs quality assurance → Prefer quality (thorough is default; efficient is opt-in and explicitly accepts lower verification coverage)
  - [T-2] Prompt brevity vs explicit mode rules → Prefer brevity in core skills (detail in reference file)
  - [T-3] Prescriptive routing tables vs flexible guidance → Prefer prescriptive tables (clear rules are easier to follow than judgment calls)

## 3. Global Invariants (The Constitution)

- [INV-G1] Default behavior unchanged: when no `mode` field in manifest AND no `--mode` argument to /do, all behavior must be identical to the current (pre-feature) /do and /verify behavior.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /do SKILL.md and /verify SKILL.md. Confirm that when mode is not specified (or is 'thorough'), the behavior described matches the pre-change behavior: all verifiers launch in a single message, all quality gate reviewers run, no parallelism limits, no escalation caps, manifest-verifier runs in /define. Compare against git diff to verify no default-path behavior changed."
  ```

- [INV-G2] Mode routing table accuracy: the reference file's routing table must match the agreed design exactly.
  ```yaml
  verify:
    method: codebase
    prompt: "In skills/do/references/BUDGET_MODES.md, verify the routing table contains exactly: efficient (haiku checker, reviewers SKIPPED, sequential, max 1 fix-verify loop, manifest-verifier SKIPPED, auto-escalate after 2 fails, cap 3 escalations), balanced (inherit checker, inherit reviewers, max 4 parallel, max 2 fix-verify loops, manifest-verifier SKIPPED, escalate after loop limit), thorough (inherit checker, inherit reviewers, unlimited parallel, unlimited loops, manifest-verifier runs, no escalation)."
  ```

- [INV-G3] No prompt anti-patterns: changes to skill files must not introduce prescriptive HOW instructions, arbitrary limits without rationale, weak language, or buried critical info.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the changed sections of skills/do/SKILL.md, skills/verify/SKILL.md, and skills/define/SKILL.md for prompt anti-patterns: prescriptive HOW (should state goals), arbitrary limits (should have rationale), weak language ('try to', 'maybe'), buried critical info. Also check that mode-related instructions are WHAT/WHY not HOW."
  ```

- [INV-G4] Skill descriptions include --mode parameter: /do and /verify skill descriptions must show the `--mode` syntax so it's visible to the model.
  ```yaml
  verify:
    method: codebase
    prompt: "Check that skills/do/SKILL.md and skills/verify/SKILL.md frontmatter 'description' fields include '--mode' parameter syntax."
  ```

- [INV-G5] Information density: reference file and skill additions must have no redundant content — every sentence earns its place.
  ```yaml
  verify:
    method: subagent
    agent: code-simplicity-reviewer
    prompt: "Review skills/do/references/BUDGET_MODES.md and the mode-related additions to skills/do/SKILL.md, skills/verify/SKILL.md, and skills/define/SKILL.md. Flag any redundant content, unnecessary verbosity, or information that doesn't earn its place."
  ```

- [INV-G6] CLAUDE.md adherence: all changes follow project conventions (kebab-case naming, prompt-engineering principles, plugin structure).
  ```yaml
  verify:
    method: subagent
    agent: context-file-adherence-reviewer
    prompt: "Verify all changed files follow CLAUDE.md conventions: kebab-case naming, plugin structure, prompt-engineering principles."
  ```

- [INV-G7] Project gates pass: lint, format, typecheck pass.
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy 2>&1 | tail -5"
  ```

- [INV-G8] Criterion-level model override precedence: when a manifest criterion specifies `model: <value>` in its verify block, that overrides the mode-level model routing. Mode sets defaults; criterion-level is explicit.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify skills/do/references/BUDGET_MODES.md states that per-criterion model overrides in manifest verify blocks take precedence over mode-level routing."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Use prompt-engineering skill for all prompt changes — ensures WHAT/WHY not HOW approach.
- [PG-2] Document load-bearing assumptions — identify what must remain true for modes to work (Agent tool model param, inherit behavior).
- [PG-3] Reference file approach — mode details in `references/BUDGET_MODES.md`, core skills get minimal pointers. Zero complexity added for default (thorough) path users.

## 5. Known Assumptions

- [ASM-1] Agent tool `model` param works as documented (sonnet/opus/haiku) | Default: works | Impact if wrong: mode can't route subagents to cheaper models — feature is ineffective
- [ASM-2] `inherit` means parent session model | Default: yes | Impact if wrong: balanced/thorough might not use user's preferred model
- [ASM-3] Cheapest-tier model (haiku on Claude, flash on Gemini, etc.) can run criteria-checker competently for bash/codebase verification | Default: mostly competent | Impact if wrong: efficient mode has high false-failure rate — mitigated by escalation mechanism (R-1)
- [ASM-4] Manifest schema is forward-compatible (adding optional `mode` field doesn't break older parsers) | Default: yes, skills parse manifests loosely | Impact if wrong: older /do versions error on new manifests
- [ASM-5] post_compact_hook.py preserves --mode in /do args recovery (VERIFIED: hook passes full `do_args` string, line 71). Additionally, mode is in the manifest `mode:` field which /do re-reads after compaction (AC-2.1 precedence) | Default: safe | Impact if wrong: n/a — two recovery paths

## 6. Deliverables (The Work)

### Deliverable 1: Mode Reference File
*New file: `claude-plugins/manifest-dev/skills/do/references/BUDGET_MODES.md`*

**Acceptance Criteria:**
- [AC-1.1] File contains the complete mode routing table with all three levels (efficient/balanced/thorough) and all 6 dimensions (checker model, reviewers, parallelism, fix-verify loops, manifest-verifier, escalation). Uses Claude-specific model names (haiku) since sync-tools converts per CLI.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify skills/do/references/BUDGET_MODES.md contains a table with columns for all 6 dimensions and rows for all 3 mode levels matching: efficient (haiku/SKIPPED/sequential/max 1/SKIPPED/auto after 2, cap 3), balanced (inherit/inherit/max 4/max 2/SKIPPED/after loop limit), thorough (inherit/inherit/unlimited/unlimited/runs/no escalation)."
  ```

- [AC-1.2] File contains escalation rules: efficient auto-escalates after 2 failures on same criterion, cap at 3 total escalations per /do run (then suggest switching to balanced). Balanced escalates after fix-verify loop limit hit.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify BUDGET_MODES.md defines escalation rules: efficient = auto-escalate after 2 failures per criterion, cap 3 total escalations then suggest mode switch. Balanced = escalate after loop limit."
  ```

- [AC-1.3] File contains /verify parallelism overrides: efficient=sequential, balanced=max 4 concurrent, thorough=all at once.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify BUDGET_MODES.md specifies verification parallelism per level: efficient=one at a time, balanced=batches of max 4, thorough=all in single message."
  ```

- [AC-1.4] File contains /define manifest-verifier rules: efficient+balanced skip it, thorough runs it.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify BUDGET_MODES.md specifies manifest-verifier behavior: skipped for efficient and balanced, runs for thorough."
  ```

- [AC-1.5] File states override precedence: (1) per-criterion `model:` overrides mode-level routing, (2) explicit model override also overrides the "reviewers SKIPPED" rule (criterion runs even in efficient mode), (3) INV-G verification always runs regardless of mode (skip only applies to deliverable-level quality gates).
  ```yaml
  verify:
    method: codebase
    prompt: "Verify BUDGET_MODES.md contains all three override rules: criterion-level model overrides mode routing, explicit model overrides reviewer skip, and INV-G verification always runs (skip only affects deliverable-level gates)."
  ```

### Deliverable 2: /do Skill Mode Integration
*Edit: `claude-plugins/manifest-dev/skills/do/SKILL.md`*

**Acceptance Criteria:**
- [AC-2.1] /do SKILL.md parses mode from: (1) `--mode <level>` argument, (2) manifest `mode:` field, with argument taking precedence. Default: thorough. Invalid value → error and halt.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /do SKILL.md describes mode parsing: --mode arg > manifest mode field > default thorough. All three sources mentioned with precedence order. Invalid mode value produces error and halts."
  ```

- [AC-2.2] /do SKILL.md contains a conditional pointer to the reference file: when mode != thorough, read `references/BUDGET_MODES.md`.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /do SKILL.md has a conditional instruction to read references/BUDGET_MODES.md only when mode is not thorough."
  ```

- [AC-2.3] /do passes mode to /verify as argument: `/verify <manifest> <log> --mode <level>`.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /do SKILL.md instructs passing mode to /verify invocation as --mode argument."
  ```

- [AC-2.4] Skill description (frontmatter) includes `--mode` parameter syntax.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /do SKILL.md frontmatter description field mentions --mode parameter."
  ```

- [AC-2.5] /do enforces fix-verify loop limits per mode: tracks iteration count, stops at the mode's limit, and escalates when limit is reached.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /do SKILL.md (or the reference file it points to) instructs /do to track fix-verify loop iterations and enforce mode-specific limits: efficient=max 1, balanced=max 2, thorough=unlimited. When limit is hit, /do must escalate."
  ```

- [AC-2.6] /do enforces escalation cap in efficient mode: tracks total escalations, suggests mode switch to user after 3.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /do SKILL.md (or the reference file it points to) instructs /do to count escalations in efficient mode and suggest switching to balanced after 3 total escalations in a single /do run."
  ```

### Deliverable 3: /verify Skill Mode Integration
*Edit: `claude-plugins/manifest-dev/skills/verify/SKILL.md`*

**Acceptance Criteria:**
- [AC-3.1] /verify SKILL.md accepts `--mode <level>` in its arguments, defaulting to thorough.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /verify SKILL.md describes accepting --mode argument with thorough default."
  ```

- [AC-3.2] /verify SKILL.md has a mode-aware parallelism section that explicitly overrides the default 'launch all in single message' rule per mode level.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /verify SKILL.md has a section that overrides default parallelism based on mode: efficient=sequential, balanced=max 4, thorough=all at once. The override must be explicit (not ambiguous with the existing parallelism rule)."
  ```

- [AC-3.3] /verify routes subagent model per mode level: efficient=haiku for criteria-checker (reviewers skipped), balanced+thorough=inherit.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /verify SKILL.md instructs model routing: efficient mode uses haiku for criteria-checker and skips reviewer subagents. Balanced and thorough use inherit."
  ```

- [AC-3.4] Skill description (frontmatter) includes `--mode` parameter syntax.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /verify SKILL.md frontmatter description field mentions --mode parameter."
  ```

### Deliverable 4: /define Manifest Schema Update
*Edit: `claude-plugins/manifest-dev/skills/define/SKILL.md`*

**Acceptance Criteria:**
- [AC-4.1] Manifest schema in /define includes optional `mode: efficient|balanced|thorough` field at the top level.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /define SKILL.md manifest schema template includes an optional mode field with the three valid values."
  ```

- [AC-4.2] /define respects mode for its own manifest-verifier step: reads mode from manifest, skips manifest-verifier for efficient+balanced.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify /define SKILL.md verification loop section checks the manifest's mode field and skips manifest-verifier invocation when mode is efficient or balanced."
  ```

### Deliverable 5: Documentation and Versioning
*Edit: READMEs, plugin.json*

**Acceptance Criteria:**
- [AC-5.1] Root README.md documents the execution mode feature: what it is, how to use it (`--mode` arg or manifest field), the three levels and their behavior summary.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify README.md has a section documenting execution modes: the three levels, how to specify (--mode arg or manifest field), and a summary of each level's behavior."
  ```

- [AC-5.2] Plugin version bumped to 0.64.0 (minor: new feature).
  ```yaml
  verify:
    method: bash
    command: "grep '\"version\"' claude-plugins/manifest-dev/.claude-plugin/plugin.json | grep -q '0.64.0'"
  ```

- [AC-5.3] Plugin README (`claude-plugins/manifest-dev/README.md`) updated to mention execution modes.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify claude-plugins/manifest-dev/README.md mentions execution modes feature."
  ```

### Deliverable 6: Sync-Tools Budget Mode Conversion
*Edit: `.claude/skills/sync-tools/SKILL.md` and `.claude/skills/sync-tools/references/{codex,gemini,opencode}-cli.md`*

**Acceptance Criteria:**
- [AC-6.1] Sync-tools SKILL.md includes a conversion rule for BUDGET_MODES.md: replace Claude-specific model names (haiku, sonnet, opus) with `inherit` for all target CLIs. Model tier routing is Claude Code-only; other CLIs use session model for all tiers.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify .claude/skills/sync-tools/SKILL.md includes a conversion rule for skill reference files containing Claude model names: replace haiku/sonnet/opus with 'inherit' for all target CLIs."
  ```

- [AC-6.2] Each sync-tools reference file documents that model tier routing is Claude Code-only and all budget tiers use `inherit` on that CLI.
  ```yaml
  verify:
    method: codebase
    prompt: "Verify all three sync-tools reference files note that BUDGET_MODES.md model names are replaced with 'inherit' — model tier routing is Claude Code-specific."
  ```

### Deliverable 7: Run /sync-tools
*Execute: `/sync-tools` to regenerate dist/ for all target CLIs*

**Acceptance Criteria:**
- [AC-7.1] `/sync-tools` has been run successfully after all other changes, regenerating dist/ for gemini, opencode, and codex.
  ```yaml
  verify:
    method: bash
    command: "git diff --name-only | grep -c '^dist/' | xargs -I{} test {} -gt 0 && echo 'dist/ has changes' || echo 'FAIL: dist/ not updated'"
  ```

- [AC-7.2] The generated dist/ files include a CLI-adapted BUDGET_MODES.md reference file in each CLI's skill distribution (with CLI-specific model names, not Claude names).
  ```yaml
  verify:
    method: bash
    command: "for cli in gemini opencode codex; do test -f dist/$cli/skills/do/references/BUDGET_MODES.md && echo \"$cli: OK\" || echo \"$cli: MISSING\"; done"
  ```

- [AC-7.3] The generated dist/ READMEs mention execution modes feature.
  ```yaml
  verify:
    method: bash
    command: "for cli in gemini opencode codex; do grep -qi 'mode\\|budget\\|efficient\\|thorough' dist/$cli/README.md && echo \"$cli README: OK\" || echo \"$cli README: MISSING mode docs\"; done"
  ```
