---
kind: feature
covers: claude-plugins/manifest-dev/skills/design/scripts/design-tools.mjs, claude-plugins/manifest-dev/skills/review-design/scripts/design-check.mjs
---
# design-instruments

Two local command-line tools under the design skills: `design-tools.mjs` measures a supplied HTML page or image (and structured observations) and `design-check.mjs` triages an HTML page. Neither fetches, renders for you, or scores quality.

## How a user reaches it

- Run directly with `node` from the skill directory.
- The design skill's instruments reference (`design/references/instruments/usage.md`).
- review-design's step that runs the HTML check.
- Other `design-tools.mjs` commands: `image <PNG|JPEG|WebP|GIF|RGBA.json> [--artifacts dir]`, `appearance <image|features.json|->`, `journey|data|timeline|survey|content|viewing|palette <JSON>`, and `compare <report.json> --other <report.json>`.

## Scenarios

### catalog
Run: `node claude-plugins/manifest-dev/skills/design/scripts/design-tools.mjs catalog`
Proves: exit `0`; JSON with `version` and an `instruments` object.
Check: read

### inspect
Run: `d=$(mktemp -d) && printf '%s' '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Loans</title></head><body><h1>Loans today</h1><p>42 books out.</p></body></html>' > "$d/page.html" && node claude-plugins/manifest-dev/skills/design/scripts/design-tools.mjs inspect "$d/page.html" --output "$d/inspect.json" && cat "$d/inspect.json"`
Proves: exit `0`; `inspect.json` has `schemaVersion`, `command: "inspect"`, `coverage` and `observations`.
Check: read

### refuses-a-url
Run: `node claude-plugins/manifest-dev/skills/design/scripts/design-tools.mjs inspect https://example.com; test $? -eq 1`
Proves: exit `1` with `Supply a local artifact; the agent owns acquisition`.
Check: read

### html-check
Run: `d=$(mktemp -d) && printf '%s' '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Loans</title></head><body><h1>Loans today</h1><p>42 books out.</p></body></html>' > "$d/page.html" && node claude-plugins/manifest-dev/skills/review-design/scripts/design-check.mjs "$d/page.html"`
Proves: exit `0`; `NOTE`/`OK`/`FINDING` lines, `SKIPPED  render samples` when Playwright is absent, and a closing count line.
Check: read

## Gotchas

- Needs Node 20+; Python 3 for HTML; Pillow for native images; Playwright with Chromium only for design-check's render samples. Commands run from the repository root, and the scratch page and outputs go to a temporary directory outside it.
- Exit `0` means the run completed, findings or not; read the output.
- Without Playwright the render samples are `SKIPPED`, which is not a pass.
- Raster input is capped at 512 px on the long edge.
- `tests/test_design_instruments.py` (runs `tests/fixtures/design-instruments/test-instruments.mjs`) and `tests/test_design_check.py` also check it; `scripts/design-evals/` is the harness for wider experiments and says what it does not measure.
- Not yet driven: the design skill's instruments reference, review-design's HTML check.
