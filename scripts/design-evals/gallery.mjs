function galleryClient(results) {
  const key =
    "design-instruments-review-v2-" + results.provenance.fixtureSHA256;
  let choices = {};
  let revealed = new Set();
  try {
    const saved = JSON.parse(localStorage.getItem(key) || "{}");
    if (saved && typeof saved === "object") {
      if (
        saved.choices &&
        typeof saved.choices === "object" &&
        !Array.isArray(saved.choices)
      )
        choices = saved.choices;
      if (Array.isArray(saved.revealed))
        revealed = new Set(
          saved.revealed.filter((id) =>
            results.families.some((f) => f.id === id),
          ),
        );
    }
  } catch {}
  const storageWarning = () => {
    const e = document.querySelector("#storage-status");
    e.hidden = false;
    document.querySelector("#storage-message").textContent =
      "Browser storage is unavailable. Export your judgments before leaving to keep them.";
  };
  const persist = () => {
    localStorage.setItem(
      key,
      JSON.stringify({ choices, revealed: [...revealed] }),
    );
  };
  const h = (s) =>
    String(s).replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const sides = (id) =>
    id.split("").reduce((s, c) => s + c.charCodeAt(0), 0) % 2
      ? ["after", "before"]
      : ["before", "after"];
  function viewButton(f, view, label) {
    return `<button data-view="${view}" data-case="${h(f.id)}" aria-pressed="${view === "wide"}">${label}</button>`;
  }
  function viewControls(f) {
    const wide =
      f.id === "report" ? "Print · first PDF page" : "Wide · 1024 × 768";
    return `<div class="view-controls"><span>View:</span>
      ${viewButton(f, "wide", wide)}
      ${f.id === "report" ? "" : viewButton(f, "narrow", "Narrow · 390 × 768")}
      ${f.id === "email" ? viewButton(f, "images-off", "Images absent") : ""}
    </div>`;
  }
  function alternative(f, variant, index) {
    const side = ["A", "B"][index];
    return `<figure class="alternative">
      <figcaption>Alternative ${side}</figcaption>
      <button class="image-button" data-zoom="${h(f.id)}" data-variant="${variant}" aria-label="Enlarge alternative ${side} for ${h(f.title)}">
        <img class="preview" data-variant="${variant}" src="${h(f.views[variant + "-wide"])}" alt="Alternative ${side} for ${h(f.title)}">
      </button>
    </figure>`;
  }
  function judgmentControls(f) {
    const buttons = ["A", "B", "Tie", "Both need work", "Insufficient evidence"]
      .map(
        (label) =>
          `<button data-choice="${label}" data-case="${h(f.id)}" aria-pressed="${choices[f.id]?.choice === label}">${label}</button>`,
      )
      .join("");
    return `<div class="choices"><span class="choices-label">Which better serves this brief?</span>${buttons}</div>`;
  }
  function evidence(f, pair) {
    const measurements = JSON.stringify(
      {
        observations: f.observations,
        traces: f.traces,
        printEvidence: f.printEvidence,
      },
      null,
      2,
    );
    const unfavorable = results.attacks
      .filter((a) => a.family === f.id)
      .map((a) => a.correction || a.evidence)
      .join(" ");
    const pdfLinks =
      f.id === "report"
        ? '<a href="report/before-print/artifact.pdf">Original PDF</a><a href="report/after-print/artifact.pdf">Alternative PDF</a>'
        : "";
    return `<button class="reveal" data-reveal="${h(f.id)}" aria-expanded="false" aria-controls="evidence-${h(f.id)}">Reveal identities and evidence</button>
      <div class="evidence" id="evidence-${h(f.id)}" hidden>
        <p class="result-note">A = ${pair[0]}; B = ${pair[1]}. Owner preference is pending.</p>
        <p>${h(f.selection)}</p>
        <div class="links">
          <a href="${h(f.id)}/before.html" target="_blank" rel="noopener">Open original interactive artifact</a>
          <a href="${h(f.id)}/after.html" target="_blank" rel="noopener">Open alternative interactive artifact</a>
          ${pdfLinks}
        </div>
        <details><summary>Measurements and scenario traces</summary><pre>${h(measurements)}</pre></details>
        <p style="margin:16px 0 0">${h(unfavorable)}</p>
      </div>`;
  }
  function caseHTML(f, index) {
    const pair = sides(f.id);
    return `<section class="case" id="case-${h(f.id)}" data-split="${h(f.split)}">
      <div class="case-meta">
        <p class="eyebrow">Comparison ${String(index + 1).padStart(2, "0")} / ${h(f.id)}</p>
        <h2>${h(f.title)}</h2><p class="case-brief">${h(f.brief)}</p>
      </div>
      ${viewControls(f)}
      <div class="comparison">${pair.map((variant, i) => alternative(f, variant, i)).join("")}</div>
      ${judgmentControls(f)}
      ${evidence(f, pair)}
    </section>`;
  }
  document.querySelector("#cases").innerHTML = results.families
    .map(caseHTML)
    .join("");
  document.querySelector("#calibration").innerHTML =
    '<pre style="white-space:pre-wrap;overflow-wrap:anywhere">' +
    h(
      JSON.stringify(
        {
          development: results.calibration,
          independentTransfer: results.transfer,
        },
        null,
        2,
      ),
    ) +
    "</pre>";
  function refresh(filter = true) {
    const value = document.querySelector("#family-filter").value;
    if (filter)
      for (const f of results.families)
        document.querySelector("#case-" + f.id).hidden = !(
          value === "all" ||
          value === f.split ||
          (value === "unjudged" && !choices[f.id])
        );
    document.querySelector("#progress").textContent =
      Object.keys(choices).filter((id) =>
        results.families.some((f) => f.id === id),
      ).length +
      " of " +
      results.families.length +
      " judged";
  }
  document.querySelector("#family-filter").onchange = () => refresh(true);
  document.addEventListener("click", (event) => {
    const b = event.target.closest("button");
    if (!b) return;
    if (b.dataset.choice) {
      const id = b.dataset.case;
      choices[id] = {
        choice: b.dataset.choice,
        revealedBeforeChoice: revealed.has(id),
        time: new Date().toISOString(),
        sideMapping: sides(id),
        view: document.querySelector(
          "#case-" + id + " [data-view][aria-pressed=true]",
        ).dataset.view,
      };
      try {
        persist();
      } catch {
        storageWarning();
      }
      for (const button of document.querySelectorAll(
        "#case-" + id + " [data-choice]",
      ))
        button.setAttribute("aria-pressed", button === b);
      refresh(false);
    }
    if (b.dataset.reveal) {
      const id = b.dataset.reveal;
      revealed.add(id);
      try {
        persist();
      } catch {
        storageWarning();
      }
      document.querySelector("#evidence-" + id).hidden = false;
      b.setAttribute("aria-expanded", "true");
      b.textContent = "Identities and evidence revealed";
    }
    if (b.dataset.view) {
      const id = b.dataset.case,
        view = b.dataset.view,
        f = results.families.find((f) => f.id === id);
      for (const img of document.querySelectorAll("#case-" + id + " .preview"))
        img.src = f.views[img.dataset.variant + "-" + view];
      for (const button of document.querySelectorAll(
        "#case-" + id + " [data-view]",
      ))
        button.setAttribute("aria-pressed", button === b);
    }
    if (b.dataset.zoom) {
      const img = b.querySelector("img");
      document.querySelector("#zoom-image").src = img.src;
      document.querySelector("#zoom-image").alt = img.alt;
      document.querySelector("#zoom-title").textContent = img.alt;
      document.querySelector("#zoom-image").style.maxWidth = "none";
      document.querySelector("#fit-zoom").setAttribute("aria-pressed", "false");
      document.querySelector("#zoom").showModal();
    }
  });
  document.querySelector("#storage-export").onclick = () =>
    document.querySelector("#export").click();
  document.querySelector("#fit-zoom").onclick = () => {
    const b = document.querySelector("#fit-zoom"),
      fit = b.getAttribute("aria-pressed") !== "true";
    b.setAttribute("aria-pressed", fit);
    document.querySelector("#zoom-image").style.maxWidth = fit
      ? "100%"
      : "none";
  };
  document.querySelector("#close-zoom").onclick = () =>
    document.querySelector("#zoom").close();
  document.querySelector("#export").onclick = () => {
    const blob = new Blob(
      [
        JSON.stringify(
          {
            schemaVersion: 1,
            evidence: "Explicit local reviewer choices; not a population study",
            fixtureProvenance: results.provenance,
            choices,
          },
          null,
          2,
        ),
      ],
      { type: "application/json" },
    );
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "design-review-judgments.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };
  refresh();
}
export function gallery(results) {
  const payload = JSON.stringify(results).replace(/</g, "\\u003c");
  return `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Design instruments · comparison room</title><style>
 :root{color-scheme:light;--ink:#182b3a;--muted:#486171;--line:#ccd8df;--accent:#145969;--paper:#f5f7f8}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,sans-serif}header,main,footer{max-width:1440px;margin:auto;padding:36px 48px}header{border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);font-weight:650;margin:0 0 14px}h1{font-size:clamp(34px,4vw,56px);letter-spacing:-.045em;line-height:1.05;margin:0 0 18px;max-width:820px}h2{font-size:28px;letter-spacing:-.025em;margin:0 0 12px}h3{font-size:18px;margin:0 0 12px}p{margin:0 0 16px}.intro{max-width:820px;color:var(--muted);font-size:18px}.toolbar,.view-controls,.choices{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.toolbar{margin-top:24px}button,select{font:inherit;border:1px solid var(--line);background:white;border-radius:7px;padding:9px 14px;color:var(--ink);cursor:pointer;min-height:44px}button:hover{border-color:var(--accent)}button[aria-pressed=true],.primary{background:var(--accent);color:white;border-color:var(--accent)}button:focus-visible,a:focus-visible,select:focus-visible{outline:3px solid #bc550c;outline-offset:3px}a{color:var(--accent)}#storage-status{position:fixed;bottom:12px;right:12px;left:12px;z-index:30;margin:0;padding:14px 18px;background:#fff4e5;color:#813c10;border:2px solid #b15b0a;border-radius:9px;box-shadow:0 4px 24px #182b3a33;font-weight:600}#storage-status button{margin-top:8px;display:block}#progress{font-size:14px;color:var(--muted);margin-inline-start:auto}.case{padding:30px 0 44px;border-bottom:1px solid var(--line)}.case-meta{max-width:840px}.case-brief{color:var(--muted)}.view-controls{margin:20px 0}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:18px}.alternative{margin:0;background:white;border:1px solid var(--line);border-radius:10px;overflow:hidden}.alternative figcaption{padding:12px 18px;border-bottom:1px solid var(--line);font-weight:650}.preview{display:block;width:100%;height:auto;cursor:zoom-in}.image-button{display:block;padding:0;border:0;border-radius:0;width:100%;background:white}.choices{margin:20px 0 14px}.choices-label{width:100%;font-weight:600}.reveal{background:transparent}.evidence{margin-top:20px;padding:24px;background:#e9eff2;border-radius:9px}.evidence[hidden]{display:none}.evidence pre{font:12px/1.55 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;max-height:360px;overflow:auto;background:#fff;padding:16px;border:1px solid var(--line)}.result-note{font-weight:600}.links{display:flex;gap:18px;flex-wrap:wrap}.summary{margin:32px 0;padding:24px;border:1px solid var(--line);background:white;border-radius:10px}.summary details{margin-top:16px}.summary li{margin-bottom:8px}footer{color:var(--muted);font-size:14px}dialog{border:1px solid var(--line);border-radius:10px;padding:0;width:min(96vw,1500px);max-width:1500px;height:94vh;background:var(--paper);color:var(--ink)}dialog::backdrop{background:#0d2333c4}.dialogbar{position:sticky;top:0;display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:white;border-bottom:1px solid var(--line);z-index:1}#zoom-image{display:block;max-width:none;width:auto;margin:auto}.zoom-canvas{overflow:auto;height:calc(94vh - 74px)} @media(max-width:740px){header,main,footer{padding:24px}h2{font-size:24px}.comparison{grid-template-columns:1fr}.evidence{padding:16px}#progress{width:100%;margin:4px 0 0}.case{padding-top:24px}.toolbar button{flex:1}}@media(prefers-reduced-motion:no-preference){button{transition:background .12s,border-color .12s}}
 </style><body><header><p class="eyebrow">Design instruments / constructed comparison room</p><h1>Judge the design.<br>Then inspect the measurements.</h1><p class="intro">${results.families.length} fictional briefs, with matched alternatives. Some revisions help; some pursue a better number and lose essential meaning. The identities and measurements stay hidden until you choose to reveal them.</p><p class="intro">These are constructed examples, not measured human UX improvements. Your choices are saved in this browser only. No choices have been pre-filled.</p><div class="toolbar"><label for="family-filter">Show</label><select id="family-filter"><option value="all">All ${results.families.length} comparisons</option><option value="train">Development families</option><option value="heldout">Transfer families</option><option value="unjudged">Not yet judged</option></select><button id="export" class="primary">Export my judgments</button><span id="progress" aria-live="polite"></span></div><div id="storage-status" role="status" hidden><span id="storage-message"></span><button id="storage-export">Export judgments now</button></div></header><main><div id="cases"></div><section class="summary"><h2>What the experiments establish</h2><p>Observations became more accurate for clipping, relationships, fine image patterns and zero text exposure. A grouping threshold fitted to a few layouts is still withheld as general advice. We did not fit a universal design-quality score.</p><details><summary>Inspect the calibration and unfavorable cases</summary><div id="calibration"></div><p><a href="summary.json">Experiment summary (JSON)</a> · <a href="results.json">Full observations (JSON)</a></p></details></section></main><footer>Inputs are fictional and self-contained. All gallery families were available during development. A separate six-case transfer check was specified independently after instrument freeze. Neither is an audience study. Actual email clients, assistive announcements, touch hardware and native slide/document hosts remain outside this adapter's evidence.</footer><dialog id="zoom"><div class="dialogbar"><strong id="zoom-title"></strong><div><button id="fit-zoom" aria-pressed="false">Fit to view</button> <button id="close-zoom">Close</button></div></div><div class="zoom-canvas" tabindex="0" role="region" aria-label="Image at original scale; scroll to inspect"><img id="zoom-image" alt=""></div></dialog><script>
 (${galleryClient.toString()})(${payload});
 </script></body></html>`;
}
