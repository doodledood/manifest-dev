#!/usr/bin/env bash
set -euo pipefail
# Each subject owns its history; keep the outer drive from staging them as gitlinks.
cat > .gitignore <<'IGNORE'
/exception/
/speculation/
/missing/
/manifest/
IGNORE
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
for name in exception speculation missing; do
  mkdir -p "$name"
  cp "$fixture/$name/"* "$name/"
  (
    cd "$name"
    git init -q
    git branch -M main
    git config user.name 'Review fixture'
    git config user.email 'review@example.invalid'
    git config commit.gpgsign false
    git config core.hooksPath /dev/null
    cp base.py application.py
    git add application.py
    if [[ -f README.md ]]; then git add README.md; fi
    git commit -qm 'Baseline'
    git switch -qc feature/change
    cp head.py application.py
    git add application.py
    git commit -qm 'Requested change'
  )
done
mkdir -p manifest
(
  cd manifest
  git init -q
  bash "$fixture/../pr-judgment/scaffold.sh"
)
cp "$fixture/manifest.md" manifest/manifest.md
