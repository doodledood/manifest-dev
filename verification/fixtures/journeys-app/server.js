// Waymark: a small trip planner's Saved places page.
// No dependencies: `node server.js` serves it on PORT (default 4180). State lives in memory.
const http = require("http");

const PORT = Number(process.env.PORT || 4180);
const TRIPS = {
  lisbon: {
    title: "Lisbon", owner: "Maya", firstDay: Date.UTC(2026, 4, 12), dayCount: 3,
    places: [
      "Belém Tower", "LX Factory", "Time Out Market", "Alfama walk",
      "Gulbenkian Museum", "Miradouro da Graça", "Pastéis de Belém",
    ],
  },
  porto: { title: "Porto", owner: "Maya", firstDay: Date.UTC(2026, 8, 3), dayCount: 2, places: [] },
};
const dayLabel = (trip, d) =>
  new Date(trip.firstDay + d * 86400000).toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", timeZone: "UTC" });
const MAX_NAME = 80;
const LAST_SLOT = 20; // the latest hour a planned place starts at
const startHour = new Map(); // email -> hour the day plan starts at; unset means 9

const page = (title, body) => `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>${title} — Waymark</title>
<style>body{font-family:system-ui,sans-serif;max-width:560px;margin:0 auto;padding:16px;overflow-wrap:anywhere}
nav a{display:inline-block;margin-right:12px;padding:10px 0}nav a[aria-current]{font-weight:700;text-decoration:none}
li{margin:6px 0}.day{margin-top:16px}.error{color:#a40000}button,input,select{font-size:16px;padding:6px;min-height:44px}</style>
</head><body>${body}</body></html>`;

const escape = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const userOf = (req) => {
  const raw = (/(?:^|;\s*)user=([^;]+)/.exec(req.headers.cookie || "") || [])[1];
  try {
    return raw && decodeURIComponent(raw);
  } catch {
    return undefined;
  }
};
const send = (res, status, html, headers = {}) => {
  res.writeHead(status, { "content-type": "text/html; charset=utf-8", ...headers });
  res.end(html);
};
const redirect = (res, to, headers = {}) => {
  res.writeHead(303, { location: to, ...headers });
  res.end();
};
const readForm = (req) =>
  new Promise((done) => {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => done(new URLSearchParams(body)));
  });
const signinLink = (path) => `/signin?next=${encodeURIComponent(path)}`;

function home(req, res) {
  const user = userOf(req);
  const trips = Object.entries(TRIPS).map(([id, t]) => `<li><a href="/trips/${id}">${t.title}</a></li>`).join("");
  const body = user
    ? `<h1>Your trips</h1><p>Signed in as ${escape(user)}.</p><ul>${trips}</ul>`
    : `<h1>Waymark</h1><p>Plan trips with friends.</p><p><a href="/signin">Sign in</a></p>`;
  send(res, 200, page("Waymark", body));
}

function signinForm(req, res, url, error = "") {
  const next = url.searchParams.get("next") || "/";
  send(res, error ? 400 : 200, page("Sign in", `<h1>Sign in</h1>${error ? `<p class="error" role="alert">${error}</p>` : ""}
<form method="post" action="/signin"><input type="hidden" name="next" value="${escape(next)}">
<label>Email <input name="email" type="email" required></label> <button>Sign in</button></form>`));
}

async function signin(req, res) {
  const form = await readForm(req);
  const email = (form.get("email") || "").trim();
  const next = form.get("next") || "/";
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    const url = new URL(`http://x/signin?next=${encodeURIComponent(next)}`);
    return signinForm(req, res, url, "Enter an email address like name@example.com.");
  }
  const safeNext = next.startsWith("/") && !next.startsWith("//") ? next : "/";
  redirect(res, safeNext, { "set-cookie": `user=${encodeURIComponent(email)}; Path=/; HttpOnly` });
}

function planDays(trip, list, hour) {
  const fits = Math.floor((LAST_SLOT - hour) / 2) + 1;
  const perDay = Math.min(Math.ceil(list.length / trip.dayCount), fits);
  const days = [];
  for (let i = 0; i < list.length && days.length < trip.dayCount; i += perDay) days.push(list.slice(i, i + perDay));
  return { days, unplanned: list.slice(perDay * trip.dayCount) };
}

const ERRORS = {
  empty: "Type a place name to add it.",
  long: `Place names can be up to ${MAX_NAME} characters.`,
  duplicate: "That place is already saved for this trip.",
  session: "You were signed out, so the place wasn't added. It's still typed below; tap Add.",
};

// Every form posts in place: while it waits the button says so, and when the server cannot be
// reached or answers with an error, the page stays as it was and says what wasn't saved.
// A message shown once is dropped from the address, so Back never brings it back.
const PAGE_SCRIPT = `<script>
const shown = new URL(location.href);
if (shown.searchParams.has("error")) {
  shown.searchParams.delete("error");
  shown.searchParams.delete("typed");
  history.replaceState(null, "", shown.pathname + shown.search);
}
document.querySelectorAll("form[data-what]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector("button");
    const note = form.querySelector(".error");
    const label = button.textContent;
    button.disabled = true;
    button.textContent = "Saving…";
    note.textContent = "";
    const failed = () => {
      note.textContent = "Couldn't reach Waymark, so " + form.dataset.what + " wasn't saved. Nothing you chose is lost; try again.";
      button.disabled = false;
      button.textContent = label;
    };
    try {
      const r = await fetch(form.action, { method: "post", body: new URLSearchParams(new FormData(form)) });
      if (!r.ok || !r.redirected) return failed();
      location.href = r.url;
    } catch {
      failed();
    }
  });
});
</script>`;

function tripPage(req, res, url, id) {
  const trip = TRIPS[id];
  const path = `/trips/${id}`;
  const user = userOf(req);
  if (!user) {
    return send(res, 200, page(trip.title, `<h1>${trip.title} trip: saved places</h1>
<p>Sign in to see the places your group saved for this trip.</p><p><a href="${signinLink(url.pathname + url.search)}">Sign in</a></p>`));
  }
  const mode = url.searchParams.get("mode") === "plan" ? "plan" : "list";
  const code = url.searchParams.get("error");
  const error = code && Object.hasOwn(ERRORS, code) ? ERRORS[code] : "";
  const typed = url.searchParams.get("typed") || "";
  const current = (m) => (m === mode ? ' aria-current="page"' : "");
  const nav = `<nav><a href="${path}"${current("list")}>List</a><a href="${path}?mode=plan"${current("plan")}>Day plan</a></nav>`;
  const add = `<form method="post" action="${path}/places" data-what="the place"><input type="hidden" name="mode" value="${mode}">
<label>Add a place <input name="name" maxlength="${MAX_NAME}" value="${escape(typed)}"></label> <button>Add</button>
<p class="error" role="alert">${error || ""}</p></form>`;
  let main;
  if (mode === "list") {
    main = trip.places.length
      ? `<h2>Saved places (${trip.places.length})</h2><ul>${trip.places.map((p) => `<li>${escape(p)}</li>`).join("")}</ul>`
      : `<h2>Saved places (0)</h2><p>No places yet. Add the first one above.</p>`;
  } else {
    const hour = startHour.get(user) || 9;
    const options = [8, 9, 10].map((h) => `<option value="${h}"${h === hour ? " selected" : ""}>${h}:00</option>`).join("");
    const setting = `<form method="post" action="${path}/start" data-what="the start time"><label>Start each day at
<select name="hour">${options}</select></label> <button>Save</button><p class="error" role="alert"></p></form>`;
    const { days, unplanned } = planDays(trip, trip.places, hour);
    const planned = days
      .map((dayPlaces, d) => `<div class="day"><h3>${dayLabel(trip, d)}</h3><ul>${dayPlaces
        .map((p, i) => `<li>${String(hour + 2 * i).padStart(2, "0")}:00 — ${escape(p)}</li>`)
        .join("")}</ul></div>`)
      .join("");
    const rest = unplanned.length
      ? `<div class="day"><h3>Not in the plan (${unplanned.length})</h3><p>These don't fit in ${trip.dayCount} days.</p><ul>${unplanned
        .map((p) => `<li>${escape(p)}</li>`).join("")}</ul></div>`
      : "";
    main = `<h2>Day plan</h2>${setting}${trip.places.length ? planned + rest : "<p>No places to plan yet.</p>"}`;
  }
  const dates = `${dayLabel(trip, 0)} – ${dayLabel(trip, trip.dayCount - 1)}`;
  send(res, 200, page(trip.title, `<h1>${trip.title} · ${dates}</h1>${nav}${add}${main}${PAGE_SCRIPT}`), { "cache-control": "no-store" });
}

async function addPlace(req, res, id) {
  const trip = TRIPS[id];
  const user = userOf(req);
  const form = await readForm(req);
  const mode = form.get("mode") === "plan" ? "plan" : "list";
  const back = `/trips/${id}${mode === "plan" ? "?mode=plan" : ""}`;
  const name = (form.get("name") || "").trim().replace(/\s+/g, " ");
  if (!user) {
    const kept = new URLSearchParams({ ...(mode === "plan" ? { mode } : {}), error: "session", typed: name });
    return redirect(res, signinLink(name ? `/trips/${id}?${kept}` : back));
  }
  const fail = (code) => {
    const query = new URLSearchParams({ ...(mode === "plan" ? { mode } : {}), error: code, typed: name });
    redirect(res, `/trips/${id}?${query}`);
  };
  if (!name) return fail("empty");
  if (name.length > MAX_NAME) return fail("long");
  if (trip.places.some((p) => p.toLowerCase() === name.toLowerCase())) return fail("duplicate");
  trip.places.push(name);
  redirect(res, back);
}

async function setStart(req, res, id) {
  const user = userOf(req);
  if (!user) return redirect(res, signinLink(`/trips/${id}?mode=plan`));
  const form = await readForm(req);
  const hour = Number(form.get("hour"));
  if ([8, 9, 10].includes(hour)) startHour.set(user, hour);
  redirect(res, `/trips/${id}?mode=plan`);
}

function notFound(req, res) {
  const way = userOf(req) ? `<a href="/">See your trips</a>` : `<a href="/signin">Sign in</a> to see your trips`;
  send(res, 404, page("Not found", `<h1>No trip here</h1><p>This link doesn't match a trip on Waymark. Ask whoever shared it for a new link.</p><p>${way}</p>`));
}

http
  .createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    const tripPath = /^\/trips\/([^/]+?)\/?(places|start)?\/?$/i.exec(url.pathname);
    const id = tripPath && tripPath[1].toLowerCase();
    if (tripPath && !Object.hasOwn(TRIPS, id)) return notFound(req, res);
    const route = `${req.method} ${tripPath ? `/trips/:id${tripPath[2] ? `/${tripPath[2]}` : ""}` : url.pathname}`;
    if (route === "GET /") return home(req, res);
    if (route === "GET /signin") return signinForm(req, res, url);
    if (route === "POST /signin") return signin(req, res);
    if (route === "GET /trips/:id") {
      const canonical = `/trips/${id}`;
      if (url.pathname !== canonical) return redirect(res, canonical + url.search);
      return tripPage(req, res, url, id);
    }
    if (route === "POST /trips/:id/places") return addPlace(req, res, id);
    if (route === "POST /trips/:id/start") return setStart(req, res, id);
    notFound(req, res);
  })
  .listen(PORT, () => console.log(`Waymark on http://localhost:${PORT}`));
