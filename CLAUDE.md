# CLAUDE.md

## Project Overview

Manifest-dev marketplace - manifest-driven development workflows for Claude Code. Front-load the thinking so AI agents get it right the first time.

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

Read before modifying the plugin:

- **@docs/CUSTOMER.md** - Who we build for, messaging guidelines
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design
- **docs/PROMPTING.md** - First-principles prompting derived from LLM training

## Repository Structure

- `.claude-plugin/marketplace.json` - Marketplace registry (single plugin)
- `claude-plugins/manifest-dev/` - The manifest-dev plugin
- `docs/` - Foundational documents
- `tests/` - Test suite
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

### Plugin Components

The manifest-dev plugin contains:
- `agents/` - Specialized agent definitions (markdown)
- `skills/` - Skills with `SKILL.md` files
- `hooks/` - Event handlers for Claude Code events
- `tests/hooks/` - Test suite for hooks (at repo root)

**Naming convention**: Use kebab-case (`-`) for all file and skill names (e.g., `code-bugs-reviewer.md`, `define`).

### Hooks

Hooks are Python scripts in `hooks/` that respond to Claude Code events. Shared utilities live in `hook_utils.py`.

**Hook structure**:
- `hook_utils.py` - Shared transcript parsing, skill invocation detection
- `stop_do_hook.py` - Blocks premature stops during /do workflow
- `pretool_escalate_hook.py` - Gates /escalate calls to require /verify first

**When modifying hooks**:
1. Run tests: `pytest tests/hooks/ -v`
2. Run linting: `ruff check --fix claude-plugins/manifest-dev/hooks/ && black claude-plugins/manifest-dev/hooks/`
3. Run type check: `mypy claude-plugins/manifest-dev/hooks/`

**Test coverage**: Tests in `tests/hooks/` cover edge cases (invalid JSON, missing files, malformed transcripts), workflow detection, and hook output format. Add tests for any new hook logic.

### Skills

Skills are the primary way to extend Claude Code. Each skill lives in `skills/{skill-name}/SKILL.md`.

**Invocation modes**:
- **Auto-invoked**: Claude discovers and invokes skills based on semantic matching with the description
- **User-invoked**: Users can explicitly invoke via `/skill-name` (controlled by `user-invocable` frontmatter, defaults to `true`)
- **Programmatic**: Other skills can invoke skills by referencing them (e.g., "invoke the verify skill with arguments")

**Skill frontmatter**:
```yaml
---
name: skill-name           # Required: lowercase, hyphens, max 64 chars
description: '...'         # Required: max 1024 chars, drives auto-discovery
user-invocable: true       # Optional: show in slash command menu (default: true)
---
```

### Writing and Updating Prompts

Follow the principles in `docs/PROMPTING.md` for all prompt work - crafting new prompts, updating existing ones, or reviewing prompt structure.

### Tool Definitions

**Skills**: Omit `tools` frontmatter to inherit all tools from the invoking context (recommended default).

**Agents**: MUST explicitly declare all needed tools in frontmatter - agents run in isolation and won't inherit tools.

### Invoking Skills from Skills

When a skill needs to invoke another skill, use clear directive language:

```markdown
Invoke the manifest-dev:<skill> skill with: "<arguments>"
```

Examples:
- `Invoke the manifest-dev:verify skill with: "$MANIFEST_PATH"`
- `Invoke the manifest-dev:escalate skill with: "AC-5 blocking"`

**Why**: Vague language like "consider using the X skill" is ambiguous - Claude may just read the skill file instead of invoking it. Clear directives like "Invoke the X skill" ensure the skill is actually called.

## Plugin Versioning

When updating plugin files, bump version in `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new skills/agents
- **Major** (x.0.0): Breaking changes

README-only changes don't require version bumps.

**After version bump**: Add entry to `CHANGELOG.md`:
```
## YYYY-MM-DD
- [manifest-dev] vX.Y.Z - Brief description of change
```

## Adding New Components

When adding agents, skills, or hooks:
1. Create the component file in the appropriate directory
2. Bump plugin version (minor for new features)
3. Update affected `README.md` files
4. Update `plugin.json` description/keywords if the new component adds significant capability

## Before PR

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Run hook tests if hooks were modified
pytest tests/hooks/ -v
```

Bump plugin version if plugin files changed.
