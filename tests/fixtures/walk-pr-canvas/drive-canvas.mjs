// Drives walk-pr's canvas reference shell in headless Chromium and checks the interaction
// rules its header comment promises. Run by tests/test_walk_pr_canvas.py; exits non-zero with
// the failed checks listed. Network is blocked: the CDN diff and highlight scripts fail to load,
// which the shell already tolerates.
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const shell = fileURLToPath(
  new URL(
    "../../../claude-plugins/manifest-dev-tools/skills/walk-pr/assets/canvas-reference.html",
    import.meta.url,
  ),
);
const { chromium } = createRequire(import.meta.url)("playwright");
const failures = [];
const check = (name, ok, detail = "") => {
  if (!ok) failures.push(`${name}${detail ? `: ${detail}` : ""}`);
};

const browser = await chromium.launch({ headless: true });
async function scenario(name, body) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  await context.route(/^https?:/, (route) => route.abort());
  await context.addInitScript(() => {
    window.__copied = null;
    Object.defineProperty(navigator, "clipboard", {
      value: { writeText: (t) => ((window.__copied = t), Promise.resolve()) },
    });
  });
  const page = await context.newPage();
  page.setDefaultTimeout(5000);
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(pathToFileURL(shell).href);
  try {
    await body(page);
  } catch (e) {
    failures.push(`${name}: ${e.message}`);
  }
  check(`${name}: no page errors`, errors.length === 0, errors.join("; "));
  await context.close();
}
const step = (page) => page.textContent("#stepnum");
const isOpen = (page, id) =>
  page.evaluate((i) => document.getElementById(i).classList.contains("open"), id);
const jump = (page, i) =>
  page.evaluate((n) => document.querySelectorAll("#dots .dot")[n].click(), i);
const settle = (page) => page.waitForTimeout(400);
const atStep = async (page, name, want) => {
  const got = await step(page);
  check(name, got === want, `at ${got}, want ${want}`);
};

// The dots of pin steps shared the map pins' `pin` class: hidden by its style, and a click
// went to the map-pin handler with no pin id.
await scenario("pin-step dots", async (page) => {
  const widths = await page.evaluate(() =>
    [...document.querySelectorAll("#dots .dot")].map((d) => d.getBoundingClientRect().width),
  );
  check("every step dot is visible", widths.every((w) => w > 0), widths.join(","));
  await page.click("#dots .dot:nth-child(4)");
  await settle(page);
  await atStep(page, "clicking a pin step's dot goes to that step", "4 / 13");
  check("and opens its sheet", await isOpen(page, "sheet"));
});

await browser.close();
if (failures.length) {
  console.error(failures.map((f) => `FAIL ${f}`).join("\n"));
  process.exit(1);
}
console.log("canvas shell: all checks passed");
