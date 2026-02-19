# GEMINI.md

## Project Overview

manifest-dev marketplace -- verification-first manifest workflows for Gemini, with agents, skills, and hooks. This is a Gemini-optimized version of the manifest-dev framework.

## Development Commands

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Test hooks (run after ANY hook changes)
pytest tests/hooks/ -v

# Test Gemini extension locally
# (Placeholder for Gemini-specific testing commands)
```

## Foundational Documents

Read before building extensions:

- **@docs/CUSTOMER.md** - Who we build for, messaging guidelines
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design
- **@docs/PROMPTING.md** - First-principles prompting.

## Repository Structure

- `gemini-extension.json` - Configuration for Gemini extensions
- `claude-plugins/` - Individual plugins/extensions (initially sharing the same structure)

### Extension Components

Each extension can contain:
- `agents/` - Specialized agent definitions (markdown)
- `skills/` - Skills with `SKILL.md` files
- `hooks/` - Event handlers

## Naming Convention
Use kebab-case (`-`) for all file and skill names.

## Before PR

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Run hook tests if hooks were modified
pytest tests/hooks/ -v
```
