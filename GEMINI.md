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
# The repo includes a `gemini-extension.json` and root-level `skills/` and
# `hooks/` directories (symlinks) so Gemini tools that support extensions can
# discover agents, skills, and hooks without custom paths.
#
# Example workflow (adjust to your Gemini CLI/tooling):
#
# From repo root
# 1) Add/refresh this extension in your Gemini tool
#    (replace with your CLI's extension install command)
#    e.g.: gemini extensions add .
#
# 2) Start a new session and invoke the skills by name
#    e.g., run the Define → Do → Verify loop
#    gemini run "Use define to create a manifest for <task>"
#    gemini run "Use do with ./manifest.md and write logs to ./manifest.log"
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

## Notes
- The `directories` in `gemini-extension.json` point to `claude-plugins` (for plugin-style content) and `hooks`/`tests` at the repo root. The root-level `hooks` symlink points at `claude-plugins/manifest-dev/hooks`.
- If your CLI expects a different command surface, map the skills 1:1: `define`, `do`, `verify`, `done`, `escalate`.
