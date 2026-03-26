# manifest-dev for Codex CLI

Verification-first manifest workflows adapted for Codex CLI.

## What's Included

| Component | Count | Status |
|-----------|-------|--------|
| Skills | 7 | Full compatibility (Agent Skills Open Standard) |
| Agents | 14 TOML stubs + reference AGENTS.md | Multi-agent config + bundled reference guide |
| Execution rules | 1 | Starlark .rules file |
| Config | 1 | Multi-agent TOML config |
| Hooks | 0 | Not available (Codex has no hook system yet) |

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash
```

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash -s -- uninstall
```

### Skills only

```bash
npx skills add doodledood/manifest-dev --all -a codex
```

## Execution Modes

| Mode | Verification | Parallelism | Best For |
|------|-------------|-------------|----------|
| **thorough** (default) | Full reviewer agents, unlimited fix loops | All at once | Production-quality work |
| **balanced** | Full model capability, capped loops | Batched (max 4) | Standard development |
| **efficient** | Skips reviewer subagents, lighter checks | Sequential | Quick iterations, low-risk changes |

## Known Limitations

1. **Skills are the only fully compatible component** -- agents are TOML stubs, hooks impossible.
2. **No workflow enforcement** -- without hooks, the chain is advisory.
3. **6 default tools** -- `shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`.
4. **Hooks not shipped** -- Issue #2109 (453+ upvotes). No timeline.
5. **$ARGUMENTS not supported** -- Claude Code skill extension only.

## Source

Generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev). The Claude Code plugin is the source of truth.
