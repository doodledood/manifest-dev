# ADR: Use installed Manifest Dev plugins

## Status
Accepted

## Area
Repo layout

## Context
Published skills were also exposed through repository-local symlinks. Installing the plugin therefore exposed the same skills twice during repository work.

## Decision
Load published skills through installed plugins. Keep plugin source and distribution metadata intact; retain only repository-specific maintenance skills in the local skill directories. Test source changes using a locally installed marketplace. The skills CLI remains a supported alternative distribution for users who choose individual skills.

## Alternatives Considered
- **Keep synchronized copies**: preserves availability without plugins, but creates duplicate discovery and a second update mechanism.
- **Remove copies only**: leaves scripts and setup guidance able to recreate them.

## Consequences

### Positive
- Each harness has one installation owner for Manifest Dev skills.
- Repository-specific skills retain their own source and discovery paths.

### Negative
- Contributors must install the plugin to use its skills in this repository.

## Source
- Supersedes in part 20260705-keep-plugin-first-layout-npx-skills-compatible
