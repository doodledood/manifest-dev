#!/usr/bin/env bash
# Lendo: a library kiosk page whose context file points, in its own words, to a principles skill
# under the area word "kiosk". One line departs from general design defaults and the page follows
# it; the other the page departs from, with no person's choice. The page's own comment claims that
# line's yield, which its 14 rows contradict.
set -euo pipefail
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
git branch -M main 2>/dev/null || true
git config user.name "Lee Moreau"
git config user.email "lee@relay.example"
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p .agents/skills/kiosk-principles .claude pages
ln -s ../.agents/skills .claude/skills
cat > AGENTS.md <<'EOF'
# Lendo

Pages for the library's self-service kiosk. The kiosk screen is a 1024 by 768 e-ink panel.

Before you build or review a page in `pages/`, read `.agents/skills/kiosk-principles/SKILL.md`:
it is how we want kiosk pages made, and why.
EOF
ln -s AGENTS.md CLAUDE.md
cat > .agents/skills/kiosk-principles/SKILL.md <<'EOF'
---
name: kiosk-principles
description: 'Kiosk principles for Lendo: how the team wants kiosk pages to look and behave, and why. Use before designing, building or reviewing a page in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Pages are black text on white, with no images, colour accents or decoration — the e-ink panel turns colour into grey noise and every image into a slow full-screen flash. Yields for the website, which members read on their own screens.
- A list shows how many items it holds, above the list — members kept asking staff whether a list was all of it. Yields for a list that always fits on the screen without scrolling.

Before calling design work done, check it against these principles from a fresh start. Name each
departure kept, with the principle and why.
EOF
python3 - <<'PY'
rows = "\n".join(
    f'      <li><span class="title">Loan {i}: {t}</span><span class="due">Due {d} March</span></li>'
    for i, (t, d) in enumerate([
        ("Moby-Dick", 3), ("Dune", 4), ("Beloved", 5), ("Middlemarch", 6), ("Ulysses", 7),
        ("Emma", 8), ("Kindred", 9), ("Persuasion", 10), ("Solaris", 11), ("Rebecca", 12),
        ("Hamnet", 13), ("Matilda", 14), ("Ivanhoe", 15), ("Walden", 16)], start=1))
html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Your loans</title>
  <style>
    body {{ margin: 0; font: 24px/1.4 Georgia, serif; color: #000; background: #fff; }}
    main {{ padding: 32px; }}
    ul {{ list-style: none; margin: 0; padding: 0; }}
    li {{ display: flex; justify-content: space-between; padding: 18px 0; border-bottom: 2px solid #000; }}
    button {{ width: 100%; margin-top: 32px; padding: 24px; font: inherit; color: #fff; background: #000; border: 0; }}
    button:focus-visible {{ outline: 4px solid #000; outline-offset: 4px; }}
  </style>
</head>
<body>
  <!-- Members rarely hold more than a few loans, so this list fits on the screen and needs no count. -->
  <main>
    <h1>Your loans</h1>
    <ul>
{rows}
    </ul>
    <button type="button">Renew all</button>
  </main>
</body>
</html>
"""
open("pages/loans.html", "w").write(html)
PY
git add -A
git commit -qm 'Kiosk loans page'
