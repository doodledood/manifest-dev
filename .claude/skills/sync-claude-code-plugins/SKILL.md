---
name: sync-claude-code-plugins
description: 'Sync the prompt-engineering plugin from a local clone of claude-code-plugins into .claude/ so the repo is self-contained for isolated/web environments. Copies agents/skills, removes only previously-synced items that disappeared upstream. Other content in .claude/ is left alone. Use when asked to sync claude-code-plugins, pull prompt-engineering, refresh prompt-engineering plugin.'
user-invocable: true
metadata:
  internal: true
---

**User request**: $ARGUMENTS

Sync prompt-engineering plugin components from a local sibling clone of `claude-code-plugins` into this repo's `.claude/` directory. The plugin OWNS only the files it ships — other content in `.claude/agents/` and `.claude/skills/` (manifest-dev sync, KB skills, anything else) must be left alone.

## Source & Target

| Role | Path |
|------|------|
| Source repo | `../claude-code-plugins` (relative to this repo's root) |
| Source components | `<source_repo>/claude-plugins/prompt-engineering/` |
| Target | `.claude/` in this repo |
| Tracking file | `.claude/.claude-code-plugins-sync.json` |

## Sync scope

| Component | Source dir | Target dir |
|-----------|-----------|------------|
| Agents | `agents/` | `.claude/agents/` |
| Skills | `skills/` | `.claude/skills/` |

prompt-engineering ships no hooks today.

## Territory model

**Deletion invariant**: only items in `tracked` (the previously-synced set) are eligible for removal when they disappear upstream. Items never in `tracked` are invisible — that's how project-local content stays safe.

The tracked set lives in `.claude/.claude-code-plugins-sync.json`:

```json
{
  "version": 1,
  "last_synced_at": "ISO-8601 timestamp",
  "agents": ["prompt-reviewer.md", "..."],
  "skills": ["prompt-engineering", "..."]
}
```

First run (file missing): `tracked` is empty, no deletions happen, file is written at end.

## Sync algorithm

Pre-flight: abort if `<source_repo>/claude-plugins/prompt-engineering/` is missing — silent absence is a misconfigured path, not upstream removal. Do not delete on this signal. If the source is a clean git repo, `git pull --ff-only` first; surface a warning and proceed if pulling fails.

For each component (agents/skills):

- **Copy** every source item over its target path. Skip if target is a symlink. **Skip retired items** (see denylist below) even when an older upstream checkout still ships them.
- **Re-apply local metadata** after copying: every non-symlink synced skill's `SKILL.md` must carry `metadata:` / `internal: true` in its frontmatter — add it back when the upstream copy lacks it. Synced skills are repo-maintenance tooling in this repo; the flag keeps skill pickers and directory scrapers from listing them as product skills.
- **Delete** items in `tracked − source` from target. Skip if target is a symlink, doesn't exist, or is the `sync-claude-code-plugins` skill itself.
- **Refresh** `.claude/.claude-code-plugins-sync.json` with the current source listing **minus the denylist**.

Source listing excludes `README.md` and `.claude-plugin/` (plugin metadata, not content).

**Retirement denylist** (never copy or track, regardless of upstream): `agents/prompt-reviewer.md`. manifest-dev-tools ships its own `review-prompt` skill (plugin-owned symlink at `.claude/skills/review-prompt`) and manifest-dev ships **zero agents**, so the upstream prompt-engineering `prompt-reviewer` agent must not be reintroduced — it is already removed from `.claude/agents/` and dropped from the tracked set.

## .agents mirror

After each sync, ensure `.agents/skills/<name>` is a symlink to `../../.claude/skills/<name>` for every tracked skill, and remove the symlink for any skill removed from `tracked`. This lets non-Claude coding agents (Codex, etc.) read the same skills without duplicating content. Only skills are mirrored — `.agents/agents/` is out of scope.

- Create the symlink if missing.
- If `.agents/skills/<name>` exists and is not a symlink, skip it — that's project-local content, don't clobber.
- Create `.agents/skills/` if missing, but never `.agents/` itself (the user opts in by creating it).

## Gotchas

- **Upstream copies drop the internal flag.** Upstream `claude-code-plugins` skills ship without `metadata: internal: true`; a plain copy silently reverts the flag on the non-symlink synced skills (observed 2026-07-05). The re-apply step above exists for this — do not skip it.

- **Source must exist**: missing source path means abort, not "delete all tracked items."
- **Nested skills directory**: source skills live at `skills/prompt-engineering/`, `skills/compress-prompt/`, etc. Copy each skill directory into `.claude/skills/<skill-name>/` — don't copy the outer `skills/` folder or you get `.claude/skills/skills/`.
- **`review-prompt` is plugin-owned, not upstream**: manifest-dev-tools ships its own `review-prompt` skill, symlinked at `.claude/skills/review-prompt`. The upstream prompt-engineering plugin also ships a `review-prompt`, but the "skip if target is a symlink" rule above means this sync leaves the plugin's symlink alone (it neither overwrites nor deletes it). Do not re-add `review-prompt` to the tracking file.
- **Symlinks look like directories to `cp`/`rm`/`find`**: a symlinked target overwritten by `cp -R` corrupts the linked plugin's source files; a symlinked directory deleted by `rm -rf` removes the link, not the plugin, but a recursive find that follows the link will. Use `[ -L path ]` before every overwrite and every delete.

## Output

Summary table per component (agents/skills): items added, updated, removed, symlinks skipped, and removals refused (e.g. due to symlink). Show the net change to the tracking file.

## Never

- Overwrite, remove, or follow into symlinks under `.claude/` — check `[ -L path ]` before every copy, delete, or recursive descent
- Replace a non-symlink at `.agents/skills/<name>` — leave project-local content alone
- Create `.agents/` itself (only manage `.agents/skills/<name>` entries inside an existing `.agents/`)
- Delete items not in the tracked set — even if they're not in source
- Delete the `sync-claude-code-plugins` skill
- Treat a missing source path as upstream removal — abort instead
- Copy plugin metadata (`README.md`, `.claude-plugin/`) or the source repo's own `.claude/` directory
- Modify the source repo (other than the optional `git pull --ff-only`)
