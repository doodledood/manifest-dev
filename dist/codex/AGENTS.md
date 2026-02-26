# manifest-dev Agents

These agents are part of the manifest-dev verification-first workflow. They run as scoped subagents in Claude Code and Gemini CLI, with converted versions available for OpenCode.

Codex CLI uses a fundamentally different agent system (TOML config, 2 tools: shell + apply_patch) that is incompatible with these markdown agents (YAML frontmatter, 9+ named tools). The descriptions below are provided for reference when using the manifest workflow skills.

## claude-md-adherence-reviewer

Verify that code changes comply with CLAUDE.md instructions and project standards. Audits pull requests, new code, and refactors against rules defined in CLAUDE.md files. Use after implementing features, before PRs, or when validating adherence to project-specific rules. Triggers: CLAUDE.md compliance, project standards, adherence check.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a read-only CLAUDE.md compliance auditor. Your mission is to audit code changes for violations of project-specific instructions defined in CLAUDE.md files, reporting only verifiable violations with exact rule citations.


## code-bugs-reviewer

Audit code changes for logical bugs without modifying files. Use when reviewing git diffs, checking code before merge, or auditing specific files for defects. Produces a structured bug report with severity ratings. Triggers: bug review, audit code, check for bugs, review changes, pre-merge check.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a read-only bug auditor. Your sole output is a structured bug report identifying logical defects in code changes. You never modify repository files.


## code-coverage-reviewer

Verify that code changes have adequate test coverage. Analyzes the diff between current branch and main, identifies logic changes, and reports coverage gaps with specific recommendations. Use after implementing a feature, before a PR, or when reviewing code quality. Triggers: check coverage, test coverage, coverage gaps, are my changes tested.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a read-only test coverage reviewer. Your mission is to analyze code changes and verify that new/modified logic has adequate test coverage, reporting gaps with actionable recommendations.


## code-design-reviewer

Audit code for design fitness issues — whether code is the right approach given what already exists in the framework, codebase, and configuration systems. Identifies reinvented wheels, misplaced responsibilities, under-engineering, short-sighted interfaces, concept misuse, and incoherent changes. Use after implementing a feature, before a PR, or when code feels like the wrong approach despite being correct.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a read-only design fitness auditor. Your mission is to find code where the approach is wrong given what already exists — the right answer built the wrong way, responsibilities in the wrong system, or changes that don't hold together as a unit.


## code-maintainability-reviewer

Use this agent when you need a comprehensive maintainability audit of recently written or modified code. Focuses on code organization: DRY violations, coupling, cohesion, consistency, dead code, and architectural boundaries. This agent should be invoked after implementing a feature, completing a refactor, or before finalizing a pull request.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a Code Maintainability Architect. Your mission is to audit code for maintainability issues and produce actionable reports.


## code-simplicity-reviewer

Audit code for unnecessary complexity, over-engineering, and cognitive burden. Identifies solutions more complex than the problem requires — not structural issues like coupling or DRY (handled by maintainability-reviewer), but implementation complexity that makes code harder to understand than necessary. Use after implementing a feature, before a PR, or when code feels over-engineered.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a read-only simplicity auditor. Your mission is to find code where implementation complexity exceeds problem complexity — catching over-engineering, premature optimization, and cognitive burden before they accumulate.


## code-testability-reviewer

Audit code for testability issues. Identifies code requiring excessive mocking, business logic buried in IO, non-deterministic inputs, and tight coupling that makes verification hard. Use after implementing features, during refactoring, or before PRs. Triggers: testability, hard to test, too many mocks, testable design.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a read-only testability auditor. Your mission is to identify code where important logic is difficult to verify in isolation — requiring excessive mocking, entangled with IO, or dependent on non-deterministic inputs — and suggest ways to reduce test friction.


## criteria-checker

Read-only verification agent. Validates a single criterion using any automated method: commands, codebase analysis, file inspection, reasoning, web research. Returns structured PASS/FAIL results.

**Tools (Claude Code)**: Bash, Read, Glob, Grep, WebFetch, WebSearch

**Summary**: Verify a SINGLE criterion from a Manifest. You are READ-ONLY—check, don't modify. Spawned by /verify in parallel.


## docs-reviewer

Audit documentation and code comments for accuracy against recent code changes. Performs read-only analysis comparing docs to code, producing a report of required updates without modifying files. Use after implementing features, before PRs, or when validating doc accuracy. Triggers: docs review, documentation audit, stale docs check.

**Tools (Claude Code)**: Bash, BashOutput, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, Skill

**Summary**: You are a read-only documentation auditor. Your mission is to identify documentation and code comments that have drifted from the code and report exactly what needs updating.


## manifest-verifier

Reviews /define manifests for gaps and outputs actionable continuation steps. Returns specific questions to ask and areas to probe so interview can continue.

**Tools (Claude Code)**: Read, Grep, Glob

**Summary**: Find gaps in the manifest that would cause implementation failure or rework. Output actionable questions to continue the interview.


## type-safety-reviewer

Audit code for type safety issues across typed languages (TypeScript, Python, Java/Kotlin, Go, Rust, C#). Identifies type holes that let bugs through, opportunities to make invalid states unrepresentable, and ways to push runtime checks into compile-time guarantees. Use when reviewing type safety, strengthening types before a PR, or auditing code for type holes.

**Tools (Claude Code)**: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill

**Summary**: You are a read-only type safety auditor. Your mission is to audit code for type safety issues — pushing as many potential bugs as possible into the type system while balancing correctness with practicality.

