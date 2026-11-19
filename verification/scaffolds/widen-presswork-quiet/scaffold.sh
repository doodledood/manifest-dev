#!/usr/bin/env bash
# Presswork with a change on feature/finishing that adds two named concepts where widening an
# existing one would be wrong. Quiet hours: a shop setting for when the press may not run, which
# nothing existing schedules. Lamination: a job setting beside `finish`, which looks close, but the
# glossary and decision 0001 say a finish is the press coating and lamination is a later machine
# step; the change's record says why it does not widen `finish`. The review-code recipe's
# widen-quiet scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../widen-presswork/scaffold.sh"
git switch -qc feature/finishing
git config user.name 'Theo Marchetti'
git config user.email 'theo@presswork.example'
mkdir -p config

cat > config/shop.toml <<'EOF'
# Hours when the press may not run: the building shares a wall with flats.
quiet_hours = { start = 22, end = 7 }
EOF

cat > src/presswork/shop.py <<'EOF'
"""Shop-wide settings read from config/shop.toml."""
import tomllib
from pathlib import Path

_CONFIG = Path(__file__).resolve().parents[2] / "config" / "shop.toml"


def quiet_hours() -> tuple[int, int]:
    hours = tomllib.loads(_CONFIG.read_text())["quiet_hours"]
    return hours["start"], hours["end"]


def press_may_run(hour: int) -> bool:
    start, end = quiet_hours()
    return not (hour >= start or hour < end)
EOF

cat > src/presswork/jobs.py <<'EOF'
"""A print job: one document, printed on one stock."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    job_id: str
    customer_id: str
    pages: int
    copies: int
    stock: str
    finish: str = "matte"
    proof: bool = False
    laminate: bool = False

    def sheets(self) -> int:
        """Sheets of stock the job uses: two pages per sheet, printed on both sides."""
        return -(-self.pages // 2) * self.copies
EOF

cat > src/presswork/lamination.py <<'EOF'
"""Lamination: a film the laminator adds to printed sheets after the press run."""
from presswork.jobs import Job

SETUP_CENTS = 500
PER_SHEET_CENTS = 3


def cost(job: Job) -> int:
    if not job.laminate:
        return 0
    return SETUP_CENTS + PER_SHEET_CENTS * job.sheets()
EOF

cat > src/presswork/pricing.py <<'EOF'
"""Quotes a job, caching each quote by the customer's profile and the job's paper and size."""
from presswork import catalogue, customers, lamination
from presswork.jobs import Job

FINISH_PER_SHEET = {"matte": 1, "gloss": 2}
_cache: dict[tuple[str, str, int, int, str, bool], int] = {}


def quote(job: Job) -> int:
    customer = customers.get(job.customer_id)
    key = (customer.profile_hash(), job.stock, job.pages, job.copies, job.finish, job.laminate)
    if key not in _cache:
        sheets = job.sheets()
        printing = sheets * (catalogue.price_per_sheet(job.stock) + FINISH_PER_SHEET[job.finish])
        _cache[key] = printing + lamination.cost(job)
    return _cache[key]
EOF

cat > src/presswork/press.py <<'EOF'
"""Plans the press run for a job: which stock to load and how many sheets."""
from dataclasses import dataclass

from presswork import shop
from presswork.jobs import Job


@dataclass(frozen=True)
class Run:
    stock: str
    sheets: int
    finish: str


def plan_run(job: Job) -> list[Run]:
    return [Run(job.stock, job.sheets(), job.finish)]


def can_start(hour: int) -> bool:
    """Whether a run may start at this hour of the day."""
    return shop.press_may_run(hour)
EOF

cat > tests/test_finishing.py <<'EOF'
from presswork import customers, press, pricing
from presswork.customers import Customer
from presswork.jobs import Job


def setup_function() -> None:
    customers.CUSTOMERS["c3"] = Customer("c3", "Northside Bakery")
    pricing._cache.clear()


def test_lamination_adds_setup_and_a_cost_per_sheet() -> None:
    menu = Job("j4", "c3", pages=2, copies=50, stock="card-300", laminate=True)
    assert pricing.quote(menu) == 50 * 16 + 500 + 3 * 50


def test_lamination_leaves_the_finish_as_ordered() -> None:
    menu = Job("j5", "c3", pages=2, copies=50, stock="card-300", finish="gloss", laminate=True)
    assert press.plan_run(menu) == [press.Run("card-300", 50, "gloss")]


def test_the_press_does_not_start_in_quiet_hours() -> None:
    assert press.can_start(9)
    assert not press.can_start(23)
    assert not press.can_start(6)
EOF

cat >> CONTEXT.md <<'EOF'

**Lamination**:
A film the laminator adds to a job's printed sheets after the press run, with its own setup cost.

**Quiet hours**:
The hours of the day when the press may not run.
EOF

cat > docs/decisions/0002-lamination-and-quiet-hours.md <<'EOF'
# 0002: Lamination is its own job setting, and quiet hours a shop setting

Status: Accepted
Decided by: Rosa Lindqvist (shop owner)

## Context
Bakeries order laminated menus, and the neighbours asked that the press stop at night.

## Decision
- A job takes `laminate`, a yes or no, priced by the laminator: a setup cost and a cost per sheet.
  `finish` stays the press coating, as decision 0001 says: a laminated menu still has a matte or
  gloss coat under the film, so a "laminated" value of `finish` would lose the coat and price a
  laminator setup per press sheet.
- The shop takes `quiet_hours` in `config/shop.toml`, read by the press before a run starts.
  Nothing in Presswork schedules the press today, so there is nothing to extend.

## Alternatives considered
- A `laminated` value of `finish`: rejected above.
- Quiet hours hard-coded in the press module: the hours change with the lease.
EOF

git add -A
git commit -qm 'Add lamination and quiet hours'
