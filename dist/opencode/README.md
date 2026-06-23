# manifest-dev — OpenCode CLI Distribution

Verification-first manifest workflows for OpenCode CLI, distributed as an **OpenCode plugin**: a clone of this repo plus one line of config. No installer, no files copied into your config directories, nothing placed in shared Agent Skills directories (so nothing bleeds into Pi, Claude Code, or Codex installs).

manifest-dev ships **zero agents** — every capability is a skill. Quality review is the `review-code` skill (one dimension per invocation); the former functional agents are skills too (`check-pr`, `poll-slack`, `review-prompt`). Verification is always a general-purpose subagent whose prompt activates the relevant skill. For TUI ergonomics, the plugin also registers slash-command wrappers for user-invocable skills (for example `/figure-out`, `/define`, `/do`, `/prompt-engineering`, `/review-pr`).

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 18 | Core workflow skills plus manifest-dev-tools utilities (incl. `review-code`, `check-pr`, `poll-slack`, `review-prompt`) |
| Plugin | 1 | Dependency-free OpenCode plugin that registers the skills payload, user-invocable slash-command wrappers, and AGENTS.md context |
| Context | 1 | AGENTS.md workflow overview, registered via `instructions` |
| Commands | 16 | Runtime command wrappers registered by the plugin for user-invocable skills; no command files are copied or generated |
| Agents | 0 | None — all capabilities are skills |

## Requirements

**OpenCode v1.2.16 or newer.** Basis: this distribution was live-verified on v1.2.16, v1.3.13, v1.14.31, and v1.17.3 (plugin `config` hook + `skills.paths` registration + skill discovery, see Mechanism Verification below). Older versions can't be verified the same way (`opencode debug skill` doesn't exist before ~v1.2). Current OpenCode exposes skills through the `skill` tool; manifest-dev's slash UX is provided by plugin-registered command wrappers.

## Installation

1. Clone the repo (anywhere; `~/.manifest-dev/repo` is the documented default):

```bash
git clone https://github.com/doodledood/manifest-dev.git ~/.manifest-dev/repo
```

2. Add the plugin to your **global** OpenCode config (`~/.config/opencode/opencode.json`):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["~/.manifest-dev/repo/dist/opencode/plugin"]
}
```

3. Restart OpenCode. Config (including plugins and skills) loads once at startup and is not hot-reloaded.

The `~/` form in plugin paths is live-verified on v1.17.3 but not explicitly documented by OpenCode (its docs show `./relative` — resolved from the declaring config file — and `file:///absolute`; bare absolute paths are also accepted by the spec parser and were live-verified across all four tested versions). If you prefer not to rely on `~` expansion, use an absolute path:

```json
{ "plugin": ["/home/you/.manifest-dev/repo/dist/opencode/plugin"] }
```

For a single project instead of global, put the same `plugin` entry in the project's `opencode.json`.

### Updating

Add this alias once (e.g. `~/.zshrc` / `~/.bashrc`):

```bash
alias manifest-dev-update='if [ -d ~/.manifest-dev/repo/.git ]; then git -C ~/.manifest-dev/repo pull --ff-only; else git clone https://github.com/doodledood/manifest-dev.git ~/.manifest-dev/repo; fi'
```

Then updating is one command — `manifest-dev-update` — followed by an OpenCode restart. The plugin has zero npm dependencies, so `git pull` is the entire update.

### Uninstalling

Remove the `plugin` entry from your opencode.json and delete the clone. Nothing else was installed.

### Migrating from the retired installer

Versions of this distribution before June 2026 shipped a `curl | bash` installer that copied suffixed skills and commands into `~/.config/opencode/`. Those copies keep loading as stale skills/commands until you remove them:

```bash
find ~/.config/opencode/skills -maxdepth 1 -name '*-manifest-dev*' -exec rm -rf {} + 2>/dev/null
find ~/.config/opencode/commands -maxdepth 1 -name '*-manifest-dev*' -exec rm -f {} + 2>/dev/null
```

The old installer also copied an `AGENTS.md` to `~/.config/opencode/AGENTS.md` — delete it only if you haven't made it your own (the plugin registers this repo's copy automatically).

## Usage

Skills appear under their original names. Invoke user-facing skills via slash-command wrappers — `/figure-out`, `/define`, `/do`, `/auto`, `/babysit-pr`, `/review-pr`, `/prompt-engineering`, and the rest of the user-invocable set — or just describe the task and let skill auto-discovery match it. Internal helpers with `user-invocable: false` (`done`, `escalate`) remain available to the model through the `skill` tool but do not appear as slash commands.

## How It Works (Mechanism Verification)

The plugin (`plugin/index.js`) is a dependency-free ES module. Its `config` hook mutates the live merged config once at startup: it appends `dist/opencode/skills` to `skills.paths`, scans the bundled skill frontmatter and adds `cfg.command` wrappers for user-invocable skills, and appends `dist/opencode/AGENTS.md` to `instructions`. All paths resolve from the plugin file's own location (`import.meta.url`), so the clone can live anywhere. Missing assets degrade to a console warning — a throwing config hook would break OpenCode startup.

Evidence (live runs against real binaries, 2026-06-11, sandboxed `XDG_*` homes):

- **Hook-before-discovery ordering**: a test plugin's `config` hook appended `skills.paths`; `opencode debug skill` then listed the registered skill — verified on v1.2.16, v1.3.13, v1.14.31, v1.17.3. With this repo's actual plugin on v1.17.3, all 18 skills were discovered from `dist/opencode/skills`, and `opencode debug config` showed the resolved config containing the `skills.paths`, `command`, and `instructions` entries.
- **Plugin contract**: function export (default or named) returning a hooks object; `config(cfg)` is called "once on init with the merged config". Confirmed live and by OpenCode's own built-in `customize-opencode` skill (registered in code at `packages/core/src/plugin/skill.ts`, shipped inside `opencode-ai@1.17.3`), which also documents `skills.paths` ("scanned recursively for `**/SKILL.md`"), the `command` and `instructions` keys, and the plugin spec forms. Current upstream docs say skills are model-visible through the `skill` tool and slash commands are command-backed; manifest-dev registers wrappers accordingly.
- **`~` in plugin paths**: a `"plugin": ["~/…"]` entry loaded and its skills were discovered (v1.17.3).
- **Failure-soft**: invoking the hook with the sibling assets absent produced warnings and no throw; existing user `skills.paths`/`instructions` values are preserved (append, not overwrite), and existing user/project commands are not overwritten.
- **Not exercised live**: actual injection of the AGENTS.md *content* into a session's system context (needs an LLM session, not available in the verification sandbox). Basis for shipping it: `instructions` is a documented config key and the resolved config accepted the entry.

## Feature Parity with Claude Code

| Feature | Claude Code | OpenCode | Notes |
|---------|------------|----------|-------|
| Skills | Full | Full | Identical payload, registered via plugin `skills.paths` |
| Slash commands | Plugin-namespaced (`/manifest-dev:define`) | Plugin-registered wrappers, bare names (`/define`) | Wrappers call the corresponding skill and are generated only for user-invocable skills |
| Agents | None (all skills) | None (all skills) | Verification activates a skill from a general-purpose subagent |
| Hooks | None shipped | None shipped | Use a durable goal-setting/continuation backstop for unattended turn continuation (`/do` = auditable all-criteria-PASS; `/auto` = full Read anatomy → manifest → `/do` gate ledger) |

## Known Limitations

1. **Frontmatter controls mostly ignored by OpenCode** — OpenCode's skill loader honors only `name`/`description`; `disable-model-invocation` has no effect, so all 18 skills remain model-visible through the `skill` tool. manifest-dev's plugin consumes `user-invocable` only for slash-wrapper registration: `done` and `escalate` are not slash-listed.
2. **Bare names, first-found-wins** — skills keep their original names (`define`, `do`, `auto`); OpenCode dedups same-name skills by discovery order with a logged warning. A project-local skill named `do` shadows manifest-dev's skill. Same-name user/project commands also shadow manifest-dev's slash wrappers because the plugin does not overwrite existing commands.
3. **No hook backstop for `/do` or `/auto`** — use a host-provided goal-setting/continuation backstop when you want the host CLI to keep long runs moving across turns. `/do` needs auditable all-criteria-PASS: every manifest gate listed with fresh independent PASS evidence, not a summary claim. `/auto` needs one full-chain parent goal: full autonomous Read anatomy, then manifest written, then `/do` gate-ledger PASS. If no such capability is available, copy the contract the skill prints into your continuation mechanism.
4. **$ARGUMENTS pass-through** — slash wrappers use OpenCode command-template `$ARGUMENTS` to prompt `Use the <skill> skill with: $ARGUMENTS`.

## Directory Structure

```
dist/opencode/
├── plugin/                          # OpenCode plugin (the install surface)
│   ├── package.json                 #   dependency-free ESM package
│   └── index.js                     #   config hook: registers skills/ + slash wrappers + AGENTS.md
├── skills/                          # 18 skills (core + tools), original names
│   ├── review-code/                 #   quality review, one dimension per invocation
│   ├── check-pr/  poll-slack/       #   former functional agents, now skills
│   ├── define/  do/  auto/  ...      #   workflow skills
│   └── review-prompt/  prompt-engineering/  review-pr/  ...
├── AGENTS.md                        # Context file, registered via instructions
└── README.md                        # This file
```
