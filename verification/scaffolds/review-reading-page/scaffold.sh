#!/usr/bin/env bash
# Fernleaf Housing Co-op: a guide page members come to read, in a project with no principles skill.
# The text is what its reader came for. It holds a term most members meet here for the first time,
# glossed in one short line beside it, and an action that cannot be undone after seven days, whose
# consequence is stated before the button. The review-design recipe's reading scenario reviews it: a review that
# counts explaining sentences as a cost must still leave all three alone.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
. "$(dirname "${BASH_SOURCE[0]}")/../../../scripts/scaffold-playwright.sh"
link_playwright
git branch -M main
git config user.name 'Ines Moreau'
git config user.email 'ines@fernleaf.example'
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p pages
cat > AGENTS.md <<'EOF'
# Fernleaf Housing Co-op: members' guide

Guide pages for the co-op's members. A member opens `pages/leaving.html` when they are thinking
about moving out. They read it start to finish, usually at home and often on a phone, because the
decision costs them money and their room. Some then give notice from the page.

Open the page in a browser to see it. `package.json` lists Playwright for anything that renders it.
EOF
ln -s AGENTS.md CLAUDE.md
cat > package.json <<EOF
{
  "name": "fernleaf-guide",
  "private": true,
  "devDependencies": { "$playwright_module": "*" }
}
EOF
cat > pages/leaving.html <<'EOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Leaving the co-op — Fernleaf members' guide</title>
  <style>
    :root { --ink: #1c2420; --soft: #4e5a53; --paper: #fcfbf7; --line: #cfd6cf; --leaf: #1f6b45; --warn: #8a2c12; }
    * { box-sizing: border-box; }
    body { margin: 0; font: 18px/1.6 Georgia, "Times New Roman", serif; color: var(--ink); background: var(--paper); }
    main { max-width: 36rem; margin: 0 auto; padding: 28px 18px 64px; }
    .guide { margin: 0 0 6px; font: 600 0.85rem/1.3 system-ui, sans-serif; letter-spacing: 0.04em; text-transform: uppercase; color: var(--soft); }
    h1 { font-size: 2rem; line-height: 1.15; margin: 0 0 18px; }
    h2 { font-size: 1.25rem; line-height: 1.25; margin: 32px 0 8px; }
    p { margin: 0 0 16px; }
    .gloss { margin: -8px 0 16px; padding-left: 12px; border-left: 3px solid var(--leaf); font: 0.9rem/1.45 system-ui, sans-serif; color: var(--soft); }
    .notice { margin-top: 36px; padding: 18px; border: 2px solid var(--warn); border-radius: 10px; }
    .notice h2 { margin-top: 0; }
    .consequence { font: 600 1rem/1.45 system-ui, sans-serif; color: var(--warn); }
    button { min-height: 48px; padding: 10px 20px; font: 600 1rem/1.2 system-ui, sans-serif; color: #fff; background: var(--warn); border: 0; border-radius: 8px; }
    button:focus-visible { outline: 3px solid var(--ink); outline-offset: 3px; }
  </style>
</head>
<body>
  <main>
    <p class="guide">Members' guide</p>
    <h1>Leaving the co-op</h1>
    <p>You can leave Fernleaf at any time. It takes 28 days, and your money comes back in two parts.</p>

    <h2>How much notice you give</h2>
    <p>You give 28 days' notice. The 28 days start on the day we receive it, not on the first of the month. You pay rent until the last of those days, even if you move out sooner. If a new member moves into your room before the 28 days end, your rent stops on the day they move in.</p>

    <h2>What you get back</h2>
    <p>You get back your deposit and your share capital.</p>
    <p class="gloss"><dfn>Share capital</dfn> is the £150 you paid in when you joined.</p>
    <p>We return the deposit within 14 days of your last day, less the cost of any damage beyond ordinary wear. We go through the room with you before you leave, so you see the same list we do. Share capital comes back in full, but later: the members' meeting approves repayments once a quarter, so it can take up to three months.</p>

    <h2>What stays with the house</h2>
    <p>Anything bought from the house fund stays, including furniture you chose. Anything you bought yourself is yours to take. If you and the house shared the cost of something, the treasurer works out a fair buy-out with you before your last day.</p>

    <h2>If you change your mind</h2>
    <p>For the first 7 days after you give notice, you can withdraw it by telling any committee member. After that, your room belongs to the next person on the waiting list, and coming back means joining that list yourself. It is currently about eight months long.</p>

    <section class="notice" aria-labelledby="notice-heading">
      <h2 id="notice-heading">Give notice</h2>
      <p class="consequence">After 7 days you cannot take this back, and your room is offered to the waiting list.</p>
      <button type="button">Give 28 days' notice</button>
    </section>
  </main>
</body>
</html>
EOF
git add -A
git commit -qm 'Leaving the co-op guide page'
