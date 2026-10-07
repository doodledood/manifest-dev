# Design instrument experiments

This harness evaluates the optional instruments shipped with `design`, then creates a local blind comparison gallery. It checks constructed geometric, semantic and behavioral facts. It does **not** measure human preference, task speed, comprehension or the design skill's causal improvement over an unassisted model.

## Run

Use Node.js 20+, Playwright 1.48+ with Chromium, Python with `pypdf`, and Poppler's `pdftoppm`. The last two are development dependencies for extracting and rendering the actual printed PDF; ordinary instrument users do not need them. Install these in an existing development environment rather than in the skill distribution.

```sh
npm install --save-dev playwright
npx playwright install chromium
python3 -m pip install pypdf
node scripts/design-evals/run.mjs /tmp/design-instruments-review
python3 -m http.server 8765 --bind 127.0.0.1 --directory /tmp/design-instruments-review
```

Open `http://127.0.0.1:8765`. The output directory contains HTML alternatives, observations, interaction traces, screenshots, printed PDFs and their rasterized pages. Keep it outside the checkout: these are review artifacts, not shipped skill data.

An explicit output directory must not already exist, and its parent must exist. Each rerun uses a fresh directory, so a failed run cannot mix new artifacts into a prior successful gallery. Omitting the argument creates a unique temporary directory and prints its location.

For dependencies installed elsewhere, set `DESIGN_TOOLS_PLAYWRIGHT` to the module directory, `DESIGN_EVAL_PYTHON` to the Python executable with `pypdf`, and `DESIGN_EVAL_PDFTOPPM` to the `pdftoppm` executable. `DESIGN_TOOLS_CHROMIUM` optionally selects a compatible Chromium executable. Missing dependencies fail rather than producing empty evidence.

The focused regressions run with:

```sh
DESIGN_TOOLS_TEST_BROWSER=1 node --test tests/fixtures/design-instruments/test-instruments.mjs
```

Without `DESIGN_TOOLS_TEST_BROWSER=1`, browser regressions explicitly skip; a skipped run does not establish browser behavior. The Python property suite also invokes these regressions through `tests/test_design_instruments.py`.

## Evidence and splits

`calibration.mjs` compares baseline/refined measurements with authored known relations. Its training cases and development challenge cases were available during refinement. They are regressions, **not untouched holdouts**. A spacing-cutoff search uses only training cases, but its challenge results still do not establish a universal grouping threshold.

`fixtures.mjs` supplies twelve fictional gallery families: dashboard, form, chart, article, explainer, game, reading deck, poster, mixed-direction transfer, email, printed report and explorable. Six develop the tools; six transfer the approach to other artifact families. All twelve were available during development. Their different jobs and content do not establish broad stylistic generalization, native-host fidelity or a representative sample of real products. The internal `heldout` tag labels the latter gallery group; the gallery calls it “Transfer families” to avoid implying untouched data.

`transfer.mjs` supplies a separate six-case evaluation, specified in an independent review context after the instrument code was frozen, before its first execution. It covers common-region ownership, a clipped departure notice, a descending linear scale, audio-tour intervals, dialog cancellation/focus and recipe prerequisites. [transfer-freeze.json](transfer-freeze.json) records those initial instrument and case hashes; each run also records the current instrument hashes. The cases were not used to retune the measurements. Subsequent reviews repaired browser compatibility/resource reporting and consolidated CLI registration/artifact manifests; these adapter repairs leave the measurement algorithms intact. Reruns use the now-known cases as regressions. Their expected facts come from the independent fixture specification, not from the instruments' output. Six cases remain a small constructed sample; a successful factual check is not a UX-quality success.

`run.mjs` invokes the public CLI, including every advertised command, selected browser simulations, malformed inputs and a copied standalone skill. It also renders deliberately misleading edits and a six-candidate dashboard spacing search. It compares actual rendered table text with the incumbent before accepting a search candidate. PDF text extraction and page rasterization are both retained: extraction alone cannot reveal clipped glyphs.

The gallery initially conceals which side is original/revised and all measurement explanations. Choices are empty until supplied by the reviewer. A revelation is remembered across reload, so later choices remain marked as informed. Judgments are stored under the fixture hash in the local browser and can be exported. Changing fixtures starts a separate set of choices. This supports an owner comparison, not a controlled population study.

## Recorded result — 2026-10-07

The committed [summary.json](summary.json) records the actual run and source hashes. It contains no participant responses or owner preferences.

| Diagnostic | Baseline → refinement | Result and decision |
|---|---|---|
| Named proximity | Center distance → edge gap relative to competitors, in label em | Training agreement 3/4 → 4/4; development challenges 1/5 → 4/5. Retain distances; withhold a general cutoff. A connector exception remains unfavorable. |
| Named box availability | Size/visibility flags → viewport and ancestor-clip intersection | Training agreement 2/3 → 3/3; challenges 0/3 → 3/3. Retain bounded box observations; internal glyph clipping and paint occlusion still need inspection. |
| Pixel variation | Centered derivative → forward adjacent differences | Both derivatives agree on three training patterns; refinement detects both fine checkerboards missed by baseline. Retain a pixel descriptor, not a complexity, gaze or beauty score. |
| Independent transfer | Frozen instruments → six newly specified cases | All six expected factual checks pass, including the expected **negative** proximity margin in an enclosure-owned layout. That proxy is inapplicable there; this is not six quality successes. |
| Dashboard search | Six requested CSS margins, 8–350 px | Four candidates expose both named facts and preserve table text. The 20 px CSS margin is an author choice on a plateau; 8 px and 20 px render identically because adjacent margins collapse. Requested margin is not measured separation, and the choice has no numerical superiority over the other three. |

The run reports zero failed checks. Independent reviews also exercised browser behavior and inspected rendered gallery/PDF evidence. The printed baseline loses portions of glyphs under its print CSS; the revision is legible over two pages. The text extractor alone had retained those strings, illustrating why it cannot clear print fidelity.

### Unfavorable results retained

- Reducing article words deletes the decisive study qualification. The shorter candidate is rejected.
- Co-visibility can improve by shrinking important type; physical size and actual viewing conditions still matter. This counterexample is reasoned, not a measured reader outcome.
- A fabricated one-step journey graph reports a short route while the executed form fails recovery. Declared graph quality cannot establish actual behavior.
- Independent per-row chart widths, premature calculator rounding/stale state, a counter that answers only the first tap, image-only email actions and hidden print content violate separately specified facts.
- High text contrast does not distinguish three crossing series drawn in the same color. A rendered monochrome chart retains this failure.
- Hidden hit boxes, ancestor clipping and unsupported paint are exposed separately from nominal dimensions or contrast numbers.
- A zero-duration text event has no defined reading rate. Fabricated survey responses are invalid evidence, regardless of their aggregate.

Not every attack is an executed artifact: `summary.json` labels executed cases and reasoned counterexamples separately. No single direction is desirable for total words, edge density, animation count, path length or spacing. Neither the runtime skill nor this harness has a composite quality score or a required optimization loop.

## Limits and future calibration

Research coverage is broader than these constructed checks. The [runtime basis map](../../claude-plugins/manifest-dev/skills/design/references/instruments/basis.md) accounts for contextual concerns such as expression, emotion, trust, novelty, fun and audience learning. A local adjacent-pixel map is not the published feature-congestion model; no learned visual-importance model is bundled. Native slides, actual email clients, assistive announcements, touch hardware, physical projection and audience outcomes remain outside this adapter's evidence.

To claim design uplift, add a separately specified set of real briefs, an unassisted comparison arm, blinded audience judgments or task outcomes, and repeated runs that expose model and judge noise. Keep independent outcome axes and unfavorable cases. A later instrument refinement requires a fresh transfer set; rerunning these now-known cases supplies regression evidence only.
