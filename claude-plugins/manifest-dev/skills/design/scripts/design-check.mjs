#!/usr/bin/env node
// design-check.mjs — bounded triage for an HTML artifact, not conformance.
//
// Usage: node design-check.mjs <file.html>
//
// Static heuristics always run (no browser needed): focus-visible presence,
// reduced-motion gating, single-theme color definitions, spacing-rhythm drift,
// and figures against structural content (a page carrying sequences,
// definition lists, or comparison/flow vocabulary with no figure at all).
// Render samples (opaque flat-color text contrast, overflow at 320/390px, target
// candidates, transparent body background) run when Playwright with a Chromium
// browser is available; otherwise they are reported as SKIPPED so the gap
// stays visible instead of silently passing.
//
// Exit code 0 = checks completed (findings, if any, are printed);
// exit code 1 = the run itself failed (bad usage, unreadable file, crash).

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const file = process.argv[2];
if (!file) {
  console.error("usage: node design-check.mjs <file.html>");
  process.exit(1);
}

let html;
try {
  html = readFileSync(resolve(file), "utf8");
} catch (e) {
  console.error(`cannot read ${file}: ${e.message}`);
  process.exit(1);
}

const findings = []; // Measured candidates, still subject to applicability review.
const notes = [];
const ok = [];
const skipped = [];

// ---------- static checks ----------

// Gather CSS: <style> blocks plus inline style attributes.
const styleBlocks = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map(
  (m) => m[1],
);
const css = styleBlocks.join("\n");
const inlineStyles = [...html.matchAll(/style\s*=\s*"([^"]*)"/gi)]
  .map((m) => m[1])
  .join(";");

const hasInteractive =
  /<(button|a\s|a>|input|select|textarea)/i.test(html) ||
  /role\s*=\s*"button"/i.test(html);
const hasFocusVisible = /:focus-visible/.test(css);
const stripsOutline = /outline\s*:\s*(none|0)/.test(css + inlineStyles);

if (hasInteractive && !hasFocusVisible) {
  notes.push(
    "focus-visible: interactive elements present but no :focus-visible rule — a visible browser default may be sufficient; verify it" +
      (stripsOutline ? ", and an outline:none rule strips even that" : ""),
  );
} else if (stripsOutline && !hasFocusVisible) {
  notes.push(
    "focus-visible: outline stripped (outline:none) with no :focus-visible replacement",
  );
} else {
  notes.push("focus: source syntax inspected; verify the actual keyboard indicator and order");
}

const hasMotion =
  /@keyframes|animation\s*:|animation-name|transition\s*:/.test(css) ||
  /animation\s*:|transition\s*:/.test(inlineStyles);
const hasReducedMotion = /prefers-reduced-motion/.test(css);
if (hasMotion && !hasReducedMotion) {
  notes.push(
    "reduced-motion: animations/transitions present but no prefers-reduced-motion block gates them",
  );
} else {
  notes.push("motion: source syntax inspected; verify actual behavior with the preference enabled");
}

// Single-theme colors: custom properties defined only inside a dark-scheme
// block have no light-theme value (or vice versa).
const darkBlocks = [
  ...css.matchAll(
    /@media[^{]*prefers-color-scheme\s*:\s*dark[^{]*\{([\s\S]*?)\}\s*\}/g,
  ),
]
  .map((m) => m[1])
  .join("\n");
const propDefs = (block) =>
  new Set([...block.matchAll(/(--[\w-]+)\s*:/g)].map((m) => m[1]));
if (darkBlocks) {
  const darkProps = propDefs(darkBlocks);
  const lightCss = css.replace(
    /@media[^{]*prefers-color-scheme\s*:\s*dark[^{]*\{[\s\S]*?\}\s*\}/g,
    "",
  );
  const lightProps = propDefs(lightCss);
  const darkOnly = [...darkProps].filter((p) => !lightProps.has(p));
  if (darkOnly.length) {
    notes.push(
      `single-theme colors: defined only in the dark block, no light value: ${darkOnly.join(", ")}`,
    );
  } else {
    notes.push("two-theme tokens");
  }
} else {
  notes.push(
    "themes: no prefers-color-scheme block detected; class/attribute themes and actual support require inspection",
  );
}

// Spacing rhythm: distinct px values across margin/padding/gap.
const spacingVals = [
  ...css.matchAll(/(?:^|[;{\s])(?:margin|padding|gap|row-gap|column-gap)[\w-]*\s*:\s*([^;}]+)/g),
]
  .flatMap((m) => [...m[1].matchAll(/(\d+(?:\.\d+)?)px/g)].map((v) => parseFloat(v[1])))
  .filter((v) => v > 0);
const distinct = [...new Set(spacingVals)].sort((a, b) => a - b);
if (distinct.length > 10) {
  const counts = {};
  for (const v of spacingVals) counts[v] = (counts[v] || 0) + 1;
  const singles = distinct.filter((v) => counts[v] === 1);
  notes.push(
    `spacing rhythm: ${distinct.length} distinct px spacing values (${distinct.join(", ")}) — a held rhythm needs far fewer` +
      (singles.length ? `; used once each (off-scale candidates): ${singles.join(", ")}` : ""),
  );
} else if (distinct.length) {
  notes.push(`spacing rhythm (${distinct.length} distinct values)`);
}

// Figures against structural content: a page whose subject is structural or
// comparative — sequences, definition lists, comparison or flow vocabulary in
// its headings — and which carries no figure at all is the signature of
// content encoded as prose that a figure would carry. Heuristic: the
// structural signals are counted, not judged, so a prose-only page over a
// non-structural subject stays clean.
const bodyHtml = html
  .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
  .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "");
const proseWords = bodyHtml
  .replace(/<[^>]+>/g, " ")
  .split(/\s+/)
  .filter(Boolean).length;
const figureCount = (bodyHtml.match(/<(svg|figure|img|canvas|picture|video)\b/gi) || []).length;
const structuralSignals = [];
const dlCount = [...bodyHtml.matchAll(/<dl\b[\s\S]*?<\/dl>/gi)].filter(
  (m) => (m[0].match(/<dt\b/gi) || []).length >= 3,
).length;
if (dlCount) structuralSignals.push(`${dlCount} definition list(s) of 3+ terms`);
const olCount = [...bodyHtml.matchAll(/<ol\b[\s\S]*?<\/ol>/gi)].filter(
  (m) => (m[0].match(/<li\b/gi) || []).length >= 3,
).length;
if (olCount) structuralSignals.push(`${olCount} ordered list(s) of 3+ steps`);
const headingText = [...bodyHtml.matchAll(/<(h[1-6]|caption|th)\b[^>]*>([\s\S]*?)<\/\1>/gi)]
  .map((m) => m[2].replace(/<[^>]+>/g, " "))
  .join(" | ");
const flowWords = headingText.match(
  /\b(vs\.?|versus|before|after|flow|flows|pipeline|lane|lanes|phase|phases|stack|architecture|stage|stages|lifecycle|state|states|route|routes|compare|comparison|option|options)\b|→|⇒/gi,
) || [];
if (flowWords.length)
  structuralSignals.push(
    `comparison/flow vocabulary in ${flowWords.length} heading(s) or table label(s)`,
  );
if (figureCount === 0 && proseWords >= 400 && structuralSignals.length >= 2) {
  notes.push(
    `figures: review encoding on a page with no detected figure (${structuralSignals.join("; ")}; ${proseWords} words of prose) — vocabulary is not proof a figure is needed; inspect the task model and existing tables`,
  );
} else if (figureCount === 0 && proseWords >= 400 && structuralSignals.length === 1) {
  notes.push(
    `figures: none on a ${proseWords}-word page with ${structuralSignals[0]} — check the encoding line assigned that content to prose deliberately`,
  );
} else if (figureCount) {
  notes.push(`figures (${figureCount} figure-bearing element(s))`);
} else {
  notes.push("figures (no structural content detected)");
}

// ---------- render checks ----------

const relLum = ({ r, g, b }) => {
  const f = (c) => {
    c /= 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};
const ratio = (a, b) => {
  const [hi, lo] = [relLum(a), relLum(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};

// Resolve Playwright from the script's own tree first, then from the
// invoker's working directory (where a project's node_modules usually lives).
let chromium = null;
for (const name of ["playwright", "playwright-core"]) {
  if (chromium) break;
  try {
    ({ chromium } = await import(name));
    break;
  } catch {
    /* try cwd resolution */
  }
  try {
    const req = createRequire(resolve(process.cwd(), "noop.js"));
    const m = await import(pathToFileURL(req.resolve(name)).href);
    chromium = m.chromium ?? m.default?.chromium ?? null;
  } catch {
    /* not here either */
  }
}

// Some environments ship a Chromium binary without a matching Playwright
// browser registry; allow pointing straight at it.
const chromiumPath =
  process.env.DESIGN_CHECK_CHROMIUM ||
  (existsSync("/opt/pw-browsers/chromium") ? "/opt/pw-browsers/chromium" : null);

async function launchBrowser() {
  try {
    return await chromium.launch();
  } catch (e) {
    if (chromiumPath) return await chromium.launch({ executablePath: chromiumPath });
    throw e;
  }
}

if (!chromium) {
  skipped.push("render samples — Playwright not available");
} else {
  let browser;
  try {
    browser = await launchBrowser();
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, colorScheme: "light" });
    await page.goto(pathToFileURL(resolve(file)).href, { waitUntil: "load" });
    // Freeze animations/transitions so geometry and color measurements are
    // stable (a rotating element inflates its own bounding box).
    await page.addStyleTag({
      content: "*, *::before, *::after { animation: none !important; transition: none !important; }",
    });

    const parse = (s) => {
      const m = s && s.match(/^rgba?\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)(?:,\s*([\d.]+))?\)$/);
      return m
        ? { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] }
        : null;
    };

    // Body background.
    const bodyBg = await page.evaluate(() => {
      const bg = (el) => getComputedStyle(el).backgroundColor;
      return { body: bg(document.body), html: bg(document.documentElement) };
    });
    const bodyC = parse(bodyBg.body);
    const htmlC = parse(bodyBg.html);
    if (!bodyC || !htmlC) {
      skipped.push("body background: unsupported color syntax; inspect the actual canvas");
    } else if (bodyC.a === 0 && htmlC.a === 0) {
      notes.push(
        "body background: transparent on both <body> and <html> — the artifact borrows its host's background and can render unreadable",
      );
    } else {
      ok.push("body background");
    }

    // Conservative samples only: unhandled paint is SKIPPED, never a pass.
    const textInventory = await page.evaluate(() => {
      const out = [];
      const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const seen = new Set();
      let n;
      while ((n = walk.nextNode())) {
        if (!n.textContent.trim()) continue;
        const el = n.parentElement;
        if (!el || seen.has(el)) continue;
        seen.add(el);
        const cs = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        if (cs.visibility !== "visible" || cs.display === "none" || !rect.width || !rect.height) continue;
        const backgrounds = [];
        const effects = [];
        if (el.namespaceURI !== "http://www.w3.org/1999/xhtml") effects.push("non-HTML text paint");
        for (let a = el; a; a = a.parentElement) {
          const style = getComputedStyle(a);
          backgrounds.push(style.backgroundColor);
          if (Number(style.opacity) !== 1) effects.push("opacity");
          if (style.backgroundImage !== "none") effects.push("background image");
          if (style.filter !== "none" || (style.backdropFilter && style.backdropFilter !== "none")) effects.push("filter");
          if (style.mixBlendMode !== "normal" || style.backgroundBlendMode !== "normal") effects.push("blend");
          if (style.maskImage && style.maskImage !== "none") effects.push("mask");
          if (style.textShadow !== "none") effects.push("text shadow");
        }
        if (cs.webkitTextFillColor && cs.webkitTextFillColor !== cs.color) effects.push("text fill");
        if (parseFloat(cs.webkitTextStrokeWidth) > 0) effects.push("text stroke");
        if (el.closest('[disabled], [aria-disabled="true"]')) effects.push("inactive-control exception needs review");
        out.push({
          text: n.textContent.trim().slice(0, 40), tag: el.tagName.toLowerCase(),
          color: cs.color, backgrounds, effects,
          fontSize: parseFloat(cs.fontSize), fontWeight: parseInt(cs.fontWeight, 10) || 400,
        });
      }
      return { samples: out.slice(0, 400), total: out.length };
    });
    let measured = 0;
    let contrastFails = 0;
    const exclusions = new Map();
    const exclude = (reason) => exclusions.set(reason, (exclusions.get(reason) || 0) + 1);
    for (const sample of textInventory.samples) {
      if (sample.effects.length) { exclude([...new Set(sample.effects)].join(", ")); continue; }
      const fg = parse(sample.color);
      if (!fg || fg.a !== 1) { exclude("unsupported or transparent foreground"); continue; }
      let bg = null;
      let reason = "no known opaque background";
      for (const value of sample.backgrounds) {
        const color = parse(value);
        if (!color) { reason = "unsupported background color"; break; }
        if (color.a === 0) continue;
        if (color.a !== 1) { reason = "transparent background requires compositing"; break; }
        bg = color;
        break;
      }
      if (!bg) { exclude(reason); continue; }
      measured++;
      const large = sample.fontSize >= 24 || (sample.fontSize >= 14 * 96 / 72 && sample.fontWeight >= 700);
      const floor = large ? 3 : 4.5;
      const value = ratio(fg, bg);
      if (value < floor) {
        contrastFails++;
        if (contrastFails <= 10) findings.push(
          `contrast candidate: ${value.toFixed(4)}:1 (< ${floor}:1) on <${sample.tag}> "${sample.text}" — confirm applicable text exceptions and actual paint`,
        );
      }
    }
    if (contrastFails > 10) findings.push(`contrast: ${contrastFails - 10} further below-threshold samples`);
    const excluded = [...exclusions.values()].reduce((a, b) => a + b, 0);
    notes.push(`contrast coverage light@1440: ${measured} measured, ${contrastFails} below threshold, ${excluded} skipped, ${textInventory.total - textInventory.samples.length} beyond sample limit`);
    for (const [reason, count] of exclusions) skipped.push(`contrast: ${count} sample(s): ${reason}`);
    if (textInventory.total > textInventory.samples.length) skipped.push("contrast: remaining text beyond the 400-element sample limit");
    if (measured && !contrastFails) ok.push(`contrast: ${measured} supported opaque samples met their thresholds; other paint, states and text are not certified`);
    notes.push("render scope: initial light-theme DOM text, animations frozen; inspect overlap, pseudo-elements, canvas/SVG, other themes and interactive states with appropriate tools");

    // Width and target candidates require applicability/exception review.
    for (const width of [320, 390]) {
      await page.setViewportSize({ width, height: 844 });
      await page.waitForTimeout(150);
      const narrow = await page.evaluate(() => {
        const doc = document.scrollingElement || document.documentElement;
        const small = [];
        let inspected = 0;
        for (const el of document.querySelectorAll(
          'button, a[href], input:not([type="hidden"]), select, textarea, summary, [role="button"], [role="checkbox"], [role="radio"], [role="switch"], [role="tab"]',
        )) {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          if (style.display === "none" || style.visibility !== "visible" || !rect.width || !rect.height) continue;
          inspected++;
          if (rect.width < 24 || rect.height < 24) small.push({
            tag: el.tagName.toLowerCase(), text: (el.textContent || "").trim().slice(0, 30),
            w: Math.round(rect.width), h: Math.round(rect.height),
          });
        }
        return { overflow: doc.scrollWidth > window.innerWidth + 1, scrollWidth: doc.scrollWidth, small: small.slice(0, 10), smallCount: small.length, inspected };
      });
      if (narrow.overflow) notes.push(`overflow@${width}: content width ${narrow.scrollWidth}px — inspect loss of content/function and necessary two-dimensional-content exceptions`);
      else ok.push(`overflow@${width}: no page-width overflow in this state; zoom and content loss remain separate checks`);
      for (const target of narrow.small) notes.push(
        `target candidate@${width}: <${target.tag}> "${target.text}" ${target.w}×${target.h}px — review spacing, equivalent, inline, user-agent and essential exceptions before grading`,
      );
      notes.push(`target coverage@${width}: ${narrow.inspected} detected controls, ${narrow.smallCount} undersized bounding boxes; effective hit areas and custom controls need review`);
    }
  } catch (e) {
    skipped.push(`render checks failed to run: ${e.message.split("\n")[0]}`);
  } finally {
    if (browser) await browser.close();
  }
}

// ---------- report ----------

for (const f of findings) console.log(`FINDING  ${f}`);
for (const n of notes) console.log(`NOTE     ${n}`);
for (const s of skipped) console.log(`SKIPPED  ${s}`);
for (const o of ok) console.log(`OK       ${o}`);
console.log(
  `\n${findings.length} finding(s), ${notes.length} note(s), ${skipped.length} skipped — ${file}`,
);
