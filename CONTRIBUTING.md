# Contributing to manifest-dev

Thank you for your interest in contributing! This guide covers development of the manifest-dev plugin.

## Quick Start

1. **Fork and clone** the repository
2. **Create a branch**: `git checkout -b your-feature`
3. **Develop** following the structure below
4. **Test locally** before submitting
5. **Submit a PR**

## Plugin Structure

```
claude-plugins/manifest-dev/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata and hooks config
├── agents/                  # Agent definitions (markdown)
├── hooks/                   # Python event handlers
│   ├── hook_utils.py        # Shared utilities
│   ├── stop_do_hook.py      # Stop enforcement
│   ├── pretool_escalate_hook.py  # Escalation gating
│   └── pyproject.toml       # Hook package config
└── skills/                  # Skills with SKILL.md files
    ├── define/              # Manifest builder
    ├── do/                  # Manifest executor
    ├── verify/              # Verification runner
    ├── done/                # Completion summary
    └── escalate/            # Structured escalation
```

## Adding Components

### Skills

Create `skills/{skill-name}/SKILL.md` with frontmatter:

```yaml
---
name: skill-name
description: 'Clear description (max 1024 chars)'
user-invocable: true
---
```

### Agents

Create `agents/{agent-name}.md` with frontmatter:

```yaml
---
description: What this agent does
tools: [Bash, Read, Write, Grep, Glob]
---
```

Agents MUST declare all needed tools explicitly.

### Hooks

Add Python scripts to `hooks/`. Update `plugin.json` hooks section. Write tests in `tests/hooks/`.

## Testing

```bash
# Run hook tests
pytest tests/hooks/ -v

# Lint and format
ruff check --fix claude-plugins/ && black claude-plugins/

# Type check
mypy
```

## Pre-Submission Checklist

- [ ] Plugin version bumped in `plugin.json`
- [ ] CHANGELOG.md updated
- [ ] Hook tests pass (if hooks modified)
- [ ] Linting and type checks pass
- [ ] README.md updated if components added/removed
- [ ] No sensitive information (API keys, secrets)
- [ ] Naming follows kebab-case convention

## Pull Request Process

1. **Title**: Brief description of change
2. **Description**: What changed, why, how to test
3. **Review**: Maintainers test functionality and provide feedback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
