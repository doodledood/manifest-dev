#!/usr/bin/env node
import { mkdir, writeFile, readFile, mkdtemp, cp } from "node:fs/promises";
import { resolve, join, basename } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { tmpdir } from "node:os";
import { spawn, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  families,
  structuredExamples,
  width,
  height,
  document,
} from "./fixtures.mjs";
import { calibration, attacks } from "./calibration.mjs";
import { transferCases } from "./transfer.mjs";
import { gallery } from "./gallery.mjs";
const root = resolve(fileURLToPath(new URL("../..", import.meta.url)));
const cli = fileURLToPath(new URL("./capture.mjs", import.meta.url));
const out = process.argv[2]
  ? resolve(process.argv[2])
  : await mkdtemp(join(tmpdir(), "design-instruments-review-"));
if (process.argv[2]) {
  try {
    await mkdir(out);
  } catch (error) {
    if (error.code === "EEXIST")
      throw new Error(
        "Output directory already exists. Use a new directory to preserve the previous gallery and its provenance.",
      );
    throw error;
  }
}
async function command(args, alternateCli = cli) {
  return new Promise((yes, no) => {
    const p = spawn(process.execPath, [alternateCli, ...args], {
      env: process.env,
    });
    let stdout = "",
      stderr = "";
    p.stdout.on("data", (d) => (stdout += d));
    p.stderr.on("data", (d) => (stderr += d));
    p.on("error", no);
    p.on("exit", (code) => {
      if (code !== 0) no(new Error(`${args[0]} failed: ${stderr}`));
      else {
        try {
          yes(JSON.parse(stdout));
        } catch {
          no(
            new Error(`Invalid JSON from ${args[0]}: ${stdout.slice(0, 300)}`),
          );
        }
      }
    });
  });
}
const failures = [];
const check = (condition, id) => {
  if (!condition) failures.push(id);
};
const results = {
  schemaVersion: 1,
  evidence:
    "Constructed fixtures and local observations; no human preference or participant UX outcomes.",
  calibration: calibration(),
  families: [],
  attacks: [],
  structured: {},
  errors: [],
  isolated: null,
};
for (const family of families) {
  const dir = join(out, family.id);
  await mkdir(dir, { recursive: true });
  const plan = {
    entities: family.entities || {},
    groups: family.groups || [],
    links: family.links || [],
    alignments: family.alignments || [],
  };
  const planPath = join(dir, "plan.json");
  await writeFile(planPath, JSON.stringify(plan));
  const record = {
    id: family.id,
    split: family.split,
    title: family.title,
    brief: family.brief,
    selection: family.selection,
    views: {},
    traces: {},
    observations: {},
  };
  for (const variant of ["before", "after"]) {
    const html = join(dir, `${variant}.html`);
    await writeFile(html, family[variant]);
    for (const [view, w] of [
      ["wide", width],
      ["narrow", 390],
    ]) {
      const artifacts = join(dir, `${variant}-${view}`);
      const args = [
        "inspect",
        html,
        "--tools",
        [...new Set([...family.tools, "image"])].join(","),
        "--spec",
        planPath,
        "--width",
        String(w),
        "--height",
        String(height),
        "--artifacts",
        artifacts,
      ];
      const r = await command(args);
      await writeFile(
        join(dir, `${variant}-${view}.json`),
        JSON.stringify(r, null, 2),
      );
      check(
        r.environment.pageErrors.length === 0,
        `${family.id}/${variant}/${view}: page errors`,
      );
      record.views[`${variant}-${view}`] =
        `${family.id}/${variant}-${view}/view.png`;
      record.observations[`${variant}-${view}`] = r.observations;
    }
    if (family.steps) {
      const path = join(dir, "scenario.json");
      await writeFile(path, JSON.stringify({ steps: family.steps }));
      const trace = await command([
        "probe",
        html,
        "--spec",
        path,
        "--width",
        "390",
        "--height",
        String(height),
      ]);
      record.traces[variant] = trace.observations.probe.records;
      await writeFile(
        join(dir, `${variant}-trace.json`),
        JSON.stringify(trace, null, 2),
      );
    }
    if (family.id === "email") {
      const r = await command([
        "inspect",
        html,
        "--tools",
        "targets,access,media,copy,image",
        "--images-off",
        "--width",
        "390",
        "--height",
        String(height),
        "--artifacts",
        join(dir, `${variant}-images-off`),
      ]);
      record.views[`${variant}-images-off`] =
        `${family.id}/${variant}-images-off/view.png`;
      record.observations[`${variant}-images-off`] = r.observations;
    }
    if (family.id === "report") {
      await command([
        "print",
        html,
        "--artifacts",
        join(dir, `${variant}-print`),
      ]);
      const extracted = spawnSync(
        process.env.DESIGN_EVAL_PYTHON || "python3",
        [
          join(root, "scripts/design-evals/pdf-evidence.py"),
          join(dir, `${variant}-print/artifact.pdf`),
        ],
        { encoding: "utf8", timeout: 30000 },
      );
      if (extracted.status !== 0)
        throw new Error(
          "PDF evidence needs a Python with pypdf; set DESIGN_EVAL_PYTHON. " +
            extracted.stderr,
        );
      record.printEvidence = record.printEvidence || {};
      record.printEvidence[variant] = JSON.parse(extracted.stdout);
      const rasterized = spawnSync(
        process.env.DESIGN_EVAL_PDFTOPPM || "pdftoppm",
        [
          "-scale-to",
          "1200",
          "-png",
          join(dir, `${variant}-print/artifact.pdf`),
          join(dir, `${variant}-print/page`),
        ],
        { encoding: "utf8", timeout: 30000 },
      );
      if (rasterized.status !== 0)
        throw new Error(
          "PDF raster evidence needs pdftoppm; set DESIGN_EVAL_PDFTOPPM. " +
            rasterized.stderr,
        );
      record.views[`${variant}-screen`] = record.views[`${variant}-wide`];
      record.views[`${variant}-wide`] =
        `${family.id}/${variant}-print/page-1.png`;
      record.views[`${variant}-narrow`] =
        `${family.id}/${variant}-print/page-1.png`;
    }
  }
  if (family.id === "dashboard")
    check(
      record.observations["after-wide"].visibility.groups[0].fullyVisible
        .length >
        record.observations["before-wide"].visibility.groups[0].fullyVisible
          .length,
      "dashboard change must increase actual named co-visibility",
    );
  if (family.id === "form") {
    const a = record.traces.after.at(-1).values["#note"];
    const b = record.traces.before.at(-1).values["#note"];
    check(
      a.value === "Valve checked at 10:15" && b.value === "",
      "form independent draft preservation",
    );
  }
  if (family.id === "chart")
    check(
      record.observations["after-wide"].geometry.alignments[0].rangePx < 0.1 &&
        record.observations["before-wide"].geometry.alignments[0].rangePx > 20,
      "chart independent common-scale plot width",
    );
  if (family.id === "game")
    check(
      record.traces.after.at(-1).values["#count"].text === "3" &&
        record.traces.before.at(-1).values["#count"].text === "1",
      "game repeated counter",
    );
  if (family.id === "article")
    check(
      record.observations["after-wide"].copy.totalWords <
        record.observations["before-wide"].copy.totalWords &&
        !family.after.includes("single-site pilot"),
      "article harmful word-count improvement",
    );
  if (family.id === "explorable") {
    const after = record.traces.after[0].values,
      before = record.traces.before[0].values;
    check(
      after["#duration"].text === (2400 / 333).toFixed(2) &&
        after["#shownFlow"].text === "333",
      "calculator full precision/context",
    );
    check(
      before["#duration"].text !== after["#duration"].text,
      "calculator negative oracle",
    );
    check(
      record.traces.after[1].values["#duration"].text ===
        after["#duration"].text,
      "calculator invalid input preservation",
    );
  }
  if (family.id === "rtl")
    check(
      record.observations["after-narrow"].visibility.groups[0].fullyVisible
        .length === 4 &&
        record.observations["before-narrow"].visibility.groups[0].fullyVisible
          .length < 4,
      "RTL required account, amount, action and note remain available",
    );
  if (family.id === "email") {
    const labelVisible = (variant) =>
      record.observations[`${variant}-images-off`].copy.entries.some(
        (e) => e.text === "Review the route map" && e.visible,
      );
    check(
      labelVisible("after") && !labelVisible("before"),
      "email visible action label in images-off stress condition",
    );
  }
  if (family.id === "report") {
    for (const section of [
      "Decision and scope",
      "Costs and assumptions",
      "Risks and rollback",
      "Evidence and next review",
    ])
      check(
        record.printEvidence.after.text.includes(section),
        `PDF includes ${section}`,
      );
    check(
      record.printEvidence.after.pages > record.printEvidence.before.pages,
      "PDF pagination differs from clipped negative fixture",
    );
  }
  results.families.push(record);
  console.log(
    `${family.id}: captured wide/narrow ${family.steps ? "and executed scenario" : ""}`,
  );
}
// Every advertised instrument is exercised together on a suitable artifact.
const all = await command([
  "inspect",
  join(out, "form/after.html"),
  "--tools",
  "geometry,visibility,typography,copy,color,access,targets,media,motion,image",
  "--spec",
  join(out, "form/plan.json"),
]);
check(
  Object.keys(all.observations).length === 10,
  "all browser instruments execute",
);
for (const [name, spec] of Object.entries(structuredExamples)) {
  const path = join(out, `${name}.json`);
  await writeFile(path, JSON.stringify(spec));
  results.structured[name] = (await command([name, path])).observations[name];
}
check(
  results.structured.data[0].differences.length === 0 &&
    results.structured.data[0].marks.every((m) => m.positionErrorPx === 0),
  "data independent linear mapping",
);
check(
  results.structured.timeline.events.find((e) => e.id === "instant")
    .wordsPerSecond === null,
  "zero text exposure cannot be rate zero",
);
check(
  results.structured.survey.axes.find((a) => a.axis === "clarity")
    .excludedIncomplete === 1,
  "survey incomplete axes preserved",
);
// Actually attack supplied artifacts, not just write down possible gaming stories.
const attackFixtures = [
  {
    id: "clipped-facts",
    html: document(
      '<main><h1>Current state</h1><div style="height:30px;overflow:hidden;position:relative"><p id="fact" style="position:absolute;top:100px">Essential incident</p></div></main>',
    ),
    tools: "visibility",
    plan: {
      entities: { fact: "#fact" },
      groups: [{ id: "needed", members: ["fact"] }],
    },
    accept: (r) => !r.observations.visibility.groups[0].allFullyVisibleNow,
  },
  {
    id: "hidden-hit-box",
    html: document(
      '<main><h1>Control</h1><div style="opacity:0"><button id="control" style="width:300px;height:150px">Save</button></div></main>',
    ),
    tools: "targets",
    accept: (r) =>
      r.observations.targets.controls.every(
        (c) => !c.visible && c.points.every((p) => !p.receivesPointer),
      ),
  },
  {
    id: "monochrome-series",
    html: document(
      '<main><h1>Three categories</h1><p style="color:#000;background:#fff">Legend: A — B — C, each in black.</p><svg aria-label="Three series using identical solid black lines without direct labels" width="480" height="240"><path d="M20 200 Q200 20 450 80" fill="none" stroke="black" stroke-width="4"/><path d="M20 100 Q250 220 450 50" fill="none" stroke="black" stroke-width="4"/><path d="M20 160 Q230 50 450 150" fill="none" stroke="black" stroke-width="4"/></svg></main>',
    ),
    tools: "color",
    accept: (r) => r.observations.color.measured.some((c) => c.ratio === 21),
  },
  {
    id: "paint-gap",
    html: document(
      '<main><div style="position:relative"><div style="position:absolute;inset:0;background:black"></div><p id="overlay" style="position:relative;color:white">White text over a nonancestor black layer</p></div></main>',
    ),
    tools: "color",
    accept: (r) =>
      r.observations.color.unmeasured.some((c) =>
        c.reason.includes("nonancestor"),
      ),
  },
];
for (const attack of attackFixtures) {
  const dir = join(out, "attacks", attack.id);
  await mkdir(dir, { recursive: true });
  const html = join(dir, "artifact.html"),
    plan = join(dir, "plan.json");
  await writeFile(html, attack.html);
  await writeFile(plan, JSON.stringify(attack.plan || {}));
  const r = await command([
    "inspect",
    html,
    "--tools",
    `${attack.tools},image`,
    "--spec",
    plan,
    "--artifacts",
    dir,
  ]);
  check(attack.accept(r), `attack ${attack.id} observed oracle`);
  results.attacks.push({
    id: attack.id,
    observations: r.observations,
    evidence: "Executed artifact",
  });
}
for (const attack of attacks)
  if (!results.attacks.some((a) => a.id === attack.id)) {
    const family = results.families.find((f) => f.id === attack.family);
    const disposition = [
      "missing-qualification",
      "plot-width-drift",
      "fake-route",
      "one-tap-only",
      "image-only-cta",
      "premature-rounding",
      "hidden-print-text",
    ].includes(attack.id)
      ? "Executed family comparison"
      : attack.id === "instant-text"
        ? "Executed timeline"
        : attack.id === "fine-pattern"
          ? "Executed pixel calibration"
          : "Reasoned counterexample; no measured outcome";
    results.attacks.push({
      ...attack,
      evidence: disposition,
      ...(disposition === "Executed family comparison"
        ? { family: family.id }
        : {}),
    });
  }
// Deliberately misdeclare a direct saved route; compare with the real failed-save trace.
const fakePath = join(out, "fake-route.json");
await writeFile(
  fakePath,
  JSON.stringify({
    nodes: [{ id: "draft" }, { id: "saved" }],
    edges: [{ from: "draft", to: "saved", cost: 1 }],
    tasks: [{ id: "save", from: "draft", to: "saved" }],
  }),
);
const fakeRoute = (await command(["journey", fakePath])).observations
  .journey[0];
const actualFailure = results.families
  .find((f) => f.id === "form")
  .traces.after.at(-1).values["#status"].text;
check(
  fakeRoute.minimumDeclaredCost === 1 &&
    actualFailure.includes("Connection unavailable"),
  "fraudulent route remains distinct from observed failure",
);
const fakeRecord = results.attacks.find((a) => a.id === "fake-route");
Object.assign(fakeRecord, {
  evidence: "Executed misleading declaration and actual form failure trace",
  declared: fakeRoute,
  observedStatus: actualFailure,
});
// Local design-parameter search. Numeric objective is not its acceptance evidence.
const search = [];
for (const gap of [8, 20, 60, 120, 240, 350]) {
  const dir = join(out, "search");
  await mkdir(dir, { recursive: true });
  const html = join(dir, `gap-${gap}.html`);
  await writeFile(
    html,
    families[0].after.replace("margin-top:20px", `margin-top:${gap}px`),
  );
  const r = await command([
    "inspect",
    html,
    "--tools",
    "visibility,geometry",
    "--spec",
    join(out, "dashboard/plan.json"),
    "--width",
    String(width),
    "--height",
    String(height),
    "--artifacts",
    join(dir, `gap-${gap}-views`),
  ]);
  search.push({
    requestedMarginTopPx: gap,
    fullyVisibleFacts: r.observations.visibility.groups[0].fullyVisible.length,
    preservedTableText:
      r.observations.geometry.entities.readings.text ===
      results.families.find((f) => f.id === "dashboard").observations[
        "before-wide"
      ].geometry.entities.readings.text,
    selected: gap === 20,
  });
}
check(
  search.every((c) => c.preservedTableText),
  "search retains actual rendered table text",
);
results.designSearch = {
  family: "dashboard",
  objective: "Explore named facts simultaneously visible",
  candidates: search,
  selection:
    "20 px CSS margin retained by the author on a co-visibility plateau. Adjacent margins collapse, so requested margin is not measured separation; 8 px and 20 px render identically. Equal objective values do not resolve composition; owner judgment is pending.",
};
// Standalone copy exercises same public entrypoint, no neighboring skills needed.
const isolated = await mkdtemp(join(tmpdir(), "design-instruments-isolated-"));
await cp(
  join(root, "claude-plugins/manifest-dev/skills/design"),
  join(isolated, "design"),
  { recursive: true },
);
const isolatedCli = join(isolated, "design/scripts/design-tools.mjs");
const standalone = await command(
  [
    "inspect",
    join(out, "form/after-wide/observations.json"),
    "--tools",
    "targets",
  ],
  isolatedCli,
);
const standaloneData = await command(
  ["data", join(out, "data.json")],
  isolatedCli,
);
results.isolated = {
  suppliedControls: standalone.observations.targets.controls.length,
  dataSeries: standaloneData.observations.data.length,
  selfContained: true,
};
check(
  results.isolated.suppliedControls > 0 && results.isolated.dataSeries === 1,
  "isolated install executes",
);
// Actionable failures are part of the exercised contract.
async function expectError(args, fragment) {
  const p = spawn(process.execPath, [cli, ...args], { env: process.env });
  let stderr = "";
  p.stderr.on("data", (d) => (stderr += d));
  const code = await new Promise((yes, no) => {
    p.on("error", no);
    p.on("exit", yes);
  });
  const pass = code !== 0 && stderr.includes(fragment);
  check(pass, `error ${fragment}`);
  results.errors.push({ command: args[0], expected: fragment, observed: pass });
}
await expectError(["inspect", join(out, "form/after.html")], "needs --tools");
await expectError(["data", join(out, "missing.json")], "Cannot read JSON");
await expectError(
  [
    "inspect",
    join(out, "form/after.html"),
    "--tools",
    "targets",
    "--width",
    "NaN",
  ],
  "finite number",
);
await expectError(["image", join(out, "data.json")], "Unsupported image");
await expectError(
  ["print", join(out, "form/after.html")],
  "requires --artifacts",
);
await expectError(
  ["inspect", "https://example.test", "--tools", "copy"],
  "Remote URLs require",
);
const badPlan = join(out, "bad-plan.json");
await writeFile(
  badPlan,
  JSON.stringify({ entities: { missing: "#nonexistent" } }),
);
await expectError(
  [
    "inspect",
    join(out, "form/after.html"),
    "--tools",
    "geometry",
    "--spec",
    badPlan,
  ],
  "must match exactly one",
);
const image = await command([
  "image",
  join(out, "poster/after-wide/view.png"),
  "--artifacts",
  join(out, "image-only"),
]);
check(
  image.observations.image.analysisSize.width <= 512 &&
    image.observations.image.analysisSize.height <= 512,
  "image-only bound",
);
const comparison = await command([
  "compare",
  join(out, "explainer/before-wide.json"),
  "--other",
  join(out, "explainer/after-wide.json"),
]);
check(
  comparison.observations.compare.numericDeltas.some((d) =>
    d.path.includes("return-label"),
  ),
  "compare named array observations",
);
// Record current versions; preserve the initial independent evaluation separately.
results.transfer = {
  initialEvaluation: JSON.parse(
    await readFile(new URL("./transfer-freeze.json", import.meta.url), "utf8"),
  ),
  evidence:
    "Cases were independently specified for the initial frozen evaluation. Reruns use now-known cases as regression evidence; original hashes remain traceable.",
  instrumentHashes: Object.fromEntries(
    await Promise.all(
      [
        "measurements.mjs",
        "observations.mjs",
        "pixels.mjs",
        "artifact-input.py",
        "design-tools.mjs",
      ].map(async (name) => [
        name,
        createHash("sha256")
          .update(
            await readFile(
              join(
                root,
                "claude-plugins/manifest-dev/skills/design/scripts",
                name,
              ),
            ),
          )
          .digest("hex"),
      ]),
    ),
  ),
  cases: [],
};
for (const c of transferCases) {
  const dir = join(out, "transfer", c.id);
  await mkdir(dir, { recursive: true });
  let args;
  if (c.html) {
    const html = join(dir, "artifact.html"),
      plan = join(dir, "plan.json");
    await writeFile(html, c.html);
    await writeFile(plan, JSON.stringify(c.plan));
    args = [
      c.command,
      html,
      "--spec",
      plan,
      "--width",
      String(c.width || 800),
      "--height",
      String(c.height || 600),
    ];
    if (c.command === "inspect")
      args.push("--tools", c.tools, "--artifacts", dir);
  } else {
    const input = join(dir, "input.json");
    await writeFile(input, JSON.stringify(c.input));
    args = [c.command, input];
  }
  const r = await command(args);
  const observed = c.check(r);
  check(observed, `independent transfer ${c.id}`);
  const record = {
    id: c.id,
    expected: c.expected,
    applicability: c.applicability,
    observed,
    observations: r.observations,
  };
  if (c.revisedHTML) {
    const html = join(dir, "revised.html");
    await writeFile(html, c.revisedHTML(c.html));
    const revised = await command([
      c.command,
      html,
      "--spec",
      join(dir, "plan.json"),
      "--width",
      String(c.width),
      "--height",
      String(c.height),
      "--tools",
      c.tools,
    ]);
    record.revisedObserved = c.revisedCheck(revised);
    check(record.revisedObserved, `independent transfer revision ${c.id}`);
  }
  results.transfer.cases.push(record);
}
results.failures = failures;
results.provenance = {
  fixtureSHA256: createHash("sha256")
    .update(await readFile(new URL("./fixtures.mjs", import.meta.url)))
    .digest("hex"),
  calibrationSHA256: createHash("sha256")
    .update(await readFile(new URL("./calibration.mjs", import.meta.url)))
    .digest("hex"),
};
await writeFile(
  join(out, "results.json"),
  JSON.stringify(results, null, 2) + "\n",
);
await writeFile(join(out, "index.html"), gallery(results));
const publicSummary = {
  schemaVersion: 1,
  evidence: results.evidence,
  provenance: results.provenance,
  calibration: results.calibration,
  transfer: results.transfer,
  families: results.families.map(({ id, split, title, brief, selection }) => ({
    id,
    split,
    title,
    brief,
    selection,
  })),
  attacks: results.attacks.map(({ id, evidence, outcome, correction }) => ({
    id,
    evidence,
    outcome,
    correction,
  })),
  designSearch: results.designSearch,
  structuredCommands: Object.keys(results.structured),
  errors: results.errors,
  isolated: results.isolated,
  failures,
};
await writeFile(
  join(out, "summary.json"),
  JSON.stringify(publicSummary, null, 2) + "\n",
);
console.log(`Review gallery: ${join(out, "index.html")}`);
console.log(`Checks: ${failures.length === 0 ? "PASS" : failures.join("; ")}`);
if (failures.length) process.exitCode = 1;
