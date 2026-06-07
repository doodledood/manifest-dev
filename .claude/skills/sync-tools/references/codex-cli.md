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
| Skills (`SKILL.md` + companions) | YES — `"skills": "./skills/"` | All shared skills, including the `code-review` skill with its per-dimension references |
| MCP servers (`.mcp.json`) | YES | None currently |
| Apps (`.app.json`) | YES | None currently |
| Hooks (`hooks/hooks.json`) | YES (manifest field exists) | manifest-dev ships none to Codex; Codex hook execution is still limited (Issue #2109) — do not fabricate |
| **Agents / subagent roles** | **NO** | Reviewers are the `code-review` **skill**; other agents degrade to general-purpose (see below) |

**Agents are not a plugin component.** Codex plugins bundle skills/MCP/apps/hooks only. Consequences for manifest-dev:

- The 13 quality-dimension reviewers are **not agents** anymore — they are dimensions of the bundled `code-review` skill. They ship automatically as part of that skill's directory.
- The surviving agents (`criteria-checker`, `github-pr-lifecycle`, `slack-poller`, `prompt-reviewer`) cannot be bundled. On Codex they **degrade to the general-purpose subagent**: a manifest gate with `verify.agent: <name>` falls back to general-purpose driven by its `verify.prompt`. The skills and task files already carry general-purpose fallbacks (e.g. PROMPTING.md's prompt-reviewer fallback; `verify.agent` default is general-purpose). Document this as a known limitation; do not generate TOML agent stubs.

## Distribution layout

```
.agents/plugins/marketplace.json          # repo-root registry (the ONLY file under .agents/plugins/)
dist/codex/
├── plugins/
│   ├── manifest-dev/                      # core plugin
│   │   ├── .codex-plugin/plugin.json
│   │   └── skills/                        # core skills incl. code-review/ (with references/*)
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
      "policy": { "installation": "AVAILABLE", "authentication": "NONE" },
      "category": "Productivity"
    },
    {
      "name": "manifest-dev-tools",
      "source": { "source": "local", "path": "./dist/codex/plugins/manifest-dev-tools" },
      "policy": { "installation": "AVAILABLE", "authentication": "NONE" },
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

- **Core plugin** (`manifest-dev`): the user-invocable and supporting skills from `claude-plugins/manifest-dev/skills/`, including `code-review/` with its full `references/` set. Exclude the `sync-tools` meta-tool.
- **Tools plugin** (`manifest-dev-tools`): skills from `claude-plugins/manifest-dev-tools/skills/`.

Per-skill body adaptations (unchanged from the open-standard rules):

- **Tool-name references in operational prose** → Codex names: Bash→`shell_command`, Read→`read_file`, Edit→`apply_patch`, Grep→`grep_files`, Glob/Write/WebFetch→`shell_command`, WebSearch→`web_search`, AskUserQuestion→`request_user_input`, TaskCreate/Todo→`update_plan`. Leave teaching/reference content (`references/*.md` explaining Claude Code conventions) unchanged.
- **Context file**: operational "write to CLAUDE.md" → "AGENTS.md". Do not rewrite "CLAUDE.md" in comparative/research text. The `code-review` skill's `context-file-adherence` dimension reference already uses generic "context file" language — no special handling.
- **Model tiers**: in `references/execution-modes/`, replace Claude model names (haiku/sonnet/opus) with `inherit`.
- **Session line**: omit the `Session: ~/.claude/.../<id>.jsonl` line from `define`'s completion template — Codex has no agent-visible session-id env var (issue #8923).
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

```bash
# Add the marketplace (GitHub shorthand resolves .agents/plugins/marketplace.json)
codex plugin marketplace add doodledood/manifest-dev

# Then install the plugins from the Codex /plugins UI, or:
codex plugin marketplace list
```

Local development against a checkout:

```bash
codex plugin marketplace add ./   # repo root; reads .agents/plugins/marketplace.json
```

Installed plugins are cached under `~/.codex/plugins/cache/manifest-dev/<plugin>/<version>/` and loaded from there — never from the shared `~/.agents/skills/` tree.

## AGENTS.md / context

manifest-dev's own `CLAUDE.md`-style context is not required for plugin consumers. If a generated context file is produced for the dist README, describe the workflow (define → do → verify → done) and note that reviewers are the `code-review` skill's dimensions, not standalone agents.

## Known limitations

1. **No agent bundling** — reviewers are the `code-review` skill; `criteria-checker` / `github-pr-lifecycle` / `slack-poller` / `prompt-reviewer` degrade to general-purpose via `verify.prompt` fallbacks.
2. **Hooks** — manifest-dev ships none to Codex; Codex hook execution remains limited (Issue #2109).
3. **No `/auto` or `/babysit-pr` runtime command** — they ship as skills that chain `/do`; only Pi has native runtime wrappers.
4. **Experimental tools** — `read_file`/`grep_files`/`list_dir` availability is model-gated server-side.
5. **`$ARGUMENTS`** — Claude Code extension; skills relying on it use the open-standard argument mechanism Codex provides.
6. **Model tier routing is Claude-only** — `execution-modes/*` Claude model names become `inherit`.
