# manifest-dev Agents

## Workflow

This project uses a **define -> do -> verify -> done** workflow:

1. **define** -- Interview-driven manifest builder. Scopes the task, identifies acceptance criteria, global invariants, risks, and trade-offs. Produces a manifest file.
2. **do** -- Manifest executor. Iterates through deliverables, implementing each according to the manifest.
3. **verify** -- Spawns parallel verification agents to check acceptance criteria and invariants against the implementation.
4. **done** -- Completion marker. Summarizes execution, notes any deviations, and closes the workflow.

**Shortcut**: **auto** -- End-to-end autonomous execution that chains /define (autonomous interview) and /do into a single command. Use when you want to define and execute a task without manual intervention during planning.

Skills handle the workflow orchestration. Agents listed below are specialized verification subagents spawned by the `verify` skill and supporting skills.

> **Codex CLI note**: On Codex, these agents are approximated using TOML config stubs in `agents/`. Codex agents have 6 default tools (`shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`) plus experimental tools (`read_file`, `list_dir`, `grep_files`) that may be available depending on model configuration. Review agents use `sandbox_mode = "read-only"` to enforce read-only behavior.

---

## Verification Agent

### criteria-checker
Read-only verification agent. Validates a single acceptance criterion or global invariant using any automated method: shell commands, codebase analysis, file inspection, reasoning, or web research. Returns structured PASS/FAIL results with evidence. Core to the `verify` skill workflow -- spawned in parallel, one per criterion.

**Codex approximation**: Use `shell_command` for running tests, linting, and file inspection. Use `web_search` for research-based criteria. Report results via `update_plan` to track verification progress.

---

## Code Review Agents

### change-intent-reviewer
Adversarially analyzes whether code, prompt, or config changes achieve their stated intent. Reconstructs change intent from diff context, then systematically attacks the logic to find behavioral divergences -- where behavior won't match what the author expects. Produces a structured intent analysis report.

**Codex approximation**: Use `shell_command` to run `git diff origin/main...HEAD` and `git log`, then read files for context. Reconstruct intent from diffs, commit messages, tests, and comments. Report divergences in the structured format.

### code-bugs-reviewer
Audits code changes for mechanical defects -- runtime failures, resource issues, and structural code flaws. Focuses on defects detectable from code patterns (race conditions, resource leaks, edge cases, dangerous defaults, fail-loudly violations) rather than intent-behavior analysis. Produces a structured bug report with severity ratings (Critical/High/Medium/Low). Read-only: analyzes `git diff` output and source files without modifying anything.

**Codex approximation**: Use `shell_command` to run `git diff origin/main...HEAD`, then read files for context. Report findings in the structured bug report format.

### code-design-reviewer
Audits code for design fitness -- whether code is the right approach given what already exists in the framework, codebase, and configuration systems. Identifies reinvented wheels, misplaced responsibilities (code vs config boundary), under-engineering, short-sighted interfaces, concept misuse, and incoherent PR scope.

**Codex approximation**: Use `shell_command` for git diff, grep, and find operations to understand the codebase context. Use `web_search` to verify framework capabilities when needed.

### code-simplicity-reviewer
Identifies unnecessary complexity, over-engineering, premature optimization, and cognitive burden. Catches solutions more complex than the problem requires -- not structural issues like coupling (handled by maintainability), but implementation complexity that makes code harder to understand than necessary.

**Codex approximation**: Review diff output via `shell_command`, focusing on abstraction layers, indirection, and complexity relative to the problem being solved.

### code-maintainability-reviewer
Comprehensive maintainability audit focusing on code organization: DRY violations, coupling, cohesion, consistency, dead code, architectural boundary leakage, concept drift, and migration debt. Examines how changes affect long-term codebase health.

**Codex approximation**: Use `shell_command` for broad codebase searches (grep for patterns, find for structure). Cross-reference changed code against existing patterns.

### code-coverage-reviewer
Verifies that code changes have adequate test coverage by proactively enumerating edge cases from the code's logic. Analyzes the diff, derives specific test scenarios with concrete inputs and expected outputs, and reports coverage gaps.

**Codex approximation**: Use `shell_command` to run `git diff`, identify changed logic, then search for corresponding test files. Derive concrete test scenarios from code paths. Run test suites if available to check coverage.

### code-testability-reviewer
Identifies testability issues -- code requiring excessive mocking, business logic buried in IO operations, non-deterministic inputs, hidden dependencies, and tight coupling that makes verification difficult. Suggests structural improvements to reduce test friction.

**Codex approximation**: Analyze changed code via `shell_command` (git diff + file reading), identify functions with high IO/mock requirements.

### contracts-reviewer
Verifies API and interface contract correctness with evidence. Checks both outbound (code calls external/internal APIs correctly per documentation) and inbound (changes don't break consumers of your interfaces). Evidence-based -- cites actual API docs or codebase definitions.

**Codex approximation**: Use `shell_command` to run `git diff` and identify API calls and interface changes. Use `web_search` to fetch external API documentation. Search the codebase for consumers of changed interfaces. Report violations with evidence citations.

### type-safety-reviewer
Audits code for type safety issues across typed languages (TypeScript, Python, Java/Kotlin, Go, Rust, C#). Identifies `any` abuse, invalid states representable in the type system, missing exhaustiveness checks, nullability gaps, and opportunities to push runtime checks into compile-time guarantees.

**Codex approximation**: Use `shell_command` to grep for type-safety anti-patterns (`any`, untyped generics, type assertions) and review type definitions in changed files.

---

## Documentation and Compliance Agents

### docs-reviewer
Audits documentation and code comments for accuracy against recent code changes. Compares docs to code, producing a report of required updates without modifying files. Only reports issues with high confidence -- verified discrepancies between documentation and actual code behavior.

**Codex approximation**: Use `shell_command` to diff docs against code changes, grep for references to changed APIs/functions in documentation files.

### context-file-adherence-reviewer
Verifies that code changes comply with context file (AGENTS.md) instructions and project standards. Focuses on outcome-based rules (code quality requirements) rather than workflow processes. Only reports violations with exact rule citations from the project context file.

**Codex approximation**: Use `shell_command` to read AGENTS.md and other context files, then compare changed code against stated rules. On Codex, AGENTS.md is automatically loaded as the project context file.

---

## Define Workflow Agents

### manifest-verifier
Reviews manifests produced by the `define` skill for gaps that would cause implementation failure or rework. Returns specific questions to ask and areas to probe so the interview can continue. Validates completeness of acceptance criteria, invariants, assumptions, and risk areas.

**Codex approximation**: Use `shell_command` to read the manifest file, then analyze its structure against the expected format. Report gaps via structured output.

### define-session-analyzer
Analyzes `define` session transcripts to extract user preference patterns -- what users push back on, consistently prefer, add unprompted, skip, or reject. These patterns become probing hints for future `define` sessions. Used by the `learn-define-patterns` skill.

**Codex approximation**: Use `shell_command` to read JSONL session files, then write analysis results. This is the only agent that requires write access (`sandbox_mode = "workspace-write"`).

---

## How to Use on Codex CLI

1. **Installed skills are namespaced** -- Use `$define-manifest-dev`, `$do-manifest-dev`, `$verify-manifest-dev`, `$done-manifest-dev`, `$escalate-manifest-dev`, `$auto-manifest-dev`, and `$learn-define-patterns-manifest-dev` via the Agent Skills Open Standard
2. **Multi-agent system** -- Enable with `[features] multi_agent = true` in `.codex/config.toml`. TOML stubs in `agents/` configure per-role behavior.
3. **Review agents are read-only** -- All review agents use `sandbox_mode = "read-only"` to prevent accidental modifications
4. **Spawn agents by role** -- When multi-agent is enabled, Codex can spawn agents with specific roles matching the TOML config names (e.g., `code-bugs-reviewer-manifest-dev`)
5. **Default tools available** -- All agents have access to 6 default tools: `shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`
6. **Experimental tools** -- `read_file`, `list_dir`, `grep_files` may also be available depending on model configuration
