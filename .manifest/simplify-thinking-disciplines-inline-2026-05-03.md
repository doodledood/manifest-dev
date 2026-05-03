# Definition: Inline thinking-disciplines into figure-out/define and remove standalone scaffolding

## 1. Intent & Context

- **Goal:** Reduce per-prompt context overhead during /figure-out and /define sessions by embedding the thinking-disciplines *goals* (the six operational stances) into each skill — smartly, calibrated against the prompt-engineering skill's principles, fitting each skill's existing voice and structure — and removing the standalone thinking-disciplines skill, the stop-thinking-disciplines skill, the two thinking_disciplines_* hooks, and all related scaffolding.
- **Mental Model:** The disciplines' operational effect (the six stances they enforce) must remain active when each skill runs. The mechanism shifts from a separate skill + per-prompt hook reinforcement to in-skill content calibrated per skill. Smart embedding ≠ byte-identical paste — wording and placement are tailored to figure-out's open-ended thinking-partner role and define's structured interview procedure. Loss of mid-session reinforcement is an accepted trade.
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

- **Architecture:**
  - Embed the six thinking-disciplines stances into figure-out and define SKILL.md, calibrated per skill against prompt-engineering principles (information density, WHAT/WHY not HOW, no rigid step-prescription, decision rules over absolutes, low-arousal tone, no contradiction with surrounding content). Placement and phrasing are per-skill: figure-out leans toward integration with its existing thinking-partner voice (Stance/Disciplines section near the top + targeted touch-ups where existing content already encodes parts of the stance — Disagreement, Interaction Failure Modes); define leans toward integration with its Principles + Discovery & question disciplines structure. Replace the existing `Invoke ... thinking-disciplines` line in each.
  - figure-out: drop the `## Ending` references to `/stop-thinking-disciplines`; session ends conversationally.
  - Delete standalone skills (thinking-disciplines, stop-thinking-disciplines) from `claude-plugins/manifest-dev/skills/`, `.claude/skills/`, and `.agents/skills/`.
  - Delete `thinking_disciplines_prompt_hook.py` and `thinking_disciplines_pretool_hook.py`.
  - Strip thinking-disciplines branch from `post_compact_hook.py` (only handles /do recovery now).
  - Strip `parse_thinking_disciplines_flow`, `ThinkingDisciplinesState`, `_THINKING_DEACTIVATORS` from `hook_utils.py`.
  - Strip 2 hook registrations from `claude-plugins/manifest-dev/.claude-plugin/plugin.json` and `.claude/settings.json`.
  - Delete `tests/hooks/test_thinking_disciplines_flow.py` (parser tests for removed function).
  - Remove all thinking-disciplines references from `tests/hooks/test_hook_integration.py`.
  - Update `CLAUDE.md` (parser reference), root `README.md` (skill + hook tables), `claude-plugins/README.md`, `claude-plugins/manifest-dev/README.md`.
  - Bump `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version 0.100.0 → 0.101.0.
  - Regenerate `dist/{codex,gemini,opencode}/` via the `sync-tools` skill so distributions match source.

- **Execution Order:**
  - D1 → D2 → D3 → D4 → D5 → D6(version-bump only) → D7 → D6(manifest archival)
  - Rationale: embed stances first (D1), so removing the source (D2) doesn't leave figure-out/define dangling. Hook code removal (D3) before test removal (D4) keeps each step verifiable. Docs (D5) follow code/test changes. Plugin version bump (D6 part 1) precedes dist regen so dist version metadata is consistent. Dist regeneration (D7) consumes final source state. Manifest archival (D6 part 2) happens last — only after the converged, verified state is achieved.

- **Risk Areas:**
  - [R-1] Embedding preserves disciplines content but loses mid-session reinforcement | Detect: degraded sycophantic-drift pushback in long sessions (observable behavior change, not test-detectable). Acceptance: watch-and-see; rollback path is restoring the AskUserQuestion pretool hook via amendment if drift is observed in practice.
  - [R-2] Skill content might not survive compaction the same way hook re-injection did | Detect: post-compact figure-out/define behavior degrades — no automated detection. Acceptance: same watch-and-see + amendment rollback as R-1.
  - [R-3] Hidden references to thinking-disciplines outside identified surface | Detect: post-change `grep -r` returns clean
  - [R-4] Scope creep — refactoring figure-out/define content beyond the inlining | Detect: diff scoped to the inlined block + invocation-line removal + Ending-section removal in figure-out
  - [R-5] dist/ packages drift if sync-tools regeneration is forgotten | Detect: post-change `grep -r thinking-disciplines dist/` returns clean

- **Trade-offs:**
  - [T-1] Reinforcement vs context savings → Prefer context savings (user's stated goal)
  - [T-2] Strict identical inline vs per-skill smart embedding → Prefer per-skill smart embedding calibrated against prompt-engineering principles (user choice in interview round 2). Each skill's voice and structure govern placement and phrasing; the six stances must be operationally present in both. Drift risk between the two embeddings is accepted in exchange for fit-for-purpose integration.
  - [T-3] Strict cut vs partial keep (AskUserQuestion hook) → Prefer strict cut (user choice)
  - [T-4] Removal-only refactor vs targeted prompt-engineering-driven integration → Per T-2, allow the integration edits in figure-out and define needed for smart embedding (e.g., consolidating with existing Disagreement/Failure Modes content); reject any other "while we're here" cleanup. Scope-creep guard: change-intent-reviewer audits the diff against this stated intent.

## 3. Global Invariants

- [INV-G1] No remaining references to `thinking-disciplines`, `thinking_disciplines`, or `stop-thinking-disciplines` in source (excluding `.manifest/` archived manifests and `/tmp/` working files).
  ```yaml
  verify:
    method: bash
    command: "! grep -rn 'thinking-disciplines\\|thinking_disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev --include='*.md' --include='*.py' --include='*.json' --exclude-dir=.manifest --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__"
  ```

- [INV-G2] Lint passes.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "ruff check claude-plugins/"
  ```

- [INV-G3] Format passes.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "black --check claude-plugins/"
  ```

- [INV-G4] Type check passes.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "mypy"
  ```

- [INV-G5] All hook tests pass.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "pytest tests/hooks/ -v"
  ```

- [INV-G6] figure-out and define skill content changes are scoped to: (a) removing the line that invokes the thinking-disciplines skill, (b) embedding the six thinking-disciplines stances in a manner calibrated to each skill, (c) integration consolidation where existing skill content already encodes parts of the stance — e.g., merging figure-out's Disagreement and Interaction Failure Modes guidance with the embedded stances rather than producing duplicates (intentional reorganization is allowed when it serves consolidation), (d) figure-out only — removing references to `/stop-thinking-disciplines` from the Ending section. Any reorganization beyond what consolidation requires is scope creep.
  ```yaml
  verify:
    method: subagent
    phase: 2
    agent: change-intent-reviewer
    prompt: "Review the diff for claude-plugins/manifest-dev/skills/figure-out/SKILL.md and claude-plugins/manifest-dev/skills/define/SKILL.md. Allowed intent: (1) remove the line invoking the thinking-disciplines skill, (2) embed the six thinking-disciplines stances (come prepared / investigate before engaging; name confidence — verified vs inferred; sit with fog / don't synthesize prematurely; verify before proposing; genuine agreement and disagreement / no sycophantic drift; intuition is a lead) calibrated to each skill, (3) consolidate with existing skill content where it already encodes parts of the stance (e.g., figure-out's Disagreement, Interaction Failure Modes — merging is allowed and preferred over duplication), (4) figure-out only — remove the Ending section references to /stop-thinking-disciplines. Reorganization is allowed only when it serves consolidation per (3). Flag any other content changes as scope creep. Threshold: no LOW+."
  ```

- [INV-G7] Prompt quality on modified skills, judged against the prompt-engineering skill's canonical principles as defined in `claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md`. (This invariant subsumes per-skill stance presence — the prompt-reviewer agent operates against the same canonical-principles file and verifies semantic completeness.)
  ```yaml
  verify:
    method: subagent
    phase: 2
    agent: prompt-reviewer
    prompt: "Review claude-plugins/manifest-dev/skills/figure-out/SKILL.md and claude-plugins/manifest-dev/skills/define/SKILL.md against the canonical principles defined in claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md. Focus on the changes made to embed the thinking-disciplines stances: (a) operational presence of all six stances in each file — come prepared / investigate before engaging; name confidence — verified vs inferred; sit with fog / contradictions as leads; verify before proposing; genuine agreement and disagreement; intuition is a lead; (b) information density (every word earns its place; no bloat); (c) WHAT/WHY not HOW (no procedural step-prescription where the model already knows the procedure); (d) decision rules over absolutes (reserve MUST/NEVER for true invariants); (e) low-arousal emotional tone (no urgency framing, no excessive praise); (f) integration coherence (no internal contradiction with surrounding skill content; no duplicated guidance that already exists elsewhere in the same file); (g) no broken references to the removed thinking-disciplines or stop-thinking-disciplines skills. Any missing stance, principle violation, or broken reference = MEDIUM+ finding. Threshold: no MEDIUM+."
  ```

- [INV-G8] Mechanical bug detection on changed Python (post_compact_hook.py, hook_utils.py).
  ```yaml
  verify:
    method: subagent
    phase: 2
    agent: code-bugs-reviewer
    prompt: "Review the diff for claude-plugins/manifest-dev/hooks/post_compact_hook.py and claude-plugins/manifest-dev/hooks/hook_utils.py. The intent is removing all thinking-disciplines parsing and reminder logic while preserving /do recovery and existing /do flow parsing. Check for dangling imports, unused code, broken references. Threshold: no LOW+."
  ```

- [INV-G9] Maintainability and simplicity of the resulting hook utilities and post_compact_hook.
  ```yaml
  verify:
    method: subagent
    phase: 2
    agent: code-maintainability-reviewer
    prompt: "Review claude-plugins/manifest-dev/hooks/hook_utils.py and claude-plugins/manifest-dev/hooks/post_compact_hook.py after thinking-disciplines removal. Check for orphan helpers, leftover dead constants, and overall coherence of what remains. Threshold: no MEDIUM+."
  ```

- [INV-G10] dist/ distributions contain no remaining references to removed components.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "! grep -rn 'thinking-disciplines\\|thinking_disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev/dist/"
  ```

- [INV-G11] CLAUDE.md adherence on changes.
  ```yaml
  verify:
    method: subagent
    phase: 2
    agent: context-file-adherence-reviewer
    prompt: "Audit the full diff against CLAUDE.md. Specifically verify: (1) `.claude/skills/` and `.agents/skills/` are kept in sync with `claude-plugins/manifest-dev/skills/`, (2) plugin version is bumped per the versioning rule, (3) READMEs are updated per the sync checklist, (4) skill naming kebab-case rule respected. Threshold: no MEDIUM+."
  ```

## 4. Process Guidance

- [PG-1] Limit edits in figure-out/SKILL.md and define/SKILL.md to: removing the `Invoke ... thinking-disciplines` line, embedding the six stances calibrated per skill, consolidating with existing content that already encodes parts of the stance (don't duplicate Disagreement guidance in figure-out — fold it together), and (figure-out only) dropping the `/stop-thinking-disciplines` references in the Ending section. Reorganization is permitted only where consolidation requires it.
- [PG-2] When embedding, follow the prompt-engineering skill's canonical principles as defined in `claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md`: information density, WHAT/WHY not HOW, decision rules over absolutes for judgment calls, low-arousal tone. The six stances are the WHAT; HOW each skill expresses them is /do's call within those principles.
- [PG-3] Use `cp`/`mv`/`rm` via Bash for file removal and movement (per CLAUDE.md File Operations).
- [PG-4] Run `ruff check --fix claude-plugins/ && black claude-plugins/ && mypy && pytest tests/hooks/ -v` after code changes, before final review pass (per CLAUDE.md Before PR).
- [PG-5] Regenerate dist/ via the `sync-tools` skill rather than hand-editing dist/ files. Sync-tools handles deletions and removes empty parent directories.
- [PG-6] Archive the final manifest to `.manifest/simplify-thinking-disciplines-inline-2026-05-03.md` only after dist regeneration (D7) verifies clean — keeps archival tied to a fully-converged state.

## 5. Known Assumptions

- [ASM-1] (auto) Plugin version bump strategy: minor 0.100.0 → 0.101.0 | Default: minor (structural change with behavior delta — loss of reinforcement reminders) | Impact if wrong: a patch bump would be inappropriate for the behavior delta; a major bump would be over-signaling for a non-API-breaking change.
- [ASM-2] (auto) Embedding placement and section heading are per-skill, /do's call within the prompt-engineering principles + INV-G6 scope. | Default: figure-out integrates near the top with consolidation into existing Disagreement / Interaction Failure Modes content; define integrates with the existing Principles + Discovery & question disciplines structure. | Impact if wrong: prompt-reviewer (INV-G8) and stance-presence check (INV-G7) catch operational issues; placement details revisable by amendment.
- [ASM-3] (auto) The `/stop-thinking-disciplines` skill removal is total (folder deleted, no redirect, no deprecation warning) | Default: full delete; users invoking it will get the standard "skill not found" path | Impact if wrong: existing user muscle memory hits a dead command; trivially recoverable.
- [ASM-4] (auto) Manifest archival filename: `simplify-thinking-disciplines-inline-2026-05-03.md` | Default: descriptive kebab-case with date | Impact if wrong: filename can be changed at archival time.

## 6. Deliverables

### Deliverable 1: Embed thinking-disciplines stances into figure-out and define (per-skill, prompt-engineering-calibrated)

**Acceptance Criteria:**

- [AC-1.1] figure-out/SKILL.md and define/SKILL.md both pass INV-G7 (prompt-reviewer judging stance presence + prompt-engineering principles). No additional per-deliverable verify needed — INV-G7 covers both files in a single review.

- [AC-1.2] figure-out/SKILL.md contains no remaining references to `/stop-thinking-disciplines` or `thinking-disciplines` skill invocation.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking-disciplines' /home/user/manifest-dev/claude-plugins/manifest-dev/skills/figure-out/SKILL.md"
  ```

- [AC-1.3] define/SKILL.md contains no remaining `Invoke ... thinking-disciplines` line.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking-disciplines' /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md"
  ```

### Deliverable 2: Remove standalone skills

**Acceptance Criteria:**

- [AC-2.1] `claude-plugins/manifest-dev/skills/thinking-disciplines/` does not exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/claude-plugins/manifest-dev/skills/thinking-disciplines"
  ```

- [AC-2.2] `claude-plugins/manifest-dev/skills/stop-thinking-disciplines/` does not exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/claude-plugins/manifest-dev/skills/stop-thinking-disciplines"
  ```

- [AC-2.3] `.claude/skills/thinking-disciplines` does not exist as file, directory, or symlink.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/.claude/skills/thinking-disciplines && ! test -L /home/user/manifest-dev/.claude/skills/thinking-disciplines"
  ```

- [AC-2.4] `.claude/skills/stop-thinking-disciplines` does not exist as file, directory, or symlink.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/.claude/skills/stop-thinking-disciplines && ! test -L /home/user/manifest-dev/.claude/skills/stop-thinking-disciplines"
  ```

- [AC-2.5] `.agents/skills/thinking-disciplines` symlink does not exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/.agents/skills/thinking-disciplines && ! test -L /home/user/manifest-dev/.agents/skills/thinking-disciplines"
  ```

- [AC-2.6] `.agents/skills/stop-thinking-disciplines` symlink does not exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/.agents/skills/stop-thinking-disciplines && ! test -L /home/user/manifest-dev/.agents/skills/stop-thinking-disciplines"
  ```

### Deliverable 3: Remove disciplines hooks and clean shared utilities

**Acceptance Criteria:**

- [AC-3.1] `claude-plugins/manifest-dev/hooks/thinking_disciplines_prompt_hook.py` does not exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/claude-plugins/manifest-dev/hooks/thinking_disciplines_prompt_hook.py"
  ```

- [AC-3.2] `claude-plugins/manifest-dev/hooks/thinking_disciplines_pretool_hook.py` does not exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/claude-plugins/manifest-dev/hooks/thinking_disciplines_pretool_hook.py"
  ```

- [AC-3.3] `post_compact_hook.py` no longer imports or calls `parse_thinking_disciplines_flow`, no longer references `THINKING_DISCIPLINES_RECOVERY_REMINDER`, and only handles /do recovery.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking_disciplines\\|THINKING_DISCIPLINES' /home/user/manifest-dev/claude-plugins/manifest-dev/hooks/post_compact_hook.py"
  ```

- [AC-3.4] `hook_utils.py` no longer contains `parse_thinking_disciplines_flow`, `ThinkingDisciplinesState`, or `_THINKING_DEACTIVATORS`.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking_disciplines\\|ThinkingDisciplines\\|_THINKING_DEACTIVATORS' /home/user/manifest-dev/claude-plugins/manifest-dev/hooks/hook_utils.py"
  ```

- [AC-3.5] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` registers neither thinking-disciplines hook (no entries pointing to either Python file).
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking_disciplines' /home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json"
  ```

- [AC-3.6] `.claude/settings.json` registers neither thinking-disciplines hook.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking_disciplines' /home/user/manifest-dev/.claude/settings.json"
  ```

- [AC-3.7] Both plugin.json and settings.json remain valid JSON.
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json; json.load(open(\"/home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json\")); json.load(open(\"/home/user/manifest-dev/.claude/settings.json\"))'"
  ```

### Deliverable 4: Remove disciplines tests

**Acceptance Criteria:**

- [AC-4.1] `tests/hooks/test_thinking_disciplines_flow.py` does not exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/tests/hooks/test_thinking_disciplines_flow.py"
  ```

- [AC-4.2] `tests/hooks/test_hook_integration.py` contains no references to thinking-disciplines, thinking_disciplines, or stop-thinking-disciplines.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking-disciplines\\|thinking_disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev/tests/hooks/test_hook_integration.py"
  ```

- [AC-4.3] Hook test suite passes after removals.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "pytest tests/hooks/ -v"
  ```

### Deliverable 5: Update documentation

**Acceptance Criteria:**

- [AC-5.1] Root `README.md` skill table no longer lists `thinking-disciplines` or `/stop-thinking-disciplines`; hook table no longer lists `thinking_disciplines_prompt_hook` or `thinking_disciplines_pretool_hook`.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking-disciplines\\|thinking_disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev/README.md"
  ```

- [AC-5.2] `claude-plugins/README.md` does not mention thinking-disciplines or /stop-thinking-disciplines.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking-disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev/claude-plugins/README.md"
  ```

- [AC-5.3] `claude-plugins/manifest-dev/README.md` does not reference thinking-disciplines, /stop-thinking-disciplines, or the two removed hooks.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking-disciplines\\|thinking_disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev/claude-plugins/manifest-dev/README.md"
  ```

- [AC-5.4] `CLAUDE.md` does not mention `parse_thinking_disciplines_flow` or other removed symbols.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'thinking_disciplines\\|thinking-disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev/CLAUDE.md"
  ```

- [AC-5.5] Documentation accuracy on the modified files.
  ```yaml
  verify:
    method: subagent
    phase: 2
    agent: docs-reviewer
    prompt: "Review docs accuracy after thinking-disciplines removal. Check README.md (root), claude-plugins/README.md, claude-plugins/manifest-dev/README.md, and CLAUDE.md against the actual current state of skills/, hooks/, and plugin.json. Flag stale references to removed components, broken cross-references, or descriptions that no longer match. Threshold: no MEDIUM+."
  ```

### Deliverable 6: Plugin version bump and manifest archival

**Acceptance Criteria:**

- [AC-6.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is `0.101.0`.
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json; v=json.load(open(\"/home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json\"))[\"version\"]; assert v == \"0.101.0\", f\"version is {v}\"'"
  ```

- [AC-6.2] Final manifest archived to `.manifest/simplify-thinking-disciplines-inline-2026-05-03.md`.
  ```yaml
  verify:
    method: bash
    command: "test -f /home/user/manifest-dev/.manifest/simplify-thinking-disciplines-inline-2026-05-03.md"
  ```

### Deliverable 7: Regenerate multi-CLI distributions

**Acceptance Criteria:**

- [AC-7.1] No remaining references to thinking-disciplines / stop-thinking-disciplines anywhere under `dist/`.
  ```yaml
  verify:
    method: bash
    command: "! grep -rn 'thinking-disciplines\\|thinking_disciplines\\|stop-thinking-disciplines' /home/user/manifest-dev/dist/"
  ```

- [AC-7.2] `dist/codex/skills/`, `dist/gemini/skills/`, and `dist/opencode/` no longer contain thinking-disciplines or stop-thinking-disciplines skill folders.
  ```yaml
  verify:
    method: bash
    command: "! test -e /home/user/manifest-dev/dist/codex/skills/thinking-disciplines && ! test -e /home/user/manifest-dev/dist/codex/skills/stop-thinking-disciplines && ! test -e /home/user/manifest-dev/dist/gemini/skills/thinking-disciplines && ! test -e /home/user/manifest-dev/dist/gemini/skills/stop-thinking-disciplines"
  ```

- [AC-7.3] `dist/{codex,gemini,opencode}/skills/{figure-out,define}/SKILL.md` match the source skill files byte-for-byte after sync-tools regeneration.
  ```yaml
  verify:
    method: bash
    command: "for skill in figure-out define; do for dist in codex gemini opencode; do diff -q /home/user/manifest-dev/claude-plugins/manifest-dev/skills/$skill/SKILL.md /home/user/manifest-dev/dist/$dist/skills/$skill/SKILL.md || exit 1; done; done"
  ```
