# Running an instrument

The examples below use paths relative to this skill directory. To run from your project, use the installed script's absolute path instead; Playwright resolves from the invoking directory or the skill location. If you run from the skill directory while Playwright is installed in another project, set `DESIGN_TOOLS_PLAYWRIGHT` to that project's module directory.

The scripts travel with the skill; they do not need another skill, an evaluation checkout or the research corpus. All commands produce JSON on stdout, or at `--output`. Failures exit nonzero with an explanation. A completed command is an observation, not a design pass.

## Dependencies and inputs

Use Node.js 20 or newer. Structured JSON commands need only Node. Browser/image/print commands need Playwright 1.48+ and its Chromium browser. Install in the caller's project and invoke the installed script from there (replace the example absolute path):

```sh
npm install --save-dev playwright
npx playwright install chromium
node /absolute/path/to/design/scripts/design-tools.mjs catalog
```

If the module lives elsewhere, set `DESIGN_TOOLS_PLAYWRIGHT` to its module directory. `DESIGN_TOOLS_CHROMIUM` optionally selects an installed compatible Chromium executable. A missing module/browser is an error; there is no empty-report fallback.

Supply trusted local HTML, a loopback URL, a supported image, or JSON. HTML executes in Chromium, so use a trusted artifact. External page requests and WebSockets are blocked by default; file/data/blob and loopback resources are allowed. Blocked origins and page errors are reported, so incomplete assets remain visible. `--allow-network` explicitly permits remote URLs and asset loading; the instruments do not send an artifact to an analysis service. Do not infer an isolation/security guarantee from request interception.

## Browser observations

```sh
node scripts/design-tools.mjs inspect example.html --tools geometry,visibility,typography --spec plan.json --width 1440 --height 900 --artifacts views --output report.json
```

An example plan:

```json
{
  "entities": {"label":"#label", "value":"#value", "other":"#other"},
  "links": [{"id":"label-value", "from":"label", "to":"value", "competitors":["other"]}],
  "groups": [{"id":"decision", "members":["label","value"]}],
  "alignments": [{"id":"values", "members":["value","other"], "axis":"left"}]
}
```

Each named selector must match exactly one element. Select the information meant by the question: a container may include empty padding beyond its text. Include the context that makes an action or value interpretable, such as its disclosure or units. Links declare the semantic relation and competitors; groups declare what the task needs together; alignments declare comparable roles. The model chooses these. Without a plan, instruments still inventory candidates; they do not invent semantic relationships. Alignment axes are `left`, `right`, `top`, `bottom`, `width`, `height`.

`--tools` selects any of `geometry,visibility,typography,copy,color,access,targets,media,motion,image`. Choose as many as help. Options: `--width`, `--height`, `--theme light|dark`, `--motion no-preference|reduce`, `--direction ltr|rtl`, `--text-scale 1.5`, `--images-off`, and `--vision none|blurredVision|achromatopsia|deuteranopia|protanopia|tritanopia`. Text scaling changes CSS font sizes; it is a stress simulation rather than browser zoom. Direction does not translate text or know which icons should mirror. Chromium vision simulation is an inspection aid, not a model of every person's vision.

Saved evidence includes a live viewport screenshot, grayscale/blur/thumbnail views and, when selected, geometry SVG and a local edge-map SVG. The map colors normalize within each image; compare numeric magnitudes under matching parameters rather than colors across maps. `--edge-threshold` (default 0.08) and `--tile-size` (default 16 analysis pixels) are descriptor parameters, not quality thresholds. Active animation can advance between the DOM sample and screenshot: provide a stable state for precise comparisons. Named offscreen elements remain in geometry; check endpoint visibility. CSS clipping is inspected, but internal clipped glyphs, pseudo-elements, shadow roots, frames and unusual paint can exceed coverage. DOM text-node counts change with markup and whitespace tokenization is language-dependent; do not treat totalWords as reading load.

## Image-only evidence

```sh
node scripts/design-tools.mjs image diagram.png --artifacts image-views --output image-report.json
```

PNG, JPEG, WebP, GIF and SVG are decoded in Chromium. Descriptors sample the original image, downscaled to a maximum edge of 512 pixels and composited over white. The preview fits the viewport; vision simulation affects the preview, not the original-pixel descriptors. A GIF contributes the browser-decoded frame, not temporal behavior. Compare matched source dimensions/content and inspect small-size aliasing. No OCR, gaze prediction or learned importance model is included.

## Supplied interaction scenarios

```sh
node scripts/design-tools.mjs probe form.html --spec scenario.json --output trace.json
```

The `probe` command records the supplied steps, then a DOM coverage inventory. Its `--tools` option does not add another instrument; run `inspect` for additional observations.

```json
{"steps":[
  {"action":"fill", "selector":"#email", "value":"sample@example.test"},
  {"action":"click", "selector":"#save", "observe":["#email","#status"], "capture":true},
  {"action":"press", "key":"Tab", "observe":["#status"]}
]}
```

Actions: `click`, `fill`, `press`, `focus`, `hover`, `scroll` (numeric `x`,`y`), `wait` (`ms` 0–30000), `observe`. Targeted actions require one matched selector. Capture adds PNG base64 in that step's JSON record. Observations contain text/value/checked/visibility, active-element identity and geometry, and animation count. Wait is explicit; no arbitrary delay is treated as readiness. Action elapsed time includes automation and waiting, so it is noisy and is not input-to-photon latency. Browser behavior must be supplied by the fixture/application; a declared graph is not an executed interaction.

## Structured declarations

Invoke the command with a JSON file, for example `node scripts/design-tools.mjs journey graph.json`. Missing, duplicate or unknown IDs and invalid numeric inputs are errors where identities or numbers bind the observation.

**Journey:** nodes, directed edges and tasks. Costs must be finite/nonnegative; omitted edge cost is 1. An unreachable destination returns `reachable:false`, `minimumDeclaredCost:null`.

```json
{"nodes":[{"id":"start"},{"id":"saved"}],"edges":[{"from":"start","to":"saved","cost":1}],"tasks":[{"id":"save","from":"start","to":"saved"}]}
```

**Data:** arrays of declared source/display values. Optional `axis` is numeric minimum/maximum; `axisPx` maps them to pixel endpoints (which may descend). Optional `marks` are independently obtained value/position observations on that linear scale. This command does not parse a chart or verify the supplied source. Zero inclusion is information, not a rule for every encoding. Optional `proportional` checks length, area or repeated-count amounts against a supplied positive reference: `{"kind":"area","referenceValue":10,"referenceAmount":20,"observedQuantity":"radius","marks":[{"value":40,"amount":40}]}`. Radius observations under area encoding use a square-root relation. These are declared geometry checks, not extracted chart measurements.

```json
{"series":[{"id":"counts","source":[8,12],"display":[8,12],"units":"items","sourceReference":"fixture","axis":[0,20],"axisPx":[0,200],"marks":[{"value":8,"position":80},{"value":12,"position":120}]}]}
```

**Timeline:** unique event IDs, `start`/`end` in milliseconds, optional text and links. Zero exposure has no defined reading rate.

```json
{"events":[{"id":"label","start":0,"end":2000,"text":"The intake"},{"id":"part","start":500,"end":2500}],"links":[{"from":"label","to":"part"}]}
```

**Content:** unique items and their declared prerequisites, plus the presented ID order. Omitted items remain `present:false`; they do not silently count as introduced.

```json
{"items":[{"id":"concept"},{"id":"example","prerequisites":["concept"]}],"order":["concept","example"]}
```

**Survey:** only actual supplied responses, one response object per respondent, item/axis IDs, scale endpoints and optional `reverse:true`. Missing answers are excluded from item aggregates and incomplete respondent/axis combinations are counted separately; axes are never fused. Models' reactions must be labeled as model evidence outside this command.

```json
{"minimum":1,"maximum":5,"items":[{"id":"clear","axis":"clarity"},{"id":"confusing","axis":"clarity","reverse":true}],"responses":[{"clear":4,"confusing":2},{"clear":3}]}
```

**Viewing:** physical size and distance in millimeters. Returns geometric angle in arcminutes, with no legibility verdict.

```json
{"distanceMm":3000,"elements":[{"id":"caption-height","sizeMm":8}]}
```

## Print and comparisons

```sh
node scripts/design-tools.mjs print report.html --artifacts pages --paper A4
node scripts/design-tools.mjs compare before.json --other after.json
```

Print creates `artifact.pdf` through Chromium print CSS. `--paper A4|Letter` and `--landscape` apply unless CSS supplies page size. Inspect the actual PDF for page breaks, crops and content loss; browser screen measurements cannot establish pagination or native-host fidelity.

Compare aligns object keys and arrays of unique string IDs, plus positional numeric arrays. Unalignable arrays, identity changes and nonnumeric changes are listed explicitly. Automatically assigned DOM IDs can change after edits; rely on stable named entities for comparisons. `scopeMatched:false` is a reason to investigate changed conditions. No delta has an inherent good direction. Keep the original reports to interpret meaning and coverage.

**Palette:** named opaque six-digit sRGB hex colors. Optional pairs select the relevant contrast/distinction topology (all pairs otherwise); optional order describes a ramp. Oklab distances use 0–1 coordinate units, not CIELAB ΔE units, and have no built-in success cutoff. Inspect actual colors and vision previews separately.

```json
{"colors":[{"id":"ink","hex":"#102938"},{"id":"paper","hex":"#ffffff"}],"pairs":[["ink","paper"]],"order":["ink","paper"]}
```

The Oklab conversion follows [Ottosson's published equations](https://bottosson.github.io/posts/oklab/), available in the public domain. Wide-gamut color, alpha compositing and a palette's cultural/semantic fitness remain outside this command.
