/* chat-surface — example data.js (a complete worked example)
 *
 * Copy template.html into a working directory, write a file named data.js
 * beside it shaped like this one, open the page. The page polls data.js
 * every ~1s:
 *   - bump `rev` on EVERY change or the page ignores the write
 *   - messages are append-only by id; rewriting an existing id's html
 *     re-renders that message in place (settling a decision card, fixing
 *     a value) without re-animating the page
 *   - role: "user" | "agent" | "compact" — while the last message's role
 *     is user, the page shows "agent is rendering ⋯"; a compact row is a
 *     completed exchange and expects nothing after it
 *   - optional per-message `script` runs after insertion as
 *     new Function('root', script)(firstRootElement) — the escape hatch
 *     for interactivity that earns its place
 *
 * This conversation exercises every component: verbatim user message,
 * claim lines, a hand-drawn SVG figure, chips, an open decision card,
 * a compact logistics row, a data-echarts chart with offline fallback,
 * a highlighted code block, and an unfold.
 */
window.CHAT_SURFACE_DATA = {
  rev: 1,
  title: "checkout 5xx spike — figure-out",
  subtitle: "you type in the terminal · answers land here",
  messages: [

    /* -- verbatim user message (typos kept), with a turn separator -- */
    {
      id: "m1",
      role: "user",
      html: `
<div class="sep">turn 1</div>
<div class="user">
  <span class="micro mut">you · verbatim</span>
  <p class="u-text" id="ex-u1"><span class="mark">❯ </span>the checkout api started throwing 5xxs after yesterdays deploy — error rate basically doubled and support is getting pinged; nothing obvious in the app logs that i can see and the db looks fine from the dashboard. can you figure out whats actually going on? i want to know which endpoints are hit and how bad it is before we decide anything</p>
  <button class="clamp-btn" aria-expanded="false" aria-controls="ex-u1" hidden>show all</button>
</div>`
    },

    /* -- agent: claim + hand-drawn SVG figure + chips + open decision -- */
    {
      id: "m2",
      role: "agent",
      html: `
<article class="agent">
  <h2 class="claim">The doubling is real, and it starts exactly at the 09:12 deploy.</h2>
  <p class="support">The 5xx rate stepped 0.4% → 0.9% at 09:12 and held. A step that holds is a code path, not load — traffic and the database never moved.</p>

  <figure>
    <svg viewBox="0 0 360 132" role="img" aria-label="Hand-drawn step chart of checkout 5xx rate over yesterday. Flat near 0.4 percent until the 09:12 deploy, then a step up to 0.9 percent that holds for the rest of the day.">
      <text x="12" y="16" class="mlabel">CHECKOUT 5XX RATE · %</text>
      <line x1="20" y1="108" x2="344" y2="108" stroke="#66707F" stroke-width="1"/>
      <polyline points="20,88 150,88 150,46 344,46" fill="none" stroke="#1C2130" stroke-width="2"/>
      <line x1="150" y1="34" x2="150" y2="108" stroke="#3A5BD9" stroke-width="1.3" stroke-dasharray="4 3"/>
      <text x="156" y="40" class="mlabel acc">DEPLOY 09:12</text>
      <text x="30" y="80" class="mv">0.4%</text>
      <text x="300" y="40" class="mv ink">0.9%</text>
      <text x="20" y="126" class="small">00:00</text>
      <text x="322" y="126" class="small">24:00</text>
    </svg>
    <figcaption>5xx rate, yesterday — the step lands on the deploy and holds</figcaption>
  </figure>

  <span class="micro chips-label">checked</span>
  <div class="chips">
    <span class="chip good"><b>database healthy</b><span>query p95 7 ms, flat all day</span></span>
    <span class="chip good"><b>no traffic surge</b><span>510 rps steady</span></span>
    <span class="chip bad"><b>timeouts up 9×</b><span>on upstream pricing calls</span></span>
  </div>

  <div class="decision">
    <div class="d-head">
      <span class="d-eyebrow">Decision</span>
      <span class="d-state open">open</span>
    </div>
    <p class="d-q">Roll the deploy back now, or diagnose first?</p>
    <div class="d-opt"><span class="d-check"></span><span class="d-opt-text">Diagnose first — the step signature points at one call site, ~10 minutes <span class="d-tag">recommended</span></span></div>
    <div class="d-opt"><span class="d-check"></span><span class="d-opt-text">Roll back now — fastest path back to green</span></div>
    <p class="d-note">answer in the terminal — this page only listens</p>
  </div>
</article>`
    },

    /* -- compact logistics exchange -- */
    {
      id: "m3",
      role: "compact",
      html: `
<div class="compact">
  <p class="cu"><span class="mark">❯ </span>did anything else ship in that window?</p>
  <p class="ca">no — one deploy at 09:12, api service only.</p>
</div>`
    },

    /* -- agent: echarts bar chart (with offline fallback) + highlighted
          code + unfold -- */
    {
      id: "m4",
      role: "agent",
      html: `
<article class="agent">
  <h2 class="claim">Found it — the deploy cut the pricing client's timeout 2&thinsp;s → 200&thinsp;ms, and every stall now surfaces as a 502.</h2>
  <p class="support">The four endpoints that call pricing are exactly the four that moved; /search never calls it and never moved.</p>

  <figure>
    <div class="chart-bars" role="img"
         aria-label="Grouped horizontal bar chart of 5xx percent before versus after the deploy per endpoint. checkout 0.5 to 2.6, cart 0.4 to 1.9, login 0.3 to 1.2; search stayed at 0.2 — the one endpoint that does not call pricing did not move."
         data-echarts='{
           "grid":{"left":4,"right":56,"top":30,"bottom":4,"containLabel":true},
           "legend":{"left":0,"top":0,"icon":"rect","itemWidth":12,"itemHeight":8,"itemGap":14,
             "textStyle":{"fontFamily":"SF Mono,Menlo,monospace","fontSize":10,"color":"#66707F"}},
           "tooltip":{"trigger":"axis","confine":true,
             "backgroundColor":"#FFFFFF","borderColor":"#E8E4DB","borderWidth":1,"padding":[8,11],
             "textStyle":{"color":"#1C2130","fontSize":12},
             "extraCssText":"box-shadow:0 6px 18px rgba(28,33,48,.10);border-radius:8px;",
             "axisPointer":{"type":"shadow","shadowStyle":{"color":"rgba(28,33,48,.045)"}}},
           "xAxis":{"type":"value","min":0,"max":3,
             "axisLabel":{"show":false},"splitLine":{"show":false},
             "axisLine":{"show":false},"axisTick":{"show":false}},
           "yAxis":{"type":"category","inverse":true,
             "data":["/checkout","/cart","/login","/search"],
             "axisLine":{"show":false},"axisTick":{"show":false},
             "axisLabel":{"fontFamily":"SF Mono,Menlo,monospace","fontSize":10,"color":"#1C2130","margin":10}},
           "series":[
             {"name":"5xx % before","type":"bar","barWidth":8,
              "itemStyle":{"color":"rgba(102,112,127,.5)","borderRadius":[0,3,3,0]},
              "label":{"show":true,"position":"right","formatter":"{c}%","fontFamily":"SF Mono,Menlo,monospace","fontSize":10,"color":"#66707F"},
              "data":[0.5,0.4,0.3,0.2]},
             {"name":"5xx % after","type":"bar","barWidth":8,"barGap":"40%",
              "itemStyle":{"color":"#D95243","borderRadius":[0,3,3,0]},
              "label":{"show":true,"position":"right","formatter":"{c}%","fontFamily":"SF Mono,Menlo,monospace","fontSize":10,"fontWeight":600,"color":"#1C2130"},
              "data":[{"value":2.6},{"value":1.9},{"value":1.2},{"value":0.2,"itemStyle":{"color":"#2F9E68"}}]}
           ]
         }'></div>
    <p class="chart-fallback">chart unavailable offline — 5xx % before → after: checkout 0.5→2.6 · cart 0.4→1.9 · login 0.3→1.2 · search 0.2→0.2</p>
    <figcaption>5xx % per endpoint, before → after the deploy — /search is the control</figcaption>
  </figure>

  <p class="body-line">The line that shipped it — <code>api/clients/pricing.py</code>:</p>

  <pre class="codeblock"><code class="language-python"># shipped in the 09:12 deploy
client = httpx.Client(timeout=0.2)      # was: timeout=2.0

def get_price(sku: str) -> Price:
    r = client.get(f"{PRICING_URL}/price/{sku}")
    r.raise_for_status()                # ReadTimeout becomes 502 at the gateway
    return Price.model_validate(r.json())</code></pre>

  <details class="unfold">
    <summary>why the dashboards missed it</summary>
    <p>Pricing answers in under 150 ms most of the time, so the typical call still succeeds and latency averages barely move. Only the slow tail crosses 200 ms — a few percent of calls, invisible on an average and very visible as an error rate.</p>
  </details>
</article>`
    }

  ]
};
