# Codex CLI Conversion Guide

Reference for generating the **Codex plugin-native distribution** of manifest-dev (Codex v0.107.0+, plugin marketplaces, March 2026).

Codex ships manifest-dev as **native plugins installed from a repo marketplace**, not as an installer that copies files into shared directories. This is the canonical (and only) Codex distribution — the legacy `install.sh` / `install_helpers.py` / `config.toml` merge / `agents/*.toml` stub / `rules/` approach is retired.

## Why plugin-native

Plugin skills install into Codex's private plugin cache:

```
~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/
```

Nothing lands in the shared open-standard `~/.agents/skills/` directory, so manifest-dev skills no longer leak into other Agent-Skills hosts (notably Pi, which scans `~/.agents/skills` and `~/.pi/agent/skills` globally). Eliminating that leak at the source is the reason this distribution exists.

## What Codex plugins can and cannot bundle

| Component | Bundleable in a plugin? | manifest-dev handling |
|-----------|-------------------------|------------------------|
| Skills (`SKILL.md` + companions) | YES — `"skills": "./skills/"` | All shared skills, including the `review-code` skill with its per-dimension references |
| MCP servers (`.mcp.json`) | YES | None currently |
| Apps (`.app.json`) | YES | None currently |
| Hooks (`hooks/hooks.json`) | YES (manifest field exists) | manifest-dev ships none to Codex; Codex hook execution is still limited (Issue #2109) — do not fabricate |
| **Agents / subagent roles** | **NO** | manifest-dev ships no agents — all former agents are skills (see below) |

**Agents are not a plugin component, and manifest-dev ships none.** Codex plugins bundle skills/MCP/apps/hooks only — but this is not a Codex-specific limitation: manifest-dev itself ships **zero agents** on every target. Consequences:

- The 13 quality-dimension reviewers are **not agents** — they are dimensions of the bundled `review-code` skill. They ship automatically as part of that skill's directory.
- The former functional agents are now **skills**: `check-pr`, `poll-slack`, and `review-prompt` ship as ordinary bundled skills. Verification is always a general-purpose subagent whose `verify.prompt` activates the relevant skill — there is no `verify.agent` field. Do not generate TOML agent stubs.

## Distribution layout

```
.agents/plugins/marketplace.json          # repo-root registry (the ONLY file under .agents/plugins/)
dist/codex/
├── plugins/
│   ├── manifest-dev/                      # core plugin
│   │   ├── .codex-plugin/plugin.json
│   │   └── skills/                        # core skills incl. review-code/ (with references/*)
│   └── manifest-dev-tools/                # tools plugin
│       ├── .codex-plugin/plugin.json
│       └── skills/                        # tools skills
├── README.md
└── .sync-meta.json
```

Two plugins mirror the source split: `manifest-dev` (core workflow skills) and `manifest-dev-tools` (PR/dev tooling skills).

### marketplace.json (repo root `.agents/plugins/marketplace.json`)

The registry lives at the conventional repo-root path so `codex plugin marketplace add doodledood/manifest-dev` finds it. `source.path` is relative to the **repo root** (the marketplace root) and points into the generated tree:

```json
{
  "name": "manifest-dev",
  "interface": { "displayName": "manifest-dev" },
  "plugins": [
    {
      "name": "manifest-dev",
      "source": { "source": "local", "path": "./dist/codex/plugins/manifest-dev" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    },
    {
      "name": "manifest-dev-tools",
      "source": { "source": "local", "path": "./dist/codex/plugins/manifest-dev-tools" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

`policy.installation`, `policy.authentication`, and `category` are required on every entry. `.agents/plugins/` holds **only** `marketplace.json` — never a `SKILL.md` (that would land in a Pi-scanned-adjacent path and muddy the registry). Plugin payloads live under `dist/codex/`.

### plugin.json (`dist/codex/plugins/<name>/.codex-plugin/plugin.json`)

Only `plugin.json` belongs in `.codex-plugin/`; `skills/` sits at the plugin root.

```json
{
  "name": "manifest-dev",
  "version": "<plugin version from claude-plugins/manifest-dev/.claude-plugin/plugin.json>",
  "description": "Manifest-driven workflows: /define interviews and writes a Manifest; /do executes and verifies it.",
  "skills": "./skills/",
  "keywords": ["manifest-dev", "agent-skills", "workflow"]
}
```

Keep `version` in step with the source plugin's `.claude-plugin/plugin.json`.

## Skill handling

Skills copy under the Agent Skills Open Standard — same as before, into each plugin's `skills/` directory:

- **Core plugin** (`manifest-dev`): the user-invocable and supporting skills from `claude-plugins/manifest-dev/skills/`, including `review-code/` with its full `references/` set. Exclude the `sync-tools` meta-tool.
- **Tools plugin** (`manifest-dev-tools`): skills from `claude-plugins/manifest-dev-tools/skills/`.

Per-skill body adaptations (unchanged from the open-standard rules):

- **Tool-name references in operational prose** → Codex names: Bash→`shell_command`, Read→`read_file`, Edit→`apply_patch`, Grep→`grep_files`, Glob/Write/WebFetch→`shell_command`, WebSearch→`web_search`, AskUserQuestion→`request_user_input`, TaskCreate/Todo→`update_plan`. Leave teaching/reference content (`references/*.md` explaining Claude Code conventions) unchanged.
- **Context file**: operational "write to CLAUDE.md" → "AGENTS.md". Do not rewrite "CLAUDE.md" in comparative/research text. The `review-code` skill's `context-file-adherence` dimension reference already uses generic "context file" language — no special handling.
- **Model tiers**: in `references/execution-modes/`, replace Claude model names (haiku/sonnet/opus) with `inherit`.
- **No `manifest-` command prefix**: Codex skills present `/do`, `/auto`, `/babysit-pr` (the Pi-only `manifest-` prefix never applied to Codex). Codex has no native `/auto` or `/babysit-pr` runtime command, so those skills ship as ordinary skills that internally chain `/do`.

### Tool name mapping (Claude Code → Codex)

| Claude Code Tool | Codex Tool | Notes |
|-----------------|------------|-------|
| Bash / BashOutput | `shell_command` | Default for codex models |
| Read | `read_file` | Experimental — gated by model `experimental_supported_tools` |
| Write | `shell_command` | No dedicated write tool — shell `cat > file` |
| Edit | `apply_patch` | Freeform or JSON patch |
| Grep | `grep_files` | Experimental |
| Glob | `shell_command` | Use shell `find`/`ls` |
| WebFetch | `shell_command` | Use shell `curl` |
| WebSearch | `web_search` | Default tool |
| Skill | (skill system) | `$skillname` / implicit activation |
| AskUserQuestion | `request_user_input` | Always-on |
| TaskCreate/Update/Todo* | `update_plan` | Flat step list |
| Agent (spawn) | `spawn_agent` | Requires Feature::Collab — not relied on by the distribution |

Default tools (codex-optimized models): `shell_command`, `update_plan`, `request_user_input`, `apply_patch`, `web_search`, `view_image`. Experimental (model-gated): `read_file`, `list_dir`, `grep_files`.

## Namespacing

Plugin-native distribution does **not** namespace component names with install-time suffixes. Each plugin is its own namespace (`manifest-dev`, `manifest-dev-tools`), and skills keep their original directory names inside it. There is no `install_helpers.py` and no `component-namespaces.json` for Codex; the plugin boundary is the namespace. Skill `name:` frontmatter stays as authored.

## Installation

Codex separates marketplace **registration** from plugin **installation** — add the marketplace, then install each plugin:

```bash
# 1. Add the marketplace (GitHub shorthand resolves .agents/plugins/marketplace.json)
codex plugin marketplace add doodledood/manifest-dev

# 2. Install both plugins (or pick them from the Codex /plugins UI)
codex plugin add manifest-dev@manifest-dev
codex plugin add manifest-dev-tools@manifest-dev
```

Local development against a checkout:

```bash
codex plugin marketplace add ./   # repo root; reads .agents/plugins/marketplace.json
codex plugin add manifest-dev@manifest-dev
codex plugin add manifest-dev-tools@manifest-dev
```

Uninstall removes the installed plugins, then (optionally) the marketplace source:

```bash
codex plugin remove manifest-dev@manifest-dev
codex plugin remove manifest-dev-tools@manifest-dev
codex plugin marketplace remove manifest-dev
```

Installed plugins are cached under `~/.codex/plugins/cache/manifest-dev/<plugin>/<version>/` and loaded from there — never from the shared `~/.agents/skills/` tree.

## AGENTS.md / context

manifest-dev's own `CLAUDE.md`-style context is not required for plugin consumers. If a generated context file is produced for the dist README, describe the workflow (define → do → verify → done) and note that manifest-dev ships no agents — verification is a general-purpose subagent that activates skills (reviewers are the `review-code` skill's dimensions).

## Known limitations

1. **No agents at all** — manifest-dev ships zero agents. Reviewers are the `review-code` skill; `check-pr` / `poll-slack` / `review-prompt` are skills a general-purpose verifier activates via `verify.prompt`.
2. **Hooks** — manifest-dev ships none to Codex; Codex hook execution remains limited (Issue #2109).
3. **No `/auto` or `/babysit-pr` runtime command** — they ship as skills that chain `/do`; only Pi has native runtime wrappers.
4. **Experimental tools** — `read_file`/`grep_files`/`list_dir` availability is model-gated server-side.
5. **`$ARGUMENTS`** — Claude Code extension; skills relying on it use the open-standard argument mechanism Codex provides.
6. **Model tier routing is Claude-only** — `execution-modes/*` Claude model names become `inherit`.
