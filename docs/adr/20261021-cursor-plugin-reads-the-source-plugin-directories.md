# ADR: The Cursor plugin reads the source plugin directories

## Status
Accepted

## Area
Cursor distribution

## Decided by
An agent in an unattended run, with no review

## Context
Cursor installs plugins from Git repositories: a Cursor Plugin is a directory with a `.cursor-plugin/plugin.json` manifest, and a repository holding several lists them in a root `.cursor-plugin/marketplace.json` whose entries name each plugin's directory ([plugins reference](https://cursor.com/docs/reference/plugins)). Cursor resolves an entry's `source`, merges that directory's manifest over the entry, and discovers components inside it; with no `skills` path in the manifest, every subdirectory of `skills/` holding a `SKILL.md` is a skill. Paths must be relative and may not contain `..`. Both manifest schemas reject unknown keys ([cursor/plugins schemas](https://github.com/cursor/plugins/tree/main/schemas)), and the Cursor Marketplace lists a plugin only after Cursor reviews it.

`20260903-shipped-skills-are-host-neutral-and-distributions-read-source` made the source skill text the shipped text on every host and kept a copy only where a host cannot read the source tree. The question was where Cursor's manifests live, and whether Cursor needs a copy.

## Decision
Put a Cursor manifest beside the Claude Code one in each source plugin directory — `claude-plugins/manifest-dev/.cursor-plugin/plugin.json` and `claude-plugins/manifest-dev-tools/.cursor-plugin/plugin.json` — and list both in a repo-root `.cursor-plugin/marketplace.json` whose entries mirror `.claude-plugin/marketplace.json`. Neither manifest names a component path, so Cursor's default discovery reads `claude-plugins/*/skills` directly: no copy, no generation step, no change to `scripts/sync_dist.py`. `dist/cursor/` holds the install instructions only.

Both plugins ship, as on Claude Code and Codex, so the optional tools stay optional. Each manifest carries its plugin's version and uses only keys Cursor's schema accepts. The logo is the repository's `assets/logo.png` by absolute raw URL, because a relative path from a plugin directory would need `..`.

The six dependency-only skills keep `user-invocable: false`. Cursor's skill format has no field with that meaning — its `disable-model-invocation` is the inverse, rejected for the same reason in `20260903` — so Cursor lists them in its slash menu, and `dist/cursor/README.md` says so.

## Alternatives Considered
- **A generated plugin under `dist/cursor/plugins/*` with a copied `skills/`, as Codex has**: the shape that keeps every host's packaging under `dist/` — Rejected because Cursor reads the plugin directory straight from the repository, so a copy would add a drift surface with nothing to gain.
- **One manifest at `dist/cursor/` whose `skills` path points at the source directories**: keeps the source plugin directories untouched — Rejected because reaching `claude-plugins/` from there needs `..`, which Cursor forbids.
- **A single combined Cursor plugin**: one listing instead of two — Rejected because it would install the tools with the workflow, unlike every other host, and its name would differ from the Claude Code plugin it tracks.
- **A root Agent Plugins `plugin.json` as well**: the portable format Cursor also loads — Rejected for now because the repository root already holds Pi's `package.json`, a second root manifest would need its own version kept in step, and Cursor, the host this change targets, already reads the Cursor manifests.

## Consequences

### Positive
- Cursor and the hosts that install from its marketplace read the same skill files as every other host, and a skill change needs no regeneration for them.
- The checks that hold the manifests run in the existing test suite; Cursor's own validators pass on the tree.

### Negative
- Each source plugin directory now carries a second host's manifest, so a version bump touches one more file.
- The six dependency-only skills show in Cursor's slash menu.
- The logo URL points at the `main` branch, so a listing reviewed at a commit shows the logo as it is on `main`.

## Enforced by
partly — `tests/test_dist_skill_references.py` — `test_cursor_marketplace_mirrors_the_claude_marketplace`, `test_cursor_plugin_manifests_track_their_source_plugins`, `test_cursor_discovers_the_source_skills_with_no_copy` fail if the Cursor marketplace stops mirroring the Claude Code one, a manifest's name or version drifts from its source plugin or carries a key Cursor's schema rejects, a path is absolute or climbs with `..`, a manifest overrides discovery, a source plugin gains a component Cursor would also load, or anything besides the README appears under `dist/cursor`; whether Cursor accepts the listing stays with Cursor's review.

## Source
- Session: unattended run of 2026-10-21 adding Cursor packaging, executed under a Manifest
- Related: See also 20260903-shipped-skills-are-host-neutral-and-distributions-read-source, 20260531-codex-plugin-native-distribution, 20260611-opencode-plugin-native-distribution
