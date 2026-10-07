// Fictional briefs and requirements are fixed before measuring candidates.
export const width = 1024,
  height = 768;
export function document(body, css = "", script = "", language = "en") {
  return `<!doctype html><html lang="${language}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Design instrument specimen</title><style>
  *{box-sizing:border-box}body{margin:0;background:#f4f6f8;color:#182b3a;font:16px/1.5 system-ui,sans-serif}main{max-width:960px;margin:auto;padding:40px}h1,h2,p{margin:0 0 20px}h1{font-size:44px;line-height:1.08;letter-spacing:-.035em}h2{font-size:22px;line-height:1.2}small,.eyebrow{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#425a6b}.eyebrow{margin-bottom:14px}button,input{font:inherit}button{cursor:pointer;border:0;background:#153e52;color:white;padding:12px 20px;border-radius:8px}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #bc550c;outline-offset:4px}a{color:#175c7a}input{max-width:100%;border:1px solid #708595;border-radius:6px;padding:12px;background:#fff;color:#182b3a}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}td,th{padding:14px 12px;text-align:left;border-bottom:1px solid #d3dce3}th{font-size:13px}section{margin-bottom:28px}.panel{background:#fff;padding:28px;border:1px solid #d7e0e6;border-radius:12px}.row{display:flex;gap:20px;align-items:center}.value{font-size:36px;font-weight:650;font-variant-numeric:tabular-nums}.muted{color:#526b7a}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.note{border-inline-start:3px solid #ce6924;padding-inline-start:16px}.bar{height:22px;background:#216478}.status{padding:16px;background:#e5eef3;border-radius:8px;min-height:56px}label{display:block;margin:0 0 8px} @media(max-width:600px){main{padding:24px}h1{font-size:34px}.grid{grid-template-columns:1fr}.row{flex-wrap:wrap}td,th{padding:12px 6px}}
  ${css}</style><body>${body}<script>${script}</script></body></html>`;
}
const names = ["Station North", "Station East", "Station West"];
const table = `<table><caption style="text-align:left;padding:0 0 12px;font-weight:600">Current station readings</caption><thead><tr><th>Station</th><th>Flow, L/s</th><th>Pressure, bar</th></tr></thead><tbody>${names.map((n, i) => `<tr><td>${n}</td><td>${[42, 38, 51][i]}</td><td>${[2.1, 1.8, 2.4][i]}</td></tr>`).join("")}</tbody></table>`;
const dashboard = (gap) =>
  document(
    `<main><p class="eyebrow">Watershed / operations</p><h1>Today's network</h1><p class="muted">Compare the exception with the current station readings.</p><section class="panel" id="readings">${table}</section><section class="note" id="exception" style="margin-top:${gap}px"><h2>East pressure below expected range</h2><p>1.8 bar · target 2.0–2.6 bar · reported at 09:42</p><button id="inspect">Inspect Station East</button></section></main>`,
  );
const form = (retain, big) =>
  document(
    `<main style="max-width:620px"><p class="eyebrow">Field notes / draft</p><h1>Save an observation</h1><p class="muted">A simulated connection failure lets you check the recovery state.</p><section class="panel"><label for="note">Observation</label><input id="note" autocomplete="off" value="Gate valve replaced" style="width:100%"><p style="margin-top:18px" id="status" role="status">Draft is ready.</p><button id="save" style="min-height:${big ? 48 : 26}px;padding:${big ? "12px 20px" : "2px 8px"}">Save draft</button></section></main>`,
    "",
    `document.querySelector('#save').onclick=()=>{${retain ? "" : 'document.querySelector("#note").value="";'}document.querySelector('#status').textContent='Connection unavailable. Your draft ${retain ? "is still here; try again." : "could not be saved."}';};`,
  );
const chart = (uniform) =>
  document(
    `<main><p class="eyebrow">Trail survey / 120 fictional responses</p><h1>Shorter trails draw more visits</h1><p class="muted">Visits per week, same scale in every row.</p><section class="panel">${["Ridge path", "Waterfall loop (seasonal access)", "Pine trail"].map((name, i) => `<div class="chartrow"><span>${name}</span><div class="track" id="track${i}"><div class="bar" id="bar${i}" style="width:${[60, 30, 45][i]}%"></div></div><strong>${[60, 30, 45][i]}</strong></div>`).join("")}<p id="source" class="muted" style="margin:24px 0 0">Source: fictional fixture. Weekly counts, not unique visitors.</p></section></main>`,
    `.chartrow{display:grid;grid-template-columns:${uniform ? "240px 1fr 48px" : "max-content 1fr 48px"};gap:20px;align-items:center;margin:20px 0}.track{background:#ebeff2}@media(max-width:600px){.chartrow{grid-template-columns:${uniform ? "1fr" : "max-content 1fr 40px"};gap:8px}.track{min-width:100px}}`,
  );
const article = (faithful) =>
  document(
    `<main style="max-width:720px"><p class="eyebrow">Research memo / synthetic example</p><h1>A promising signal, with a narrow scope</h1><p style="font-size:24px;line-height:1.45">The new queue reduced waiting time in the trial.</p><section class="panel"><h2>What changed</h2><p>Median wait fell from 14 to 11 minutes across 24 recorded sessions.</p>${faithful ? '<p id="qualification" class="note">This was a single-site pilot with no randomized comparison. The change may reflect staffing or arrival patterns.</p>' : ""}<h2>Next decision</h2><p>Repeat the trial at a second site before adopting the queue broadly.</p></section></main>`,
  );
const explainer = (near) =>
  document(
    `<main><p class="eyebrow">Mechanism / first encounter</p><h1>One flow, two routes</h1><p>Read the branch label beside the route it names.</p><section class="panel" style="position:relative;height:360px"><div id="route" style="position:absolute;left:34px;top:180px;width:78%;height:60px;background:#dbe9ed;border-inline-start:6px solid #216478;padding:18px">Return channel → basin</div><span id="label" style="position:absolute;left:34px;top:${near ? 146 : 34}px;font-weight:650">Return channel</span><span id="competitor" style="position:absolute;right:34px;top:34px">Intake filter</span></section></main>`,
  );
const game = (block) =>
  document(
    `<main style="max-width:640px"><p class="eyebrow">Small toy / repeated action</p><h1>Find the rhythm</h1><p>Tap the pad. The counter should answer every tap.</p><section class="panel"><button id="pad" style="width:140px;height:140px;border-radius:50%;font-size:24px">Tap</button><p style="margin-top:24px">Count <strong id="count">0</strong></p><p id="feedback" role="status">Ready.</p></section></main>`,
    `#pad{transition:transform .12s}#pad:active{transform:scale(.96)}@media(prefers-reduced-motion:reduce){#pad{transition:none}}`,
    `let n=0;document.querySelector('#pad').onclick=()=>{${block ? "if(n>0)return;" : ""}document.querySelector('#count').textContent=++n;document.querySelector('#feedback').textContent='Tap registered.';};`,
  );
const deck = (together) =>
  document(
    `<main style="background:#142c3b;color:#eff5f6;min-height:768px"><p class="eyebrow" style="color:#b5ccd6">Briefing / reading deck / slide 02</p><h1 style="max-width:760px;font-size:52px">The backup route buys twelve minutes.</h1><p style="font-size:22px;max-width:600px">A second path keeps the system running while the main channel is isolated.</p><div id="claim" class="row" style="margin-top:32px"><div style="font-size:100px;line-height:1;color:#83d7d5">12</div><p>minutes of operating reserve<br><small style="color:#b5ccd6">Under the declared flow rate</small></p></div><div id="assumption" style="margin-top:${together ? 36 : 480}px;border-top:1px solid #66818f;padding-top:18px">Assumption: 2,400 L reserve at 200 L/min. This is a synthetic example, not a field guarantee.</div></main>`,
    `@media(max-width:600px){main h1{font-size:34px!important}#claim div{font-size:72px!important}}`,
  );
const poster = (expressive) =>
  document(
    `<main style="min-height:768px;background:${expressive ? "#122c29" : "#eee9df"};color:${expressive ? "#f0edcc" : "#332f26"}"><p class="eyebrow" style="color:inherit">Lantern studio / fictional exhibition</p><h1 style="font:700 ${expressive ? "92" : "62"}px/.95 Georgia,serif;max-width:600px">Light<br>through<br>leaves.</h1><div aria-hidden="true" style="height:150px;margin:32px 0;background:linear-gradient(135deg,${expressive ? "#9bc696,#215b44,#e2c14b" : "#6b7d5c,#b6bf98,#e3dcb9"});border-radius:${expressive ? "80px 0 80px 0" : "8px"}"></div><p style="font-size:22px">A study of color, shade and quiet.</p><p id="details">October 18–25 · Open 10:00–18:00<br>Fictional address · Entry is free</p></main>`,
    `@media(max-width:600px){h1{font-size:62px!important}}`,
  );
const rtl = (logical) =>
  document(
    `<main dir="rtl"><p class="eyebrow">חשבון / דוגמה בדיונית</p><h1>העברות אחרונות</h1><p>המספרים והמזהים צריכים להישאר ברורים בכל כיוון.</p><section class="panel"><div class="transfer"><span>העברה לחשבון</span><strong id="account" ${logical ? 'dir="ltr"' : ""}>AB-1042 (EUR)</strong><span class="value" dir="ltr">€1,250.00</span><button>פרטים</button></div><p id="note" class="muted">ההעברה ממתינה לאישור.</p></section></main>`,
    `.transfer{display:flex;gap:16px;align-items:center}.transfer strong{${logical ? "margin-inline-start:auto" : "margin-left:auto"};white-space:nowrap}@media(max-width:600px){.transfer{${logical ? "flex-wrap:wrap" : "width:680px"};}.panel{${logical ? "" : "overflow:hidden"};}}`,
    "",
    "he",
  );
const email = (text) =>
  document(
    `<main style="max-width:660px"><p class="eyebrow">Inbox / fictional notice</p><h1>Your route map is ready</h1><p>Review the updated paths before the field visit.</p><section class="panel"><div role="img" aria-label="Route map preview" style="height:190px;background:#d3e6de;padding:24px">North loop → ridge → basin</div>${text ? '<p style="margin-top:24px"><a id="cta" href="#details">Review the route map</a></p>' : '<a id="cta" href="#details"><svg role="img" aria-label="Review the route map" width="240" height="64"><rect width="240" height="64" fill="#153e52"/><text x="20" y="40" fill="white" font-size="18">Review the route map</text></svg></a>'}<p id="details" class="muted" style="margin-top:24px">Last updated October 6. Changes are provisional.</p></section></main>`,
  );
const report = (paginate) =>
  document(
    `<main><p class="eyebrow">Decision record / synthetic report</p><h1>Upgrade the east channel in two stages</h1><p>The staged plan limits downtime and keeps a rollback route.</p>${["Decision and scope", "Costs and assumptions", "Risks and rollback", "Evidence and next review"].map((t, i) => `<section class="panel"><h2>${t}</h2><p>${["Approve planning only. Construction requires a separate decision.", "The illustrative estimate is 18 units. Labor availability is uncertain.", "Retain the existing channel until the new route is exercised.", "These figures are fictional. Review the plan after the trial."][i]}</p><div style="height:100px;border-top:1px solid #d7e0e6;margin-top:24px">Supporting notes</div></section>`).join("")}</main>`,
    `@media print{@page{size:A4;margin:15mm}body{background:white}main{padding:0}.panel{${paginate ? "break-inside:avoid" : "height:80px;overflow:hidden"};border:0;padding:16px 0}h1{font-size:28px}}`,
  );
const explorable = (honest) =>
  document(
    `<main style="max-width:740px"><p class="eyebrow">Explorable / operating reserve</p><h1>How long will the reserve last?</h1><p>Compare input, result and assumptions in one state.</p><section class="panel"><label for="flow">Flow in liters per minute</label><input id="flow" type="number" min="1" value="200"><p style="font-size:40px;margin:24px 0"><output id="duration">12.00</output> <span style="font-size:18px">minutes</span></p><p id="basis">2,400 L reserve · <span id="shownFlow">200</span> L/min</p><p id="error" role="status"></p></section></main>`,
    "",
    `document.querySelector('#flow').oninput=()=>{let v=Number(document.querySelector('#flow').value);if(v<=0){document.querySelector('#error').textContent='Enter a flow greater than zero. Previous result retained.';return;}document.querySelector('#error').textContent='';document.querySelector('#duration').textContent=(2400/${honest ? "v" : "(Math.round(v/100)*100)"}).toFixed(2);${honest ? 'document.querySelector("#shownFlow").textContent=v;' : ""}};`,
  );
export const families = [
  {
    id: "dashboard",
    split: "train",
    title: "Compare an operational exception",
    brief:
      "An operator needs the exception and station readings together, without carrying values between views.",
    before: dashboard(350),
    after: dashboard(20),
    tools: ["geometry", "visibility"],
    entities: { readings: "#readings", exception: "#exception" },
    groups: [{ id: "decision", members: ["readings", "exception"] }],
    selection:
      "Selected co-visibility because the task names two facts needed together.",
  },
  {
    id: "form",
    split: "train",
    title: "Recover a draft after failure",
    brief:
      "Keep the exact entered note when saving fails, and make the retry action usable.",
    before: form(false, false),
    after: form(true, true),
    tools: ["access", "targets"],
    steps: [
      { action: "fill", selector: "#note", value: "Valve checked at 10:15" },
      { action: "click", selector: "#save", observe: ["#note", "#status"] },
    ],
    selection:
      "Selected an actual failure probe rather than inferring recovery from screenshots.",
  },
  {
    id: "chart",
    split: "train",
    title: "Compare counts on one scale",
    brief:
      "Preserve all labels/values and use a common plot width so bar length means the same thing in every row.",
    before: chart(false),
    after: chart(true),
    tools: ["geometry", "typography"],
    entities: { a: "#track0", b: "#track1", c: "#track2" },
    alignments: [{ id: "plots", members: ["a", "b", "c"], axis: "width" }],
    selection:
      "Selected shared plot geometry. Supplied numeric equality alone would miss differently sized plots.",
  },
  {
    id: "article",
    split: "train",
    title: "Keep a decisive qualification",
    brief:
      "A decision maker must see the result, uncertainty and adoption boundary.",
    before: article(true),
    after: article(false),
    tools: ["copy"],
    selection:
      "Rejected the shorter candidate: it deletes the decisive study limitation. Lower word count is the tempting improvement.",
  },
  {
    id: "explainer",
    split: "train",
    title: "Connect a label to its route",
    brief:
      "First-time readers should identify the return-channel label and retain the intake distinction.",
    before: explainer(false),
    after: explainer(true),
    tools: ["geometry"],
    entities: { label: "#label", route: "#route", other: "#competitor" },
    links: [
      {
        id: "return-label",
        from: "label",
        to: "route",
        competitors: ["other"],
      },
    ],
    selection:
      "Selected named relationship distances; semantic ownership comes from the brief.",
  },
  {
    id: "game",
    split: "train",
    title: "Answer repeated interaction",
    brief:
      "Every tap updates the toy counter, including the second and third tap.",
    before: game(true),
    after: game(false),
    tools: ["motion", "targets"],
    steps: [
      { action: "click", selector: "#pad" },
      { action: "click", selector: "#pad" },
      { action: "click", selector: "#pad", observe: ["#count", "#feedback"] },
    ],
    selection:
      "Selected repeated-action probes. Animation count does not establish game feel or fun.",
  },
  {
    id: "deck",
    split: "heldout",
    title: "Keep an assertion with its assumption",
    brief:
      "A reading-deck slide must show the reserve claim and operating assumption together.",
    before: deck(false),
    after: deck(true),
    tools: ["visibility", "typography"],
    entities: { claim: "#claim", assumption: "#assumption" },
    groups: [{ id: "claim-context", members: ["claim", "assumption"] }],
    selection:
      "Selected co-visibility, not a slide word budget. This is a reading deck rather than a live talk.",
  },
  {
    id: "poster",
    split: "heldout",
    title: "Give an exhibition its expression",
    brief:
      "A fictional exhibition poster should express light through leaves and preserve event details.",
    before: poster(false),
    after: poster(true),
    tools: [],
    selection:
      "Chose no quality metric. The question is subject-led expression; supplied event facts remain in both alternatives.",
  },
  {
    id: "rtl",
    split: "heldout",
    title: "Read a mixed-direction transfer",
    brief:
      "Keep Hebrew labels, a Latin account ID, amount and action available on a narrow account screen.",
    before: rtl(false),
    after: rtl(true),
    tools: ["visibility", "typography", "access"],
    entities: {
      account: "#account",
      note: "#note",
      amount: ".value",
      action: "button",
    },
    groups: [
      { id: "transfer", members: ["account", "note", "amount", "action"] },
    ],
    selection:
      "Selected narrow-layout and mixed-direction observations; no automatic mirroring score.",
  },
  {
    id: "email",
    split: "heldout",
    title: "Keep an action with images absent",
    brief:
      "A visible route-review action should remain available when images are hidden. A browser simulation does not prove an email-client result.",
    before: email(false),
    after: email(true),
    tools: ["media", "access", "targets"],
    entities: { cta: "#cta" },
    selection:
      "Selected the images-off stress view. Actual email-client delivery remains unverified.",
  },
  {
    id: "report",
    split: "heldout",
    title: "Preserve a printed decision",
    brief:
      "Print the decision, costs, rollback and review sections without hiding their text.",
    before: report(false),
    after: report(true),
    tools: ["copy"],
    selection:
      "Selected actual Chromium PDF output; the screen view cannot settle pagination.",
  },
  {
    id: "explorable",
    split: "heldout",
    title: "Keep calculator state consistent",
    brief:
      "For 333 L/min, show 2400/333 minutes and the matching input. Invalid input must preserve the preceding valid result.",
    before: explorable(false),
    after: explorable(true),
    tools: ["copy", "access"],
    steps: [
      {
        action: "fill",
        selector: "#flow",
        value: "333",
        observe: ["#duration", "#shownFlow"],
      },
      {
        action: "fill",
        selector: "#flow",
        value: "0",
        observe: ["#duration", "#error"],
      },
    ],
    selection:
      "Selected independent formula/state probes. A polished result can still use premature rounding or stale context.",
  },
];
export const structuredExamples = {
  journey: {
    nodes: [
      { id: "draft" },
      { id: "saving" },
      { id: "error" },
      { id: "saved" },
    ],
    edges: [
      { from: "draft", to: "saving" },
      { from: "saving", to: "saved" },
      { from: "saving", to: "error" },
      { from: "error", to: "draft" },
    ],
    tasks: [
      { id: "recovery", from: "error", to: "draft" },
      { id: "save", from: "draft", to: "saved" },
    ],
  },
  data: {
    series: [
      {
        id: "visits",
        source: [60, 30, 45],
        display: [60, 30, 45],
        units: "visits/week",
        sourceReference: "fictional fixture",
        axis: [0, 100],
        axisPx: [0, 300],
        marks: [
          { value: 60, position: 180 },
          { value: 30, position: 90 },
          { value: 45, position: 135 },
        ],
      },
    ],
  },
  timeline: {
    events: [
      {
        id: "label",
        start: 0,
        end: 2200,
        text: "The reserve lasts twelve minutes.",
      },
      { id: "route", start: 400, end: 2600 },
      { id: "instant", start: 0, end: 0, text: "Essential qualification" },
    ],
    links: [{ from: "label", to: "route" }],
  },
  content: {
    items: [
      { id: "reserve", role: "concept" },
      { id: "formula", role: "worked-example", prerequisites: ["reserve"] },
      { id: "retrieval", role: "question", prerequisites: ["formula"] },
    ],
    order: ["reserve", "formula", "retrieval"],
  },
  survey: {
    minimum: 1,
    maximum: 5,
    items: [
      { id: "clear", axis: "clarity" },
      { id: "confusing", axis: "clarity", reverse: true },
      { id: "engaging", axis: "engagement" },
    ],
    responses: [
      { clear: 4, confusing: 2, engaging: 3 },
      { clear: 3, engaging: 5 },
    ],
  },
  viewing: {
    distanceMm: 3000,
    elements: [
      { id: "caption-height", sizeMm: 8 },
      { id: "title-height", sizeMm: 28 },
    ],
  },
  palette: {
    colors: [
      { id: "ink", hex: "#142c3b" },
      { id: "accent", hex: "#83d7d5" },
      { id: "paper", hex: "#eff5f6" },
    ],
    pairs: [
      ["ink", "paper"],
      ["ink", "accent"],
    ],
    order: ["ink", "accent", "paper"],
  },
};
