#!/usr/bin/env node
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve, basename, extname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";
import { spawnSync } from "node:child_process";
import {
  VERSION,
  object,
  journey,
  fidelity,
  timeline,
  survey,
  content,
  viewing,
  palette,
  compare,
} from "./measurements.mjs";
import { instruments, analyzeObservations } from "./observations.mjs";
import { describePixels, heatmapSvg } from "./pixels.mjs";

const structured = {
  journey,
  data: fidelity,
  timeline,
  survey,
  content,
  viewing,
  palette,
};
const help = `Optional design instruments ${VERSION}
node scripts/design-tools.mjs catalog
node scripts/design-tools.mjs inspect <HTML|text|observations.json> [--tools copy,geometry,...] [--spec plan.json]
node scripts/design-tools.mjs image <PNG|JPEG|WebP|GIF|RGBA.json> [--artifacts views]
node scripts/design-tools.mjs appearance <image|features.json|->
node scripts/design-tools.mjs ${Object.keys(structured).join("|")} <JSON>
node scripts/design-tools.mjs compare <report.json> --other <report.json>
Options: --output report.json --edge-threshold 0.08 --tile-size 16
JSON/text input may be '-' for stdin. No capture, rendering, network or interaction.
Node 20+ for JSON/text; Python 3 for HTML; Python + Pillow for raster images.
DESIGN_TOOLS_PYTHON selects the interpreter. Supplied RGBA JSON needs only Node.
See references/instruments/usage.md for supported evidence and missing-data limits.
`;
async function source(file) {
  if (!file) throw new Error("An input file is required");
  if (/^[a-z][a-z\d+.-]*:\/\//i.test(file))
    throw new Error("Supply a local artifact; the agent owns acquisition");
  if (file === "-") {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    return Buffer.concat(chunks).toString("utf8");
  }
  return readFile(file, "utf8");
}
async function jsonFile(file) {
  try {
    return JSON.parse(await source(file));
  } catch (e) {
    throw new Error(
      `Cannot read JSON ${basename(file || "input")}: ${e.message}`,
    );
  }
}
function inputHelper(mode, input, artifacts) {
  const r = spawnSync(
    process.env.DESIGN_TOOLS_PYTHON || "python3",
    [
      fileURLToPath(new URL("./artifact-input.py", import.meta.url)),
      mode,
      ...(mode === "image"
        ? [resolve(input), ...(artifacts ? [artifacts] : [])]
        : []),
    ],
    {
      input: mode === "html" ? input : undefined,
      encoding: "utf8",
      maxBuffer: 24 * 1024 * 1024,
      timeout: 30000,
    },
  );
  if (r.error)
    throw new Error(
      `Artifact decoding needs Python 3; set DESIGN_TOOLS_PYTHON: ${r.error.message}`,
    );
  if (r.status !== 0)
    throw new Error(r.stderr.trim() || "Artifact decoding failed");
  return JSON.parse(r.stdout);
}
async function image(input, opts, artifacts) {
  let pixels;
  if (extname(input).toLowerCase() === ".json" || input === "-")
    pixels = await jsonFile(input);
  else {
    if (
      ![".png", ".jpg", ".jpeg", ".webp", ".gif"].includes(
        extname(input).toLowerCase(),
      )
    )
      throw new Error(
        "Unsupported image format; supply a raster image or bounded RGBA JSON",
      );
    pixels = inputHelper("image", input, artifacts);
  }
  object(pixels, "image pixels");
  if (
    !Number.isInteger(pixels.width) ||
    !Number.isInteger(pixels.height) ||
    pixels.width < 1 ||
    pixels.height < 1 ||
    Math.max(pixels.width, pixels.height) > 512
  )
    throw new Error(
      "Supplied analysis pixels need positive dimensions with maximum edge 512",
    );
  const description = describePixels(pixels.data, pixels.width, pixels.height, {
    threshold: Number(opts["edge-threshold"]),
    tileSize: Number(opts["tile-size"]),
  });
  if (artifacts)
    await writeFile(join(artifacts, "edges.svg"), heatmapSvg(description));
  return {
    scope: {
      basis: "supplied pixels",
      originalSize: pixels.originalSize || null,
      analysisSize: { width: pixels.width, height: pixels.height },
      decoder: pixels.decoder || "supplied RGBA",
      resampling: pixels.resampling || "none; supplied analysis resolution",
      exifOrientationApplied: pixels.exifOrientationApplied || false,
      decoding:
        pixels.scope ||
        "alpha composited over white; no original-image or frame provenance inferred",
    },
    observations: {
      image: { ...description, originalSize: pixels.originalSize || null },
    },
    ...(artifacts
      ? { artifacts: [...(pixels.artifacts || []), "edges.svg"] }
      : {}),
  };
}
async function main() {
  const { values: v, positionals: p } = parseArgs({
    allowPositionals: true,
    options: {
      help: { type: "boolean" },
      tools: { type: "string" },
      spec: { type: "string" },
      other: { type: "string" },
      output: { type: "string" },
      artifacts: { type: "string" },
      "edge-threshold": { type: "string", default: ".08" },
      "tile-size": { type: "string", default: "16" },
    },
  });
  if (v.help || !p.length) {
    console.log(help);
    return;
  }
  const [command, input] = p;
  if (p.length > 2) throw new Error("Unexpected positional arguments");
  if (command === "catalog") {
    console.log(
      JSON.stringify(
        {
          version: VERSION,
          instruments,
          structured: Object.keys(structured),
          other: ["image", "appearance", "compare"],
          inputs: {
            html: ["copy", "access", "media"],
            text: ["copy"],
            raster: ["image", "appearance"],
            observations: "choose fields needed by the question",
          },
        },
        null,
        2,
      ),
    );
    return;
  }
  if (!input) throw new Error("An input artifact is required");
  if (/^[a-z][a-z\d+.-]*:\/\//i.test(input))
    throw new Error("Supply a local artifact; the agent owns acquisition");
  const artifacts = v.artifacts ? resolve(v.artifacts) : null;
  if (artifacts && command !== "image")
    throw new Error("--artifacts applies to supplied image analysis");
  if (artifacts) await mkdir(artifacts, { recursive: true });
  let result;
  if (Object.hasOwn(structured, command))
    result = {
      observations: { [command]: structured[command](await jsonFile(input)) },
    };
  else if (command === "compare") {
    if (!v.other) throw new Error("compare requires --other");
    result = {
      observations: {
        compare: compare(await jsonFile(input), await jsonFile(v.other)),
      },
    };
  } else if (command === "appearance") {
    const r = spawnSync(
      process.env.DESIGN_TOOLS_PYTHON || "python3",
      [
        fileURLToPath(new URL("./appearance.py", import.meta.url)),
        input === "-" ? "-" : resolve(input),
      ],
      {
        input: input === "-" ? await source(input) : undefined,
        encoding: "utf8",
        timeout: 30000,
        maxBuffer: 1024 * 1024,
      },
    );
    if (r.error)
      throw new Error(`Appearance analysis needs Python 3: ${r.error.message}`);
    if (r.status !== 0)
      throw new Error(r.stderr.trim() || "Appearance analysis failed");
    result = JSON.parse(r.stdout);
  } else if (command === "image") result = await image(input, v, artifacts);
  else if (command === "inspect") {
    const ext = extname(input).toLowerCase();
    let s, defaults;
    if ([".html", ".htm"].includes(ext)) {
      s = inputHelper("html", await source(input));
      defaults = ["copy", "access", "media"];
    } else if ([".txt", ".md"].includes(ext)) {
      s = {
        nodes: [{ id: "text", text: await source(input) }],
        coverage: { basis: "supplied text source", rendered: false },
      };
      defaults = ["copy"];
    } else {
      s = await jsonFile(input);
      defaults = [];
    }
    const tools = v.tools ? v.tools.split(",").filter(Boolean) : defaults;
    if (!tools.length)
      throw new Error(
        "inspect observations needs --tools; choose instruments from catalog",
      );
    if (
      s.coverage?.rendered === false &&
      tools.some((t) => !["copy", "access", "media"].includes(t))
    )
      throw new Error(
        "Source input cannot establish rendered observations; supply measured evidence for the selected instrument",
      );
    const plan = v.spec ? await jsonFile(v.spec) : s.plan || {};
    result = {
      scope: s.scope || {
        basis:
          s.coverage?.basis ||
          "caller-supplied observations; acquisition and units are caller-owned",
      },
      coverage: s.coverage,
      observations: analyzeObservations(s, tools, plan),
    };
  } else throw new Error(`Unknown command: ${command}`);
  const report =
    JSON.stringify(
      {
        schemaVersion: 1,
        version: VERSION,
        command,
        input: basename(input),
        ...result,
      },
      null,
      2,
    ) + "\n";
  if (v.output) await writeFile(v.output, report);
  else process.stdout.write(report);
}
main().catch((e) => {
  console.error(`design-tools: ${e.message}`);
  process.exitCode = 1;
});
