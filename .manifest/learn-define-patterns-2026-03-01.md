# Definition: learn-define-patterns Skill

## 1. Intent & Context
- **Goal:** Create a plugin skill that analyzes recent /define session transcripts, extracts patterns the user iterated on (probing preferences, trade-off defaults, recurring invariants, process guidance, quality gate adjustments), and writes generalizable patterns to CLAUDE.md as probing hints for future /define sessions.
- **Mental Model:** CLAUDE.md is auto-loaded into Claude Code's context — /define doesn't explicitly read it, it's just there. By writing user preference patterns to CLAUDE.md, future /define sessions naturally discover and act on what the user previously cared about — closing the feedback loop between sessions without requiring skill file changes.

## 2. Approach

*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** Fan-out/fan-in.
  1. Main skill locates session JSONL files containing /define activity (grep for skill invocations)
  2. Spawns parallel `define-session-analyzer` agents — one per session (up to 10 most recent)
  3. Each agent analyzes one session using the dedicated agent definition, outputs structured markdown to `/tmp/define-learn-{session-id}.md` with 5+1 categories: Probing Hints, Trade-off Defaults, Recurring Invariants, Process Guidance, Quality Gate Adjustments, Other — each pattern with evidence quotes and session metadata
  4. Main skill reads all per-session analysis files, aggregates patterns across sessions
  5. Applies generalizability heuristic (project-specific references → flagged; categorical/principle patterns → kept)
  6. Semantic deduplication via LLM: identifies patterns that say the same thing in different words and merges them
  7. Detects contradictory patterns across sessions and presents conflicts to user with evidence from both sessions
  8. Presents aggregated patterns for user approval via AskUserQuestion
  9. Asks which CLAUDE.md to write to (project, user, or both)
  10. Shows diff/preview of what will change in CLAUDE.md before writing
  11. Reads existing CLAUDE.md, merges with existing `## /define Preferences` section (semantic dedup), writes approved patterns
  12. Cleans up per-session analysis files from `/tmp/` after aggregation

- **Execution Order:**
  - D1 (Agent definition) → D2 (SKILL.md) → D3 (plugin registration) → D4 (documentation)
  - Rationale: agent definition is a dependency of the skill; skill is the core deliverable; registration and docs depend on both

- **Risk Areas:**
  - [R-1] Session JSONL parsing fragility — format may vary across Claude Code versions | Detect: agent fails to extract patterns from a session
  - [R-2] CLAUDE.md write corruption — merging could damage existing content | Detect: diff preview shows unintended deletions before write
  - [R-3] Pattern noise — too many low-value patterns overwhelm user during approval | Detect: user consistently rejects most suggestions
  - [R-4] Orphaned temp files — per-session analysis files left in `/tmp/` after use | Detect: `/tmp/define-learn-*.md` files accumulate across runs

- **Trade-offs:**
  - [T-1] Pattern coverage vs noise → Prefer coverage (user approval step filters noise; missed patterns can't be recovered)
  - [T-2] Prompt detail vs capability trust → Prefer trust (goal-oriented prompt; model knows how to parse JSONL and identify patterns)
  - [T-3] Fixed structure vs flexibility → Prefer hybrid (fixed categories for consistency + freeform section for uncategorizable patterns)

## 3. Global Invariants (The Constitution)

- [INV-G1] Skill MUST NOT modify CLAUDE.md without presenting patterns to user for approval first
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the SKILL.md file at claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify that the skill workflow requires user approval (via AskUserQuestion or equivalent) BEFORE any write to CLAUDE.md. The skill must never auto-write patterns without user consent."
  ```

- [INV-G2] Skill MUST merge with existing `## /define Preferences` section — never overwrite or duplicate. Deduplication uses semantic similarity (LLM judgment), not just exact text match
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the SKILL.md file at claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify that the skill reads existing CLAUDE.md content, parses any existing /define Preferences section, deduplicates patterns using semantic similarity (not just exact text match), and merges new patterns with existing ones. Must never blind-overwrite the section."
  ```

- [INV-G3] CLAUDE.md output MUST use only standard markdown (headers, bullets, HTML comments) — no custom syntax or parsing dependencies
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the SKILL.md file at claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify that the CLAUDE.md output format specification uses only standard markdown: ## headers, ### subheaders, - bullet lists, and <!-- HTML comments -->. No custom delimiters, no YAML frontmatter, no special parsing syntax."
  ```

- [INV-G4] Skill frontmatter MUST follow plugin conventions: kebab-case name, description under 1024 chars, user-invocable: true
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify frontmatter has: name (kebab-case, max 64 chars), description (max 1024 chars, follows What+When+Triggers pattern), user-invocable: true."
  ```

- [INV-G5] Skill MUST ask which CLAUDE.md to write to (project CLAUDE.md, user ~/.claude/CLAUDE.md, or both) — never assume
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the skill explicitly asks the user which CLAUDE.md to write to before writing. Must present project CLAUDE.md and user CLAUDE.md (~/.claude/CLAUDE.md) as options."
  ```

- [INV-G6] No lint errors, type errors, or format violations in changed files
  ```yaml
  verify:
    method: bash
    command: "ruff check --fix claude-plugins/ && black --check claude-plugins/ && mypy"
  ```

- [INV-G7] Prompt follows first-principles: WHAT and WHY, not HOW. No prescriptive step sequences, no capability instructions, no arbitrary limits
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: opus
    prompt: "Review the prompt at claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md against first-principles prompting. Check for: prescriptive HOW language, arbitrary limits, capability instructions (tool names, 'use grep'), weak language ('try to', 'maybe'), rigid checklists. The prompt should state goals and constraints, trusting model capability."
  ```

- [INV-G8] Skill MUST show diff/preview of CLAUDE.md changes before writing — user must see exactly what will be added/changed
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the skill shows the user a diff or preview of what will change in CLAUDE.md BEFORE actually writing. The user must be able to see exactly what content will be added or modified."
  ```

- [INV-G9] No HIGH/CRITICAL issues from code-bugs-reviewer on SKILL.md
  ```yaml
  verify:
    method: subagent
    agent: code-bugs-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md for bugs, logic errors, or issues."
  ```

- [INV-G10] No HIGH/CRITICAL issues from code-simplicity-reviewer on SKILL.md
  ```yaml
  verify:
    method: subagent
    agent: code-simplicity-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md for unnecessary complexity or over-engineering."
  ```

- [INV-G11] No HIGH/CRITICAL issues from code-maintainability-reviewer on SKILL.md
  ```yaml
  verify:
    method: subagent
    agent: code-maintainability-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md for maintainability issues."
  ```

- [INV-G12] No HIGH/CRITICAL issues from code-design-reviewer on SKILL.md
  ```yaml
  verify:
    method: subagent
    agent: code-design-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md for design fitness issues."
  ```

- [INV-G13] No MEDIUM+ issues from docs-reviewer on documentation changes
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: opus
    prompt: "Review documentation changes in README.md, claude-plugins/manifest-dev/README.md, and claude-plugins/README.md for accuracy, completeness, and clarity regarding the learn-define-patterns skill."
  ```

- [INV-G14] CLAUDE.md adherence — all changes follow project CLAUDE.md conventions
  ```yaml
  verify:
    method: subagent
    agent: claude-md-adherence-reviewer
    model: opus
    prompt: "Review all changes for adherence to the project's CLAUDE.md conventions (naming, structure, README sync checklist, version bumping)."
  ```

- [INV-G15] No anti-patterns in the prompt (PROMPTING gate: no capability instructions, no tool names, no rigid checklists, no weak hedging language)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Check for prompt anti-patterns: capability instructions ('you can use X', 'use the Y tool'), tool name references, rigid numbered checklists that constrain execution order unnecessarily, weak hedging ('try to', 'consider', 'maybe'). Flag any found."
  ```

- [INV-G16] Prompt's invocation fit — the skill is invokable via both /learn-define-patterns and auto-discovery, and the description + frontmatter support both modes
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify: (1) frontmatter supports user invocation (user-invocable: true or defaulted), (2) description contains trigger terms that would match user requests like 'learn from define sessions' or 'extract define patterns', (3) the skill body works when invoked both explicitly via slash command and via auto-discovery."
  ```

- [INV-G17] Domain context — prompt provides sufficient context about /define sessions, CLAUDE.md format, and pattern categories without requiring external knowledge
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the prompt provides enough domain context for the model to execute: what a /define session is, what CLAUDE.md is used for, what the 5+1 pattern categories mean, what 'generalizability' means in this context. The model should not need to guess domain concepts."
  ```

- [INV-G18] Multi-phase memento — if the skill spans multiple turns or phases (analysis → approval → write), critical context is preserved across phase boundaries
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. The skill has multiple phases: session discovery, parallel analysis, aggregation, approval, write. Verify that each phase preserves or re-reads what subsequent phases need. Specifically: (1) aggregation has access to all per-session files, (2) approval has access to aggregated patterns, (3) write has access to approved patterns AND existing CLAUDE.md content."
  ```

- [INV-G19] Model-prompt fit — prompt complexity and structure match what the model can reliably execute in a single skill invocation
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Assess whether the prompt asks the model to do too many things in a single invocation, or if the fan-out architecture appropriately distributes complexity. Check that the main skill's responsibilities (orchestration, aggregation, dedup, approval, write) are feasible within a single skill execution context."
  ```

- [INV-G20] Guardrail calibration — safety constraints (user approval, diff preview, write target choice) are appropriately strict without being so rigid they prevent normal operation
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Evaluate guardrails: (1) user approval before write — appropriate for CLAUDE.md modification, (2) diff preview — appropriate for transparency, (3) write target choice — appropriate for user control. Check that none of these guardrails are so strict they create unusable friction (e.g., requiring approval for each individual pattern instead of batch approval)."
  ```

**Skipped quality gates (with reasoning):**
- CODING: type-safety-reviewer — SKILL.md is a markdown prompt file, not typed code. No type annotations to review.
- CODING: code-coverage-reviewer — No executable code to cover with tests. The deliverable is a prompt definition.
- CODING: code-testability-reviewer — Prompt files are not unit-testable in the traditional sense. Verification is via prompt-reviewer and subagent gates above.

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Document load-bearing assumptions — identify what must remain true for the skill to work (session JSONL format, CLAUDE.md section naming, /define skill invocation patterns)
- [PG-2] Keep the prompt goal-oriented — state what patterns to find and what format to output, not how to parse JSONL or how to compare sessions
- [PG-3] Per-session agent prompts should be self-contained — each agent receives enough context to analyze one session independently without knowledge of other sessions
- [PG-4] User patterns in CLAUDE.md take precedence over built-in task file guidance when /define encounters conflicts — patterns represent intentional user preferences
- [PG-5] Patterns include inline date comments for traceability; removal is via manual CLAUDE.md editing — no extra tooling for undo

## 5. Known Assumptions

- [ASM-1] Session JSONL files live at `~/.claude/projects/{encoded-path}/{session-id}.jsonl` | Default: standard Claude Code session storage | Impact if wrong: skill can't find sessions
- [ASM-2] /define sessions are identifiable by presence of `"skill":"define"` or `/define` patterns in session content | Default: skill invocation markers present | Impact if wrong: sessions not detected
- [ASM-3] CLAUDE.md exists in project root (for project CLAUDE.md) and `~/.claude/CLAUDE.md` (for user CLAUDE.md) | Default: standard locations | Impact if wrong: write target not found — skill should handle gracefully by creating the section
- [ASM-4] `## /define Preferences` section name won't conflict with user-authored sections | Default: unique section name | Impact if wrong: merge overwrites user content — skill should check for existing section before creating

## 6. Deliverables (The Work)

### Deliverable 1: Agent definition — define-session-analyzer

**Acceptance Criteria:**

- [AC-1.1] Agent file exists at `claude-plugins/manifest-dev/agents/define-session-analyzer.md` with valid frontmatter declaring all needed tools
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/agents/define-session-analyzer.md && head -20 claude-plugins/manifest-dev/agents/define-session-analyzer.md"
  ```

- [AC-1.2] Agent explicitly declares tools for: reading session JSONL files, writing analysis output to `/tmp/`, searching file contents
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/agents/define-session-analyzer.md. Verify the frontmatter declares all tools the agent needs: file reading (to read session JSONL), file writing (to write analysis output to /tmp/), content search/grep (to search within session content). Agents run in isolation and won't inherit tools — all must be declared."
  ```

- [AC-1.3] Agent prompt specifies extracting patterns in 5+1 categories (Probing Hints, Trade-off Defaults, Recurring Invariants, Process Guidance, Quality Gate Adjustments, Other) with evidence quotes and session metadata
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/agents/define-session-analyzer.md. Verify the agent prompt specifies: (1) extracting patterns in 5 named categories plus freeform, (2) including evidence quotes from the session, (3) including session metadata (session ID, date if available). The agent should output structured markdown."
  ```

- [AC-1.4] Agent output format is specified: structured markdown with category headers, bullet patterns with evidence, session metadata. Output file naming convention: `/tmp/define-learn-{session-id}.md`
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/agents/define-session-analyzer.md. Verify: (1) the output format is explicitly specified — markdown with ### category headers, - bullet patterns, evidence quotes (blockquote or inline), and session metadata at the top, (2) the output file naming convention /tmp/define-learn-{session-id}.md is specified or the agent receives the output path as input."
  ```

### Deliverable 2: SKILL.md — learn-define-patterns skill definition

**Acceptance Criteria:**

- [AC-2.1] SKILL.md exists at `claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md` with valid frontmatter
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md && head -10 claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md"
  ```

- [AC-2.2] Skill finds /define sessions in JSONL files, limited to last 10 by default
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the skill describes: (1) finding session JSONL files, (2) filtering to sessions containing /define activity, (3) limiting to last 10 sessions by default."
  ```

- [AC-2.3] Skill spawns parallel `define-session-analyzer` agents for analysis (fan-out/fan-in architecture), referencing the agent definition from Deliverable 1. Main skill reads per-session files at `/tmp/define-learn-{session-id}.md` (matching the naming convention from AC-1.4)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the skill describes: (1) spawning parallel define-session-analyzer agents (one per session) referencing the agent by name, (2) reading per-session analysis files at /tmp/define-learn-{session-id}.md matching the agent's output convention, (3) aggregating all analysis files."
  ```

- [AC-2.4] Per-session agents extract five pattern categories: probing preferences, trade-off defaults, recurring invariants, process guidance, quality gate adjustments — plus freeform observations
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the per-session agent prompt specifies extracting patterns in these categories: (1) probing preferences, (2) trade-off defaults, (3) recurring invariants, (4) process guidance, (5) quality gate adjustments, plus a freeform section for uncategorizable patterns."
  ```

- [AC-2.5] Aggregation applies generalizability heuristic: patterns referencing specific files/entities flagged as project-specific; categorical/principle patterns kept as generalizable. User filter during approval
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the skill describes: (1) a generalizability heuristic distinguishing project-specific patterns (reference specific files, variables, entities) from generalizable patterns (reference categories, principles, domains), and (2) presenting both types to the user who makes the final decision."
  ```

- [AC-2.6] CLAUDE.md output uses categorized format with `## /define Preferences` header, subcategory headers, bullet patterns with inline date comments
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify the CLAUDE.md output format matches: ## /define Preferences as the section header, ### subcategories (Probing Hints, Trade-off Defaults, Recurring Invariants, Process Guidance, Quality Gate Adjustments, Other), bullet patterns with <!-- date --> inline comments. Standard markdown only."
  ```

- [AC-2.7] Description follows What + When + Triggers pattern for auto-invocation
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the frontmatter description in claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify it follows the What + When + Triggers pattern: states what the skill does, when to use it, and trigger terms that would match user requests."
  ```

- [AC-2.8] Handles edge cases: no /define sessions found (clear message), malformed session files (skip with warning), valid session with zero patterns (skip silently, include count in summary), contradictory patterns across sessions (present both with conflict noted), existing /define Preferences section (merge), CLAUDE.md doesn't exist (create section), orphaned temp files cleaned up after aggregation
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify it handles these edge cases: (1) no /define sessions found — clear user message, (2) malformed session files — skip with warning, (3) valid session with zero extractable patterns — skip silently with count in final summary, (4) contradictory patterns across sessions — present both to user with evidence from each session and conflict noted, (5) existing /define Preferences section in CLAUDE.md — merge and semantic dedup, (6) CLAUDE.md doesn't exist — create the section, (7) per-session analysis files in /tmp/ cleaned up after aggregation."
  ```

- [AC-2.9] Prompt has no ambiguous instructions, no vague language, no implicit expectations (PROMPTING clarity gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Check every instruction for ambiguity: could it be read two ways? Are there vague terms like 'be helpful', 'use good judgment', 'when appropriate'? Are there unstated assumptions about what 'good' means? Flag any unclear instructions."
  ```

- [AC-2.10] No conflicting rules or priority collisions in the prompt (PROMPTING no-conflicts gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Identify all MUST/SHOULD rules. Check for pairs that can't both be satisfied. Verify edge cases are covered — what happens when rules conflict?"
  ```

- [AC-2.11] Critical rules are surfaced prominently, clear hierarchy (PROMPTING structure gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Skim first and last paragraphs only — are critical rules visible? Is there a clear priority hierarchy? Are important rules buried in the middle?"
  ```

- [AC-2.12] Every word earns its place — no filler content (PROMPTING information density gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. For each paragraph, ask: if I removed this sentence, would anything be lost? Flag content that doesn't earn its place."
  ```

- [AC-2.13] Prompt complexity matches task complexity — not over-engineered, not under-specified (PROMPTING complexity fit gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Compare prompt structure depth to task difficulty. Is the prompt over-engineered for what it does? Is it under-specified for complex aspects? Prompt complexity should match the task."
  ```

- [AC-2.14] Edge cases from the domain are identified and addressed in the prompt (PROMPTING edge case coverage gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Identify domain-specific edge cases (empty sessions, very large sessions, sessions with no user corrections, sessions where /define was abandoned mid-interview). Verify the prompt addresses each."
  ```

- [AC-2.15] Output format, length, and detail level match the use case (PROMPTING output calibration gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. The output is patterns written to CLAUDE.md. Verify the specified output format matches what CLAUDE.md readers (both /define and humans) would expect: concise bullets, clear categories, useful inline metadata."
  ```

- [AC-2.16] Requirements traceability — every specified requirement maps to implementation in the prompt (FEATURE gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Cross-reference with the manifest at /tmp/manifest-20260301-095848.md. Verify every requirement in the manifest (pattern types, architecture, edge cases, CLAUDE.md format, approval flow, write target choice, generalizability heuristic, semantic dedup, conflict detection, diff preview) has a corresponding instruction or constraint in the SKILL.md."
  ```

- [AC-2.17] Behavior completeness — all specified use cases and interactions implemented, not just the happy path (FEATURE gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify all use cases are covered: (1) happy path with multiple sessions, (2) single session, (3) no sessions found, (4) malformed sessions, (5) empty patterns, (6) contradictions, (7) existing CLAUDE.md section, (8) no CLAUDE.md, (9) user selects project vs user CLAUDE.md."
  ```

- [AC-2.18] Error experience — skill failures produce clear, actionable feedback (FEATURE gate)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/learn-define-patterns/SKILL.md. Verify that failure cases (no sessions, parse errors, write failures) produce clear, actionable user messages — not silent failures or raw errors."
  ```

### Deliverable 3: Plugin registration and version bump

**Acceptance Criteria:**

- [AC-3.1] Plugin version bumped from 0.61.0 (minor version increment for new feature) in `.claude-plugin/plugin.json`
  ```yaml
  verify:
    method: bash
    command: "cat claude-plugins/manifest-dev/.claude-plugin/plugin.json | python3 -c \"import sys,json; d=json.load(sys.stdin); v=d['version']; parts=v.split('.'); print('OK: ' + v) if int(parts[1]) > 61 or int(parts[0]) > 0 else print('FAIL: version is ' + v + ', expected > 0.61.0')\""
  ```

- [AC-3.2] Plugin description/keywords updated if needed to reflect new capability
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/.claude-plugin/plugin.json. Check if the description or keywords mention the ability to learn from sessions or extract patterns. If the skill adds a significant new capability category, keywords should be updated."
  ```

### Deliverable 4: Documentation updates

**Acceptance Criteria:**

- [AC-4.1] Root README.md updated with learn-define-patterns in the skills listing
  ```yaml
  verify:
    method: bash
    command: "grep -q 'learn-define-patterns' README.md && echo 'OK' || echo 'FAIL: learn-define-patterns not found in root README'"
  ```

- [AC-4.2] Plugin README.md (`claude-plugins/manifest-dev/README.md`) updated with the new skill
  ```yaml
  verify:
    method: bash
    command: "grep -q 'learn-define-patterns' claude-plugins/manifest-dev/README.md && echo 'OK' || echo 'FAIL: learn-define-patterns not found in plugin README'"
  ```

- [AC-4.3] `claude-plugins/README.md` updated if it lists plugin capabilities
  ```yaml
  verify:
    method: bash
    command: "grep -q 'learn-define-patterns' claude-plugins/README.md 2>/dev/null && echo 'OK' || echo 'WARN: check if claude-plugins/README.md lists individual skills'"
  ```

- [AC-4.4] Documentation accurately describes the skill — no MEDIUM+ issues from docs-reviewer
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: opus
    prompt: "Review all README changes related to learn-define-patterns for accuracy and completeness."
  ```
