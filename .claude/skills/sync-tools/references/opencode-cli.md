# OpenCode CLI Conversion Guide

Reference for generating the OpenCode distribution from the Claude Code plugins. Plugin-native model, live-verified against opencode **v1.17.3** (June 2026); minimum supported version **v1.2.16** (oldest version the plugin mechanism was live-verified on; current OpenCode docs expose skills through the native `skill` tool, while slash autocomplete is command-backed).

**manifest-dev ships no agents and no command files on OpenCode.** Every capability is a skill; verification is a general-purpose subagent whose prompt activates a skill. The OpenCode plugin registers the bundled skills via `skills.paths` and dynamically adds slash-command wrappers in `cfg.command` for source skills whose `user-invocable` frontmatter is not `false`. The former `install.sh`/`install_helpers.py`/`component-namespaces.json` installer surface is retired with it — the plugin below is the entire install story.

## Distribution Model

```
dist/opencode/
├── plugin/                # the install surface (one config line points here)
│   ├── package.json       # @doodledood/manifest-dev-opencode — dependency-free ESM
│   └── index.js           # config hook: registers ../skills + slash wrappers + ../AGENTS.md
├── skills/                # all compatible skills from both source payloads, original names
├── AGENTS.md              # context file, registered via `instructions`
└── README.md              # install/update/migration docs
```

Install = clone the repo + add the plugin directory's path to the `plugin` array in `~/.config/opencode/opencode.json`. Update = `git pull` + restart (config loads once at startup, no hot reload). Uninstall = remove the config line + delete the clone. Nothing is copied into `~/.config/opencode/` or any shared Agent Skills directory (`.agents/skills`, `.claude/skills`) — per-host skill sets differ (Pi excludes `do`/`done`/`escalate` as runtime-owned), so shared dirs would bleed wrong payloads across CLIs.

**Do not generate:** command files, `component-namespaces.json` (no install-time namespacing exists), install scripts of any kind. Slash UX is owned by the plugin's `config` hook, which adds `cfg.command` wrappers at startup without copying files into user config.

## Plugin Entry Contract

`package.json`: name `@doodledood/manifest-dev-opencode`, `"type": "module"`, `"main": "index.js"`, zero `dependencies`/`devDependencies`. **`version` mirrors the core `manifest-dev` plugin version** (`claude-plugins/manifest-dev/.claude-plugin/plugin.json`) — bump on sync when the core version moved. Core-only mirroring is deliberate: install is clone-by-path and updates ride `git pull`, so the version is provenance, not a resolution input; `manifest-dev-tools`-only releases ship through the same sync without a bump.

`index.js`: a named export `ManifestDevPlugin = async () => ({ config: async (cfg) => … })`. The `config` hook:

- resolves `../skills` and `../AGENTS.md` from `import.meta.url` (never cwd — the clone can live anywhere);
- **appends** the skills dir to `cfg.skills.paths` and the AGENTS.md path to `cfg.instructions`, preserving existing user entries;
- scans package-local `skills/*/SKILL.md` frontmatter and adds `cfg.command[skillName] = { description, template: "Use the <skillName> skill with: $ARGUMENTS" }` for every source user-invocable skill (`user-invocable` missing/true); `user-invocable: false` helpers such as `done` and `escalate` do not get slash commands;
- never overwrites an existing `cfg.command[skillName]`, so user/project commands intentionally shadow manifest-dev wrappers;
- is **failure-soft**: missing assets log a `console.warn` and skip; the whole body is wrapped so the hook never throws (a throwing config hook breaks OpenCode startup for every project).

Mechanism basis (live runs, sandboxed `XDG_*` homes, 2026-06-11): plugin `config`-hook mutations of `skills.paths` are visible to skill discovery — verified on v1.2.16/v1.3.13/v1.14.31/v1.17.3 via `opencode debug skill`; the full 18-skill payload + skills/instructions config mutations confirmed on v1.17.3 via `opencode debug config`. Current upstream OpenCode docs state skills are listed in the native `skill` tool description, while slash autocomplete is command-backed; therefore manifest-dev's plugin also mutates `cfg.command` for invocable skill wrappers. The plugin export/hook contract and the `skills.paths` ("scanned recursively for `**/SKILL.md`"), `command`, and `instructions` keys are documented by OpenCode's built-in `customize-opencode` skill (registered at `packages/core/src/plugin/skill.ts`) and `https://opencode.ai/docs/{skills,commands,config}`. `~/` in plugin path entries works (live-verified v1.17.3) but is undocumented — README shows it with an absolute-path alternative.

## Skill Handling

Copy skills unchanged from both source payloads (`claude-plugins/manifest-dev/skills/`, `claude-plugins/manifest-dev-tools/skills/`), including subdirectories (`references/`, `tasks/`, `scripts/`, `assets/`), then apply these substitutions:

1. **Plugin-qualifier strip**: `manifest-dev:<skill>` / `manifest-dev-tools:<skill>` → bare `<skill>` (e.g. *"Activate the manifest-dev:review-code skill"* → *"Activate the review-code skill"*; `/manifest-dev:define` → `/define`). OpenCode has no plugin namespace to resolve qualified ids, and the installer rewrite that used to handle them is retired. Same rule and rationale as Pi (Claude Code and Codex keep the qualifier).
2. **Operational tool-name remap** in skill prose (lookup table below) — e.g. *"use the Read tool"* → *"use the read tool"*, *"run Bash"* → *"use the bash tool"*. Research/reference content that teaches Claude Code conventions stays unchanged; only operational instructions remap.
3. **Execution modes**: in `references/execution-modes/`, replace Claude model-tier names (haiku, sonnet, opus) with `inherit` — OpenCode is provider-agnostic; all tiers use the session model.
4. **Session line**: OMIT lines surfacing a session-file path (e.g. `Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl` in `define/SKILL.md`'s completion template). OpenCode stores sessions in SQLite (`~/.local/share/opencode/opencode.db`), with no per-session file a skill can hand to the user.
5. **Context file**: operational `CLAUDE.md` references that mean "this CLI's context file" → `AGENTS.md` (instructions like "write to CLAUDE.md"; `define/tasks/CODING.md`'s project-preference/gate references are operational, so ALL of its CLAUDE.md mentions remap). Do NOT replace mentions of Claude Code's own file in comparative or research text.

### Skill frontmatter on OpenCode

Only `name` and `description` are honored by OpenCode's skill loader (`name` ≤ 64 chars, `^[a-z0-9]+(-[a-z0-9]+)*$`, must match the directory; missing `description` filters the skill out entirely). Claude Code extensions (`argument-hint`, `disable-model-invocation`, `tools`, `context`) are ignored by OpenCode. `user-invocable` is ignored by OpenCode itself but consumed by manifest-dev's plugin to decide which command wrappers to register: missing/true gets a slash wrapper; `false` stays skill-tool-only.

### Tool Name Mapping (Lookup Table)

For prose remaps in skills. Unmapped names and "(no equivalent)" rows both pass through unchanged — never delete or rewrite a tool mention that has no mapping.

| Claude Code Tool | OpenCode Tool Key | Notes |
|-----------------|-------------------|-------|
| Bash | `bash` | Direct equivalent |
| BashOutput | `bash` | Same tool — deduplicate |
| Read | `read` | Direct equivalent |
| Write | `write` | Direct equivalent (create/overwrite) |
| Edit | `edit` | Both do string replacement |
| Grep | `grep` | Both use ripgrep |
| Glob | `glob` | Direct equivalent |
| WebFetch | `webfetch` | Lowercase, no space |
| WebSearch | `websearch` | Lowercase, no space (requires Exa AI key) |
| Agent | `task` | Subagent spawning |
| TaskCreate / TaskUpdate | `todowrite` | Todo management (create and update) |
| TaskGet / TaskList | `todoread` | Todo management (read) |
| TaskOutput | `bash` | No direct equivalent — approximate via shell |
| TaskStop | (no equivalent) | No background task management |
| Skill | `skill` | Both load skills |
| TodoWrite | `todowrite` | Legacy name for TaskCreate |
| TodoRead | `todoread` | Legacy name for TaskGet/TaskList |
| NotebookEdit | (no equivalent) | Not available in OpenCode |
| AskUserQuestion | `question` | User interaction (interactive clients only) |
| EnterPlanMode / ExitPlanMode | (no equivalent) | `plan_exit` exists but experimental |
| EnterWorktree | (no equivalent) | No worktree support |
| TeamCreate / TeamDelete / SendMessage | (no equivalent) | No team management |
| ListMcpResourcesTool / ReadMcpResourceTool | (no equivalent) | MCP handled differently |

## Context File

Generate `dist/opencode/AGENTS.md` (workflow overview) without any suffix-namespacing language — components keep original names. It is delivered via the plugin's `instructions` registration, not copied into user config.

## README Generation

Per the SKILL.md README row, plus OpenCode-specific required elements: clone + config-line install (documented default clone path `~/.manifest-dev/repo`); one-command clone-or-pull update alias + restart note; minimum-version pin with its basis; migration note for retired-installer users (removing `*-manifest-dev*` suffixed copies from `~/.config/opencode/{skills,commands}`); explain that all skills are model-visible through the `skill` tool and user-invocable skills also appear as `/` commands via plugin-registered wrappers; known limitations — the frontmatter-controls, bare-names, `$ARGUMENTS`, and Stop-hook items from the Known Limitations list below, in that list's phrasing; mechanism-verification section preserving the evidence summary and its version pins.

## Hooks

None shipped. OpenCode hooks are additional functions on the same plugin object (`tool.execute.before`, `event`, etc.) — if a future sync ships one, it belongs in `dist/opencode/plugin/index.js` alongside the `config` hook, not in a separate payload. Note: OpenCode has no blocking Stop hook (`session.idle` is fire-and-forget), and `tool.execute.*` hooks don't fire inside subagents — re-derive the capability map before designing any future hook port.

## Known Limitations

1. **Frontmatter controls mostly ignored by OpenCode** — `disable-model-invocation` has no OpenCode effect, and all skills remain model-visible through the `skill` tool. `user-invocable` is honored only by manifest-dev's plugin when registering slash-command wrappers (`false` suppresses the wrapper, not the skill).
2. **Bare names, first-found-wins** — same-name skills dedup by discovery order with a logged warning; a project-local `do` shadows manifest-dev's skill. Same-name commands are preserved rather than overwritten, so a user/project `/do` command shadows manifest-dev's slash wrapper.
3. **$ARGUMENTS in command wrappers** — OpenCode command templates support `$ARGUMENTS`; the wrapper passes them through in the prompt `Use the <skill> skill with: $ARGUMENTS`.
4. **No Stop-hook backstop for `/do`** — for unattended continuation, use the self-contained `/goal` completion-condition form the skills print; keep the `/goal` blocks rather than dropping them.
5. **Model tier routing is Claude Code-only** — execution-mode tiers all map to `inherit` (substitution 3).
6. **Native `.claude/` compat overlap** — a user running OpenCode *inside a repo that itself contains manifest-dev-style `.claude/skills/`* gets those project skills too; project-local wins on name collisions. Not a sync concern, worth knowing when debugging duplicates.
