#!/usr/bin/env bash
# Tablewise, a restaurant-booking web app with its own page patterns: design's
# variants-of-an-experience-choice scenario prototypes a new flow on it.
set -euo pipefail
mkdir -p pages
cat > README.md <<'EOF'
# Tablewise

Book a table with friends. Pages live in `pages/` and share `pages/styles.css`: a card per step,
a sticky bottom bar holding the one primary action, steppers for counts, and a sheet that slides
up for secondary choices. Open any page directly in a browser.
EOF
cat > pages/styles.css <<'EOF'
:root { --ink: #1d2b36; --muted: #6b7a86; --accent: #c8553d; --line: #e4e7ea; --bg: #f7f5f2; }
body { margin: 0; font: 16px/1.45 system-ui, sans-serif; color: var(--ink); background: var(--bg); }
main { max-width: 440px; margin: 0 auto; padding: 16px 16px 96px; }
.card { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 16px; margin-bottom: 12px; }
.card h2 { margin: 0 0 8px; font-size: 18px; }
.muted { color: var(--muted); font-size: 14px; }
.stepper { display: flex; align-items: center; gap: 16px; }
.stepper button { width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--line); background: #fff; font-size: 20px; }
.row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--line); }
.bar { position: fixed; left: 0; right: 0; bottom: 0; background: #fff; border-top: 1px solid var(--line); padding: 12px 16px; }
.bar .primary { display: block; width: 100%; max-width: 440px; margin: 0 auto; padding: 14px; border: 0; border-radius: 12px; background: var(--accent); color: #fff; font-size: 16px; }
.sheet { position: fixed; left: 0; right: 0; bottom: 0; background: #fff; border-radius: 16px 16px 0 0; box-shadow: 0 -8px 24px rgba(0,0,0,.12); padding: 20px 16px 32px; }
EOF
cat > pages/booking.html <<'EOF'
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Book — Tablewise</title><link rel="stylesheet" href="styles.css"></head><body><main>
<div class="card"><h2>Osteria Lume</h2><p class="muted">Italian · Harbour Street · £££</p></div>
<div class="card"><h2>When</h2><div class="row"><span>Friday 14 Nov</span><span>19:30</span></div></div>
<div class="card"><h2>Guests</h2><div class="stepper"><button>−</button><strong>4</strong><button>+</button></div></div>
<div class="card"><h2>Invite your table</h2><p class="muted">Send the booking to the people coming.</p></div>
</main><div class="bar"><button class="primary">Book for 4</button></div></body></html>
EOF
cat > pages/bill.html <<'EOF'
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bill — Tablewise</title><link rel="stylesheet" href="styles.css"></head><body><main>
<div class="card"><h2>Your bill</h2><p class="muted">Osteria Lume · Friday 14 Nov · 4 guests</p>
<div class="row"><span>Burrata</span><span>£12.00</span></div>
<div class="row"><span>Tagliatelle ragù ×2</span><span>£34.00</span></div>
<div class="row"><span>Risotto</span><span>£18.50</span></div>
<div class="row"><span>Bottle, Montepulciano</span><span>£32.00</span></div>
<div class="row"><strong>Total</strong><strong>£96.50</strong></div></div>
</main><div class="bar"><button class="primary">Pay £96.50</button></div></body></html>
EOF
