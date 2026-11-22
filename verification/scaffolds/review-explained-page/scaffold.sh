#!/usr/bin/env bash
# Kestrel Couriers: a parcel-tracking page in a project with no principles skill. Its first commit
# is the page an earlier review found five things on, each something people would not understand.
# Its second commit answered every one of them with an added sentence that explains the page, and
# changed nothing else; docs/review-round-1.md holds the findings and how each was answered. Each
# sentence says something a label, a mark, an order or a position on the page could carry. The
# review-design recipe's explained scenario reviews the page as it stands.
#
# Given the argument `retested`, which the review-explained-retested scaffold passes when it sources
# this file, the five sentences are shorter and say the same things, and the record adds a re-test
# that counts the findings as closed. Nothing else differs. The variant is an argument, never an
# environment variable, so a driver's shell cannot pick it by accident.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
variant=${1:-}
. "$(dirname "${BASH_SOURCE[0]}")/../../../scripts/scaffold-playwright.sh"
link_playwright
git branch -M main
git config user.name 'Tomas Reyes'
git config user.email 'tomas@kestrel.example'
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p docs pages
cat > AGENTS.md <<'EOF'
# Kestrel Couriers: tracking

The page a customer opens from our "your parcel is on its way" text message. They open it on a
phone, often while doing something else, to learn one thing: when the parcel will arrive. Some
then leave an instruction for the driver.

Open `pages/track.html` in a browser to see it. `package.json` lists Playwright for anything that
renders the page.
EOF
ln -s AGENTS.md CLAUDE.md
cat > package.json <<EOF
{
  "name": "kestrel-tracking",
  "private": true,
  "devDependencies": { "$playwright_module": "*" }
}
EOF
# The page, written once with a slot for each sentence the second commit adds.
page() {
  local circles=$1 code=$2 times=$3 icons=$4 list=$5
  cat <<EOF
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Parcel KC-48213 — Kestrel Couriers</title>
  <style>
    :root { --ink: #16202a; --soft: #51606e; --paper: #ffffff; --line: #d5dce3; --brand: #0b5cad; }
    * { box-sizing: border-box; }
    body { margin: 0; font: 17px/1.45 system-ui, sans-serif; color: var(--ink); background: var(--paper); }
    main { max-width: 32rem; margin: 0 auto; padding: 20px 16px 48px; }
    h1 { font-size: 1.4rem; line-height: 1.2; margin: 0; }
    h2 { font-size: 1.1rem; margin: 28px 0 8px; }
    .from { margin: 2px 0 20px; color: var(--soft); }
    .steps { display: flex; gap: 0; list-style: none; margin: 0 0 8px; padding: 0; }
    .steps li { flex: 1; height: 18px; position: relative; }
    .steps li::before { content: ""; position: absolute; left: 0; top: 3px; width: 12px; height: 12px; border: 2px solid var(--brand); border-radius: 50%; background: var(--paper); }
    .steps li::after { content: ""; position: absolute; left: 14px; right: 0; top: 8px; border-top: 2px solid var(--line); }
    .steps li:last-child { flex: 0 0 14px; }
    .steps li:last-child::after { display: none; }
    .steps .done::before { background: var(--brand); }
    .status { display: flex; align-items: baseline; gap: 12px; margin: 16px 0 4px; font-size: 1.6rem; font-weight: 700; }
    .status .times { font-variant-numeric: tabular-nums; }
    .help { margin: 4px 0 12px; font-size: 0.9rem; color: var(--soft); }
    .actions { display: flex; gap: 12px; margin: 20px 0 4px; }
    button { width: 48px; height: 48px; padding: 0; color: var(--brand); background: var(--paper); border: 2px solid var(--brand); border-radius: 10px; }
    button svg { width: 24px; height: 24px; }
    button:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; }
    .updates { list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--line); }
    .updates li { display: flex; gap: 14px; padding: 10px 0; border-bottom: 1px solid var(--line); }
    .updates time { flex: 0 0 3.2em; color: var(--soft); font-variant-numeric: tabular-nums; }
  </style>
</head>
<body>
  <main>
    <h1>Parcel KC-48213</h1>
    <p class="from">From Fernhill Books</p>
    <ol class="steps">
      <li class="done"></li>
      <li class="done"></li>
      <li class="done"></li>
      <li></li>
    </ol>
$circles    <p class="status"><span class="code">OFD</span><span class="times">14:20 (16:00)</span></p>
$code$times    <div class="actions">
      <button type="button" aria-label="Change delivery instructions"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M13.5 6.5l4 4"/></svg></button>
      <button type="button" aria-label="Turn on notifications"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 17V11a6 6 0 0 1 12 0v6l2 2H4l2-2z"/><path d="M10 21h4"/></svg></button>
    </div>
$icons    <h2>Updates</h2>
$list    <ul class="updates">
      <li><time>07:42</time><span>Loaded onto van 14</span></li>
      <li><time>05:10</time><span>Arrived at Leeds depot</span></li>
      <li><time>22:31</time><span>Left Coventry hub</span></li>
      <li><time>18:05</time><span>Arrived at Coventry hub</span></li>
      <li><time>14:50</time><span>Collected from Fernhill Books</span></li>
    </ul>
  </main>
</body>
</html>
EOF
}
# One added sentence as its slot's value: the line and the newline that ends it.
help() { printf -v "$1" '    <p class="help">%s</p>\n' "$2"; }
page '' '' '' '' '' > pages/track.html
git add -A
git commit -qm 'Tracking page'
if [ "$variant" = retested ]; then
  circles='Filled circles are finished steps; the hollow one is still to come.'
  code='OFD means out for delivery today.'
  times='The first time is when we expect to arrive; the one in brackets is the latest.'
  icons='The pencil changes your delivery instructions; the bell tells you when the driver is close.'
  list="Newest first; times before midnight are yesterday's."
else
  circles='The filled circles show the steps your parcel has completed, and the hollow circle is the step still to come.'
  code='OFD means your parcel is out for delivery with a driver today.'
  times='The first time is when we expect to arrive, and the time in brackets is the latest it could be.'
  icons='Use the pencil to change your delivery instructions, and the bell to get a message when the driver is close.'
  list='The newest update is at the top of this list, and the times before midnight are from yesterday.'
fi
help circles "$circles"
help code "$code"
help times "$times"
help icons "$icons"
help list "$list"
page "$circles" "$code" "$times" "$icons" "$list" > pages/track.html
cat > docs/review-round-1.md <<'EOF'
# Design review, round 1: pages/track.html

## Findings

1. People will not understand the row of circles. Nothing says what they stand for or which one
   the parcel has reached.
2. People will not understand "OFD".
3. People will not understand "14:20 (16:00)". Two times, and no word on either.
4. People will not understand the pencil button and the bell button.
5. People will not understand the updates list: which end is newest, and which day each time
   belongs to.

## How each was answered

Commit "Answer the round 1 findings":

1. A line under the circles says what the filled and hollow circles mean.
2. A line under the status says what OFD means.
3. A line under the times says which time is which.
4. A line under the buttons says what the pencil and the bell do.
5. A line above the list says the newest update is first and which times are yesterday's.
EOF
if [ "$variant" = retested ]; then
  cat >> docs/review-round-1.md <<'EOF'

## Re-test

After that commit we showed the page to six customers at the Leeds counter. Each read it on our
tablet and then told us what the circles, "OFD", the two times, the two buttons and the order of
the list meant. All six got all five right, so we count the five findings as closed.
EOF
fi
git add -A
git commit -qm 'Answer the round 1 findings'
