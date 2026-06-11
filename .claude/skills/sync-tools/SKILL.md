---
name: sync-tools
description: 'Generate multi-CLI distribution packages from the Claude Code plugin. Converts shared skills, package assets, and runtime payloads for OpenCode, Codex CLI, and Pi under dist/. Run after changing plugin components to keep distributions in sync.'
user-invocable: true
---

# /sync-tools — Multi-CLI Distribution Generator

Generate distribution packages for OpenCode, Codex CLI, and Pi from the Claude Code plugin.

**Input**: `$ARGUMENTS` — optional CLI name (`opencode`, `codex`, `pi`) to sync one target. Empty = all targets.

## Paths

| Role | Path |
|------|------|
| Sources (read-only) | `claude-plugins/manifest-dev/` and `claude-plugins/manifest-dev-tools/` |
| Output | `dist/{opencode,codex,pi}/` |
| Conversion rules | `.claude/skills/sync-tools/references/{cli}-cli.md` |
| Per-CLI sync state | `dist/{cli}/.sync-meta.json` (records last-synced source SHA — drives diff-first workflow) |
| Pi namespace metadata | `dist/pi/component-namespaces.json` (component → owning plugin; Pi only) |
| GitHub repo | `doodledood/manifest-dev` |

## Scope

Sync only these source payloads:
- `claude-plugins/manifest-dev/` — core workflow skills.
- `claude-plugins/manifest-dev-tools/` — tools skills.

Both plugins are skills-only — manifest-dev ships no agents or hooks on any target (the former functional agents are skills).

Never sync other plugins (e.g., `manifest-dev-collab` — uses Agent Teams/Slack, inherently incompatible). Never modify source files. Skip `sync-tools` skill from output (meta-tool).

**Namespacing model is per-CLI** (see each reference file):
- **Plugin-native targets (Codex, OpenCode)**: the plugin is the distribution unit. Codex: two plugins (`manifest-dev`, `manifest-dev-tools`) each bundle their skills under original names. OpenCode: one plugin entry (`dist/opencode/plugin/`) registers the whole skills payload via `skills.paths`; skills keep bare names (native discovery is first-found-wins). No install-time suffixing, no `component-namespaces.json`, no installer. Plugin-qualified skill-reference handling (`manifest-dev:<skill>` — strip vs keep) is per-CLI: see each reference file.
- **Package target (Pi)**: each component carries plugin ownership in `component-namespaces.json` (ownership metadata — Pi keeps package-scoped skill names, no suffixing). Regenerate it on every sync from the discovered source components; never hand-maintain it.

## Per-CLI Processing

For each target CLI, read its reference file first. The reference file is **the single source of truth** for conversion rules — tool name mappings, frontmatter format, hook protocol, package shape, directory structure, and limitations. Do not duplicate conversion logic here; follow the reference.

### Diff-first sync (preferred)

Each `dist/{cli}/.sync-meta.json` records the source commit that dist was last synced from:

```json
{
  "source_commit": "<sha>",
  "source_path": "claude-plugins/manifest-dev",
  "source_paths": [
    "claude-plugins/manifest-dev",
    "claude-plugins/manifest-dev-tools"
  ],
  "synced_at": "<ISO 8601 UTC>"
}
```

On invocation, prefer a delta sync over a full re-sync:

1. Read `dist/{cli}/.sync-meta.json`. If missing, malformed, or the recorded SHA is unreachable from `HEAD` (e.g., rebased away, force-pushed branch), **fall back to full sync** for that CLI.
2. **Force full sync** if any of the following changed between recorded SHA and `HEAD` (these define the substitution rules — any change can affect every dist file):
   - `.claude/skills/sync-tools/SKILL.md`
   - `.claude/skills/sync-tools/references/{cli}-cli.md`
3. Otherwise compute `git diff --name-status <recorded-sha>..HEAD -- claude-plugins/manifest-dev/ claude-plugins/manifest-dev-tools/` and process each entry:
   - **Added / Modified**: re-apply per-CLI substitutions, write to dist counterpart
   - **Deleted**: remove dist counterpart (and parent dir if now empty)
   - **Renamed**: handle as delete-old + add-new
4. Recompute README component tables and the CLI's context file (`AGENTS.md`) only if the set of skills changed (added/removed/renamed). Body-only edits don't require regenerating these.
   - **OpenCode:** if `claude-plugins/manifest-dev/.claude-plugin/plugin.json`'s version changed between recorded SHA and `HEAD`, mirror it into `dist/opencode/plugin/package.json` per the reference file.
5. **Package target (Pi) only:** regenerate `dist/pi/component-namespaces.json` from the current dist component set and source ownership map. **Skip entirely for plugin-native Codex and OpenCode** — the plugin is the namespace there; generating namespace metadata would resurrect retired installer concepts.
6. After all writes succeed, overwrite `dist/{cli}/.sync-meta.json` with the new HEAD sha and a fresh `synced_at` UTC timestamp. Keep the file even when the diff was empty — the timestamp records "we checked".

The metadata is an **optimization, not a correctness anchor**. When in doubt — unreachable commit, ambiguous rename, mid-rebase repo state, suspicious dist drift — fall back to full sync rather than trusting the recorded SHA.

### Per-component goals

| Component | Goal |
|-----------|------|
| **Skills** | Copy unchanged (Agent Skills Open Standard = universal) from both source payloads. Include all subdirectories. Replace operational CLAUDE.md references (e.g., "write to CLAUDE.md") with CLI context file name per reference file. Replace operational tool-name references in skill body prose with the target CLI's names (e.g., "use the Read tool" → the target's read tool) — the mappings live in each reference file's tool-name lookup table. Leave research/reference content unchanged (teaching documents in `references/*.md` that explain Claude Code conventions stay Claude-Code-centric; only operational instructions remap). **Exception 1**: files in `references/execution-modes/` — replace Claude-specific model names (haiku, sonnet, opus) with `inherit`. Model tier routing is Claude Code-only; other CLIs use session model for all tiers. **Exception 2**: lines that surface a session-file path to the user (e.g. `Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl`, "Session JSONL files live at ...") — retarget per the reference file's session-line rule. If the target CLI has no per-session file the agent can locate at runtime, omit the line. |
| **Agents** | None shipped — manifest-dev has no agents on any target; the former functional agents are skills. Do not generate agent files. |
| **Hooks** | None shipped. If a future hook ships, adapt per the target's reference file — and re-derive that target's hook capability map first (the retired research is stale). |
| **Commands** | None shipped. Codex bundles skills without command shims; OpenCode lists every discovered skill as a slash command natively (≥ v1.1.48); Pi invokes `/skill:<name>` and registers runtime commands from source-owned extensions. Do not generate command files. |
| **Context file** | Workflow overview + skill descriptions in the CLI's native context format per reference file. |
| **README** | Component table, install instructions, feature parity table, required config, link to GitHub repo. |
| **Package manifest** | Generate only for targets whose reference file declares a package-native install surface. For Pi, repo-root package metadata and `pi/extensions/` runtime code are source-owned; generated shared assets under `dist/pi/` are package resources consumed by that source surface. For OpenCode, the plugin entry (`dist/opencode/plugin/package.json` + `index.js`) is generated and versioned per the reference file. |
| **Install script** | None. No target ships an install script — Codex and OpenCode are plugin-native; Pi installs via its package manager. |
| **CLI extras** | Extension manifests, plugin configs, execution rules — per reference file. |
| **Namespace metadata** | **Package target (Pi) only.** Regenerate `component-namespaces.json` from source ownership every run; every distributed component appears exactly once under its component type with its owning plugin. **Plugin-native Codex and OpenCode have none** — skip them (the plugin boundary is the namespace). |

### README install section

The CLI-native install method from the reference file is the primary method: Codex plugin marketplace add, OpenCode repo clone + plugin config line (with the clone-or-pull update alias), Pi package manager from the repo root. Include other methods from the reference file as alternatives only when they actually work for that target.

## Constraints

| Constraint | Why |
|-----------|-----|
| Shell-based text processing during sync must work in both bash and zsh | macOS default shell is zsh; bash-only constructs break |
| Reference files are authoritative for conversion rules | Avoids two sources of truth — update one place |
| Unmapped tool names in skill prose pass through unchanged | Only operational references remap; names without a lookup-table row are left as-is |
| Empty component sets skip gracefully | Codex has no hooks — note in README, don't error |
| Skill prompt bodies stay faithful to Claude Code originals | Prompts are carefully crafted — don't simplify, rewrite, or truncate for other CLIs |
| Always update `dist/{cli}/.sync-meta.json` at end of run | The recorded SHA is what next run's diff-first path keys on. Skipping the update silently degrades future syncs to full re-syncs. |

## Progress Log

Write to `/tmp/sync-tools-{timestamp}.md` after each CLI: counts, warnings, what was generated. Read the full log before writing the final summary.

## Output

Summary table after all CLIs processed:

| CLI | Skills | Agents | Hooks | Commands | Status |
|-----|--------|--------|-------|----------|--------|
| OpenCode | N (1 plugin) | none (all skills) | none | — (native skills-as-commands) | Complete |
| Codex | N (2 plugins) | none (reviewers = review-code skill) | none | — | Complete |
| Pi | N compatible | N runtime prompt assets | source-owned runtime extension | extension commands | Complete |
