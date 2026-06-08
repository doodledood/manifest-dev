# manifest-dev — OpenCode CLI Distribution

Verification-first manifest workflows for OpenCode CLI. Ported from the Claude Code manifest-dev plugin.

manifest-dev ships **zero agents** — every capability is a skill. Quality review is the `review-code` skill (one dimension per invocation); the former functional agents are skills too (`check-pr`, `poll-slack`, `review-prompt`). Verification is always a general-purpose subagent whose prompt activates the relevant skill.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 18 | Core workflow skills plus manifest-dev-tools utilities (incl. `review-code`, `check-pr`, `poll-slack`, `review-prompt`) |
| Commands | 15 | User-invocable slash commands generated from user-invocable skills |
| Context | 1 | AGENTS.md workflow overview |
| Agents | 0 | None — all capabilities are skills |

## Installation

### Option 1: Remote Install via npx skills (Skills Only)

```bash
npx skills add doodledood/manifest-dev --all -a opencode
```

This installs skills into `.opencode/skills/`. For commands too, use the full distribution install below.

### Option 2: Full Distribution Install

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
```

This installs globally to `~/.config/opencode/`, which OpenCode loads from every project. Restart OpenCode after installing or updating so the running TUI reloads commands and skills.

Or clone and run locally:

```bash
git clone https://github.com/doodledood/manifest-dev.git
cd manifest-dev
bash dist/opencode/install.sh
```

The install script:
- Copies core skills to `~/.config/opencode/skills/` with the `-manifest-dev` suffix
- Copies manifest-dev-tools skills to `~/.config/opencode/skills/` with the `-manifest-dev-tools` suffix
- Copies commands to `~/.config/opencode/commands/` with the same plugin-owned suffixes
- Copies the AGENTS.md context file
- Is idempotent — safe to re-run

To install only for the current project, pass `--local`:

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- --local
```

To install somewhere custom, set `OPENCODE_TARGET` or pass `--dir`:

```bash
OPENCODE_TARGET="$HOME/.config/opencode" bash dist/opencode/install.sh
bash dist/opencode/install.sh --dir /path/to/opencode-config
```

To uninstall only manifest-dev-managed files:

```bash
bash dist/opencode/install.sh uninstall
```

Use `bash dist/opencode/install.sh uninstall --local` to remove a project-local install.

### Manual Install

```bash
# Skills
cp -r dist/opencode/skills/* .opencode/skills/

# Commands
cp -r dist/opencode/commands/* .opencode/commands/

# Context file
cp dist/opencode/AGENTS.md .opencode/AGENTS.md
```

## Usage

After installation, invoke workflows via slash commands (namespaced with the owning plugin's suffix), e.g. `/define-manifest-dev`, `/do-manifest-dev`, `/auto-manifest-dev`, `/babysit-pr-manifest-dev-tools`, `/review-pr-manifest-dev-tools`.

## Feature Parity with Claude Code

| Feature | Claude Code | OpenCode | Notes |
|---------|------------|----------|-------|
| Skills | Full | Full | Copied unchanged (incl. the review-code/check-pr/poll-slack/review-prompt skills) |
| Commands | N/A | Full | Generated from user-invocable skills |
| Agents | None (all skills) | None (all skills) | Verification activates a skill from a general-purpose subagent |
| Hooks | None shipped | None shipped | Use `/goal /do <manifest-path>` for unattended turn continuation |

## Known Limitations

1. **No hook backstop for `/do`** — use `/goal /do <manifest-path>` when you want the host CLI to keep `/do` running across turns.
2. **$ARGUMENTS handling** — Skills using `$ARGUMENTS` work in Claude Code; behavior in OpenCode may vary.

## Directory Structure

```
dist/opencode/
├── skills/                          # 18 skills (core + tools), original names
│   ├── review-code/                 #   quality review, one dimension per invocation
│   ├── check-pr/  poll-slack/       #   former functional agents, now skills
│   ├── define/  do/  auto/  ...      #   workflow skills
│   └── review-prompt/  prompt-engineering/  review-pr/  ...
├── commands/                        # 15 user commands (from user-invocable skills)
├── component-namespaces.json        # install-time namespacing metadata
├── AGENTS.md                        # Context file
├── README.md                        # This file
├── install.sh                       # Installation script
└── install_helpers.py               # Namespacing helper
```
