# ADR: Each Cursor plugin ships its own plated logo

## Status
Accepted

## Area
Cursor distribution

## Decided by
An agent in an unattended run, with no review

## Context
`20261021-cursor-plugin-reads-the-source-plugin-directories` pointed both Cursor manifests at the repository's `assets/logo.png` by absolute raw URL on `main`, because a relative path from a plugin directory to the repository root would need `..`, which Cursor forbids.

Preparing the Cursor Marketplace listing brought two needs that record did not weigh. Cursor's submission checklist asks for a logo committed to the repository and referenced by a relative path ([plugins docs](https://cursor.com/docs/plugins), *Submission checklist*), and its schema resolves a relative `logo` against the plugin root ([plugins reference](https://cursor.com/docs/reference/plugins)). The publisher application asks for a "1:1 SVG or PNG with background plate" ([publish form](https://cursor.com/marketplace/publish)). `assets/logo.png` must stay transparent, since `tests/test_logo_assets.py` holds it transparent for the README on GitHub's dark mode and the Pages favicon. The `..` premise still holds; the absolute URL was just one way to meet it.

## Decision
Each Cursor plugin carries its own logo at `claude-plugins/<plugin>/assets/logo.png`, and its `.cursor-plugin/plugin.json` names it as `"logo": "assets/logo.png"`. The file is `assets/logo.png` composited, at the same 512×512 size, onto an opaque square plate in the site's dark card colour (`#0f131b`), and both plugins carry byte-identical copies. The transparent `assets/logo.png` stays the brand mark everywhere else.

A relative path inside the plugin needs no `..`, follows Cursor's checklist, and pins the logo to the reviewed commit rather than to whatever `main` holds later.

## Alternatives Considered
- **Keep the absolute raw URL on `main`**: no file copies — Rejected because the checklist asks for a relative path, the listing would show whatever logo `main` holds rather than the reviewed one, and the transparent mark is not the plated logo the application asks for.
- **Plate `assets/logo.png` itself**: one file for every use — Rejected because the README and favicon need the transparent field, which `tests/test_logo_assets.py` protects.
- **Generate the plated copies in `scripts/sync_dist.py`**: no committed derivative — Rejected because compositing PNGs needs an image library the script does not use, and a test can hold the copies to the source mark without one.

## Consequences

### Positive
- The listing's logo is committed, relative and reviewed with the rest of the plugin.
- The publisher application can use one plugin copy's raw URL as its logotype.

### Negative
- Two derived binaries sit in the tree, and a change to the brand mark must regenerate both.

## Enforced by
`tests/test_logo_assets.py` — `test_cursor_plugin_logos_are_the_mark_on_an_opaque_square_plate` fails when a plugin logo is missing, not square, has any transparent pixel, differs between the plugins, or no longer matches `assets/logo.png` wherever the mark is opaque; `tests/test_dist_skill_references.py` — `test_cursor_plugin_manifests_track_their_source_plugins` fails when a Cursor manifest's `logo` is not a safe relative path to a file inside its plugin.

## Source
- Session: unattended run of 2026-11-03 preparing the Cursor Marketplace listing
- Related: Narrows 20261021-cursor-plugin-reads-the-source-plugin-directories
