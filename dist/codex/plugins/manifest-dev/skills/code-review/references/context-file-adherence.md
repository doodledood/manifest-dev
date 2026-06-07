# Context-file-adherence review

Audit the change for violations of project-specific instructions defined in context files (CLAUDE.md / AGENTS.md) and project standards, reporting only verifiable violations with exact rule citations.

**The bar for every finding: "I am confident this IS a violation and can quote the exact rule being broken."** If you find yourself thinking "this might violate" or "this could be interpreted as", do NOT report it.

## Discover and load the context files at review time

Context files provide project-specific instructions to AI coding agents. They are named differently per CLI: **CLAUDE.md** (Claude Code) or **AGENTS.md** (Codex, OpenCode). You MUST discover and read the applicable context file(s) for the current CLI before auditing — the rules to enforce live there, not in this reference.

These files may already be loaded into your context by the parent framework. Check your context before reading files redundantly.

### Detecting the CLI

Determine which CLI you're running in to know which context file to prioritize:

| Signal | CLI | Primary context file |
|--------|-----|---------------------|
| `~/.codex/` directory exists | Codex CLI | `AGENTS.md` |
| `.opencode/` dir or `opencode.json` in project | OpenCode | `AGENTS.md` |
| Default (none of the above) | Claude Code | `CLAUDE.md` |

### Where to look (priority order per detected CLI)

- **Claude Code**: CLAUDE.md at project root → .claude/CLAUDE.md → .claude/rules/*.md → CLAUDE.local.md → ~/.claude/CLAUDE.md → directory-level CLAUDE.md files → @imports
- **Codex CLI**: ~/.codex/AGENTS.override.md → ~/.codex/AGENTS.md → AGENTS.override.md/AGENTS.md at each level from git root to CWD → configured fallbacks
- **OpenCode**: AGENTS.md traversing upward from CWD to git root → ~/.config/opencode/AGENTS.md → opencode.json instructions field

**Only audit against the context file for the CURRENT CLI.** Ignore stale context files from other CLIs (e.g., an unmaintained CLAUDE.md in a project that now uses Codex/AGENTS.md).

## Focus: outcome-based rules only

You review **code quality outcomes, not developer workflow processes.** Context files contain two types of instructions:

| Type | Description | Action |
|------|-------------|--------|
| **Outcome rules** | What the code/files should look like | **FLAG violations** |
| **Process rules** | How the developer should work | **IGNORE** |

- **Outcome rules** (FLAG): Naming conventions, required file structure/patterns, architecture constraints, required documentation in code.
- **Process rules** (IGNORE): Verification steps ("run tests before PR"), git workflow, workflow patterns, instructions about when to ask questions.

**The test**: Does the rule affect the FILES being committed? If yes, it's an outcome rule. If it only affects how you work, it's process.

These rule categories are guidance, not exhaustive. If you identify a context-file compliance issue that fits this dimension's domain but doesn't match a listed category, report it — just respect the out-of-scope boundaries below to maintain orthogonality.

## Actionability filter

Before reporting a violation, it must pass ALL of:

1. **Quotable rule** — You can quote the exact context-file text being broken and cite its source path. No quote, no finding.
2. **Outcome rule, not process** — The rule affects the files being committed, not how the developer works.
3. **Explicitly specified** — The naming convention, pattern, or documentation requirement is EXPLICITLY stated in a context file. General best practices belong to other dimensions, not here.
4. **Introduced by this change** — Flag violations in changed code, not pre-existing violations the change didn't introduce.
5. **Not silenced** — Skip issues explicitly silenced via comments (e.g., lint ignores) or trade-offs the change consciously documents.
6. **High confidence** — Only certain violations. An empty report beats uncertain findings.

## What NOT to flag

- **Process instructions** — workflow steps, git practices, verification checklists
- Subjective code quality concerns not explicitly in a context file
- Style preferences unless the context file mandates them
- Potential issues that "might" be problems
- Pre-existing violations not introduced by the current changes
- Issues explicitly silenced via comments (e.g., lint ignores)
- Violations where you cannot quote the exact rule being broken

## Out of scope (belongs to a sibling dimension)

Do NOT report on:

- **Intent-behavior divergence** (does the change achieve its goal?) → belongs to the change-intent dimension
- **Mechanical code defects** (race conditions, resource leaks, null handling) → belongs to the code-bugs dimension
- **API contract correctness** (wrong params, consumer breakage) → belongs to the contracts dimension
- **General maintainability** (not specified in context file) → belongs to the code-maintainability dimension
- **Over-engineering / complexity** (not specified in context file) → belongs to the code-simplicity dimension
- **Type safety** → belongs to the type-safety dimension
- **Documentation accuracy** (not specified in context file) → belongs to the docs dimension
- **Test coverage** → belongs to the test-quality dimension
- **Prose value / AI-tells in comments and doc files** (when not explicitly specified as a context-file rule) → belongs to the prose-value dimension

Only flag naming conventions, patterns, or documentation requirements EXPLICITLY specified in context files. General best practices belong to other dimensions.

**Cross-dimension boundary**: If a context file contains rules about code quality (e.g., "all functions must have tests"), only flag violations of the context-file rule itself. The underlying quality concern is owned by the appropriate specialized dimension.

## Severity calibration

- **Critical** — Violations that will break builds, deployments, or core functionality. Direct contradictions of explicit "MUST", "REQUIRED", or "OVERRIDE" instructions.
- **High** — Clear violations of explicit context-file requirements that don't break builds but deviate from mandated patterns. Wrong naming conventions, missing required code structure.
- **Medium** — Partial compliance with explicit multi-step requirements. Missing updates to related files when the context file explicitly states they should be updated together.
- **Low** — Minor deviations from explicitly stated style preferences. Violations of explicit rules with minimal practical impact.

**Calibration check**: Critical should be rare — only for build-breaking or explicit MUST/REQUIRED violations. If you're finding multiple Criticals, recalibrate.

## Dimension-specific report fields

Beyond the shared report skeleton, every finding for this dimension MUST cite the rule it breaks:

- **Violation**: clear explanation of what rule was broken
- **Context File Rule**: "<exact quote from the context file>"
- **Source**: path to the context file
- **Impact**: why this matters for the project
- **Recommended fix**: concrete change that brings the code into compliance

Every issue must reference exact context-file text with its file path — no source citation, no finding. Don't report the same violation under different names; if the PASS report is empty, full compliance is a valid and positive outcome — do not fabricate violations to fill it.
