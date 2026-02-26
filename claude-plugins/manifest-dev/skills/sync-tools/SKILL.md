---
name: sync-tools
description: 'Generate multi-CLI distribution packages from the Claude Code plugin. Converts skills, agents, and hooks for Gemini CLI, OpenCode, and Codex CLI under dist/. Run after changing plugin components to keep distributions in sync.'
user-invocable: true
---

# /sync-tools — Multi-CLI Distribution Generator

Generate distribution packages for Gemini CLI, OpenCode, and Codex CLI from the Claude Code plugin source of truth.

**Input**: `$ARGUMENTS` — optional CLI name (gemini, opencode, codex) to sync a single target. Empty = sync all three.

## Source and Output

- **Source** (read-only): `claude-plugins/manifest-dev/` — skills, agents, hooks
- **Output**: `dist/{gemini,opencode,codex}/` — per-CLI distributions
- **Reference files**: `claude-plugins/manifest-dev/skills/sync-tools/references/{gemini,opencode,codex}-cli.md`

Never modify files under `claude-plugins/manifest-dev/`. Only write to `dist/`.

## Per-CLI Processing

For each target CLI, read the corresponding reference file in `references/`. The reference file contains the complete conversion rules: tool name mappings, frontmatter format, hook protocol differences, directory structure, installation commands, and known limitations.

### Phase 1: Skills

Copy all skill directories from `claude-plugins/manifest-dev/skills/` to the CLI's dist output. SKILL.md files are copied **unchanged** — the Agent Skills Open Standard ensures universal compatibility. Copy subdirectories (scripts/, references/, assets/, tasks/) recursively.

Exception: skip the `sync-tools` skill itself — it's a meta-tool, not useful on other CLIs.

### Phase 2: Agents

Read each agent file from `claude-plugins/manifest-dev/agents/`. Convert frontmatter per the reference file's conversion rules. Keep the prompt body (everything below frontmatter) unchanged.

- **Gemini CLI**: Convert tool names, add required fields (name, kind, model, temperature, max_turns, timeout_mins). Write to `dist/gemini/agents/`.
- **OpenCode**: Convert tools array to boolean object with lowercase names, add mode: subagent. Write to `dist/opencode/agents/`.
- **Codex CLI**: Agents are incompatible. Instead, generate a single `AGENTS.md` describing all agents (name, description, purpose, tools used). Write to `dist/codex/AGENTS.md`.

If an agent declares a tool not in the reference file's mapping table, log a warning and pass the tool name through unchanged (the target CLI will ignore unknown tools gracefully).

### Phase 3: Hooks

Read each hook file from `claude-plugins/manifest-dev/hooks/`. Adapt per the reference file's protocol.

- **Gemini CLI**: Generate adapted Python hooks with the JSON output format adapter described in the reference file. Map hook event names and tool name matchers per the reference. Write to `dist/gemini/hooks/` with a `hooks.json` configuration file.
- **OpenCode**: Hooks require JS/TS rewrite (not automatable). Generate: (1) a hook stub file (`dist/opencode/hooks/index.ts`) with correct OpenCode plugin structure and event bindings, (2) a behavioral spec (`dist/opencode/hooks/HOOK_SPEC.md`) documenting what each hook does, what events it responds to, and what decisions it makes.
- **Codex CLI**: No hooks possible. Skip entirely — document in README.

Skip `hook_utils.py` shared utilities — inline relevant logic into adapted hooks or include as a helper file.

### Phase 4: Per-CLI README

Generate a README.md for each CLI in `dist/{cli}/README.md` containing:

1. What this distribution contains and what's included/excluded
2. Installation instructions specific to this CLI (from reference file)
3. Feature parity table: what works fully, what works with limitations, what's missing and WHY
4. Any required configuration (e.g., Gemini's experimental.enableAgents flag)
5. Link back to the main repo for Claude Code users

### Phase 5: CLI-Specific Extras

- **Gemini CLI**: Generate `dist/gemini/gemini-extension.json` manifest with name, version, description.
- **OpenCode**: No extras needed.
- **Codex CLI**: No extras needed.

## Progress Logging

Create a log at `/tmp/sync-tools-{timestamp}.md`. After completing each CLI, append:
- Which CLI was processed
- Number of skills, agents, hooks processed
- Any warnings (unmapped tools, skipped components, errors)
- Summary of what was generated

Read the full log before writing the final summary output.

## Edge Cases

- **Skills with subdirectories** (define/ has tasks/, sync-tools/ has references/): copy the entire skill directory tree recursively.
- **Agent with tools not in mapping table**: log warning, pass through unchanged.
- **Empty component sets** (Codex has no hooks): skip gracefully, note in README.
- **hook_utils.py**: shared utility — Gemini hooks may need inlined logic from it. Read hook_utils.py to understand what functions the hooks import, then include relevant code in the adapted hooks.

## Output Summary

After all CLIs are processed, output a summary table:

| CLI | Skills | Agents | Hooks | Status |
|-----|--------|--------|-------|--------|
| Gemini | N copied | N converted | N adapted | Complete |
| OpenCode | N copied | N converted | stubs only | Complete |
| Codex | N copied | AGENTS.md | none | Complete |
