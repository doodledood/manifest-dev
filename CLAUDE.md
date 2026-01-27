# CLAUDE.md

## Project Overview

manifest-dev marketplace -- verification-first manifest workflows for Claude Code, with agents, skills, and hooks.

## Development Commands

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Test hooks (run after ANY hook changes)
pytest tests/hooks/ -v

# Test plugin locally
/plugin marketplace add /path/to/manifest-dev
/plugin install manifest-dev@manifest-dev-marketplace
```

## Foundational Documents

Read before building plugins:

- **@docs/CUSTOMER.md** - Who we build for, messaging guidelines
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

### Plugin Components

Each plugin can contain:
- `agents/` - Specialized agent definitions (markdown)
- `skills/` - Skills with `SKILL.md` files (replaces deprecated commands)
- `hooks/` - Event handlers for Claude Code events
- `tests/hooks/` - Test suite for hooks (at repo root)

**Naming convention**: Use kebab-case (`-`) for all file and skill names (e.g., `bug-fixer.md`, `clean-slop`).

### Hooks

Hooks are Python scripts in `hooks/` that respond to Claude Code events. Shared utilities live in `hook_utils.py`.

**Hook structure** (manifest-dev):
- `hook_utils.py` - Shared transcript parsing for skill invocation detection
- `stop_do_hook.py` - Blocks premature stops during /do workflow when verification incomplete
- `pretool_escalate_hook.py` - Gates /escalate calls, requires /verify before escalation

**When modifying hooks**:
1. Run tests: `pytest tests/hooks/ -v`
2. Run linting: `ruff check --fix claude-plugins/manifest-dev/hooks/ && black claude-plugins/manifest-dev/hooks/`
3. Run type check: `mypy claude-plugins/manifest-dev/hooks/`

**Test coverage**: Tests in `tests/hooks/` cover edge cases (invalid JSON, missing files, malformed transcripts), workflow detection, todo state extraction, and hook output format. Add tests for any new hook logic.

### Skills

Skills are the primary way to extend Claude Code. Each skill lives in `skills/{skill-name}/SKILL.md`.

**Invocation modes**:
- **Auto-invoked**: Claude discovers and invokes skills based on semantic matching with the description
- **User-invoked**: Users can explicitly invoke via `/skill-name` (controlled by `user-invocable` frontmatter, defaults to `true`)
- **Programmatic**: Other skills can invoke skills by referencing them (e.g., "invoke the spec skill with arguments")

**Skill frontmatter**:
```yaml
---
name: skill-name           # Required: lowercase, hyphens, max 64 chars
description: '...'         # Required: max 1024 chars, drives auto-discovery
user-invocable: true       # Optional: show in slash command menu (default: true)
---
```

### Tool Definitions

**Skills**: Omit `tools` frontmatter to inherit all tools from the invoking context (recommended default).

**Agents**: MUST explicitly declare all needed tools in frontmatter -- agents run in isolation and won't inherit tools.

### Invoking Skills from Skills

When a skill needs to invoke another skill, use clear directive language:

```markdown
Invoke the <plugin>:<skill> skill with: "<arguments>"
```

Examples:
- `Invoke the manifest-dev:define skill with: "$ARGUMENTS"`
- `Invoke the manifest-dev:verify skill`

**Why**: Vague language like "consider using the X skill" is ambiguous -- Claude may just read the skill file instead of invoking it. Clear directives like "Invoke the X skill" ensure the skill is actually called.

**Common agent capabilities to declare in frontmatter**:
- Running commands -> needs command execution tools
- Tracking progress -> needs todo/task management tools
- Writing files (logs, notes) -> needs file writing tools
- Invoking other skills -> needs skill invocation tools
- Spawning sub-agents -> needs agent spawning tools
- Searching files -> needs file search tools

**Agent audit**: Read the skill/prompt the agent follows, identify every capability mentioned (explicit or implicit), verify all are declared in frontmatter.

See each plugin's README for architecture details.

## Plugin Versioning

When updating plugin files, bump version in `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new skills/agents
- **Major** (x.0.0): Breaking changes

README-only changes don't require version bumps.

## Adding New Components

When adding agents, skills, or hooks:
1. Create the component file in the appropriate directory
2. Bump plugin version (minor for new features)
3. Update affected plugin's `README.md` and repo root `README.md`
4. Update `plugin.json` description/keywords if the new component adds significant capability

**README sync checklist** (when adding/renaming/removing components):
- `README.md` (root) - Available Plugins section, directory structure
- `claude-plugins/README.md` - Plugin table
- `claude-plugins/<plugin>/README.md` - Component lists

**README Guidelines**: Keep READMEs high-level (overview, what it does, how to use). Avoid implementation details that require frequent updates -- readers can explore code for specifics.

## Before PR

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Run hook tests if hooks were modified
pytest tests/hooks/ -v
```

Bump plugin version if plugin files changed.
