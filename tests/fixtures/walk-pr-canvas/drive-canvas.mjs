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

// Finding: Enter or Space on a focused control advanced the story instead of pressing it.
await scenario("keys press a focused control", async (page) => {
  await page.focus("#nerd");
  await page.keyboard.press("Enter");
  check("Enter on the diffs button opens the drawer", await isOpen(page, "drawer"));
  await atStep(page, "Enter on the diffs button keeps the step", "1 / 13");
  await page.keyboard.press("Escape");
  check("Esc closes the drawer", !(await isOpen(page, "drawer")));
  await page.focus("#nerd");
  await page.keyboard.press(" ");
  check("Space on the diffs button opens the drawer", await isOpen(page, "drawer"));
  await atStep(page, "Space on the diffs button keeps the step", "1 / 13");
  await page.focus(".difffile summary");
  await page.keyboard.press("Enter");
  check(
    "Enter on a file row expands it",
    await page.evaluate(() => document.querySelector(".difffile").open),
  );
  await atStep(page, "Enter on a file row keeps the step", "1 / 13");
  await page.keyboard.press("Escape");
  await page.focus("#nerd");
  await page.keyboard.press("ArrowRight");
  await atStep(page, "ArrowRight still advances over a focused button", "2 / 13");
  await jump(page, 3);
  await settle(page);
  check("arriving at a pin step opens its sheet", await isOpen(page, "sheet"));
  await page.focus("#sh-agree");
  await page.keyboard.press("Enter");
  await settle(page);
  const answer = await page.evaluate(() =>
    localStorage.getItem("walkpr-canvas-reference-v1.pin.p3"),
  );
  check("Enter on Agree records the agreement", answer === "Agree — as recommended.", String(answer));
  await atStep(page, "Agree then moves one step on", "5 / 13");
});

// Finding: a pin step did not reopen its sheet after a step without one.
await scenario("pin sheet reopens on return", async (page) => {
  await jump(page, 3);
  await settle(page);
  check("pin sheet opens on first arrival", await isOpen(page, "sheet"));
  await page.keyboard.press("ArrowRight");
  await settle(page);
  check("a pinless step closes the pin sheet", !(await isOpen(page, "sheet")));
  await page.keyboard.press("ArrowLeft");
  await settle(page);
  check("returning to the pin step reopens its sheet", await isOpen(page, "sheet"));
});

// Finding: Esc in the auto-focused textarea left the sheet open; the completion panel had no Esc.
await scenario("Esc closes layers", async (page) => {
  await page.click("#queue");
  await settle(page);
  check(
    "the comment box takes focus",
    await page.evaluate(() => document.activeElement && document.activeElement.id === "sh-ta"),
  );
  await page.keyboard.press("Escape");
  check("Esc in the comment box closes the sheet", !(await isOpen(page, "sheet")));
  await jump(page, 12);
  await settle(page);
  check("the last step opens the completion panel", await isOpen(page, "endpanel"));
  await page.keyboard.press("Escape");
  check("Esc closes the completion panel", !(await isOpen(page, "endpanel")));
  await atStep(page, "closing it returns to the step before", "12 / 13");
});

// Finding: the bundle marked pins the reviewer never saw as captured.
await scenario("bundle marks unseen pins", async (page) => {
  await jump(page, 3);
  await settle(page);
  await jump(page, 12);
  await settle(page);
  const summary = await page.textContent("#summary");
  check("summary marks the opened pin unanswered", summary.includes("p3 — (not answered)"), summary);
  check("summary marks an unopened pin not reached", summary.includes("p1 — (not reached)"), summary);
  await page.click("#copybundle");
  await page.waitForFunction(() => window.__copied !== null);
  const bundle = await page.evaluate(() => window.__copied);
  check("no pin reads as captured", !bundle.includes("captured"), bundle);
  check(
    "the opened pin is listed as not answered",
    /pin p3 [^\n]*\n[^\n]*\n {2}user: \(not answered\)/.test(bundle),
    bundle,
  );
  const [answered, unreached] = bundle.split("## pins not reached (never opened)");
  check(
    "unopened pins are listed apart, with no answer line",
    unreached !== undefined &&
      unreached.includes("pin p1") &&
      unreached.includes("pin p2") &&
      !unreached.includes("user:"),
    bundle,
  );
  check(
    "unopened pins are not among the answered",
    !answered.includes("pin p1") && !answered.includes("pin p2"),
    bundle,
  );
});

await browser.close();
if (failures.length) {
  console.error(failures.map((f) => `FAIL ${f}`).join("\n"));
  process.exit(1);
}
console.log("canvas shell: all checks passed");
