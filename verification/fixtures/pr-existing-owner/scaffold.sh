#!/usr/bin/env bash
# Two local pull request snapshots of Branchline for review-pr's judgment pass: parallel/ adds a
# second store and nightly job that capture the full item records the visit log was decided to
# keep, with its own design note and Accepted record; ordinary/ adds an opening-hours module that
# no existing code owns.
set -euo pipefail
cat > .gitignore <<'IGNORE'
/parallel/
/ordinary/
IGNORE
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
pr_json() {
  TITLE=$1 DESCRIPTION=$2 python3 -B - <<'INNER'
import json
import os
import subprocess
from pathlib import Path

rev = lambda ref: subprocess.check_output(["git", "rev-parse", ref], text=True).strip()
Path("pr.json").write_text(json.dumps({
    "title": os.environ["TITLE"],
    "description": os.environ["DESCRIPTION"],
    "comments": [], "threads": [], "reviews": [], "linked_prs": [],
    "mode": "no-manifest", "base": rev("main"), "head": rev("HEAD"),
}, indent=2) + "\n")
INNER
}
mkdir -p parallel ordinary
(
  cd parallel
  git init -q
  bash "$fixture/base.sh"
  git switch -qc feature/checkout-snapshots
  git config user.name 'Priya Nair'
  git config user.email 'priya@branchline.example'
  mkdir -p src/branchline/snapshots docs/design
  cat > src/branchline/snapshots/__init__.py <<'EOF'
EOF
  cat > src/branchline/snapshots/store.py <<'EOF'
"""Checkout snapshots: the full item record as it was on the day of each checkout."""
from datetime import date

SNAPSHOTS: list[dict] = []


def save(day: date, rows: list[dict]) -> None:
    SNAPSHOTS.extend({"day": day, **row} for row in rows)


def for_month(year: int, month: int) -> list[dict]:
    return [row for row in SNAPSHOTS if row["day"].year == year and row["day"].month == month]
EOF
  cat > src/branchline/snapshots/job.py <<'EOF'
"""Nightly job: copy the day's checkouts with their full catalog records into the snapshot store."""
from datetime import date

from branchline import visit_log
from branchline.catalog import item
from branchline.snapshots import store


def run(day: date) -> int:
    rows = [
        {"age_band": entry["age_band"], **item(entry["id"])}
        for entry in visit_log.LOG
        if entry["at"].date() == day
    ]
    store.save(day, rows)
    return len(rows)
EOF
  cat > src/branchline/age_report.py <<'EOF'
"""Monthly checkouts by format and age band, read from the checkout snapshots."""
from collections import Counter

from branchline.snapshots import store


def by_format_and_age(year: int, month: int) -> Counter:
    return Counter((row["format"], row["age_band"]) for row in store.for_month(year, month))
EOF
  cat > tests/test_snapshots.py <<'EOF'
from datetime import date, datetime

from branchline import catalog, visit_log
from branchline.age_report import by_format_and_age
from branchline.snapshots import job


def test_report_counts_the_format_on_the_day_of_checkout():
    catalog.CATALOG["b1"] = {"id": "b1", "title": "Dune", "format": "paperback", "branch": "east"}
    visit_log.record_checkout("b1", "18-25", datetime(2026, 3, 1, 10))
    assert job.run(date(2026, 3, 1)) == 1
    catalog.CATALOG["b1"]["format"] = "ebook"
    assert by_format_and_age(2026, 3) == {("paperback", "18-25"): 1}
EOF
  cat > docs/design/checkout-snapshots.md <<'EOF'
# Checkout snapshots

The monthly age report needs each checkout's format as it was on the day. The visit log keeps only
item ids, and the catalog changes, so the report cannot rebuild it. A nightly job copies the day's
checkouts with their catalog records into a snapshot store, and the report reads from there. The
visit log stays as it is, so checkout writes at the desk stay fast.
EOF
  cat > docs/decisions/0002-checkout-snapshots-for-reports.md <<'EOF'
# 0002: Reports read checkout snapshots

Status: Accepted
Decided by: Priya Nair (author of this change)

Reports that need item details read the checkout snapshot store, filled nightly. We keep the visit
log id-only for desk speed.
EOF
  git add -A
  git commit -qm 'Add checkout snapshots for the monthly age report'
  pr_json "Add checkout snapshots for the monthly age report" \
    "The age report needs formats as they were on the day of checkout. A nightly job saves snapshots and the report reads them. Design note and decision 0002 included."
)
(
  cd ordinary
  git init -q
  bash "$fixture/base.sh"
  git switch -qc feature/opening-hours
  git config user.name 'Priya Nair'
  git config user.email 'priya@branchline.example'
  cat > src/branchline/opening_hours.py <<'EOF'
"""Opening hours for a branch on a given day: weekdays 9-18, Saturdays 10-14, closed Sundays."""
from datetime import date, time

HOURS = {5: (time(10), time(14)), 6: None}


def hours_on(day: date) -> tuple[time, time] | None:
    return HOURS.get(day.weekday(), (time(9), time(18)))
EOF
  cat > tests/test_opening_hours.py <<'EOF'
from datetime import date, time

from branchline.opening_hours import hours_on


def test_saturday_is_short_and_sunday_is_closed():
    assert hours_on(date(2026, 3, 7)) == (time(10), time(14))
    assert hours_on(date(2026, 3, 8)) is None
    assert hours_on(date(2026, 3, 9)) == (time(9), time(18))
EOF
  git add -A
  git commit -qm 'Add opening hours for the website footer'
  pr_json "Add opening hours" \
    "The website footer needs each day's opening hours. This adds a small module that answers them."
)
