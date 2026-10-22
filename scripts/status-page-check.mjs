#!/usr/bin/env node
// Renders orchestrate's status page headless in the states a person meets it in, writes a normal and
// a blurred screenshot of each, and fails on the facts a script can decide: the sample is accepted,
// nothing throws, what needs the person is styled to stand out, an open Ticket reads in its fixed
// order with its action in view, older snapshots still render, and a malformed one keeps the last
// good view. Whether the screenshots pass the squint test is read by a person or a reviewer.
//
//   node scripts/status-page-check.mjs [OUT_DIR] [--template PATH]
//
// Playwright is found as scripts/design-evals/browser.mjs finds it (DESIGN_TOOLS_PLAYWRIGHT,
// DESIGN_TOOLS_CHROMIUM). Exit codes: 0 every check held, 1 a check failed, 3 no browser.
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { browserEngine } from "./design-evals/browser.mjs";

const ROOT = resolve(import.meta.dirname, "..");
const args = process.argv.slice(2);
const at = args.indexOf("--template");
const TEMPLATE = resolve(at >= 0 ? args.splice(at, 2)[1] : join(ROOT, "claude-plugins/manifest-dev/skills/orchestrate/assets/status-page.html"));
// Screenshots go where the caller says, else beside the harness's evidence (ignored by git), one folder per run.
const OUT = resolve(args[0] || (process.env.VERIFY_RUN_ID ? join(ROOT, "verification/evidence/status-page", "shots-" + process.env.VERIFY_RUN_ID) : mkdtempSync(join(tmpdir(), "status-page-"))));
mkdirSync(OUT, { recursive: true });

// The sizes and blur the visual review reads: desktop 1440×900, phone 390×844.
const DESKTOP = { width: 1440, height: 900 };
const PHONE = { width: 390, height: 844 };
const BLUR_PAGE = "7px";
const BLUR_PANEL = "5px";
const NEW_FIELDS = ["summary", "why", "change", "done", "type", "foundWhile"];
const DATA = /(<script type="application\/json" id="orchestrate-status">)([\s\S]*?)(<\/script>)/;

const html = readFileSync(TEMPLATE, "utf8");
const sample = JSON.parse(html.match(DATA)[2]);
const failures = [];
const facts = {};
function check(name, ok, detail) {
  facts[name] = { ok: !!ok, ...(detail === undefined ? {} : { detail }) };
  if (!ok) failures.push(name + (detail === undefined ? "" : ": " + JSON.stringify(detail)));
}
// A section that throws (a control missing, a click timing out) fails by name and the run goes on.
async function section(name, fn) {
  try { await fn(); } catch (e) { check(`${name}: ran to the end`, false, e.message.split("\n")[0]); }
}
// A variant of the page with another snapshot inline, written beside the screenshots.
function variant(name, snapshot) {
  const json = JSON.stringify(snapshot, null, 1).replace(/</g, "\\u003c");
  const file = join(OUT, name + ".html");
  writeFileSync(file, html.replace(DATA, (_, a, __, c) => a + "\n" + json + "\n" + c));
  return pathToFileURL(file).href;
}

let chromium;
try {
  chromium = await browserEngine();
} catch (e) {
  console.error("status-page-check: " + e.message);
  console.error("Point DESIGN_TOOLS_PLAYWRIGHT at a playwright or playwright-core directory, and DESIGN_TOOLS_CHROMIUM at a Chromium it can launch.");
  process.exit(3);
}
let browser;
try {
  browser = await chromium.launch({ headless: true, ...(process.env.DESIGN_TOOLS_CHROMIUM ? { executablePath: process.env.DESIGN_TOOLS_CHROMIUM } : {}) });
} catch (e) {
  console.error("status-page-check: Chromium did not launch: " + e.message.split("\n")[0]);
  console.error("Set DESIGN_TOOLS_CHROMIUM to a Chromium executable this Playwright can drive.");
  process.exit(3);
}

async function open(url, { size = DESKTOP, theme = "dark", touch = false } = {}) {
  const context = await browser.newContext({ viewport: size, colorScheme: theme, reducedMotion: "reduce", hasTouch: touch, isMobile: touch, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.setDefaultTimeout(5000);
  const log = { errors: [], warnings: [] };
  page.on("pageerror", (e) => log.errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "warning" || m.type() === "error") log.warnings.push(m.text()); });
  await page.route("**/*", (r) => (/^(file|data|blob|about):/.test(r.request().url()) ? r.continue() : r.abort()));
  await page.goto(url, { waitUntil: "load" });
  // The page installs its check hook only once its inline snapshot is accepted.
  await page.waitForFunction(() => window.__orchestrateStatus, null, { timeout: 5000 }).catch(() => {
    throw new Error("the page did not accept its inline snapshot: " + (log.warnings.concat(log.errors).join(" | ") || "no message"));
  });
  await settle(page);
  return { page, context, log };
}
async function settle(page) {
  // Motion is reduced, so the page settles in moments; one that never does fails rather than being shot mid-motion.
  await page.waitForFunction(() => !window.__orchestrateStatus.busy(), null, { timeout: 5000 }).catch(() => {
    throw new Error("the page was still animating after 5 s");
  });
  await page.waitForTimeout(150);
}
async function shoot(page, name, blurTarget) {
  await page.screenshot({ path: join(OUT, name + ".png") });
  const sel = blurTarget === "panel" ? "#sheet" : "html";
  await page.evaluate(([s, b]) => { document.querySelector(s).style.filter = "blur(" + b + ")"; }, [sel, blurTarget === "panel" ? BLUR_PANEL : BLUR_PAGE]);
  await page.screenshot({ path: join(OUT, name + "-blur.png") });
  await page.evaluate((s) => { document.querySelector(s).style.filter = ""; }, sel);
}
async function openDetail(page, id) {
  await page.focus(`[data-id="${id}"]`);
  await page.keyboard.press("Enter");
  await settle(page);
}
async function closeSheet(page) {
  await page.keyboard.press("Escape");
  await settle(page);
}
// The open panel's blocks, in reading order, and whether its one action is in view above the dock.
function panelFacts(page) {
  return page.evaluate(() => {
    const body = document.getElementById("sheetBody");
    const BLOCKS = [["lede", "summary"], ["missing", "summary"], ["meta", "meta"], ["decide", "decision"], ["ba", "change"], ["sec", "status"]];
    const order = [...body.children].map((n) => {
      if (n.tagName === "H2") return "title";
      const hit = BLOCKS.find(([cls]) => n.classList.contains(cls));
      if (hit) return hit[1];
      return n.classList.contains("arow") ? (n.querySelector("h3") || {}).textContent : n.className;
    });
    const act = body.querySelector(".decide .act > *");
    const dock = document.getElementById("needsBtn").getBoundingClientRect();
    const r = act && act.getBoundingClientRect();
    const sheet = document.getElementById("sheet").getBoundingClientRect();
    const limit = innerWidth >= 760 ? innerHeight : Math.min(innerHeight, dock.top);
    return { order, actionInView: !!r && r.bottom <= limit && r.top >= sheet.top, overflowX: body.scrollWidth > body.clientWidth + 1 };
  });
}
const tones = (page) => page.evaluate(() => Object.fromEntries([...document.querySelectorAll("[data-id]")].map((g) => [g.getAttribute("data-id"), [...g.classList].find((c) => c.startsWith("n-"))])));

const statusOf = Object.fromEntries(sample.tickets.map((t) => [t.id, t.status]));
const NEEDS = new Set(["held", "grant", "proposal", "escalated", "failed"]);
const STUCK = new Set(["escalated", "failed"]);
const stuck = sample.tickets.find((t) => STUCK.has(t.status));
const held = sample.tickets.find((t) => t.status === "held");
const landed = sample.tickets.find((t) => t.status === "landed");

// 1. The graph, dark and light: what needs the person is the only loud thing.
for (const theme of ["dark", "light"]) await section(`graph ${theme}`, async () => {
  const { page, context, log } = await open(pathToFileURL(TEMPLATE).href, { theme });
  check(`${theme}: sample accepted, nothing thrown`, !log.errors.length && !log.warnings.some((w) => w.includes("ignored a snapshot")), log);
  if (theme === "dark") {
    const t = await tones(page);
    const wrong = Object.entries(t).filter(([id, c]) => NEEDS.has(statusOf[id]) !== (c === "n-you" || c === "n-stop") || STUCK.has(statusOf[id]) !== (c === "n-stop"));
    check("cards needing the person carry the loud tones, stuck ones the loudest", !wrong.length, wrong);
    const btn = await page.evaluate(() => ({ cls: document.getElementById("needsBtn").className, title: document.title }));
    check("Needs you button is urgent, and red while a Ticket is stuck", btn.cls.includes("urgent") && btn.cls.includes("stop") === !!stuck, btn.cls);
    check("tab title carries the count", btn.title.startsWith(`(${sample.needsYou.length}) `), btn.title);
    // A card recedes through its surface, never by fading its text, which would drop it below readable contrast.
    const faded = await page.evaluate(() => [...document.querySelectorAll("[data-id] text")].filter((t) => {
      let o = 1;
      for (let n = t; n && n.tagName !== "svg"; n = n.parentNode) o *= Number(getComputedStyle(n).opacity);
      return o < 0.99;
    }).map((t) => t.closest("[data-id]").getAttribute("data-id") + ": " + t.textContent.slice(0, 24)));
    check("no card text is faded", !faded.length, [...new Set(faded)].slice(0, 6));
  }
  await shoot(page, `graph-${theme}`, "page");
  if (theme === "dark") {
    for (const [name, tk] of [["detail-stuck", stuck], ["detail-held", held]]) {
      if (!tk) { check(`${name}: the sample has such a Ticket`, false); continue; }
      await openDetail(page, tk.id);
      const f = await panelFacts(page);
      const want = ["title", "summary", "meta", "decision"];
      check(`${name}: opens with title, summary, links, then the decision`, want.every((w, i) => f.order[i] === w), f.order);
      check(`${name}: where it stands comes last`, f.order[f.order.length - 1] === "status", f.order);
      check(`${name}: the decision's action is in view`, f.actionInView, f);
      check(`${name}: the evidence is folded`, await page.evaluate(() => { const d = document.querySelector("#sheetBody .decide details"); return !!d && !d.open; }));
      await shoot(page, name, "panel");
      await closeSheet(page);
    }
    const peeked = sample.tickets.find((t) => t.summary);
    await page.hover(`[data-id="${peeked.id}"]`);
    check("hovering a card shows its summary beside it", await page.waitForFunction((want) => { const p = document.getElementById("peek"); return p.classList.contains("on") && p.textContent.includes(want); }, peeked.summary, { timeout: 1500 }).then(() => true, () => false));
    await page.mouse.move(2, 880);
    await page.waitForTimeout(150);
    await page.click("#needsBtn");
    await settle(page);
    const rows = await page.evaluate(() => document.querySelectorAll("#sheetBody .row").length);
    check("Needs you lists every item", rows === sample.needsYou.length, rows);
    await shoot(page, "needs", "panel");
    await closeSheet(page);
    await page.click("#keyBtn");
    await settle(page);
    check("the key explains colours and lines", await page.evaluate(() => document.querySelectorAll("#sheetBody .legend li").length >= 8));
    await shoot(page, "key", "panel");
    await closeSheet(page);
    if (landed) {
      await openDetail(page, landed.id);
      check("a landed Ticket's done list shows as met", await page.evaluate(() => document.querySelector("#sheetBody .done.met") !== null));
      await closeSheet(page);
    }
  }
  check(`${theme}: no error after use`, !log.errors.length, log.errors);
  await context.close();
});

// 2. A phone: a tap opens the sheet with no stray focus ring; the keyboard still shows one.
await section("phone", async () => {
  const { page, context, log } = await open(pathToFileURL(TEMPLATE).href, { size: PHONE, theme: "light", touch: true });
  const first = landed || sample.tickets[0];
  const ring = () => page.evaluate(() => { const a = document.activeElement, s = getComputedStyle(a); return { id: a.id, ring: s.outlineStyle !== "none" && parseFloat(s.outlineWidth) > 0 }; });
  const box = await page.locator(`[data-id="${first.id}"]`).boundingBox();
  await page.touchscreen.tap(box.x + box.width / 2, box.y + box.height / 2);
  await settle(page);
  const tapped = await ring();
  check("phone: a tap opens the sheet and leaves no focus ring", (await page.evaluate(() => window.__orchestrateStatus.state().sheet)) === "detail" && !tapped.ring, tapped);
  check("phone: the sheet is modal", await page.evaluate(() => document.getElementById("stage").inert && document.getElementById("sheet").getAttribute("aria-modal") === "true"));
  await shoot(page, "phone-detail", "panel");
  await closeSheet(page);
  await page.evaluate((id) => document.querySelector(`[data-id="${id}"]`).focus(), first.id);
  await page.keyboard.press("Enter");
  await settle(page);
  const keyed = await ring();
  check("phone: the keyboard still shows the focus ring on Done", keyed.id === "sheetDone" && keyed.ring, keyed);
  check("phone: no error", !log.errors.length, log.errors);
  await context.close();
});

// 3. A snapshot written before the new fields existed still renders every Ticket and its peek.
await section("older snapshot", async () => {
  const old = structuredClone(sample);
  old.tickets.forEach((t) => NEW_FIELDS.forEach((f) => delete t[f]));
  const { page, context, log } = await open(variant("older-snapshot", old));
  check("older snapshot: accepted", !log.warnings.some((w) => w.includes("ignored a snapshot")), log.warnings);
  const missed = [];
  for (const t of old.tickets) {
    await openDetail(page, t.id);
    const opened = await page.evaluate((id) => window.__orchestrateStatus.state().sheet === "detail" && window.__orchestrateStatus.state().sel === id
      && document.querySelector("#sheetBody .missing") !== null, t.id);
    await closeSheet(page);
    await page.mouse.move(2, 880);
    await page.hover(`[data-id="${t.id}"]`);
    const peek = await page.waitForFunction((title) => { const p = document.getElementById("peek"); return p.classList.contains("on") && p.textContent.includes(title); }, t.title, { timeout: 1500 }).then(() => true, () => false);
    if (!opened || !peek) missed.push({ id: t.id, opened, peek });
  }
  check("older snapshot: every detail opens saying it has no summary, and every peek shows the title", !missed.length, missed);
  check("older snapshot: no error", !log.errors.length, log.errors);
  await context.close();
});

// 4. A stuck Ticket at a ready pull request still links its pull request.
await section("stuck at a ready pull request", async () => {
  const snap = structuredClone(sample);
  const t = snap.tickets.find((x) => STUCK.has(x.status));
  t.phase = "ready";
  t.pr = { id: "#299", url: "https://example.com/pull/299" };
  const { page, context } = await open(variant("stuck-with-pr", snap));
  await openDetail(page, t.id);
  check("a stuck Ticket's panel links its pull request", await page.evaluate(() => [...document.querySelectorAll("#sheetBody a")].some((a) => a.textContent.includes("#299"))));
  await context.close();
});

// 5. Long text wraps inside the panel.
await section("long text", async () => {
  const long = structuredClone(sample);
  const t = long.tickets.find((x) => x.id === held?.id) || long.tickets[0];
  const para = "This sentence stands in for a long, real explanation that an orchestrator might write about a Ticket, with names, numbers and a reason or two. ";
  t.summary = para.repeat(3).trim();
  t.why = para.repeat(4).trim();
  t.done = [para.repeat(2).trim(), para.repeat(3).trim()];
  const { page, context, log } = await open(variant("long-text", long));
  await openDetail(page, t.id);
  const f = await panelFacts(page);
  check("long text: no sideways overflow, and nothing thrown", !f.overflowX && !log.errors.length, { overflowX: f.overflowX, errors: log.errors });
  await shoot(page, "detail-long-text", "panel");
  await context.close();
});

// 6. A malformed snapshot after a good one keeps the good view and says so.
await section("malformed snapshot", async () => {
  const { page, context, log } = await open(pathToFileURL(TEMPLATE).href);
  const bad = structuredClone(sample);
  const withChange = bad.tickets.find((x) => x.change) || bad.tickets[0];
  withChange.change = { before: "only half of a change" };
  const r = await page.evaluate((d) => ({ ok: window.__orchestrateStatus.apply(d), cards: document.querySelectorAll("[data-id]").length }), bad);
  await page.waitForTimeout(1100);
  const banner = await page.evaluate(() => document.querySelector(".hud .b:not([hidden])")?.textContent || "");
  check("malformed snapshot: refused, last good view kept, banner and warning shown",
    r.ok === false && r.cards === sample.tickets.length && banner.includes("could not be read") && log.warnings.some((w) => w.includes("ignored a snapshot")), { r, banner });
  await context.close();
});

await browser.close();
writeFileSync(join(OUT, "facts.json"), JSON.stringify(facts, null, 2));
const passed = Object.values(facts).filter((f) => f.ok).length;
console.log(`screenshots and facts: ${OUT}`);
for (const [name, f] of Object.entries(facts)) console.log(`${f.ok ? "ok  " : "FAIL"}  ${name}${f.ok || f.detail === undefined ? "" : "\n      " + JSON.stringify(f.detail)}`);
console.log(`${passed} of ${Object.keys(facts).length} checks held`);
process.exit(failures.length ? 1 : 0);
