#!/usr/bin/env node
// design-check.mjs — mechanical design checks for an HTML artifact.
//
// Usage: node design-check.mjs <file.html>
//
// Static checks always run (no browser needed): focus-visible presence,
// reduced-motion gating, single-theme color definitions, spacing-rhythm drift,
// and figures against structural content (a page carrying sequences,
// definition lists, or comparison/flow vocabulary with no figure at all).
// Render checks (text contrast, horizontal overflow at 390px, touch-target
// size, transparent body background) run when Playwright with a Chromium
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

const findings = [];
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
  findings.push(
    "focus-visible: interactive elements present but no :focus-visible rule — keyboard users get no focus indicator beyond the default" +
      (stripsOutline ? ", and an outline:none rule strips even that" : ""),
  );
} else if (stripsOutline && !hasFocusVisible) {
  findings.push(
    "focus-visible: outline stripped (outline:none) with no :focus-visible replacement",
  );
} else {
  ok.push("focus-visible");
}

const hasMotion =
  /@keyframes|animation\s*:|animation-name|transition\s*:/.test(css) ||
  /animation\s*:|transition\s*:/.test(inlineStyles);
const hasReducedMotion = /prefers-reduced-motion/.test(css);
if (hasMotion && !hasReducedMotion) {
  findings.push(
    "reduced-motion: animations/transitions present but no prefers-reduced-motion block gates them",
  );
} else {
  ok.push("reduced-motion");
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
    findings.push(
      `single-theme colors: defined only in the dark block, no light value: ${darkOnly.join(", ")}`,
    );
  } else {
    ok.push("two-theme tokens");
  }
} else {
  notes.push(
    "themes: no prefers-color-scheme block found (fine for a deliberately single-theme artifact; a defect if both themes are claimed)",
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
  findings.push(
    `spacing rhythm: ${distinct.length} distinct px spacing values (${distinct.join(", ")}) — a held rhythm needs far fewer` +
      (singles.length ? `; used once each (off-scale candidates): ${singles.join(", ")}` : ""),
  );
} else if (distinct.length) {
  ok.push(`spacing rhythm (${distinct.length} distinct values)`);
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
  findings.push(
    `figures: no figure on a page carrying structural content (${structuralSignals.join("; ")}; ${proseWords} words of prose) — a mechanism, comparison, or sequence assembled from prose that a figure would carry; see the task model's encoding line`,
  );
} else if (figureCount === 0 && proseWords >= 400 && structuralSignals.length === 1) {
  notes.push(
    `figures: none on a ${proseWords}-word page with ${structuralSignals[0]} — check the encoding line assigned that content to prose deliberately`,
  );
} else if (figureCount) {
  ok.push(`figures (${figureCount} figure-bearing element(s))`);
} else {
  ok.push("figures (no structural content detected)");
}

// ---------- render checks ----------

const relLum = ({ r, g, b }) => {
  const f = (c) => {
    c /= 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
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
  skipped.push("contrast, overflow@390, touch targets, body background — Playwright not available");
} else {
  let browser;
  try {
    browser = await launchBrowser();
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto("file://" + resolve(file), { waitUntil: "load" });
    // Freeze animations/transitions so geometry and color measurements are
    // stable (a rotating element inflates its own bounding box).
    await page.addStyleTag({
      content: "*, *::before, *::after { animation: none !important; transition: none !important; }",
    });

    const parse = (s) => {
      const m = s && s.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
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
    if ((!bodyC || bodyC.a === 0) && (!htmlC || htmlC.a === 0)) {
      findings.push(
        "body background: transparent on both <body> and <html> — the artifact borrows its host's background and can render unreadable",
      );
    } else {
      ok.push("body background");
    }

    // Contrast on visible text elements.
    const textSamples = await page.evaluate(() => {
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
        if (cs.visibility === "hidden" || cs.display === "none") continue;
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) continue;
        // Effective background: nearest ancestor with a non-transparent color;
        // background images make contrast uncomputable here — mark them.
        let bg = null;
        let hasImage = false;
        for (let a = el; a; a = a.parentElement) {
          const acs = getComputedStyle(a);
          if (acs.backgroundImage && acs.backgroundImage !== "none") {
            hasImage = true;
            break;
          }
          const c = acs.backgroundColor;
          if (c && !c.startsWith("rgba(0, 0, 0, 0")) {
            bg = c;
            break;
          }
        }
        out.push({
          text: n.textContent.trim().slice(0, 40),
          tag: el.tagName.toLowerCase(),
          cls: (el.className && String(el.className).slice(0, 40)) || "",
          color: cs.color,
          bg,
          hasImage,
          fontSize: parseFloat(cs.fontSize),
          fontWeight: parseInt(cs.fontWeight, 10) || 400,
        });
      }
      return out.slice(0, 400);
    });

    let contrastFails = 0;
    let imageSkips = 0;
    for (const s of textSamples) {
      if (s.hasImage) {
        imageSkips++;
        continue;
      }
      const fg = parse(s.color);
      const bg = parse(s.bg) || { r: 255, g: 255, b: 255, a: 1 };
      if (!fg) continue;
      const large = s.fontSize >= 24 || (s.fontSize >= 18.66 && s.fontWeight >= 700);
      const floor = large ? 3.0 : 4.5;
      const r = ratio(fg, bg);
      if (r < floor - 0.01) {
        contrastFails++;
        if (contrastFails <= 10) {
          findings.push(
            `contrast: ${r.toFixed(2)}:1 (< ${floor}:1) on <${s.tag}${s.cls ? " ." + s.cls : ""}> "${s.text}" — ${s.color} on ${s.bg || "default white"}`,
          );
        }
      }
    }
    if (contrastFails > 10)
      findings.push(`contrast: ${contrastFails - 10} further failing text elements not listed`);
    if (!contrastFails) ok.push(`contrast (${textSamples.length} text elements sampled)`);
    if (imageSkips)
      notes.push(
        `contrast: ${imageSkips} text elements sit over background images — verify those against the image's worst region by eye`,
      );

    // 390px checks.
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForTimeout(150);
    const narrow = await page.evaluate(() => {
      const doc = document.scrollingElement || document.documentElement;
      const overflow = doc.scrollWidth > window.innerWidth + 1;
      const small = [];
      for (const el of document.querySelectorAll(
        'button, a[href], input[type="button"], input[type="submit"], [role="button"]',
      )) {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden") continue;
        if (r.width === 0 || r.height === 0) continue;
        if (r.width < 24 || r.height < 24)
          small.push({
            tag: el.tagName.toLowerCase(),
            text: (el.textContent || "").trim().slice(0, 30),
            w: Math.round(r.width),
            h: Math.round(r.height),
          });
      }
      return { overflow, scrollWidth: doc.scrollWidth, small: small.slice(0, 10) };
    });
    if (narrow.overflow) {
      findings.push(
        `overflow@390: page scrolls horizontally at 390px (content width ${narrow.scrollWidth}px) — wide content needs its own overflow-x wrapper`,
      );
    } else {
      ok.push("overflow@390");
    }
    if (narrow.small.length) {
      for (const t of narrow.small)
        findings.push(
          `touch target: <${t.tag}> "${t.text}" is ${t.w}×${t.h}px at 390px — below the 24px floor (44px is the target)`,
        );
    } else {
      ok.push("touch targets@390");
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
