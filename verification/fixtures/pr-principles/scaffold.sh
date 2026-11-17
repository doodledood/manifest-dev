#!/usr/bin/env bash
# Two local pull request snapshots of Shelfmark for review-pr: departs/ carries the change that
# departs from a principle with no person's choice behind it; holds/ carries the change whose
# touched principles are each followed, have a shown yield or a chosen departure, or cannot be shown
# by the change.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
cat > .gitignore <<'IGNORE'
/departs/
/holds/
IGNORE
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
scaffolds="$fixture/../../scaffolds"
snapshot() {
  local dir=$1 scaffold=$2 title=$3 description=$4
  mkdir -p "$dir"
  (
    cd "$dir"
    bash "$scaffolds/$scaffold/scaffold.sh"
    TITLE=$title DESCRIPTION=$description python3 -B - <<'INNER'
import json
import os
import subprocess
from pathlib import Path

rev = lambda ref: subprocess.check_output(["git", "rev-parse", ref], text=True).strip()
Path("pr.json").write_text(json.dumps({
    "title": os.environ["TITLE"],
    "description": os.environ["DESCRIPTION"],
    "comments": [],
    "threads": [],
    "reviews": [],
    "linked_prs": [],
    "mode": "no-manifest",
    "base": rev("main"),
    "head": rev("HEAD"),
}, indent=2) + "\n")
INNER
  )
}
snapshot departs principles-shelfmark-departs \
  "Add SMS overdue reminders for Central" \
  "Central asked for SMS reminders. This adds CentralBranchOverdueSms, guarded on the branch name so North and Harbor are untouched. Decision 0002 records why the narrow shape is intended. Tests: python3 -m pytest -q, 3 passed."
snapshot holds principles-shelfmark-holds \
  "Send a monthly loan statement to each member" \
  "Each member gets a monthly statement of their loans, oldest first, through their branch's channels, with the branch's return address from config. The long statement body is checked against a reviewed snapshot file; the greeting test checks the name only, per decision 0001. Tests: python3 -m pytest -q, 5 passed."
