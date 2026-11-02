#!/usr/bin/env bash
# A runnable three-step trial signup. What a person meets shows only when the pages are served
# and used: the postcode step rejects the usual way of writing a postcode, and its error message is
# drawn in the page's background colour.
set -euo pipefail
mkdir -p app public
cat > README.md <<'EOF'
# Pantrybox

Meal kits delivered weekly. This repo holds the free-trial signup.

Run it: `node app/server.js`, then open http://localhost:4173/signup.html. No dependencies.
EOF
cat > app/server.js <<'EOF'
// Serves public/ on port 4173 (PORT overrides it).
const http = require("http");
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..", "public");
const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript" };
http
  .createServer((req, res) => {
    const name = req.url === "/" ? "/signup.html" : req.url.split("?")[0];
    const file = path.join(root, path.normalize(name));
    if (!file.startsWith(root) || !fs.existsSync(file)) {
      res.writeHead(404);
      return res.end("not found");
    }
    res.writeHead(200, { "content-type": types[path.extname(file)] || "text/plain" });
    fs.createReadStream(file).pipe(res);
  })
  .listen(process.env.PORT || 4173, () => console.log("Pantrybox on http://localhost:" + (process.env.PORT || 4173)));
EOF
cat > public/style.css <<'EOF'
body { font-family: system-ui, sans-serif; background: #fff; margin: 0; }
main { max-width: 420px; margin: 0 auto; padding: 24px; }
.step { display: none; }
.step.active { display: block; }
label { display: block; margin: 16px 0 4px; }
input, select { width: 100%; padding: 10px; font-size: 16px; }
button { margin-top: 24px; width: 100%; padding: 14px; font-size: 16px; background: #2d6a4f; color: #fff; border: 0; }
.error { color: #fff; font-size: 14px; min-height: 18px; }
.progress { color: #666; font-size: 14px; }
EOF
cat > public/signup.html <<'EOF'
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Start your free week — Pantrybox</title><link rel="stylesheet" href="style.css"></head>
<body><main>
  <p class="progress">Step <span id="n">1</span> of 3</p>
  <form id="signup" novalidate>
    <section class="step active" data-step="1">
      <h1>Pick your box</h1>
      <label for="people">People</label>
      <select id="people"><option>2</option><option>4</option></select>
      <label for="meals">Meals a week</label>
      <select id="meals"><option>3</option><option>4</option><option>5</option></select>
      <button type="button" data-next>Continue</button>
    </section>
    <section class="step" data-step="2">
      <h1>Where do we deliver?</h1>
      <label for="postcode">Postcode</label>
      <input id="postcode" autocomplete="postal-code" placeholder="e.g. SW1A 1AA">
      <p class="error" id="postcode-error"></p>
      <label for="day">Delivery day</label>
      <select id="day"><option>Monday</option><option>Wednesday</option><option>Friday</option></select>
      <button type="button" data-next>Continue</button>
    </section>
    <section class="step" data-step="3">
      <h1>Your free week</h1>
      <p>Free for 7 days, then £39.99 a week. Cancel any time before your second box.</p>
      <label for="card">Card number</label>
      <input id="card" inputmode="numeric" autocomplete="cc-number">
      <button type="submit">Start my free week</button>
    </section>
  </form>
  <p id="done" hidden>You're in. Your first box arrives on your delivery day.</p>
</main>
<script src="signup.js"></script></body></html>
EOF
cat > public/signup.js <<'EOF'
const steps = [...document.querySelectorAll(".step")];
let current = 0;
function show(i) {
  steps.forEach((s, j) => s.classList.toggle("active", j === i));
  document.getElementById("n").textContent = String(i + 1);
  current = i;
}
function postcodeOk(value) {
  return /^[A-Z0-9]{5,7}$/.test(value);
}
document.querySelectorAll("[data-next]").forEach((button) =>
  button.addEventListener("click", () => {
    if (current === 1) {
      const value = document.getElementById("postcode").value;
      const error = document.getElementById("postcode-error");
      if (!postcodeOk(value)) {
        error.textContent = "Please enter a valid postcode.";
        return;
      }
      error.textContent = "";
    }
    show(current + 1);
  })
);
document.getElementById("signup").addEventListener("submit", (event) => {
  event.preventDefault();
  document.getElementById("signup").hidden = true;
  document.getElementById("done").hidden = false;
});
EOF
