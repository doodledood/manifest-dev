#!/usr/bin/env bash
# Two local pull request snapshots of Pantry, a static shopping-list page, for review-pr. page/
# adds a "Clear list" button beside Save in the card's header; at a phone's width the header row
# no longer fits, and the card's unchanged clipping hides Save entirely, a defect only the page
# rendered at that width shows. docs/ changes only Markdown documents.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
cat > .gitignore <<'IGNORE'
/page/
/docs/
IGNORE
base() {
  git init -q -b main
  git config user.name 'Noor Haddad'
  git config user.email 'noor@pantry.example'
  mkdir -p site docs
  cat > README.md <<'EOF'
# Pantry

A static page for keeping one shopping list in the browser. Open `site/index.html`.
EOF
  cat > docs/usage.md <<'EOF'
# Using Pantry

Type an item and press Enter to add it. Press **Save** to keep the list in this browser.
EOF
  cat > site/index.html <<'EOF'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pantry</title><link rel="stylesheet" href="style.css"></head>
<body>
<section class="card">
  <header class="card-head"><h2>Shopping list</h2><button class="save" type="button">Save</button></header>
  <input class="add" placeholder="Add an item" aria-label="Add an item">
  <ul class="items"><li>Oats</li><li>Lemons</li><li>Rice</li></ul>
</section>
<script src="app.js"></script>
</body></html>
EOF
  cat > site/style.css <<'EOF'
body { font: 16px/1.4 system-ui, sans-serif; margin: 24px; color: #222; }
.card { max-width: 420px; padding: 16px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; }
.card-head { display: flex; align-items: center; gap: 8px; }
.card-head h2 { margin: 0 auto 0 0; font-size: 20px; white-space: nowrap; }
.save { padding: 8px 14px; font-size: 15px; }
.add { width: 100%; margin: 12px 0; padding: 8px; box-sizing: border-box; }
EOF
  cat > site/app.js <<'EOF'
const items = document.querySelector('.items');
document.querySelector('.add').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.target.value.trim()) {
    const li = document.createElement('li');
    li.textContent = e.target.value.trim();
    items.append(li);
    e.target.value = '';
  }
});
document.querySelector('.save').addEventListener('click', () => {
  localStorage.setItem('pantry', items.innerHTML);
});
EOF
  git add -A && git commit -qm "feat: one shopping list with save"
}
pr() {
  local title=$1 description=$2
  git add -A && git commit -qm "$title"
  TITLE=$title DESCRIPTION=$description python3 -B - <<'INNER'
import json, os, subprocess
from pathlib import Path
rev = lambda ref: subprocess.check_output(["git", "rev-parse", ref], text=True).strip()
Path("pr.json").write_text(json.dumps({
    "title": os.environ["TITLE"], "description": os.environ["DESCRIPTION"],
    "comments": [], "threads": [], "reviews": [], "linked_prs": [],
    "mode": "no-manifest", "base": rev("main"), "head": rev("HEAD"),
}, indent=2) + "\n")
INNER
}
mkdir page docs
(
  cd page && base && git switch -qc feature/clear-list
  sed -i.bak 's|<button class="save" type="button">Save</button>|<button class="clear" type="button">Clear list</button><button class="save" type="button">Save</button>|' site/index.html && rm -f site/index.html.bak
  cat >> site/style.css <<'EOF'
.clear { min-width: 170px; padding: 8px 14px; font-size: 15px; background: #fff; border: 1px solid #b00; color: #b00; }
.save { flex-shrink: 0; }
EOF
  cat >> site/app.js <<'EOF'
document.querySelector('.clear').addEventListener('click', () => {
  items.innerHTML = '';
  localStorage.removeItem('pantry');
});
EOF
  pr "Add a Clear list button" "People asked for a quick way to start a new list. This adds a Clear list button beside Save that empties the list and forgets the saved copy."
)
(
  cd docs && base && git switch -qc docs/saving
  cat >> docs/usage.md <<'EOF'

The list is kept in this browser only: another browser or device starts empty.
EOF
  sed -i.bak 's|Open `site/index.html`.|Open `site/index.html`; `docs/usage.md` says how saving works.|' README.md && rm -f README.md.bak
  pr "Say where a saved list lives" "Two people asked why their list was missing on their phone. The docs now say a list is kept in one browser only."
)
