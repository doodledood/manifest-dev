# ADR: Keep the plugin-first repo layout; no restructure for skill-picker distribution

## Status
Accepted

## Context
An adoption investigation (seeded by the 2026-07-04 handoff report) surfaced individual-skill plunderability as a load-bearing adoption path: strangers adopt fragments, not methodologies. The `npx skills` CLI (vercel-labs/skills, skills.sh ecosystem) is the emerging standard for cross-agent skill installation, and the question arose whether manifest-dev's layout — Claude Code plugins as first-class source under `claude-plugins/`, other CLIs generated into `dist/` — blocks it. A restructure was proposed: demote the Claude Code plugin to `dist/` like the other CLIs and hoist a canonical top-level `skills/` directory as the symlink source, so `npx skills add doodledood/manifest-dev` could offer individual skills.

Empirical test (2026-07-05, run against the live repo): `npx skills add doodledood/manifest-dev --list` finds 24 skills on the current layout, and `--skill figure-out` installs the complete skill (SKILL.md + references/ + tasks/) with the repo's `.claude/skills/` symlinks resolving cleanly. The CLI natively scans `.claude/skills/`, `.agents/skills/`, and paths declared in `.claude-plugin/marketplace.json`/`plugin.json`.

## Decision
Keep the current layout: `claude-plugins/` stays the first-class source of truth, `.claude/skills/` and `.agents/skills/` remain symlink mirrors, and other CLIs stay generated under `dist/`. No top-level `skills/` hoist, no demotion of the Claude Code plugin.

The restructure's sole adoption rationale — skill-picker compatibility — is already satisfied by the existing structure, so the change would buy internal symmetry at the cost of days of churn (plugin path rewiring, sync-tools rewrite, symlink convention migration, docs) with zero adoption delta.

Two small follow-ups were accepted instead (tracked as work items, not part of this decision's structure): mark internal repo-maintenance skills `metadata: internal: true` so the picker doesn't surface them to strangers, and document the `npx skills add doodledood/manifest-dev --skill <name>` install path in the README.

## Alternatives Considered
- **Demote Claude Code plugin to `dist/`, hoist top-level `skills/` as canonical source**: Symmetric multi-dist layout with one neutral source directory — Rejected: its motivating benefit (npx-skills individual install) was verified to already work on the current layout; the remaining benefit is aesthetic symmetry, which does not pay for the migration churn or the risk to the working symlink/plugin conventions.
- **Restructure later as part of a broader multi-dist overhaul**: Deferred rather than rejected — if a future change forces touching all dist wiring anyway, symmetry can ride along; it should be judged then as a maintenance refactor on its own merits, not as an adoption lever.

## Consequences

### Positive
- `npx skills` / skills.sh distribution surface is available immediately, with no build gating it.
- Claude Code plugin conventions (marketplace.json, plugin.json, symlinked `.claude/`) stay stable; sync-tools untouched.
- Adoption work (metadata, README, directory submissions) proceeds without waiting on a structural migration.

### Negative
- Layout asymmetry persists: Claude Code is source, other CLIs are generated artifacts — contributors must keep learning this rule.
- The repo depends on third-party skill-picker CLIs continuing to scan `.claude/skills/` and plugin manifests; if the ecosystem converges on a top-level `skills/` convention as the only scanned path, this decision needs revisiting.

## Source
- Session: figure-out adoption-strategy session, 2026-07-05 (log: `~/.manifest-dev/logs/figure-out-log-20260705-054411.md`)
- Related: 20260611-opencode-plugin-native-distribution, 20260531-codex-plugin-native-distribution
