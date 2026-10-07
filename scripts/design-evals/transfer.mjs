// Independently specified after instrument freeze, before execution. No tuning.
export const transferCases = [
  {
    id: "museum-enclosure",
    command: "inspect",
    tools: "geometry,visibility",
    width: 800,
    height: 600,
    html: '<!doctype html><html lang="en"><meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0;font:16px sans-serif}#pass{position:absolute;left:40px;top:40px;width:320px;height:260px;border:4px solid #164;padding:0}#label{position:absolute;left:160px;top:20px;width:130px;height:24px}#price{position:absolute;left:20px;top:190px;width:280px;height:40px}#audio{position:absolute;left:380px;top:64px;width:180px;height:40px;border:2px solid #888}</style><body><section id="pass" aria-label="Gallery admission"><strong id="label">Gallery entry</strong><p id="price" style="margin:0">€12 / adult</p></section><aside id="audio">Audio guide €4</aside></body></html>',
    plan: {
      entities: { label: "#label", price: "#price", audio: "#audio" },
      links: [
        {
          id: "admission-price",
          from: "label",
          to: "price",
          competitors: ["audio"],
        },
      ],
      groups: [{ id: "admission", members: ["label", "price"] }],
    },
    expected:
      "The enclosing admission panel owns the €12 price; both facts visible. Proximity-only interpretation is inapplicable and must retain its unfavorable negative margin.",
    check: (r) =>
      r.observations.geometry.associations[0].competitorMinusIntendedEm < 0 &&
      r.observations.visibility.groups[0].allFullyVisibleNow,
    applicability:
      "Proximity proxy INAPPLICABLE: common region supplies the association.",
  },
  {
    id: "departure-board",
    command: "inspect",
    tools: "visibility",
    width: 400,
    height: 600,
    html: '<!doctype html><html lang="en"><meta charset="utf-8"><style>body{margin:0;font:20px sans-serif}#gate,#notice{position:absolute;left:24px;width:280px;box-sizing:border-box;background:#eef;padding:12px}#gate{top:24px;height:64px}#notice{top:590px;height:80px}</style><body><div id="gate">Train 18 · Platform 4</div><div id="notice">Boarding closes at 17:42.</div></body></html>',
    plan: {
      entities: { gate: "#gate", notice: "#notice" },
      groups: [{ id: "boarding-decision", members: ["gate", "notice"] }],
    },
    expected:
      "Only gate fully visible initially; moving notice top to420 keeps text and makes both fully visible.",
    revisedHTML: (h) => h.replace("top:590px", "top:420px"),
    check: (r) =>
      !r.observations.visibility.groups[0].allFullyVisibleNow &&
      r.observations.visibility.groups[0].fullyVisible.join(",") === "gate",
    revisedCheck: (r) => r.observations.visibility.groups[0].allFullyVisibleNow,
    applicability: "Initial-view box availability, not comprehension.",
  },
  {
    id: "thermometer-scale",
    command: "data",
    input: {
      series: [
        {
          id: "gallery-temperature",
          source: [-10, 0, 10, 30],
          display: [-10, 0, 10, 30],
          units: "°C",
          sourceReference: "fictional fixed thermometer readings",
          axis: [-10, 30],
          axisPx: [300, 100],
          marks: [
            { value: -10, position: 300 },
            { value: 0, position: 250 },
            { value: 10, position: 210 },
            { value: 30, position: 100 },
          ],
        },
      ],
    },
    expected:
      "Values agree; mark errors0,0,+10,0; zero included and none outside axis.",
    check: (r) =>
      r.observations.data[0].differences.length === 0 &&
      r.observations.data[0].marks.map((m) => m.positionErrorPx).join(",") ===
        "0,0,10,0" &&
      r.observations.data[0].zeroIncluded &&
      r.observations.data[0].valuesOutsideAxis.length === 0,
    applicability:
      "Supplied linear coordinates only; descending scale supported.",
  },
  {
    id: "audio-tour",
    command: "timeline",
    input: {
      events: [
        {
          id: "speech",
          start: 1000,
          end: 5000,
          text: "The east bell marks the entrance to atrium.",
        },
        { id: "map", start: 3500, end: 6500 },
        {
          id: "exit",
          start: 7700,
          end: 8200,
          text: "Continue through the arch.",
        },
      ],
      links: [
        { from: "speech", to: "map" },
        { from: "map", to: "exit" },
      ],
    },
    expected:
      "Speech4000ms/2 words per second; map3000ms; overlap1500ms then gap1200ms; exit500ms/8 words per second.",
    check: (r) => {
      const t = r.observations.timeline;
      return (
        t.events[0].durationMs === 4000 &&
        t.events[0].wordsPerSecond === 2 &&
        t.events[1].durationMs === 3000 &&
        t.events[2].wordsPerSecond === 8 &&
        t.relations[0].overlapMs === 1500 &&
        t.relations[1].gapMs === 1200
      );
    },
    applicability: "Declared exposure/overlap, no safe-rate verdict.",
  },
  {
    id: "costume-picker",
    command: "probe",
    html: '<!doctype html><html lang="en"><meta charset="utf-8"><body><h1>Choose costume size</h1><button id="open">Edit size</button><section id="panel" hidden><label for="size">Size</label><input id="size" value="M"><button id="cancel">Cancel</button></section><script>openButton=document.querySelector("#open");panel=document.querySelector("#panel");sizeInput=document.querySelector("#size");openButton.onclick=()=>{panel.hidden=false;sizeInput.focus()};document.querySelector("#cancel").onclick=()=>{panel.hidden=true;openButton.focus()};</script></body></html>',
    plan: {
      steps: [
        { action: "focus", selector: "#open" },
        {
          action: "press",
          selector: "#open",
          key: "Enter",
          observe: ["#size"],
        },
        { action: "fill", selector: "#size", value: "L" },
        { action: "click", selector: "#cancel", observe: ["#size"] },
        {
          action: "press",
          selector: "#open",
          key: "Enter",
          observe: ["#size"],
        },
      ],
    },
    expected:
      "Open Size M focused; cancel hides it and retains L, focus returns to open; reopen L focused.",
    check: (r) => {
      const t = r.observations.probe.records;
      return (
        t[1].values["#size"].value === "M" &&
        t[1].activeElement.id === "size" &&
        !t[3].values["#size"].visible &&
        t[3].values["#size"].value === "L" &&
        t[3].activeElement.id === "open" &&
        t[4].values["#size"].visible &&
        t[4].values["#size"].value === "L" &&
        t[4].activeElement.id === "size"
      );
    },
    applicability:
      "Supplied cancellation/focus scenario, not a full dialog audit.",
  },
  {
    id: "recipe-dependencies",
    command: "content",
    input: {
      items: [
        { id: "weigh", role: "prepare" },
        { id: "mix", role: "step", prerequisites: ["weigh"] },
        { id: "preheat", role: "prepare" },
        { id: "bake", role: "step", prerequisites: ["mix", "preheat"] },
      ],
      order: ["mix", "weigh", "bake"],
    },
    expected:
      "preheat absent/-1; mix prerequisite false; bake mix true/preheat false.",
    check: (r) => {
      const t = r.observations.content.items;
      return (
        t[2].position === -1 &&
        !t[2].present &&
        !t[1].prerequisites[0].introducedEarlier &&
        t[3].prerequisites[0].introducedEarlier &&
        !t[3].prerequisites[1].introducedEarlier
      );
    },
    applicability: "Declared order/necessity supplied, no measured learning.",
  },
];
