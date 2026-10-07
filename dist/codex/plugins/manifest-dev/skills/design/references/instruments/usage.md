# Supplying evidence to an instrument

The agent obtains artifacts and observations with the tools available in its environment. These scripts analyze local inputs; they do not open a browser, fetch resources, execute HTML, take screenshots, run interactions or export documents. Supply a screenshot, an HTML/text file, measured observations or a structured declaration. PDF pages and video frames can be supplied as images; obtain their text, timing or interaction evidence separately when the question needs it.

Paths below are relative to the installed design skill. Use the installed script's absolute path from your project. Commands return JSON on stdout or at `--output`; errors exit nonzero. `catalog` and `--help` list the current interface.

## Inputs and dependencies

| Input | Supported evidence | Runtime |
|---|---|---|
| Observations/declarations JSON | Selected supplied fields and arithmetic | Node.js 20+ |
| Text or Markdown | Text counts/repeated strings; Markdown is treated as text | Node.js 20+ |
| HTML source | Source text, headings, label/control attributes, language and media declarations | Node.js 20+ and Python 3 |
| PNG, JPEG, WebP, GIF | Decoded image variation and derived inspection views | Node.js 20+, Python 3 and Pillow |
| RGBA JSON | Supplied bounded pixels; no decoder required | Node.js 20+ |

HTML extraction uses Python's standard library. Image decoding uses the established Pillow library rather than a custom decoder. Install Pillow in the Python environment when needed; `DESIGN_TOOLS_PYTHON` selects another interpreter. JSON/text tools do not need Python. Neither path needs a browser installation or an analysis service.

Each instrument needs only the evidence its question requires. Source HTML cannot establish layout, computed paint, actual pointer reception or motion. Supplied observations can come from a browser, native app, design tool, screenshot annotations or another source. Record the collection method, artifact/state, viewport/crop and coordinate units in `scope`; keep estimates distinct from measurements. Missing evidence is unmeasured or rejected, never an empty success.

## HTML and text

```sh
node scripts/design-tools.mjs inspect screen.html --tools copy,access,media --output source-report.json
node scripts/design-tools.mjs inspect article.md --tools copy
```

HTML's default instruments are `copy,access,media`; text defaults to `copy`. Hidden-by-CSS source text can appear in the inventory. Scripts, styles, templates and head text are excluded; scripts and external resources are not executed or fetched. This is a source parser, without browser tree repair or accessible-name computation. Labels and attributes are candidates, not complete accessible names. Hidden inputs are excluded from action candidates. Declared image dimensions do not establish actual rendered dimensions or crop.

## Supplied observations

```sh
node scripts/design-tools.mjs inspect observations.json --tools geometry,visibility --spec plan.json --output report.json
```

A minimal observation for geometry/visibility:

```json
{
  "scope": {"artifact":"screen.png", "coordinateUnits":"image pixels", "method":"supplied region annotations"},
  "viewport": {"x":0,"y":0,"width":390,"height":844},
  "entities": {
    "label": {"box":{"x":20,"y":20,"width":80,"height":20},"visible":true},
    "value": {"box":{"x":20,"y":48,"width":160,"height":32},"visible":true}
  }
}
```

An optional plan, also accepted as the input's `plan` field:

```json
{"links":[{"id":"label-value","from":"label","to":"value"}],"groups":[{"id":"decision","members":["label","value"]}],"alignments":[{"id":"left-edges","members":["label","value"],"axis":"left"}]}
```

The caller names relationships, competitors and facts needed together. Boxes use pixel coordinates (CSS pixels or image pixels); convert other units before supplying them and record the conversion. Boxes must share a coordinate system and have finite `x,y,width,height`; dimensions are nonnegative. Geometry retains pixel gaps when `fontSize` is absent and returns null em distances. Alignment axes are `left,right,top,bottom,width,height`.

Visibility requires a viewport and observed `visible` booleans. Supply `visibleBox` when the evidence establishes the area remaining after ancestor clipping. Without it, viewport containment is reported but ancestor clipping and full co-visibility remain unmeasured unless another known failure already settles the result. Select the information itself: empty container padding is not the text, and a button's relevant context may include its disclosure or units. Boxes do not establish every paint occlusion or internal glyph clipping.

Other fields are supplied only when selecting their instrument:

| Instrument | Fields |
|---|---|
| `copy` | `nodes`: records with `text`; optional `headings` and `controls` |
| `typography` | `nodes` with measured `lines` and positive `fontSize`; optional font/weight/lineHeight/box and `glyphWidths` |
| `color` | `nodes` with `color`, nearest-first `backgrounds` and explicit `paintEffects` exclusions |
| `access` | `controls`; optional `headings,media,languages` |
| `targets` | `controls` with boxes; optional `points` containing measured pointer reception |
| `media` | `media` asset records |
| `motion` | `animations` timing records |

Text records need not have unique parent IDs: fragmented text can share an element. Line counts/fonts are not inferred from source. Color supports opaque `rgb()/rgba()` samples; unsupported/translucent/layered paint remains unmeasured. Supplying an empty paint-effects array is a claim about inspected coverage. Target boxes alone do not establish hit reception; missing pointer samples are listed explicitly. Timing records establish only their supplied state.

## Images

```sh
node scripts/design-tools.mjs image screenshot.png --artifacts views --output image-report.json
```

Descriptors use supplied image pixels, composited over white and downsampled with Pillow LANCZOS to a maximum edge of 512. Reports record decoder/version/resampling; compare matched crops, content and analysis parameters. EXIF orientation is applied; embedded ICC profiles are not transformed. GIF uses the first frame, not temporal behavior. SVG rasterization belongs to acquisition: supply a raster image.

`--artifacts` writes an edge-map SVG plus grayscale, blur and thumbnail PNGs for native images. These are transforms of supplied pixels, not new captures or eyesight simulations. Map colors normalize within each image; numeric magnitudes are needed for comparisons across maps. `--edge-threshold` (0.08) and `--tile-size` (16 analysis pixels) are descriptor parameters, not quality thresholds. No OCR, gaze, congestion or learned importance predictor is included.

A decoder-free input is `{"width":2,"height":2,"data":[...16 integer RGBA bytes...]}`. Dimensions must be positive and maximum edge 512; alpha is composited over white. The supplied resolution is retained. No original size, frame or resampling provenance is inferred. RGBA analysis can emit the edge map; other views require a native image.

## Structured declarations

Invoke `node scripts/design-tools.mjs <command> input.json`. JSON/text inputs also accept `-` for stdin. Missing/duplicate/unknown IDs and invalid numeric values fail where they bind the computation.

| Command | Supplied input and interpretation |
|---|---|
| `journey` | `nodes:[{id}], edges:[{from,to,cost}], tasks:[{from,to}]`. Nonnegative finite costs; default edge cost 1. Unreachable destinations retain `reachable:false` and null cost. Declared routes do not predict human effort. |
| `data` | `series:[{id,source:[values],display:[values],axis:[min,max],axisPx:[start,end],marks:[{value,position}]}]`. Independent source values/mark coordinates are caller-owned. Optional `proportional` checks length/area/count against supplied references. |
| `timeline` | `events:[{id,start,end,text}], links:[{from,to}]`, milliseconds. Zero exposure has no defined reading rate. No recommended timing or comprehension verdict. |
| `content` | `items:[{id,prerequisites:[ids]}], order:[ids]`. Presence and prerequisite order only; missing items remain missing. |
| `survey` | `minimum,maximum,items:[{id,axis,reverse}],responses:[{itemId:value}]`. Actual responses, separate axes and missingness; no fabricated participants or composite score. |
| `viewing` | `distanceMm,elements:[{id,sizeMm}]`. Geometric angular size, not a legibility threshold. |
| `palette` | `colors:[{id,hex}],pairs:[[id,id]],order:[ids]`. Opaque six-digit sRGB, Oklab/OKLCH distances and contrast; no aesthetic/semantic verdict. Conversion follows [Ottosson's equations](https://bottosson.github.io/posts/oklab/). |

## Comparisons

```sh
node scripts/design-tools.mjs compare before.json --other after.json
```

Comparison matches object keys and arrays of unique IDs, plus positional numeric arrays. Identity changes, unalignable arrays and nonnumeric changes remain explicit. Keep source reports and use stable named entities. No delta has an inherent good direction; changed state, units, decoder or crop can make a comparison inappropriate. Inspect the artifact before retaining an edit.
