---
name: sync-tools
description: 'Generate multi-CLI distribution packages from the Claude Code plugin. Converts skills, agents, and hooks for Gemini CLI, OpenCode, and Codex CLI under dist/. Run after changing plugin components to keep distributions in sync.'
user-invocable: true
---

# /sync-tools — Multi-CLI Distribution Generator

Generate distribution packages for Gemini CLI, OpenCode, and Codex CLI from the Claude Code plugin.

**Input**: `$ARGUMENTS` — optional CLI name (gemini, opencode, codex) to sync one target. Empty = all three.

## Paths

| Role | Path |
|------|------|
| Source (read-only) | `claude-plugins/manifest-dev/` |
| Output | `dist/{gemini,opencode,codex}/` |
| Conversion rules | `.claude/skills/sync-tools/references/{cli}-cli.md` |
| GitHub repo | `doodledood/manifest-dev` |

## Scope

Only sync `claude-plugins/manifest-dev/`. Never sync other plugins (e.g., `manifest-dev-collab` — uses Agent Teams/Slack, inherently incompatible). Never modify source files. Skip `sync-tools` skill from output (meta-tool).

## Per-CLI Processing

For each target CLI, read its reference file first. The reference file is **the single source of truth** for conversion rules — tool name mappings, frontmatter format, hook protocol, directory structure, and limitations. Do not duplicate conversion logic here; follow the reference.

### Per-component goals

| Component | Goal |
|-----------|------|
| **Skills** | Copy unchanged (Agent Skills Open Standard = universal). Include all subdirectories. Replace operational CLAUDE.md references (e.g., "write to CLAUDE.md") with CLI context file name per reference file. Leave research/reference content unchanged. **Exception**: files in `references/execution-modes/` — replace Claude-specific model names (haiku, sonnet, opus) with `inherit`. Model tier routing is Claude Code-only; other CLIs use session model for all tiers. |
| **Agents** | Convert frontmatter per reference file. Keep prompt body as identical as possible to Claude Code original — categories, actionability filters, severity guidelines, output formats, out-of-scope sections are the core value. Only change: frontmatter format, namespace suffix, context file name (CLAUDE.md → CLI name per reference file), genuinely unsupported features (document as limitation, don't remove). |
| **Hooks** | Adapt to the target hook protocol per reference file. Generate complete, installable hook/plugin payloads. Document unavoidable runtime gaps, but do not ship stubs or require manual post-install wiring. |
| **Commands** | Generate command files from user-invocable skills (`user-invocable: true`, the default). Per reference file. |
| **Context file** | Workflow overview + agent descriptions in the CLI's native context format per reference file. |
| **README** | Component table, install instructions, feature parity table, required config, link to GitHub repo. |
| **Install script** | Idempotent `install.sh` that copies all components to the CLI's standard locations. |
| **CLI extras** | Extension manifests, plugin configs, execution rules — per reference file. |

### README install section

Remote install (no clone needed) must be the primary method. Use the repo from the Paths table with the standard skills installer (`npx skills add`). Include CLI-native install methods from the reference file as alternatives. Full distribution install via `install.sh` as secondary.

### Install script constraints

- Idempotent (safe to re-run for updates)
- Never overwrite user-owned shared entrypoints or config files; merge shared config additively
- Only replace installer-managed namespaced files or extension-private files owned by this distribution
- Full setup must complete from `install.sh` alone; no required manual follow-up steps
- Install scripts namespace all components with `-manifest-dev` suffix at install time via `install_helpers.py`
- Selective cleanup: delete only `*-manifest-dev*` files/dirs, never `rm -rf` shared directories
- `dist/` keeps original names; namespacing is an install-time concern

## Constraints

| Constraint | Why |
|-----------|-----|
| Frontmatter conversion must work in both bash and zsh | macOS default shell is zsh; bash-only constructs break |
| Reference files are authoritative for conversion rules | Avoids two sources of truth — update one place |
| Unmapped agent tools pass through unchanged | Target CLI ignores unknown tools gracefully |
| Empty component sets skip gracefully | Codex has no hooks — note in README, don't error |
| Agent/skill prompt bodies stay faithful to Claude Code originals | Prompts are carefully crafted — don't simplify, rewrite, or truncate for other CLIs |

## Progress Log

Write to `/tmp/sync-tools-{timestamp}.md` after each CLI: counts, warnings, what was generated. Read the full log before writing the final summary.

## Output

Summary table after all CLIs processed:

| CLI | Skills | Agents | Hooks | Commands | Status |
|-----|--------|--------|-------|----------|--------|
| Gemini | N | N converted | N adapted | — | Complete |
| OpenCode | N | N converted | N adapted | N | Complete |
| Codex | N | AGENTS.md + N TOML | none | — | Complete |
