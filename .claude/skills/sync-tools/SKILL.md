---
name: sync-tools
description: 'Regenerate the Codex distribution copy of the plugin skills and check it for drift. Run after changing anything under claude-plugins/*/skills. OpenCode and Pi read the source tree directly and need no sync.'
user-invocable: true
metadata:
  internal: true
---

# /sync-tools — distribution sync

Every host reads the same skill files. The Claude Code plugins under `claude-plugins/` are the source; OpenCode (`dist/opencode/plugin/index.js`) and Pi (repo-root `package.json`, `pi.skills`) point straight at `claude-plugins/*/skills`. Only Codex needs a copy, because it installs a plugin into its own cache, and that copy is generated:

```bash
python3 scripts/sync_dist.py          # regenerate dist/codex/plugins/*/skills byte-identically from source
python3 scripts/sync_dist.py --check  # exit 1 on any drift (tests/test_dist_skill_references.py runs this)
```

Run the first command after any change under `claude-plugins/*/skills`, then commit the regenerated tree with the change. There is no per-host rewrite: shipped skill text names no host primitive (`tests/test_skill_frontmatter.py` enforces that), so a copy is a copy.

## Hand-maintained packaging files

These are not generated. Edit them when what they describe changes:

| File | What it carries |
|------|-----------------|
| `dist/codex/plugins/manifest-dev/.codex-plugin/plugin.json`, `dist/codex/plugins/manifest-dev-tools/.codex-plugin/plugin.json` | Codex plugin manifests; `version` must equal the source plugin's `.claude-plugin/plugin.json` version |
| `.agents/plugins/marketplace.json` | Codex marketplace registry pointing at the two plugin directories |
| `dist/opencode/plugin/index.js`, `dist/opencode/plugin/package.json` | OpenCode plugin entry (registers the source skill dirs and slash-command wrappers); `version` tracks `manifest-dev`'s |
| `dist/opencode/AGENTS.md` | OpenCode instructions file the plugin registers |
| `dist/pi/prompts/*.md` | Pi prompt-template aliases (`/do`, `/auto`, `/babysit-pr`) |
| `dist/codex/README.md`, `dist/opencode/README.md`, `dist/pi/README.md` | Per-host install and update instructions |

Version bumps follow the repo's Versioning rules; this skill does not bump anything.
