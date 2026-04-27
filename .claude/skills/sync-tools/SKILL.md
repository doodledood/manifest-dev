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
| Per-CLI sync state | `dist/{cli}/.sync-meta.json` (records last-synced source SHA — drives diff-first workflow) |
| GitHub repo | `doodledood/manifest-dev` |

## Scope

Only sync `claude-plugins/manifest-dev/`. Never sync other plugins (e.g., `manifest-dev-collab` — uses Agent Teams/Slack, inherently incompatible). Never modify source files. Skip `sync-tools` skill from output (meta-tool).

## Per-CLI Processing

For each target CLI, read its reference file first. The reference file is **the single source of truth** for conversion rules — tool name mappings, frontmatter format, hook protocol, directory structure, and limitations. Do not duplicate conversion logic here; follow the reference.

### Diff-first sync (preferred)

Each `dist/{cli}/.sync-meta.json` records the source commit that dist was last synced from:

```json
{
  "source_commit": "<sha>",
  "source_path": "claude-plugins/manifest-dev",
  "synced_at": "<ISO 8601 UTC>"
}
```

On invocation, prefer a delta sync over a full re-sync:

1. Read `dist/{cli}/.sync-meta.json`. If missing, malformed, or the recorded SHA is unreachable from `HEAD` (e.g., rebased away, force-pushed branch), **fall back to full sync** for that CLI.
2. **Force full sync** if any of the following changed between recorded SHA and `HEAD` (these define the substitution rules — any change can affect every dist file):
   - `.claude/skills/sync-tools/SKILL.md`
   - `.claude/skills/sync-tools/references/{cli}-cli.md`
3. Otherwise compute `git diff --name-status <recorded-sha>..HEAD -- claude-plugins/manifest-dev/` and process each entry:
   - **Added / Modified**: re-apply per-CLI substitutions, write to dist counterpart
   - **Deleted**: remove dist counterpart (and parent dir if now empty)
   - **Renamed**: handle as delete-old + add-new
4. Recompute README component tables and the CLI's context file (`GEMINI.md` / `AGENTS.md`) only if the set of skills/agents changed (added/removed/renamed). Body-only edits don't require regenerating these.
5. After all writes succeed, overwrite `dist/{cli}/.sync-meta.json` with the new HEAD sha and a fresh `synced_at` UTC timestamp. Keep the file even when the diff was empty — the timestamp records "we checked".

The metadata is an **optimization, not a correctness anchor**. When in doubt — unreachable commit, ambiguous rename, mid-rebase repo state, suspicious dist drift — fall back to full sync rather than trusting the recorded SHA.

### Per-component goals

| Component | Goal |
|-----------|------|
| **Skills** | Copy unchanged (Agent Skills Open Standard = universal). Include all subdirectories. Replace operational CLAUDE.md references (e.g., "write to CLAUDE.md") with CLI context file name per reference file. Leave research/reference content unchanged. **Exception 1**: files in `references/execution-modes/` — replace Claude-specific model names (haiku, sonnet, opus) with `inherit`. Model tier routing is Claude Code-only; other CLIs use session model for all tiers. **Exception 2**: lines that surface a session-file path to the user (e.g. `Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl`, "Session JSONL files live at ...") — retarget per the reference file's "Session File Adaptation" section. If the target CLI has no per-session file the agent can locate at runtime, omit the line. |
| **Agents** | Convert frontmatter per reference file. Keep prompt body as identical as possible to Claude Code original — categories, actionability filters, severity guidelines, output formats, out-of-scope sections are the core value. Only change: frontmatter format, namespace suffix, context file name (CLAUDE.md → CLI name per reference file), genuinely unsupported features (document as limitation, don't remove). |
| **Hooks** | Adapt to the target hook protocol per reference file. Generate complete, installable hook/plugin payloads. Document unavoidable runtime gaps, but do not ship stubs or require manual post-install wiring. |
| **Commands** | Generate command files from user-invocable skills (`user-invocable: true`, the default). Per reference file. |
| **Context file** | Workflow overview + agent descriptions in the CLI's native context format per reference file. |
| **README** | Component table, install instructions, feature parity table, required config, link to GitHub repo. |
| **Install script** | `install.sh` and `install_helpers.py` are **infrastructure files** — update incrementally, never regenerate. They contain logic not derivable from source (piped execution detection, temp dir cloning, cleanup traps, argument parsing, settings merging). Only modify sections that reflect changed components (step counts, file lists, component names). |
| **CLI extras** | Extension manifests, plugin configs, execution rules — per reference file. |

### README install section

Remote install (no clone needed) must be the primary method. Use the repo from the Paths table with the standard skills installer (`npx skills add`). Include CLI-native install methods from the reference file as alternatives. Full distribution install via `install.sh` as secondary.

### Install script constraints

- **Incremental updates only**: `install.sh` and `install_helpers.py` are maintained infrastructure — read existing content, modify only what changed. Never rewrite from scratch. Regression risk: infrastructure logic (piped `curl | bash` support, trap handlers, argument parsing) is invisible to component-level sync and will be lost on regeneration.
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
| `install.sh` and `install_helpers.py` are infrastructure — update incrementally, never regenerate | These contain manually-added logic (piped execution, traps, arg parsing) not derivable from source. Regeneration causes silent regressions. |
| Frontmatter conversion must work in both bash and zsh | macOS default shell is zsh; bash-only constructs break |
| Reference files are authoritative for conversion rules | Avoids two sources of truth — update one place |
| Unmapped agent tools pass through unchanged | Target CLI ignores unknown tools gracefully |
| Empty component sets skip gracefully | Codex has no hooks — note in README, don't error |
| Agent/skill prompt bodies stay faithful to Claude Code originals | Prompts are carefully crafted — don't simplify, rewrite, or truncate for other CLIs |
| Always update `dist/{cli}/.sync-meta.json` at end of run | The recorded SHA is what next run's diff-first path keys on. Skipping the update silently degrades future syncs to full re-syncs. |

## Progress Log

Write to `/tmp/sync-tools-{timestamp}.md` after each CLI: counts, warnings, what was generated. Read the full log before writing the final summary.

## Output

Summary table after all CLIs processed:

| CLI | Skills | Agents | Hooks | Commands | Status |
|-----|--------|--------|-------|----------|--------|
| Gemini | N | N converted | N adapted | — | Complete |
| OpenCode | N | N converted | N adapted | N | Complete |
| Codex | N | AGENTS.md + N TOML | none | — | Complete |
