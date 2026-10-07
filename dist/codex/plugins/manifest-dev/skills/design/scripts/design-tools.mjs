#!/usr/bin/env node
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve, basename, extname, join } from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import {
  VERSION,
  finite,
  object,
  array,
  named,
  content,
  compare,
  viewing,
  palette,
  associations,
  coVisibility,
  textSummary,
  colorSamples,
  journey,
  fidelity,
  timeline,
  survey,
} from "./measurements.mjs";
import { openArtifact, probe, snapshot } from "./browser.mjs";
import {
  decodePixels,
  describePixels,
  heatmapSvg,
  inspectionViews,
} from "./pixels.mjs";

const instruments = {
  geometry: "Rendered boxes, relationships, grouping, alignment and repetition",
  visibility: "Simultaneous visibility of caller-named decision information",
  typography: "Rendered text lines, font roles and numeric glyph widths",
  copy: "Text, heading, action-label and repeated-string inventories",
  color: "Supported opaque DOM text contrast with explicit exclusions",
  access: "Semantic/name candidates, label associations and coverage gaps",
  targets: "Control boxes and sampled actual pointer reception",
  media: "Assets, dimensions, alternatives and crop/context candidates",
  motion: "Active animation timing inventory in this inspected state",
  image: "Pixel descriptors, local edge map and comparison evidence",
};
const structuredCommands = {
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
node scripts/design-tools.mjs inspect <HTML-or-loopback-URL> --tools geometry,visibility --spec plan.json
node scripts/design-tools.mjs image <PNG-JPEG-WebP-GIF-SVG> --artifacts views
node scripts/design-tools.mjs probe <HTML-or-loopback-URL> --spec steps.json
node scripts/design-tools.mjs ${Object.keys(structuredCommands).join("|")} <JSON>
node scripts/design-tools.mjs print <HTML-or-loopback-URL> --artifacts pages --paper A4|Letter [--landscape]
node scripts/design-tools.mjs compare <report.json> --other <report.json>

Options: --width 1440 --height 900 --theme light|dark --motion no-preference|reduce
--direction ltr|rtl --text-scale 1 --images-off --vision none|blurredVision|achromatopsia|deuteranopia|protanopia|tritanopia
--artifacts <directory> --output <JSON-path> --spec <JSON-path>
--edge-threshold 0.08 --tile-size 16 --allow-network

Choose instruments; none is a required suite or design verdict. Browser commands need
Playwright + Chromium. Set DESIGN_TOOLS_PLAYWRIGHT to a module directory when it is
outside the project. Network is blocked except loopback unless explicitly enabled.
--text-scale changes CSS text sizes; it is a stress simulation, not browser zoom.
See references/instruments/index.md and usage.md in this skill for input schemas and limits.
`;
async function jsonFile(file) {
  if (!file) throw new Error("An input file is required");
  try {
    return JSON.parse(await readFile(file, "utf8"));
  } catch (e) {
    throw new Error(`Cannot read JSON ${basename(file)}: ${e.message}`);
  }
}
function enumValue(value, allowed, name) {
  if (!allowed.includes(value))
    throw new Error(`${name} must be ${allowed.join("|")}`);
  return value;
}
function positive(value, name) {
  const v = Number(value);
  finite(v, name);
  if (v <= 0 || v > 16384) throw new Error(`${name} must be >0 and <=16384`);
  return v;
}
function integer(value, name) {
  const n = positive(value, name);
  if (!Number.isInteger(n)) throw new Error(`${name} must be an integer`);
  return n;
}
function validatePlan(spec) {
  object(spec, "measurement plan");
  if (spec.entities) object(spec.entities, "entities");
  for (const key of ["links", "groups", "alignments", "steps"])
    if (spec[key]) array(spec[key], key);
  for (const [id, selector] of Object.entries(spec.entities || {}))
    if (!id || typeof selector !== "string" || !selector)
      throw new Error("entity names/selectors must be nonempty strings");
  const known = (id) => {
    if (!Object.hasOwn(spec.entities || {}, id))
      throw new Error(`Unknown named entity: ${id}`);
  };
  for (const link of spec.links || []) {
    object(link, "link");
    if (link.competitors) array(link.competitors, "competitors");
    known(link.from);
    known(link.to);
    for (const id of link.competitors || []) known(id);
  }
  for (const group of spec.groups || []) {
    object(group, "group");
    if (!Array.isArray(group.members) || !group.members.length)
      throw new Error("groups need nonempty members");
    for (const id of group.members) known(id);
  }
  for (const group of spec.alignments || []) {
    object(group, "alignment");
    if (!Array.isArray(group.members) || !group.members.length)
      throw new Error("alignments need nonempty members");
    for (const id of group.members) known(id);
  }
}
function alignment(groups, entities) {
  return groups.map((g) => {
    const axis = enumValue(
      g.axis || "left",
      ["left", "right", "top", "bottom", "width", "height"],
      "alignment axis",
    );
    const vals = g.members.map((id) => {
      const b = entities[id].box;
      return {
        id,
        value:
          axis === "left"
            ? b.x
            : axis === "right"
              ? b.x + b.width
              : axis === "top"
                ? b.y
                : axis === "bottom"
                  ? b.y + b.height
                  : b[axis],
      };
    });
    return {
      id: g.id,
      axis,
      values: vals,
      rangePx:
        vals.reduce((m, v) => Math.max(m, v.value), -Infinity) -
        vals.reduce((m, v) => Math.min(m, v.value), Infinity),
      limits:
        "Caller-selected comparable roles. Optical alignment and intentional variation require judgment.",
    };
  });
}
function geometrySvg(s, spec) {
  const escape = (value) =>
    String(value).replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&apos;",
        })[c],
    );
  const boxes = Object.keys(spec.entities || {}).map((id) => {
    const b = s.entities[id].box;
    return `<g><title>${escape(id)}</title><rect x="${b.x}" y="${b.y}" width="${b.width}" height="${b.height}" fill="none" stroke="#04a"/><text x="${b.x}" y="${b.y + 12}" font-size="12" fill="#04a">${escape(id)}</text></g>`;
  });
  const lines = (spec.links || []).map((l) => {
    const a = s.entities[l.from].box,
      b = s.entities[l.to].box;
    return `<line x1="${a.x + a.width / 2}" y1="${a.y + a.height / 2}" x2="${b.x + b.width / 2}" y2="${b.y + b.height / 2}" stroke="#b23"/>`;
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${s.viewport.width}" height="${s.viewport.height}">${boxes.join("")}${lines.join("")}</svg>`;
}
async function saveInspectionViews(page, screenshot, directory) {
  const files = [];
  for (const [name, data] of Object.entries(
    await inspectionViews(page, screenshot),
  )) {
    const file = `${name}.png`;
    await writeFile(join(directory, file), Buffer.from(data, "base64"));
    files.push(file);
  }
  return files;
}
async function rendered(file, opts, spec, tools, artifacts) {
  return openArtifact(file, opts, async (page, environment) => {
    if (tools.includes("print")) {
      await page.emulateMedia({ media: "print" });
      await page.pdf({
        path: join(artifacts, "artifact.pdf"),
        format: opts.paper,
        landscape: opts.landscape,
        printBackground: true,
        preferCSSPageSize: true,
      });
      return {
        environment,
        scope: {
          media: "print",
          paper: opts.paper,
          landscape: opts.landscape,
          preferCSSPageSize: true,
        },
        artifacts: ["artifact.pdf"],
        limits:
          "Chromium print output. Inspect actual PDF pages for pagination and content; screen box observations do not establish final page positions. Native document exports and physical printing remain unmeasured.",
      };
    }
    const result = {
      environment,
      scope: {
        viewport: { width: opts.width, height: opts.height },
        pixelCapture:
          "Live state; animation may advance between DOM sample and screenshot. Use a stable supplied state for matched comparisons",
        theme: opts.theme,
        motion: opts.motion,
        direction: opts.direction,
        textScale: opts.textScale,
        imagesOff: opts.imagesOff,
        vision: opts.vision,
      },
      observations: {},
    };
    if (tools.includes("probe"))
      result.observations.probe = await probe(page, spec);
    const s = await snapshot(page, spec);
    result.coverage = s.coverage;
    if (tools.includes("geometry"))
      result.observations.geometry = {
        entities: s.entities,
        associations: associations(spec.links || [], s.entities),
        alignments: alignment(spec.alignments || [], s.entities),
        limits:
          "Reported boxes, not optical boundaries or quality. No required geometry scale.",
      };
    if (tools.includes("visibility"))
      result.observations.visibility = {
        groups: coVisibility(spec.groups || [], s.entities, s.viewport),
        documentSize: s.documentSize,
        limits:
          "Viewport and named-element boxes. Content loss can occur without page overflow.",
      };
    if (tools.includes("typography")) {
      const glyphWidths = await page.evaluate(
        (selectors) =>
          selectors.map((selector) => {
            const e = document.querySelector(selector),
              s = getComputedStyle(e),
              span = document.createElement("span");
            // Append a hidden measuring span to inherit this exact font shaping context.
            span.style.cssText =
              "position:absolute;visibility:hidden;white-space:pre;padding:0;border:0;margin:0;display:inline-block;";
            for (const key of [
              "fontFamily",
              "fontSize",
              "fontWeight",
              "fontStyle",
              "fontStretch",
              "fontVariantNumeric",
              "fontFeatureSettings",
              "fontVariationSettings",
              "fontOpticalSizing",
              "letterSpacing",
              "direction",
            ])
              span.style[key] = s[key];
            document.body.append(span);
            const widths = {};
            for (const g of "-+0123456789.,%") {
              span.textContent = g;
              widths[g] = span.getBoundingClientRect().width;
            }
            span.remove();
            return {
              selector,
              font: s.font,
              variation: s.fontVariationSettings,
              numeric: s.fontVariantNumeric,
              widths,
            };
          }),
        Object.values(spec.entities || {}),
      );
      result.observations.typography = {
        ...textSummary(s.nodes),
        glyphWidths,
        limits:
          "DOM Range line estimates and DOM glyph advances inherited from selected elements. Font features, fallback, shaping and optical fit need actual-content inspection.",
      };
    }
    if (tools.includes("copy"))
      result.observations.copy = {
        ...textSummary(s.nodes),
        headings: s.headings,
        actions: s.controls.map((e) => ({
          id: e.id,
          text: e.text,
          nameCandidate: e.nameCandidate,
          visible: e.visible,
        })),
        limits:
          "Counts and candidate labels, not specificity, tone, honest information scent or comprehension.",
      };
    if (tools.includes("color"))
      result.observations.color = colorSamples(s.nodes);
    if (tools.includes("access"))
      result.observations.access = {
        controls: s.controls.map(
          ({
            id,
            tag,
            role,
            nameCandidate,
            namingSource,
            associatedLabels,
            placeholder,
            formAttributes,
            tabIndex,
            visible,
          }) => ({
            id,
            tag,
            role,
            nameCandidate,
            namingSource,
            associatedLabels,
            placeholder,
            formAttributes,
            tabIndex,
            visible,
          }),
        ),
        headings: s.headings,
        media: s.media,
        languages: s.languages,
        limits:
          "DOM candidate inventory, not the full accessibility tree or conformance. aria-labelledby, descriptions, shadow roots, frames and assistive announcements require appropriate inspection.",
      };
    if (tools.includes("targets"))
      result.observations.targets = {
        controls: s.controls,
        limits:
          "Five viewport sample points per detected control; not a measured complete hit region or touch-error predictor. Inline/equivalent/spacing/platform exceptions remain contextual.",
      };
    if (tools.includes("media"))
      result.observations.media = {
        assets: s.media,
        limits:
          "DOM dimensions and alternatives. Documentary truth, relevance, optical fit, print and actual email-client behavior are not measured.",
      };
    if (tools.includes("motion"))
      result.observations.motion = {
        animations: s.animations,
        limits:
          "Active Web Animations inventory at the sampled state, not all motion, canvas/video, frame-time or input-to-photon timing.",
      };
    if (tools.includes("image") || artifacts) {
      const screenshot = await page.screenshot();
      if (tools.includes("image")) {
        const pixels = await decodePixels(page, screenshot, "image/png");
        result.observations.image = {
          ...describePixels(pixels.data, pixels.width, pixels.height, {
            threshold: opts.edgeThreshold,
            tileSize: opts.tileSize,
          }),
          originalSize: pixels.originalSize,
        };
      }
      if (artifacts) {
        await writeFile(join(artifacts, "view.png"), screenshot);
        const viewFiles = await saveInspectionViews(
          page,
          screenshot,
          artifacts,
        );
        if (tools.includes("geometry"))
          await writeFile(
            join(artifacts, "geometry.svg"),
            geometrySvg(s, spec),
          );
        if (result.observations.image)
          await writeFile(
            join(artifacts, "edges.svg"),
            heatmapSvg(result.observations.image),
          );
        result.artifacts = [
          "view.png",
          ...viewFiles,
          ...(tools.includes("geometry") ? ["geometry.svg"] : []),
          ...(result.observations.image ? ["edges.svg"] : []),
        ];
      }
    }
    return result;
  });
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
      width: { type: "string", default: "1440" },
      height: { type: "string", default: "900" },
      theme: { type: "string", default: "light" },
      motion: { type: "string", default: "no-preference" },
      direction: { type: "string" },
      "text-scale": { type: "string", default: "1" },
      "images-off": { type: "boolean" },
      vision: { type: "string", default: "none" },
      "allow-network": { type: "boolean" },
      "edge-threshold": { type: "string", default: ".08" },
      "tile-size": { type: "string", default: "16" },
      paper: { type: "string", default: "A4" },
      landscape: { type: "boolean" },
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
          structured: Object.keys(structuredCommands),
          other: ["probe", "image", "compare", "print"],
        },
        null,
        2,
      ),
    );
    return;
  }
  if (!input) throw new Error("An input file or loopback URL is required");
  let result;
  if (Object.hasOwn(structuredCommands, command))
    result = {
      observations: {
        [command]: structuredCommands[command](await jsonFile(input)),
      },
    };
  else if (command === "compare") {
    if (!v.other) throw new Error("compare requires --other");
    result = {
      observations: {
        compare: compare(await jsonFile(input), await jsonFile(v.other)),
      },
    };
  } else if (["inspect", "probe", "image", "print"].includes(command)) {
    const opts = {
      width: integer(v.width, "width"),
      height: integer(v.height, "height"),
      theme: enumValue(v.theme, ["light", "dark"], "theme"),
      motion: enumValue(v.motion, ["no-preference", "reduce"], "motion"),
      direction: v.direction
        ? enumValue(v.direction, ["ltr", "rtl"], "direction")
        : null,
      textScale: positive(v["text-scale"], "text scale"),
      imagesOff: !!v["images-off"],
      vision: enumValue(
        v.vision,
        [
          "none",
          "blurredVision",
          "achromatopsia",
          "deuteranopia",
          "protanopia",
          "tritanopia",
        ],
        "vision",
      ),
      allowNetwork: !!v["allow-network"],
      edgeThreshold: Number(v["edge-threshold"]),
      tileSize: Number(v["tile-size"]),
      paper: enumValue(v.paper, ["A4", "Letter"], "paper"),
      landscape: !!v.landscape,
    };
    const spec = v.spec ? await jsonFile(v.spec) : {};
    validatePlan(spec);
    const tools =
      command === "image"
        ? ["image"]
        : command === "probe"
          ? ["probe"]
          : command === "print"
            ? ["print"]
            : (v.tools || "").split(",").filter(Boolean);
    if (!tools.length)
      throw new Error(
        "inspect needs --tools; use catalog to choose instruments",
      );
    for (const t of tools)
      if (command === "inspect" && !Object.hasOwn(instruments, t))
        throw new Error(`Unknown instrument: ${t}`);
    const artifacts = v.artifacts ? resolve(v.artifacts) : null;
    if (command === "print" && !artifacts)
      throw new Error("print requires --artifacts directory");
    if (artifacts) await mkdir(artifacts, { recursive: true });
    let url;
    if (/^https?:\/\//.test(input)) {
      const u = new URL(input);
      if (
        !opts.allowNetwork &&
        !["localhost", "127.0.0.1", "[::1]"].includes(u.hostname)
      )
        throw new Error("Remote URLs require explicit --allow-network");
      url = input;
    } else if (command === "image") {
      const mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
      }[extname(input).toLowerCase()];
      if (!mime) throw new Error("Unsupported image format");
      const image = (await readFile(input)).toString("base64");
      url = `data:text/html,${encodeURIComponent(`<html><body style="margin:0"><img style="max-width:100vw;max-height:100vh;object-fit:contain" alt="Supplied image" src="data:${mime};base64,${image}"></body></html>`)}`;
      // Image descriptors use original image pixels, independently of viewport crop.
      result = await openArtifact(url, opts, async (page, environment) => {
        const pixels = await decodePixels(
          page,
          Buffer.from(image, "base64"),
          mime,
        );
        const description = describePixels(
          pixels.data,
          pixels.width,
          pixels.height,
          { threshold: opts.edgeThreshold, tileSize: opts.tileSize },
        );
        let artifactFiles;
        if (artifacts) {
          await writeFile(
            join(artifacts, "edges.svg"),
            heatmapSvg(description),
          );
          const shot = await page.screenshot();
          await writeFile(join(artifacts, "view.png"), shot);
          artifactFiles = [
            "view.png",
            "edges.svg",
            ...(await saveInspectionViews(page, shot, artifacts)),
          ];
        }
        return {
          environment,
          scope: { imageSize: pixels.originalSize, vision: opts.vision },
          observations: {
            image: { ...description, originalSize: pixels.originalSize },
          },
          ...(artifactFiles ? { artifacts: artifactFiles } : {}),
          limits:
            "Descriptors use original pixels; --vision affects the inspection preview only. GIF descriptors use the browser-decoded frame, not temporal behavior.",
        };
      });
    } else {
      await readFile(input);
      url = pathToFileURL(resolve(input)).href;
    }
    if (!result) result = await rendered(url, opts, spec, tools, artifacts);
  } else throw new Error(`Unknown command: ${command}`);
  result = {
    schemaVersion: 1,
    version: VERSION,
    command,
    input: basename(input),
    ...result,
  };
  const output = JSON.stringify(result, null, 2) + "\n";
  if (v.output) await writeFile(v.output, output);
  else process.stdout.write(output);
}
main().catch((e) => {
  console.error(`design-tools: ${e.message}`);
  process.exitCode = 1;
});
