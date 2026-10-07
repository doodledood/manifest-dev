import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, readFile, cp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";
import {
  associations,
  coVisibility,
  contrast,
  content,
  fidelity,
  journey,
  timeline,
  survey,
  palette,
  viewing,
  compare,
} from "../../../claude-plugins/manifest-dev/skills/design/scripts/measurements.mjs";
import {
  describePixels,
  heatmapSvg,
} from "../../../claude-plugins/manifest-dev/skills/design/scripts/pixels.mjs";
const skill = fileURLToPath(
  new URL(
    "../../../claude-plugins/manifest-dev/skills/design",
    import.meta.url,
  ),
);
const cli = join(skill, "scripts/design-tools.mjs");
const capture = fileURLToPath(
  new URL("../../../scripts/design-evals/capture.mjs", import.meta.url),
);
const dir = await mkdtemp(join(tmpdir(), "design-instrument-tests-"));
function run(args, script = cli, env = process.env) {
  const result = spawnSync(process.execPath, [script, ...args], {
    encoding: "utf8",
    env,
    timeout: 35000,
  });
  return result;
}
function observation(args, script = cli) {
  const r = run(args, script);
  assert.equal(r.status, 0, r.stderr);
  return JSON.parse(r.stdout);
}
async function fixture(name, body, css = "", script = "") {
  const path = join(dir, name);
  await writeFile(
    path,
    `<!doctype html><html lang="en"><meta charset="utf-8"><style>body{background:white;color:black}${css}</style><body>${body}<script>${script}</script></body></html>`,
  );
  return path;
}
async function json(name, value) {
  const path = join(dir, name);
  await writeFile(path, JSON.stringify(value));
  return path;
}
function captured(args) {
  return observation(args, capture);
}
function captureRun(args) {
  return run(args, capture);
}
const browser = { skip: process.env.DESIGN_TOOLS_TEST_BROWSER !== "1" };

test("edge gap handles a wide semantic target and surfaces endpoint status", () => {
  const entities = {
    label: {
      box: { x: 0, y: 0, width: 60, height: 20 },
      fontSize: 20,
      visible: true,
    },
    target: { box: { x: 0, y: 24, width: 800, height: 40 }, visible: true },
    other: { box: { x: 100, y: 0, width: 40, height: 20 }, visible: false },
  };
  const result = associations(
    [{ from: "label", to: "target", competitors: ["other"] }],
    entities,
  )[0];
  assert.equal(result.intendedGapPx, 4);
  assert.equal(result.gapInLabelEm, 0.2);
  assert.equal(result.competitorMinusIntendedEm, 1.8);
  assert.deepEqual(result.endpointVisibility, { from: true, to: true });
});
test("visibility distinguishes dimensional fit from actual clipping/viewport position", () => {
  const viewport = { x: 0, y: 0, width: 300, height: 200 };
  const e = {
    box: { x: 20, y: 100, width: 80, height: 30 },
    visibleBox: { x: 20, y: 100, width: 80, height: 0 },
    visible: true,
  };
  const r = coVisibility(
    [{ id: "needed", members: ["e"] }],
    { e },
    viewport,
  )[0];
  assert.equal(r.boundsFitViewport, true);
  assert.equal(r.allFullyVisibleNow, false);
  assert.deepEqual(r.fullyVisible, []);
});
test("contrast known extremes and exact nonrounded ratio", () => {
  assert.equal(contrast([0, 0, 0], [1, 1, 1]), 21);
  assert.equal(contrast([1, 1, 1], [1, 1, 1]), 1);
  assert(contrast([112 / 255, 120 / 255, 125 / 255], [1, 1, 1]) < 4.5);
});
test("linear mark coordinates expose mismatch independently of value equality", () => {
  const r = fidelity({
    series: [
      {
        id: "bars",
        source: [10, 20],
        display: [10, 20],
        axis: [0, 100],
        axisPx: [0, 200],
        marks: [{ value: 20, position: 80 }],
      },
    ],
  })[0];
  assert.equal(r.differences.length, 0);
  assert.equal(r.marks[0].positionErrorPx, 40);
});
test("journey preserves unreachable state and nonnegative weighted costs", () => {
  const graph = {
    nodes: [{ id: "a" }, { id: "b" }, { id: "c" }],
    edges: [{ from: "a", to: "b", cost: 2 }],
    tasks: [
      { from: "a", to: "b" },
      { from: "a", to: "c" },
    ],
  };
  const r = journey(graph);
  assert.equal(r[0].minimumDeclaredCost, 2);
  assert.equal(r[1].reachable, false);
  assert.equal(r[1].minimumDeclaredCost, null);
  assert.throws(
    () => journey({ ...graph, edges: [{ from: "a", to: "b", cost: -1 }] }),
    /nonnegative/,
  );
});
test("timeline distinguishes undefined zero exposure from real rate", () => {
  const r = timeline({
    events: [
      { id: "zero", start: 0, end: 0, text: "Keep this qualification" },
      { id: "normal", start: 0, end: 2000, text: "Four words live here" },
    ],
    links: [{ from: "zero", to: "normal" }],
  });
  assert.equal(r.events[0].wordsPerSecond, null);
  assert.equal(r.events[1].wordsPerSecond, 2);
  assert.throws(
    () =>
      timeline({
        events: [
          { id: "same", start: 0, end: 1 },
          { id: "same", start: 0, end: 1 },
        ],
      }),
    /unique/,
  );
});
test("survey keeps complete respondent axes and reverse scoring separate", () => {
  const r = survey({
    minimum: 1,
    maximum: 5,
    items: [
      { id: "good", axis: "clarity" },
      { id: "bad", axis: "clarity", reverse: true },
      { id: "fun", axis: "feeling" },
    ],
    responses: [
      { good: 4, bad: 2, fun: 5 },
      { good: 1, fun: 2 },
    ],
  });
  assert.equal(r.axes[0].mean, 4);
  assert.equal(r.axes[0].completeResponses, 1);
  assert.equal(r.axes[0].excludedIncomplete, 1);
  assert.equal(r.axes[1].mean, 3.5);
  assert.throws(
    () =>
      survey({
        minimum: 1,
        maximum: 5,
        items: [{ id: "x" }],
        responses: [{ x: 6 }],
      }),
    /outside/,
  );
});
test("content missing items do not become introduced prerequisites", () => {
  const r = content({
    items: [{ id: "concept" }, { id: "example", prerequisites: ["concept"] }],
    order: ["example"],
  });
  assert.equal(r.items[0].present, false);
  assert.equal(r.items[1].prerequisites[0].introducedEarlier, false);
  assert.throws(
    () => content({ items: [{ id: "x" }], order: ["bad"] }),
    /unknown/,
  );
});
test("palette Oklab reference colors and declared topology", () => {
  const r = palette({
    colors: [
      { id: "black", hex: "#000000" },
      { id: "white", hex: "#ffffff" },
      { id: "red", hex: "#ff0000" },
    ],
    pairs: [["black", "white"]],
  });
  assert.deepEqual(r.colors[0].oklab, [0, 0, 0]);
  assert(Math.abs(r.colors[1].oklab[0] - 1) < 1e-7);
  assert(Math.abs(r.colors[2].oklab[0] - 0.627955) < 1e-6);
  assert.equal(r.comparisons.length, 1);
  assert.equal(r.comparisons[0].contrastRatio, 21);
  assert.throws(
    () => palette({ colors: [{ id: "x", hex: "#fff" }] }),
    /six-digit/,
  );
});
test("viewing describes angle without a readability pass", () => {
  const r = viewing({
    distanceMm: 100,
    elements: [{ id: "size", sizeMm: 200 }],
  });
  assert.equal(r.elements[0].angleArcMinutes, 5400);
  assert(!("pass" in r));
});
test("adjacent-pixel descriptor sees checkerboard cancellation case", () => {
  const data = [];
  for (let y = 0; y < 8; y++)
    for (let x = 0; x < 8; x++) {
      const v = (x + y) % 2 ? 255 : 0;
      data.push(v, v, v, 255);
    }
  const r = describePixels(data, 8, 8);
  assert.equal(r.edgeFraction, 1);
  assert(r.meanGradient > 1);
  assert.equal(r.luminanceHistogramEntropyBits, 1);
  assert.throws(() => describePixels([], 8, 8), /matching RGBA/);
});
test("compare aligns stable ids after reorder and discloses missing identity", () => {
  const r = compare(
    {
      observations: {
        items: [
          { id: "x", gap: 20 },
          { id: "y", gap: 4 },
        ],
        raw: [{ gap: 1 }],
      },
    },
    {
      observations: {
        items: [
          { id: "y", gap: 4 },
          { id: "x", gap: 8 },
        ],
        raw: [{ gap: 0 }],
      },
    },
  );
  assert.equal(r.numericDeltas.length, 1);
  assert.equal(r.numericDeltas[0].delta, -12);
  assert(r.unmatched.some((p) => p.includes("array identities")));
});
test("public structured CLI and actionable errors", async () => {
  const path = await json("data.json", {
    series: [{ id: "n", source: [2], display: [3] }],
  });
  assert.equal(
    observation(["data", path]).observations.data[0].differences[0].display,
    3,
  );
  for (const [args, text] of [
    [["inspect", path], "needs --tools"],
    [["data", join(dir, "missing")], "Cannot read JSON"],
    [["image", path], "positive dimensions"],
    [["--bogus"], "Unknown option"],
  ]) {
    const r = run(args);
    assert.notEqual(r.status, 0);
    assert(r.stderr.includes(text), r.stderr);
  }
});
test("harness retries cannot mix artifacts with a prior successful gallery", async () => {
  const previous = join(dir, "prior-run");
  await mkdir(previous);
  await writeFile(join(previous, "index.html"), "Previous gallery");
  await writeFile(join(previous, "before.html"), "Previous artifact");
  const runner = fileURLToPath(
    new URL("../../../scripts/design-evals/run.mjs", import.meta.url),
  );
  const r = run([previous], runner);
  assert.notEqual(r.status, 0);
  assert(r.stderr.includes("Output directory already exists"), r.stderr);
  assert.equal(
    await readFile(join(previous, "index.html"), "utf8"),
    "Previous gallery",
  );
  assert.equal(
    await readFile(join(previous, "before.html"), "utf8"),
    "Previous artifact",
  );
});
test(
  "development acquisition feeds the shared observation algorithms",
  browser,
  async () => {
    const isolated = join(dir, "isolated");
    await cp(skill, isolated, { recursive: true });
    const html = await fixture(
      "all with spaces.html",
      '<main><h1>Compare</h1><label for="n">Count</label><input id="n" type="number" inputmode="numeric" autocomplete="off" value="11"><p id="value">12 items</p><button id="save">Save</button><img alt="" width="16" height="16" src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22/%3E"></main>',
    );
    const spec = await json("all-plan.json", {
      entities: { value: "#value", save: "#save" },
      groups: [{ id: "needed", members: ["value", "save"] }],
    });
    const r = captured(
      [
        "inspect",
        html,
        "--tools",
        "geometry,visibility,typography,copy,color,access,targets,media,motion,image",
        "--spec",
        spec,
        "--artifacts",
        join(dir, "views"),
      ],
      capture,
    );
    assert.equal(Object.keys(r.observations).length, 10);
    assert.equal(r.environment.pageErrors.length, 0);
    assert.equal(r.coverage.controls, 2);
    assert.equal(r.observations.visibility.groups[0].allFullyVisibleNow, true);
    assert(r.observations.color.measured.some((n) => n.ratio === 21));
    assert(
      r.observations.access.controls.find((c) => c.tag === "input")
        .formAttributes.inputmode === "numeric",
    );
    for (const name of [
      "view.png",
      "geometry.svg",
      "grayscale.png",
      "blur.png",
      "thumbnail.png",
      "edges.svg",
    ])
      assert((await readFile(join(dir, "views", name))).length > 0);
  },
);
test(
  "ancestor clipping and probe opacity obey observation contract",
  browser,
  async () => {
    const html = await fixture(
      "clipped.html",
      '<div style="height:30px;overflow:hidden;position:relative"><p id="gone" style="position:absolute;top:100px">Gone</p></div><div style="opacity:0"><button id="hidden">Hidden</button></div>',
    );
    const spec = await json("clip-plan.json", {
      entities: { gone: "#gone", hidden: "#hidden" },
      groups: [{ id: "fact", members: ["gone"] }],
    });
    const r = captured([
      "inspect",
      html,
      "--tools",
      "visibility,targets",
      "--spec",
      spec,
    ]);
    assert.equal(r.observations.visibility.groups[0].allFullyVisibleNow, false);
    assert.deepEqual(r.observations.visibility.groups[0].hidden, ["gone"]);
    assert(
      r.observations.targets.controls[0].points.every(
        (p) => !p.receivesPointer,
      ),
    );
    const steps = await json("steps.json", {
      steps: [{ action: "observe", observe: ["#hidden"] }],
    });
    assert.equal(
      captured(["probe", html, "--spec", steps]).observations.probe.records[0]
        .values["#hidden"].visible,
      false,
    );
  },
);
test(
  "contrast leaves layered and translucent paint explicitly unmeasured",
  browser,
  async () => {
    const html = await fixture(
      "paint.html",
      '<p>Opaque</p><p style="color:rgba(0,0,0,.1)">Translucent</p><div style="position:relative"><div style="position:absolute;inset:0;background:black"></div><p style="position:relative;color:white">Layered</p></div>',
    );
    const r = captured(["inspect", html, "--tools", "color"]).observations
      .color;
    assert(r.measured.some((n) => n.text === "Opaque"));
    assert(r.unmeasured.some((n) => n.reason.includes("foreground")));
    assert(r.unmeasured.some((n) => n.reason.includes("nonancestor")));
  },
);
test(
  "probe preserves real draft on failure and diagnoses invalid selectors/actions",
  browser,
  async () => {
    const html = await fixture(
      "recovery.html",
      '<label for="draft">Draft</label><input id="draft"><button id="save">Save</button><p id="status"></p>',
      "",
      "document.querySelector('#save').onclick=()=>document.querySelector('#status').textContent='Failed; try again'",
    );
    const spec = await json("recovery.json", {
      steps: [
        { action: "fill", selector: "#draft", value: "retain this" },
        {
          action: "click",
          selector: "#save",
          observe: ["#draft", "#status"],
          capture: true,
        },
      ],
    });
    const r = captured([
      "probe",
      html,
      "--spec",
      spec,
    ]).observations.probe.records.at(-1);
    assert.equal(r.values["#draft"].value, "retain this");
    assert.equal(r.values["#status"].text, "Failed; try again");
    assert(r.screenshotBase64.length > 100);
    const bad = await json("bad-action.json", { steps: [{ action: "click" }] });
    const e = captureRun(["probe", html, "--spec", bad]);
    assert.notEqual(e.status, 0);
    assert(e.stderr.includes("needs a selector"));
  },
);
test(
  "images, vision stress, print, and remote resources declare actual scope",
  browser,
  async () => {
    const html = await fixture(
      "delivery.html",
      '<h1>Delivery</h1><p>Preserved text</p><img src="https://example.test/pixel.png" alt="Remote illustrative asset">',
      "@media print{h1{break-after:page}}",
    );
    const r = captured([
      "inspect",
      html,
      "--tools",
      "image,media",
      "--vision",
      "deuteranopia",
      "--artifacts",
      join(dir, "delivery"),
    ]);
    assert(r.environment.blockedOrigins.includes("https://example.test"));
    const img = captured([
      "image",
      join(dir, "delivery/view.png"),
      "--artifacts",
      join(dir, "decoded"),
    ]);
    assert(
      img.observations.image.analysisSize.width <= 512 &&
        img.observations.image.analysisSize.height <= 512,
    );
    const print = captured([
      "print",
      html,
      "--artifacts",
      join(dir, "printed"),
    ]);
    assert.equal(print.scope.media, "print");
    assert(
      (await readFile(join(dir, "printed/artifact.pdf")))
        .subarray(0, 5)
        .equals(Buffer.from("%PDF-")),
    );
  },
);
test(
  "scenario resource blocks remain visible after initial page load",
  browser,
  async () => {
    const html = await fixture(
      "late-request.html",
      '<button id="load">Load details</button><p id="status"></p>',
      "",
      "document.querySelector('#load').onclick=async()=>{try{await fetch('https://example.test/late.json')}catch{document.querySelector('#status').textContent='Unavailable'}}",
    );
    const { openArtifact } =
      await import("../../../scripts/design-evals/browser.mjs");
    const r = await openArtifact(
      pathToFileURL(html).href,
      {
        width: 390,
        height: 768,
        theme: "light",
        motion: "no-preference",
        textScale: 1,
      },
      async (page, environment) => {
        await page.click("#load");
        await page.waitForFunction(
          () => document.querySelector("#status").textContent === "Unavailable",
        );
        return { environment };
      },
    );
    assert.deepEqual(r.environment.blockedOrigins, ["https://example.test"]);
  },
);

test("large accepted inputs avoid argument-expansion limits", () => {
  const values = Array(150000).fill(10);
  const r = fidelity({
    series: [{ id: "large", source: values, display: values }],
  })[0];
  assert.deepEqual(r.sourceRange, [10, 10]);
  const pixels = describePixels(
    new Uint8Array(512 * 512 * 4).fill(255),
    512,
    512,
    { tileSize: 1 },
  );
  assert.doesNotThrow(() => heatmapSvg(pixels));
});
test("area-encoded radius uses square-root relation and preserves a mismatch", () => {
  const r = fidelity({
    series: [
      {
        id: "bubbles",
        source: [10, 40],
        display: [10, 40],
        proportional: {
          kind: "area",
          observedQuantity: "radius",
          referenceValue: 10,
          referenceAmount: 20,
          marks: [{ value: 40, amount: 80 }],
        },
      },
    ],
  })[0];
  assert.equal(r.proportional.marks[0].expectedAmount, 40);
  assert.equal(r.proportional.marks[0].error, 40);
});
test(
  "gallery persists exposure, separates revisions, and retains an active comparison",
  browser,
  async () => {
    const { gallery } =
      await import("../../../scripts/design-evals/gallery.mjs");
    const { browserEngine } =
      await import("../../../scripts/design-evals/browser.mjs");
    const image =
      "data:image/svg+xml," +
      encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="768"><rect width="1024" height="768" fill="#eef"/></svg>',
      );
    const make = (hash) =>
      gallery({
        provenance: { fixtureSHA256: hash },
        families: [
          {
            id: "sample",
            split: "train",
            title: "Compare",
            brief: "Inspect these alternatives",
            selection: "Test",
            views: {
              "before-wide": image,
              "after-wide": image,
              "before-narrow": image,
              "after-narrow": image,
            },
            observations: {},
            traces: {},
          },
        ],
        attacks: [],
        calibration: {},
      });
    const path = join(dir, "gallery.html");
    await writeFile(path, make("v1"));
    const engine = await browserEngine();
    const b = await engine.launch();
    try {
      const page = await b.newPage({ viewport: { width: 390, height: 800 } });
      await page.goto(new URL("file://" + path).href);
      await page.selectOption("#family-filter", "unjudged");
      await page.click('[data-choice="A"]');
      assert(await page.locator("#case-sample").isVisible());
      assert(await page.locator("[data-reveal]").isVisible());
      await page.click("[data-reveal]");
      await page.reload();
      await page.click('[data-choice="B"]');
      const saved = await page.evaluate(() =>
        JSON.parse(localStorage.getItem("design-instruments-review-v2-v1")),
      );
      assert.equal(saved.choices.sample.revealedBeforeChoice, true);
      await page.click(".image-button");
      assert.equal(
        await page
          .locator("#zoom-image")
          .evaluate((e) => e.getBoundingClientRect().width),
        1024,
      );
      assert(
        await page
          .locator(".zoom-canvas")
          .evaluate((e) => e.scrollWidth > e.clientWidth),
      );
      await page.keyboard.press("Escape");
      await writeFile(path, make("v2"));
      await page.reload();
      assert.equal(
        await page.locator('[data-choice="B"]').getAttribute("aria-pressed"),
        "false",
      );
      assert.equal(
        await page.locator("#progress").textContent(),
        "0 of 1 judged",
      );
      await page.addInitScript(() => {
        Storage.prototype.setItem = () => {
          throw new Error("unavailable");
        };
      });
      await page.reload();
      await page.click('[data-choice="A"]');
      assert(await page.locator("#storage-status").isVisible());
      assert(
        (await page.locator("#storage-status").textContent()).includes(
          "Export",
        ),
      );
      const warning = await page.locator("#storage-status").boundingBox();
      assert(warning.y >= 0 && warning.y + warning.height <= 800);
      const download = page.waitForEvent("download");
      await page.click("#storage-export");
      assert.equal(
        (await download).suggestedFilename(),
        "design-review-judgments.json",
      );
    } finally {
      await b.close();
    }
  },
);

test("copied skill inventories source HTML without browser or execution", async () => {
  const isolated = join(dir, "portable-install");
  await cp(skill, isolated, { recursive: true });
  const html = await fixture(
    "source-only.html",
    '<h1>Task</h1><label for="n">Count &amp; units</label><input id="n"><div style="display:none"><p>Source-only qualification</p></div><img src="https://example.test/remote.png" alt="Map">',
    "",
    `throw new Error('Do not execute'); fetch('https://example.test/never');`,
  );
  const r = run(["inspect", html], join(isolated, "scripts/design-tools.mjs"), {
    ...process.env,
    DESIGN_TOOLS_PLAYWRIGHT: "/nonexistent/module",
  });
  assert.equal(r.status, 0, r.stderr);
  const report = JSON.parse(r.stdout);
  assert.equal(report.coverage.rendered, false);
  assert(
    report.observations.copy.entries.some(
      (n) => n.text === "Source-only qualification",
    ),
  );
  assert(
    report.observations.access.controls[0].associatedLabels.includes(
      "Count & units",
    ),
  );
  assert.equal(
    report.observations.media.assets[0].src,
    "https://example.test/remote.png",
  );
  assert(
    !report.observations.copy.entries.some((n) => n.text.includes("fetch(")),
  );
  assert.equal(report.observations.copy.entries[0].lines, undefined);
  const unsupported = run(["inspect", html, "--tools", "visibility"]);
  assert.notEqual(unsupported.status, 0);
  assert(unsupported.stderr.includes("Source input cannot establish rendered"));
  assert(!report.environment);
});

test("supplied boxes work without acquisition and missing evidence stays unknown", async () => {
  const box = { x: 0, y: 10, width: 20, height: 20 };
  const input = await json("supplied-observations.json", {
    scope: { coordinateUnits: "image pixels", artifact: "supplied mockup" },
    entities: {
      label: { box, visible: true },
      value: { box: { ...box, y: 40 }, visible: true },
    },
    viewport: { x: 0, y: 0, width: 100, height: 100 },
    plan: {
      links: [{ from: "label", to: "value" }],
      groups: [{ id: "needed", members: ["label", "value"] }],
    },
  });
  const r = observation(["inspect", input, "--tools", "geometry,visibility"]);
  assert.equal(r.observations.geometry.associations[0].intendedGapPx, 10);
  assert.equal(r.observations.geometry.associations[0].gapInLabelEm, null);
  assert.equal(r.observations.visibility.groups[0].allFullyVisibleNow, null);
  assert.deepEqual(r.observations.visibility.groups[0].fullyWithinViewport, [
    "label",
    "value",
  ]);
  assert.deepEqual(
    r.observations.visibility.groups[0].unmeasuredAncestorClipping,
    ["label", "value"],
  );
  const noGeometry = await json("no-geometry.json", {
    nodes: [{ text: "A value" }],
  });
  const missing = run(["inspect", noGeometry, "--tools", "typography"]);
  assert.notEqual(missing.status, 0);
  assert(missing.stderr.includes("rendered line counts"));
  const unsupported = run([
    "inspect",
    "https://example.test/page",
    "--tools",
    "copy",
  ]);
  assert.notEqual(unsupported.status, 0);
  assert(unsupported.stderr.includes("agent owns acquisition"));
});

test("raw RGBA and stdin need neither browser nor Python", async () => {
  const input = JSON.stringify({
    width: 2,
    height: 2,
    data: Array(4).fill([0, 0, 0, 0]).flat(),
  });
  const r = spawnSync(process.execPath, [cli, "image", "-"], {
    input,
    encoding: "utf8",
    env: {
      ...process.env,
      DESIGN_TOOLS_PYTHON: "/nonexistent/python",
      DESIGN_TOOLS_PLAYWRIGHT: "/nonexistent/module",
    },
  });
  assert.equal(r.status, 0, r.stderr);
  const measured = JSON.parse(r.stdout).observations.image;
  assert.equal(measured.meanGradient, 0);
  assert.equal(measured.colorfulnessDescriptor, 0);
  assert.equal(measured.luminanceHistogramEntropyBits, 0);
  assert.throws(() => describePixels([256, 0, 0, 255], 1, 1), /integer bytes/);
});

test(
  "native raster decoding is browser-free and records provenance",
  { skip: process.env.DESIGN_TOOLS_TEST_IMAGES !== "1" },
  async () => {
    const path = join(dir, "transparent.png");
    const python = spawnSync(
      process.env.DESIGN_TOOLS_PYTHON || "python3",
      [
        "-c",
        "from PIL import Image; import sys; Image.new('RGBA', (640, 320), (0,0,0,0)).save(sys.argv[1])",
        path,
      ],
      { encoding: "utf8" },
    );
    assert.equal(python.status, 0, python.stderr);
    const r = run(
      ["image", path, "--artifacts", join(dir, "native-views")],
      cli,
      { ...process.env, DESIGN_TOOLS_PLAYWRIGHT: "/nonexistent/module" },
    );
    assert.equal(r.status, 0, r.stderr);
    const report = JSON.parse(r.stdout);
    assert.deepEqual(report.observations.image.originalSize, {
      width: 640,
      height: 320,
    });
    assert.equal(report.observations.image.analysisSize.width, 512);
    assert.equal(report.observations.image.meanGradient, 0);
    assert(report.scope.decoder.startsWith("Pillow"));
    for (const name of [
      "grayscale.png",
      "blur.png",
      "thumbnail.png",
      "edges.svg",
    ])
      assert((await readFile(join(dir, "native-views", name))).length > 0);
  },
);

test("shipped runtime contains no browser acquisition dependency", async () => {
  const { readdir } = await import("node:fs/promises");
  for (const name of await readdir(join(skill, "scripts"))) {
    if (!/\.(mjs|py)$/.test(name)) continue;
    const code = await readFile(join(skill, "scripts", name), "utf8");
    assert(
      !/playwright|chromium|page\.evaluate|page\.screenshot|openArtifact/.test(
        code,
      ),
      name,
    );
  }
  const catalog = observation(["catalog"]);
  assert(!catalog.other.includes("probe"));
  assert(!catalog.other.includes("print"));
});

test("HTML candidates distinguish option/value text from labels and image-link alternatives", async () => {
  const path = await fixture(
    "source-name-evidence.html",
    '<select id="choice"><option>London</option></select><textarea id="note">My value</textarea><a href="/tickets"><img alt="Buy tickets" src="ticket.png"></a><label for="named">City</label><select id="named"><option>London</option></select>',
  );
  const report = observation(["inspect", path, "--tools", "access"]);
  const controls = report.observations.access.controls;
  assert.equal(
    controls.find((c) => c.sourceId === "choice").nameCandidate,
    null,
  );
  assert.equal(controls.find((c) => c.sourceId === "note").nameCandidate, null);
  assert.equal(
    controls.find((c) => c.tag === "a").nameCandidate,
    "Buy tickets",
  );
  assert.equal(
    controls.find((c) => c.sourceId === "named").nameCandidate,
    "City",
  );
});

test("appearance feature input preserves frozen axes and rejects invented/missing values", async () => {
  const profile = JSON.parse(
    await readFile(join(skill, "scripts/appearance-profile.json"), "utf8"),
  );
  const values = Object.fromEntries(
    profile.models.complexity.features.map((name, i) => [
      name,
      profile.models.complexity.model.means[i],
    ]),
  );
  const path = await json("appearance-features.json", { features: values });
  const result = observation(["appearance", path]);
  assert.equal(
    result.observations.appearance.frozenModelSHA256,
    profile.frozenModelSHA256,
  );
  assert.deepEqual(Object.keys(result.observations.appearance.axes), [
    "complexity",
    "aesthetics",
    "craftsmanship",
    "novelty",
  ]);
  assert(
    !Object.hasOwn(result.observations.appearance.axes, "technical-condition"),
  );
  assert.match(result.observations.appearance.limits, /not UX quality/);
  const missing = await json("appearance-missing.json", {
    features: { gradient_512: 0 },
  });
  assert.match(
    run(["appearance", missing]).stderr,
    /Missing\/nonfinite feature/,
  );
  const falseValue = await json("appearance-bool.json", {
    features: { ...values, gradient_128: false },
  });
  assert.match(
    run(["appearance", falseValue]).stderr,
    /Missing\/nonfinite feature/,
  );
});

test("native observations reject contradictory clips and incomplete hit evidence", async () => {
  const offscreen = await json("contradictory-clip.json", {
    entities: {
      value: {
        box: { x: 500, y: 500, width: 20, height: 20 },
        visibleBox: { x: 0, y: 0, width: 20, height: 20 },
        visible: true,
      },
    },
    viewport: { x: 0, y: 0, width: 100, height: 100 },
    plan: { groups: [{ id: "value", members: ["value"] }] },
  });
  assert.match(
    run(["inspect", offscreen, "--tools", "visibility"]).stderr,
    /within its original box/,
  );
  const incomplete = await json("incomplete-hit.json", {
    controls: [
      {
        id: "save",
        box: { x: 0, y: 0, width: 20, height: 20 },
        points: [{ x: 10, y: 10 }],
      },
    ],
  });
  assert.match(
    run(["inspect", incomplete, "--tools", "targets"]).stderr,
    /observed receivesPointer/,
  );
  const source = await json("source-observations.json", {
    coverage: { rendered: false },
    nodes: [{ text: "Source text" }],
  });
  assert.equal(
    observation(["inspect", source, "--tools", "copy"]).observations.copy
      .totalWords,
    2,
  );
  const badColor = await json("invalid-rgb.json", {
    nodes: [
      {
        id: "ink",
        text: "Ink",
        color: "rgb(999,999,999)",
        backgrounds: ["rgb(255,255,255)"],
        paintEffects: [],
      },
    ],
  });
  const r = observation(["inspect", badColor, "--tools", "color"]).observations
    .color;
  assert.equal(r.measured.length, 0);
  assert.equal(r.unmeasured.length, 1);
});

test("source labels preserve inline word fragments and dir-only context", async () => {
  const html = await fixture(
    "fragments.html",
    '<div dir="rtl"><button>Re<span>try</span></button></div>',
  );
  const r = observation(["inspect", html]);
  assert.equal(r.observations.access.controls[0].nameCandidate, "Retry");
  assert(r.observations.access.languages.some((e) => e.direction === "rtl"));
});

test("source action candidates include native and declared controls without hidden inputs", async () => {
  const html = await fixture(
    "source-controls.html",
    '<input type="hidden" name="token"><input type="submit" value="Save"><details><summary>Details</summary></details><div role="tab">Tab</div><div role="switch">Switch</div>',
  );
  const controls = observation(["inspect", html]).observations.access.controls;
  assert.equal(controls.length, 4);
  assert(controls.some((c) => c.nameCandidate === "Save"));
  assert(controls.some((c) => c.tag === "summary"));
  assert(controls.some((c) => c.role === "switch"));
});
