#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp "$fixture"/{subscription.py,billing.py} .
git branch -M main
git config user.name 'Subscription fixture'
git config user.email 'subscription@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Subscription lifecycle with one transition function'
git switch -qc feature/pause
cp "$fixture"/change/{subscription.py,billing.py} .
git add .
git commit -qm 'Let subscribers pause and resume'
