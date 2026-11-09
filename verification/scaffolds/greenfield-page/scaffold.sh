#!/usr/bin/env bash
# A new project with one web page and no history beyond its first commit: the setup-project
# recipe's greenfield-principles scenario.
set -euo pipefail
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
mkdir -p site
cat > README.md <<'EOF'
# Tidepool

A one-page site where a neighbourhood swimming club posts this week's pool times and closures.
Open `site/index.html` in a browser.
EOF
cat > site/index.html <<'EOF'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Tidepool</title></head>
<body><h1>This week at the pool</h1><ul id="times"><li>Mon 07:00–09:00 lanes</li></ul></body></html>
EOF
git -c user.name="Lee Okafor" -c user.email=lee@tidepool.example add -A
git -c user.name="Lee Okafor" -c user.email=lee@tidepool.example commit -qm "feat: first page"
