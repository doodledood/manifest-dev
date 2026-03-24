# Definition: Add --auto flag to orchestrate skill

## 1. Intent & Context
- **Goal:** Add a `--auto` flag to the orchestrate skill that makes the agent act as the owner. All phases still run, external stakeholders still participate normally (Slack messages, PR reviews, QA) — only the owner's decisions, approvals, and answers are replaced by the agent. Recommended for smaller, well-scoped tasks but no restrictions.
- **Mental Model:** `--auto` replaces the **owner's role**, not all human interaction. External stakeholders (Slack channels, PR reviewers, QA testers) are still messaged and waited on. Only decisions that would route to the owner are automated. In solo/local mode this means effectively full autonomy; in Slack+GitHub mode it means the agent posts, waits for reviewers, waits for QA — but handles owner decisions itself. `--interview autonomous` controls Phase 1 only; `--auto` extends owner-replacement across the entire pipeline (Phases 0–6). Progressive disclosure: auto mode details live in a reference doc, loaded only when the flag is present.
- **Mode:** thorough

## 2. Approach

- **Architecture:**
  - New reference file `skills/orchestrate/references/AUTO_MODE.md` containing all auto-mode behavioral rules per phase, decision logging format, and override semantics.
  - Minimal additions to `SKILL.md`: flag definition in `$ARGUMENTS`, state file schema update (`auto: false`), conditional "read AUTO_MODE.md if --auto" directive, and resume restoration logic.
  - Progressive disclosure pattern: SKILL.md stays lean; agent reads ref doc only when flag is active.

- **Execution Order:**
  - D1 (AUTO_MODE.md reference doc) → D2 (SKILL.md updates) → D3 (plugin.json + READMEs)
  - Rationale: Ref doc defines the behavior that SKILL.md references. SKILL.md must point to a doc that exists. READMEs document what's already built.

- **Risk Areas:**
  - [R-1] Composition conflict between AUTO_MODE.md and SKILL.md phase descriptions | Detect: prompt-reviewer flags contradictory instructions
  - [R-2] Regression in non-auto flow from flag parsing changes | Detect: existing flag combinations tested via criteria-checker
  - [R-3] Context rot during long auto runs — agent forgets auto-specific behaviors mid-execution | Detect: AUTO_MODE.md includes re-read directive at phase transitions

- **Trade-offs:**
  - [T-1] Inline auto docs vs reference doc → Prefer reference doc because progressive disclosure keeps SKILL.md lean and avoids context bloat for non-auto runs
  - [T-2] Per-phase auto notes vs consolidated ref doc → Prefer consolidated because one doc is easier to maintain and review holistically
  - [T-3] Guardrails on complexity vs trust user → Prefer trust user because --auto is opt-in; user accepts the autonomy trade-off
  - [T-4] Brevity vs explicit guidance in AUTO_MODE.md → Prefer brief behavioral deltas per phase (what changes vs normal mode) over verbose full descriptions. Lean enough to avoid context bloat, explicit enough to not be misinterpreted during long runs

## 3. Global Invariants (The Constitution)

- [INV-G1] Non-auto behavior unchanged: existing flag combinations (`--medium`, `--review-platform`, `--interview`, `--mode`, `--resume`) produce identical behavior when `--auto` is absent.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read SKILL.md. Verify that all non-auto flag documentation, phase descriptions, and state file schema are unchanged in semantics (additions for --auto are allowed, but existing behavior descriptions must not be altered). Check that --auto conditional logic is isolated (if auto: ...) and does not affect default code paths."
  ```

- [INV-G2] Override semantics: explicit flags take precedence over --auto implied defaults. `--auto --review-platform github` must not conflict.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read SKILL.md and AUTO_MODE.md. Verify that override semantics are documented: explicit flags override --auto defaults. Check for any language that contradicts composability (e.g., '--auto forces X' without mentioning override)."
  ```

- [INV-G3] Decision logging: every decision the agent makes AS the owner (manifest approval, escalation resolution, owner-routed questions) must be logged to `/tmp/orchestrate-auto-decisions-{run_id}.md` with context, decision, and reasoning.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify that decision logging is specified for each phase where the agent makes decisions that would normally route to the owner (Phase 0 context, Phase 1 interview, Phase 2 manifest approval, Phase 3 escalations, and any owner-routed questions in Phases 4-5). Each must log to the dedicated decision file with context, decision, and reasoning."
  ```

- [INV-G4] Halt on unresolvable: auto mode must halt and ask the user when an escalation is truly unresolvable (missing credentials, ambiguous requirements with no reasonable default). Auto mode is not silent-failure mode.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify that halt conditions are explicitly documented — the agent must stop and ask the user when facing truly unresolvable issues. Check that examples are given (missing credentials, ambiguous requirements with no reasonable default)."
  ```

- [INV-G5] External stakeholder interactions preserved: auto mode must not skip or alter interactions with external stakeholders (Slack messages, PR review requests, QA involvement). Only owner-routed decisions are automated.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify that the document explicitly states external stakeholder interactions (Slack messages, PR review requests/responses, QA tester involvement) are NOT affected by auto mode. Only decisions that would route to the owner are automated. Check that no phase delta suggests skipping or altering stakeholder communication."
  ```

- [INV-G6] Prompt quality: no MEDIUM or higher issues from prompt-reviewer across all changed/created prompt files.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review these files in claude-plugins/manifest-dev-orchestrate/: skills/orchestrate/SKILL.md and skills/orchestrate/references/AUTO_MODE.md"
    phase: 2
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] High-signal changes only: every addition to SKILL.md must address a real behavioral need. Don't add verbose explanations for obvious behaviors.
- [PG-2] Right-sized changes: --auto is a focused feature. Don't restructure existing SKILL.md sections that work fine.
- [PG-3] Match existing SKILL.md patterns: flag documentation style, state file schema format, error handling format, resume section format should match what's already there.

## 5. Known Assumptions

- [ASM-1] `--interview autonomous` already works correctly in /define | Default: assumed working | Impact if wrong: Phase 1 auto behavior breaks
- [ASM-2] State file flag restoration works reliably for existing flags | Default: assumed working | Impact if wrong: --auto won't persist across resumes
- [ASM-3] The orchestrate lead already has the capability to read reference docs conditionally | Default: assumed (agent can read files) | Impact if wrong: ref doc pattern won't work (but agents can always read files, so this is safe)

## 6. Deliverables (The Work)

### Deliverable 1: AUTO_MODE.md Reference Document
*New file: `claude-plugins/manifest-dev-orchestrate/skills/orchestrate/references/AUTO_MODE.md`*

**Acceptance Criteria:**
- [AC-1.1] Document covers all 7 phases (0–6) with auto-mode behavioral deltas. Each phase describes what owner decisions the agent handles. External stakeholder interactions (Slack, PR reviews, QA) remain unchanged. Phases without owner-decision changes explicitly state "no change."
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify all 7 phases (0-6) are addressed. Each phase must describe what OWNER decisions the agent handles in auto mode. Verify the doc makes clear that external stakeholder interactions (Slack messages, PR reviews, QA testing) still happen normally — only owner-routed decisions are automated. Phases with no change must say so explicitly."
  ```

- [AC-1.2] Documents implied defaults: `--interview autonomous`, `--medium local`, `--review-platform github` (all overridable by explicit flags).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify that implied defaults are listed (--interview autonomous, --medium local, --review-platform github) and each is marked as overridable by explicit flags."
  ```

- [AC-1.3] Documents decision log format: file path pattern (`/tmp/orchestrate-auto-decisions-{run_id}.md`), what gets logged per phase, and entry structure (context, decision, reasoning).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify decision log format is specified: file path pattern, per-phase logging requirements, and entry structure (must include context, decision, reasoning for each entry)."
  ```

- [AC-1.4] Documents halt conditions: when auto mode must stop and ask the user (missing credentials, ambiguous requirements with no reasonable default, etc.).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify halt conditions are documented with concrete examples of when auto mode must stop and ask the user."
  ```

- [AC-1.5] Documents resume behavior: when resuming with auto=true in state, agent re-reads AUTO_MODE.md and re-applies behavioral changes.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify resume behavior is documented: auto flag persists in state, agent re-reads this document on resume when auto=true."
  ```

- [AC-1.6] Content uses brief behavioral deltas per phase (what changes vs normal mode), not full phase descriptions. Follows T-4 trade-off.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify each phase section describes the behavioral DELTA (what changes in auto mode) rather than restating the full phase flow. Each section should be concise — a few sentences or a short list, not paragraphs."
  ```

- [AC-1.7] Documents flag conflict resolution: explicit overrides always win. Example: `--auto --interview thorough` → thorough interview (override), auto applies to all other phases.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read AUTO_MODE.md. Verify that flag conflict resolution is documented: explicit flags always override --auto implied defaults. Check for an example showing --auto with a contradicting explicit flag (e.g., --auto --interview thorough)."
  ```

### Deliverable 2: SKILL.md Updates
*Modified file: `claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md`*

**Acceptance Criteria:**
- [AC-2.1] `--auto` flag documented in `$ARGUMENTS` section with one-line description and pointer to AUTO_MODE.md.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read SKILL.md. Verify --auto flag appears in the $ARGUMENTS flag list with a brief description and explicit instruction to read references/AUTO_MODE.md when the flag is present."
  ```

- [AC-2.2] State file schema includes `auto: false` in the `flags` object.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read SKILL.md. Find the state file schema (JSON template). Verify the 'flags' object includes 'auto': false alongside existing interview and mode fields."
  ```

- [AC-2.3] Resume section updated: restores `auto` from `state.flags`, re-reads AUTO_MODE.md when auto=true, allows `--auto` as override flag alongside `--resume`.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read SKILL.md. Find the resume section. Verify it mentions restoring the auto flag from state.flags, re-reading AUTO_MODE.md when auto is true, and allowing --auto as an override alongside --resume."
  ```

- [AC-2.4] Flag resolution order documented: parse --auto first, apply implied defaults, then apply explicit flag overrides.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read SKILL.md or AUTO_MODE.md. Verify flag resolution order is documented: --auto parsed first, implied defaults applied, explicit flags override."
  ```

- [AC-2.5] Error Handling section includes `--auto` validation: boolean flag (no value expected), document behavior if unexpected value follows.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read SKILL.md. Find the Error Handling section. Verify --auto has a validation entry consistent with the pattern of other flags in that section."
  ```

### Deliverable 3: Plugin Version Bump and README Updates

**Acceptance Criteria:**
- [AC-3.1] Plugin version bumped (minor) in `claude-plugins/manifest-dev-orchestrate/.claude-plugin/plugin.json`.
  ```yaml
  verify:
    method: bash
    command: "cat claude-plugins/manifest-dev-orchestrate/.claude-plugin/plugin.json | python3 -c \"import json,sys; v=json.load(sys.stdin)['version']; parts=v.split('.'); assert int(parts[1])>=1, f'Minor version not bumped: {v}'\""
  ```

- [AC-3.2] `claude-plugins/manifest-dev-orchestrate/README.md` documents `--auto` flag in the flags/usage section.
  ```yaml
  verify:
    method: bash
    command: "grep -q '\\-\\-auto' claude-plugins/manifest-dev-orchestrate/README.md && echo 'PASS: --auto documented in orchestrate README'"
  ```

- [AC-3.3] Root `README.md` updated if orchestrate plugin description mentions flags or modes.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read the root README.md. Check if the orchestrate plugin description mentions specific flags or modes. If yes, verify --auto is included. If the description is high-level and doesn't list flags, this criterion passes (no update needed)."
  ```
