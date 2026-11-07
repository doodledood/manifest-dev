#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture"/app/. .
git branch -M main
git config user.name 'Courier fixture'
git config user.email 'courier@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Courier service'
