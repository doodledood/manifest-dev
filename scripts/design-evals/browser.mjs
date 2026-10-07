import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

export async function browserEngine() {
  const candidates = process.env.DESIGN_TOOLS_PLAYWRIGHT
    ? [process.env.DESIGN_TOOLS_PLAYWRIGHT]
    : ["playwright", "playwright-core"];
  const roots = [
    import.meta.url,
    pathToFileURL(resolve(process.cwd(), "package.json")).href,
  ];
  for (const candidate of candidates)
    for (const root of roots) {
      try {
        const req = createRequire(root);
        const mod = await import(pathToFileURL(req.resolve(candidate)).href);
        return mod.chromium || mod.default.chromium;
      } catch {
        /* Try the next documented module location. */
      }
    }
  throw new Error(
    "Playwright unavailable. Install playwright and its Chromium browser in your project, or set DESIGN_TOOLS_PLAYWRIGHT to its module directory.",
  );
}
export async function openArtifact(file, options, callback) {
  const chromium = await browserEngine();
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.DESIGN_TOOLS_CHROMIUM
      ? { executablePath: process.env.DESIGN_TOOLS_CHROMIUM }
      : {}),
  });
  try {
    const page = await browser.newPage({
      viewport: { width: options.width, height: options.height },
      deviceScaleFactor: 1,
      colorScheme: options.theme,
      reducedMotion: options.motion,
      serviceWorkers: "block",
    });
    if (typeof page.routeWebSocket !== "function")
      throw new Error(
        "Playwright 1.48 or newer is required: WebSocket interception is unavailable. Upgrade playwright before inspecting an artifact.",
      );
    const blocked = [],
      errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.route("**/*", async (route) => {
      const u = new URL(route.request().url());
      const local =
        ["file:", "data:", "blob:", "about:"].includes(u.protocol) ||
        ["localhost", "127.0.0.1", "[::1]"].includes(u.hostname);
      if (local || options.allowNetwork) await route.continue();
      else {
        blocked.push(u.origin);
        await route.abort();
      }
    });
    await page.routeWebSocket("**/*", (socket) => {
      const u = new URL(socket.url());
      if (
        options.allowNetwork ||
        ["localhost", "127.0.0.1", "[::1]"].includes(u.hostname)
      )
        socket.connectToServer();
      else {
        blocked.push(u.origin);
        socket.close();
      }
    });
    await page.goto(file, { waitUntil: "load", timeout: 30000 });
    await page.evaluate(async () => {
      await document.fonts.ready;
    });
    if (options.direction)
      await page.evaluate(
        (d) => (document.documentElement.dir = d),
        options.direction,
      );
    if (options.imagesOff)
      await page.addStyleTag({
        content:
          "img,picture,video,canvas,svg{visibility:hidden!important} *{background-image:none!important}",
      });
    if (options.textScale !== 1)
      await page.evaluate((scale) => {
        const nodes = [...document.querySelectorAll("*")];
        const sizes = nodes.map((e) =>
          parseFloat(getComputedStyle(e).fontSize),
        );
        nodes.forEach((e, i) =>
          e.style.setProperty(
            "font-size",
            `${sizes[i] * scale}px`,
            "important",
          ),
        );
      }, options.textScale);
    if (options.vision) {
      const cdp = await page.context().newCDPSession(page);
      await cdp.send("Emulation.setEmulatedVisionDeficiency", {
        type: options.vision,
      });
    }
    const environment = {
      browserVersion: browser.version(),
      blockedOrigins: [...new Set(blocked)],
      pageErrors: errors,
    };
    const result = await callback(page, environment);
    // Scenarios can trigger resource requests after the initial page load.
    environment.blockedOrigins = [...new Set(blocked)];
    return result;
  } finally {
    await browser.close();
  }
}

// Runs in the page. Semantic ownership comes from the explicit measurement plan.
export async function snapshot(page, spec = {}) {
  return page.evaluate((spec) => {
    const box = (e) => {
      const r = e.getBoundingClientRect();
      return { x: r.x, y: r.y, width: r.width, height: r.height };
    };
    const visible = (e) => {
      const r = e.getBoundingClientRect();
      if (!r.width || !r.height) return false;
      for (let a = e; a; a = a.parentElement) {
        const s = getComputedStyle(a);
        if (
          s.visibility === "hidden" ||
          s.display === "none" ||
          Number(s.opacity) === 0
        )
          return false;
      }
      return true;
    };
    const ids = new WeakMap(),
      entities = Object.create(null);
    let ordinal = 0;
    const getId = (e) => {
      if (!ids.has(e)) {
        let id;
        do {
          id = `auto:${++ordinal}`;
        } while (Object.hasOwn(spec.entities || {}, id));
        ids.set(e, id);
      }
      return ids.get(e);
    };
    const clipBox = (e) => {
      const r = box(e);
      let x = r.x,
        y = r.y,
        right = r.x + r.width,
        bottom = r.y + r.height;
      for (let a = e.parentElement; a; a = a.parentElement) {
        const s = getComputedStyle(a),
          b = box(a);
        const left = b.x + a.clientLeft,
          top = b.y + a.clientTop;
        if (["hidden", "clip", "scroll", "auto"].includes(s.overflowX)) {
          x = Math.max(x, left);
          right = Math.min(right, left + a.clientWidth);
        }
        if (["hidden", "clip", "scroll", "auto"].includes(s.overflowY)) {
          y = Math.max(y, top);
          bottom = Math.min(bottom, top + a.clientHeight);
        }
      }
      return {
        x,
        y,
        width: Math.max(0, right - x),
        height: Math.max(0, bottom - y),
      };
    };
    const record = (e) => {
      const s = getComputedStyle(e),
        clipped = clipBox(e);
      return {
        box: box(e),
        visibleBox: clipped,
        visible: visible(e) && clipped.width > 0 && clipped.height > 0,
        contentClipCandidate:
          (e.scrollWidth > e.clientWidth + 1 &&
            ["hidden", "clip"].includes(s.overflowX)) ||
          (e.scrollHeight > e.clientHeight + 1 &&
            ["hidden", "clip"].includes(s.overflowY)),
        tag: e.tagName.toLowerCase(),
        text: (e.innerText || e.textContent || "").trim(),
        fontSize: parseFloat(s.fontSize),
        scrollWidth: e.scrollWidth,
        clientWidth: e.clientWidth,
        scrollHeight: e.scrollHeight,
        clientHeight: e.clientHeight,
        overflowX: s.overflowX,
        overflowY: s.overflowY,
        direction: s.direction,
        position: s.position,
        font: s.font,
        fontFamily: s.fontFamily,
        lineHeight: s.lineHeight,
        weight: s.fontWeight,
        color: s.color,
        nameCandidate:
          e.getAttribute("aria-label") ||
          e.getAttribute("alt") ||
          e.labels?.[0]?.textContent ||
          e.textContent?.trim() ||
          "",
        namingSource: e.hasAttribute("aria-label")
          ? "aria-label"
          : e.hasAttribute("alt")
            ? "alt"
            : e.labels?.length
              ? "label"
              : "text",
        formAttributes: Object.fromEntries(
          [
            "type",
            "inputmode",
            "autocomplete",
            "required",
            "min",
            "max",
            "minlength",
            "maxlength",
            "pattern",
            "multiple",
            "readonly",
          ].map((k) => [k, e.getAttribute(k)]),
        ),
        placeholder: e.getAttribute("placeholder"),
        role: e.getAttribute("role"),
        tabIndex: e.tabIndex,
      };
    };
    for (const [id, selector] of Object.entries(spec.entities || {})) {
      let matches;
      try {
        matches = document.querySelectorAll(selector);
      } catch {
        throw new Error(`Invalid selector for ${id}: ${selector}`);
      }
      if (matches.length !== 1)
        throw new Error(
          `Entity ${id} must match exactly one element; matched ${matches.length}: ${selector}`,
        );
      ids.set(matches[0], id);
      entities[id] = { ...record(matches[0]), selector };
    }
    const candidates = [
      ...document.querySelectorAll(
        "h1,h2,h3,h4,h5,h6,p,li,dt,dd,th,td,label,button,a[href],input,select,textarea,img,figure,figcaption,svg,canvas,video,[role]",
      ),
    ];
    for (const e of candidates) {
      const id = getId(e);
      entities[id] = entities[id] || record(e);
    }
    const nodes = [];
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
    );
    let n;
    while ((n = walker.nextNode())) {
      if (!n.textContent.trim()) continue;
      const e = n.parentElement;
      if (!e || e.closest("script,style,noscript")) continue;
      const s = getComputedStyle(e),
        range = document.createRange();
      range.selectNodeContents(n);
      const rects = [...range.getClientRects()];
      const lineYs = new Set(
        rects
          .filter((r) => r.width && r.height)
          .map((r) => Math.round(r.y * 10) / 10),
      );
      const backgrounds = [],
        paintEffects = [];
      if (e.namespaceURI !== "http://www.w3.org/1999/xhtml")
        paintEffects.push("non-HTML paint");
      for (let a = e; a; a = a.parentElement) {
        const c = getComputedStyle(a);
        backgrounds.push(c.backgroundColor);
        if (c.backgroundImage !== "none") paintEffects.push("background image");
        if (Number(c.opacity) !== 1) paintEffects.push("opacity");
        if (
          c.filter !== "none" ||
          (c.backdropFilter && c.backdropFilter !== "none")
        )
          paintEffects.push("filter");
        if (c.mixBlendMode !== "normal") paintEffects.push("blend");
        if (c.textShadow !== "none") paintEffects.push("text shadow");
        if (c.maskImage && c.maskImage !== "none") paintEffects.push("mask");
      }
      if (s.webkitTextFillColor && s.webkitTextFillColor !== s.color)
        paintEffects.push("text fill");
      if (parseFloat(s.webkitTextStrokeWidth) > 0)
        paintEffects.push("text stroke");
      if (!visible(e)) paintEffects.push("hidden");
      for (let a = e; a; a = a.parentElement)
        for (const pseudo of ["::before", "::after"]) {
          const q = getComputedStyle(a, pseudo);
          if (
            q.content !== "none" &&
            q.content !== "normal" &&
            q.display !== "none" &&
            (q.backgroundImage !== "none" ||
              q.backgroundColor !== "rgba(0, 0, 0, 0)" ||
              q.content !== '""')
          )
            paintEffects.push("generated paint");
        }
      const paintRect = range.getBoundingClientRect(),
        px = paintRect.x + paintRect.width / 2,
        py = paintRect.y + paintRect.height / 2,
        top = document.elementFromPoint(px, py);
      if (
        document.elementsFromPoint(px, py).some((p) => {
          if (p === e || e.contains(p) || p.contains(e)) return false;
          const q = getComputedStyle(p);
          return (
            q.backgroundColor !== "rgba(0, 0, 0, 0)" ||
            q.backgroundImage !== "none"
          );
        })
      )
        paintEffects.push("nonancestor background candidate");
      if (top && top !== e && !e.contains(top))
        paintEffects.push("possible paint occlusion");
      const r = range.getBoundingClientRect();
      nodes.push({
        id: getId(e),
        text: n.textContent.trim(),
        box: { x: r.x, y: r.y, width: r.width, height: r.height },
        lines: lineYs.size,
        visible: visible(e),
        fontSize: parseFloat(s.fontSize),
        lineHeight: s.lineHeight,
        font: s.fontFamily,
        weight: s.fontWeight,
        color: s.color,
        backgrounds,
        paintEffects: [...new Set(paintEffects)],
      });
    }
    const controls = [
      ...document.querySelectorAll(
        "button,a[href],input:not([type=hidden]),textarea,select,summary,[role=button],[role=tab],[role=checkbox],[role=switch]",
      ),
    ].map((e) => {
      const r = box(e);
      const points = [
        [0.5, 0.5],
        [0.1, 0.1],
        [0.9, 0.1],
        [0.1, 0.9],
        [0.9, 0.9],
      ].map(([x, y]) => {
        const px = r.x + x * r.width,
          py = r.y + y * r.height;
        const top = document.elementFromPoint(px, py);
        return {
          x: px,
          y: py,
          receivesPointer:
            visible(e) && !!top && (top === e || e.contains(top)),
          top: top ? getId(top) : null,
        };
      });
      return {
        id: getId(e),
        ...record(e),
        disabled: !!e.disabled,
        points,
        associatedLabels: [...(e.labels || [])].map((x) =>
          x.textContent.trim(),
        ),
      };
    });
    const animations = document.getAnimations().map((a) => ({
      target: a.effect?.target ? getId(a.effect.target) : null,
      playState: a.playState,
      timing: a.effect
        ? Object.fromEntries(
            Object.entries(a.effect.getComputedTiming()).map(([k, v]) => [
              k,
              typeof v === "number" && !Number.isFinite(v) ? String(v) : v,
            ]),
          )
        : null,
    }));
    const doc = document.scrollingElement || document.documentElement;
    return {
      entities,
      nodes,
      controls,
      animations,
      viewport: { x: 0, y: 0, width: innerWidth, height: innerHeight },
      documentSize: { width: doc.scrollWidth, height: doc.scrollHeight },
      headings: [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].map(
        (e) => ({
          id: getId(e),
          level: Number(e.tagName[1]),
          text: e.textContent.trim(),
          visible: visible(e),
        }),
      ),
      media: [...document.querySelectorAll("img,svg,canvas,video")].map(
        (e) => ({
          id: getId(e),
          ...record(e),
          naturalWidth: e.naturalWidth || null,
          naturalHeight: e.naturalHeight || null,
          alt: e.getAttribute("alt"),
        }),
      ),
      coverage: {
        textNodes: nodes.length,
        semanticCandidates: candidates.length,
        controls: controls.length,
        iframes: document.querySelectorAll("iframe").length,
        openShadowRoots: [...document.querySelectorAll("*")].filter(
          (e) => e.shadowRoot,
        ).length,
      },
      languages: [...document.querySelectorAll("[lang],[dir]")].map((e) => ({
        tag: e.tagName.toLowerCase(),
        lang: e.lang,
        dir: e.dir,
      })),
    };
  }, spec);
}

export async function probe(page, spec) {
  if (!Array.isArray(spec.steps) || !spec.steps.length)
    throw new Error("probe plan needs a nonempty steps array");
  const records = [];
  for (const [index, step] of spec.steps.entries()) {
    if (!step || typeof step !== "object")
      throw new Error(`Step ${index} must be an object`);
    if (
      ["click", "fill", "focus", "hover"].includes(step.action) &&
      typeof step.selector !== "string"
    )
      throw new Error(`${step.action} needs a selector`);
    if (
      step.observe &&
      (!Array.isArray(step.observe) ||
        step.observe.some((s) => typeof s !== "string"))
    )
      throw new Error("observe must be a selector array");
    const start = performance.now();
    const target = step.selector ? page.locator(step.selector) : null;
    if (target && (await target.count()) !== 1)
      throw new Error(
        `Step ${index}: selector must match exactly one element: ${step.selector}`,
      );
    if (step.action === "click") await target.click();
    else if (step.action === "fill") {
      if (typeof step.value !== "string")
        throw new Error("fill needs a string value");
      await target.fill(step.value);
    } else if (step.action === "press") {
      if (typeof step.key !== "string") throw new Error("press needs a key");
      if (target) await target.press(step.key);
      else await page.keyboard.press(step.key);
    } else if (step.action === "focus") await target.focus();
    else if (step.action === "hover") await target.hover();
    else if (step.action === "scroll") {
      if (!Number.isFinite(step.x || 0) || !Number.isFinite(step.y))
        throw new Error("scroll needs numeric x/y");
      await page.evaluate((s) => scrollTo(s.x || 0, s.y), step);
    } else if (step.action === "wait") {
      if (!Number.isFinite(step.ms) || step.ms < 0 || step.ms > 30000)
        throw new Error("wait ms must be 0–30000");
      await page.waitForTimeout(step.ms);
    } else if (step.action !== "observe")
      throw new Error(`Unknown probe action: ${step.action}`);
    const elapsedMs = performance.now() - start;
    const captured = await page.evaluate((selectors) => {
      const values = {};
      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length !== 1)
          throw new Error(`Observation selector needs one match: ${selector}`);
        const e = elements[0],
          r = e.getBoundingClientRect();
        let visible = r.width > 0 && r.height > 0;
        for (let a = e; a; a = a.parentElement) {
          const s = getComputedStyle(a);
          if (
            s.visibility === "hidden" ||
            s.display === "none" ||
            Number(s.opacity) === 0
          )
            visible = false;
        }
        values[selector] = {
          text: e.textContent?.trim() || "",
          value: "value" in e ? e.value : null,
          visible,
          checked: "checked" in e ? e.checked : null,
        };
      }
      const f = document.activeElement;
      return {
        values,
        activeElement: {
          id: f?.id || null,
          tag: f?.tagName.toLowerCase() || null,
          box: f
            ? {
                x: f.getBoundingClientRect().x,
                y: f.getBoundingClientRect().y,
                width: f.getBoundingClientRect().width,
                height: f.getBoundingClientRect().height,
              }
            : null,
          text: f?.textContent?.trim() || "",
        },
        animationCount: document.getAnimations().length,
      };
    }, step.observe || []);
    if ((step.observe || []).length) {
      const selectors = Object.fromEntries(
        step.observe.map((selector, i) => [`observed:${i}`, selector]),
      );
      const observed = await snapshot(page, { entities: selectors });
      step.observe.forEach((selector, i) => {
        captured.values[selector].visible =
          observed.entities[`observed:${i}`].visible;
        captured.values[selector].visibleBox =
          observed.entities[`observed:${i}`].visibleBox;
      });
    }
    const record = { index, action: step.action, elapsedMs, ...captured };
    if (step.capture)
      record.screenshotBase64 = (await page.screenshot()).toString("base64");
    records.push(record);
  }
  return {
    records,
    limits:
      "Action elapsed times include automation overhead and waiting; they are noisy observations, not input-to-photon latency. Supplied scenarios do not establish production reliability or human understanding.",
  };
}
