#!/usr/bin/env bash
# Hearth Rota: a volunteer sign-up page whose marks nobody labelled, in a project that accepted the
# shipped design starter set. Its design-principles skill holds the set's plain lines, each choice
# at its default side, and the lines offered where a surface responds to input; the line offered
# where a surface presents data is left out, since a sign-up list presents none. The set is read
# from this checkout or, with STARTER_SETS_AT=<revision>, from that revision, so two drives can
# differ in the set alone. A hallway test left six findings, each something volunteers did not
# understand and each one a label, a mark, an order or a position on the page could carry. The
# setup-project recipe's design-set-repair scenario asks an agent with none of this repository's
# plugins to repair them.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
. "$(dirname "${BASH_SOURCE[0]}")/../../../scripts/scaffold-playwright.sh"
link_playwright
git branch -M main
git config user.name 'Noor Haddad'
git config user.email 'noor@hearth.example'
git config commit.gpgsign false
git config core.hooksPath /dev/null
set_path=claude-plugins/manifest-dev/skills/setup-project/references/starter-principles/design.md
mkdir -p .claude/skills/design-principles docs pages
if [ -n "${STARTER_SETS_AT:-}" ]; then
  git -C "$DRIVE_CHECKOUT" show "$STARTER_SETS_AT:$set_path" > .starter-design.md
else
  cp "$DRIVE_CHECKOUT/$set_path" .starter-design.md
fi
python3 -B - .starter-design.md > .claude/skills/design-principles/SKILL.md <<'PY'
import sys
lines = open(sys.argv[1]).read().split("## Lines", 1)[1].splitlines()
input_condition = "- Only where a surface responds to input: "
out = []
for i, line in enumerate(lines):
    if line.startswith(input_condition):
        out.append("- " + line[len(input_condition):])
    elif line.startswith("- Only where "):
        pass  # The page presents no data, so that line's condition is not met here.
    elif line.startswith("- Choice — "):
        default = next(l for l in lines[i + 1:] if l.lstrip().startswith("- Default side: "))
        out.append("- " + default.split("- Default side: ", 1)[1])
    elif line.startswith("- "):
        out.append(line)
if len(out) < 8:
    sys.exit("scaffold: the design starter set gave too few lines")
print("""---
name: design-principles
description: 'Design principles for Hearth Rota: how its people want its pages designed, and why. Use before planning, designing, building or reviewing a page in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.
""")
print("\n".join(out))
print("""
Before calling design work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.""")
PY
rm .starter-design.md
cat > CLAUDE.md <<'EOF'
# Hearth Rota

The sign-up page for volunteer shifts at Hearth Community Kitchen. Volunteers open it on their
phones, about once a week, to see which shifts still need people and to put their name down.

## Project surfaces

- **Design work** — load the `design-principles` skill (`.claude/skills/design-principles/SKILL.md`) before planning, designing, building or reviewing a page in this project.
EOF
ln -s CLAUDE.md AGENTS.md
cat > package.json <<EOF
{
  "name": "hearth-rota",
  "private": true,
  "devDependencies": { "$playwright_module": "*" }
}
EOF
cat > docs/hallway-test.md <<'EOF'
# Hallway test: the shifts page

Eight volunteers, each on their own phone, none of whom had seen the page before. The note in
brackets is what the thing means.

1. Six did not understand the coloured dot beside each shift. (Amber: the shift still needs
   people. Green: it is full. Grey: sign-up has closed.)
2. Five did not understand "2/5". (Two of the shift's five places are taken.)
3. Seven did not understand how to sign up: three tapped the shift's day, and the others found no
   control they knew. (The "+" puts your name down for that shift.)
4. Five did not understand the letters K, F and D. (Kitchen, front of house, delivery.)
5. Four did not understand the greyed-out shift. (Sign-up for it has closed.)
6. Three did not understand the star. (It marks a shift the volunteer is already on.)
EOF
cat > pages/shifts.html <<'EOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shifts this week — Hearth Kitchen</title>
  <style>
    :root { --ink: #1d1b18; --soft: #5b564d; --paper: #fbf8f3; --line: #d9d2c5; --amber: #a85504; --green: #2e6b3a; --grey: #77726a; }
    * { box-sizing: border-box; }
    body { margin: 0; font: 17px/1.45 system-ui, sans-serif; color: var(--ink); background: var(--paper); }
    main { max-width: 34rem; margin: 0 auto; padding: 20px 16px 48px; }
    h1 { font-size: 1.5rem; line-height: 1.2; margin: 0 0 4px; }
    .week { margin: 0 0 16px; color: var(--soft); }
    ul { list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--line); }
    li { display: grid; grid-template-columns: 12px 1fr 1.5em 2.5em 1.2em 44px; align-items: center; gap: 10px; min-height: 64px; padding: 8px 0; border-bottom: 1px solid var(--line); }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .amber { background: var(--amber); }
    .green { background: var(--green); }
    .grey { background: var(--grey); }
    .when { font-weight: 600; }
    .when span { display: block; font-weight: 400; color: var(--soft); }
    .role { font-weight: 700; text-align: center; }
    .count { font-variant-numeric: tabular-nums; text-align: right; }
    .star { color: var(--amber); text-align: center; }
    .closed .when, .closed .when span, .closed .role, .closed .count { color: var(--grey); }
    button { width: 44px; height: 44px; font: inherit; font-size: 1.4rem; line-height: 1; color: var(--ink); background: #fff; border: 2px solid var(--ink); border-radius: 8px; }
    button:focus-visible { outline: 3px solid var(--amber); outline-offset: 2px; }
  </style>
</head>
<body>
  <main>
    <h1>Shifts this week</h1>
    <p class="week">9 to 14 March</p>
    <ul id="shifts">
      <li class="closed"><span class="dot grey"></span><span class="when">Mon 9 Mar<span>11:00 to 14:00</span></span><span class="role">K</span><span class="count">2/5</span><span></span><span></span></li>
      <li><span class="dot green"></span><span class="when">Mon 9 Mar<span>17:00 to 20:00</span></span><span class="role">K</span><span class="count">5/5</span><span></span><span></span></li>
      <li><span class="dot amber"></span><span class="when">Tue 10 Mar<span>11:00 to 14:00</span></span><span class="role">F</span><span class="count">2/5</span><span></span><button type="button">+</button></li>
      <li><span class="dot amber"></span><span class="when">Wed 11 Mar<span>17:00 to 20:00</span></span><span class="role">K</span><span class="count">3/5</span><span class="star">★</span><span></span></li>
      <li><span class="dot amber"></span><span class="when">Thu 12 Mar<span>11:00 to 14:00</span></span><span class="role">D</span><span class="count">1/3</span><span></span><button type="button">+</button></li>
      <li><span class="dot green"></span><span class="when">Fri 13 Mar<span>17:00 to 20:00</span></span><span class="role">F</span><span class="count">4/4</span><span class="star">★</span><span></span></li>
      <li><span class="dot amber"></span><span class="when">Sat 14 Mar<span>09:00 to 12:00</span></span><span class="role">D</span><span class="count">0/3</span><span></span><button type="button">+</button></li>
    </ul>
  </main>
  <script>
    // Signing up takes a place and marks the shift as one of the volunteer's own.
    document.getElementById("shifts").addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button) return;
      const row = button.closest("li");
      const count = row.querySelector(".count");
      const [taken, places] = count.textContent.split("/").map(Number);
      count.textContent = `${taken + 1}/${places}`;
      if (taken + 1 === places) row.querySelector(".dot").className = "dot green";
      row.children[4].className = "star";
      row.children[4].textContent = "★";
      button.remove();
    });
  </script>
</body>
</html>
EOF
git add -A
git commit -qm 'Shifts page, with the hallway test that found what volunteers did not understand'
