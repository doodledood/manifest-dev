#!/usr/bin/env bash
# Presswork on main: a print shop's job system whose principles skills are the architecture and
# code starter sets, read from this checkout or, with STARTER_SETS_AT=<revision>, from that
# revision, so two drives can differ in the sets alone. A print job takes one paper stock; a
# customer profile carries preferences that the quote cache keys on. The base the review-code
# widen scenarios branch from, and the project the setup-project widen-plan scenario plans in.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
git init -q
git branch -M main
git config user.name 'Rosa Lindqvist'
git config user.email 'rosa@presswork.example'
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p .claude/skills/architecture-principles .claude/skills/code-principles docs/decisions src/presswork tests

sets=claude-plugins/manifest-dev/skills/setup-project/references/starter-principles
starter_set() {
  if [ -n "${STARTER_SETS_AT:-}" ]; then
    git -C "$DRIVE_CHECKOUT" show "$STARTER_SETS_AT:$sets/$1.md"
  else
    cat "$DRIVE_CHECKOUT/$sets/$1.md"
  fi
}
# The lines a project of this kind takes as written: the set's plain lines. Conditional lines and
# choices are left out, since their conditions and sides are the setup's call, not the fixture's.
plain_lines() {
  starter_set "$1" | awk '/^## Lines/ { body = 1; next } body && /^- / && !/^- Only where/ && !/^- Choice —/'
}
skill() {
  local area=$1 title=$2
  {
    printf -- "---\nname: %s-principles\ndescription: '%s principles for Presswork: how its people want %s work done, and why. Use before planning, designing, building or reviewing %s work in this project.'\n---\n\n" "$area" "$title" "$area" "$area"
    printf 'Edit rule: each line is a principle with its reason and when it yields. Decisions go to the\ndecision records, rules a check can hold go to the check, and a line is added only on a person'"'"'s\nyes, after sharpening an existing line is ruled out.\n\n'
    plain_lines "$area"
    printf '\nBefore calling %s work done, check it against these principles from a fresh start — a new\nsession, or a reviewer who did not do the work. Fix what departs unless the person chose the\ndeparture, and check again only after a fix, until a check finds none. Name each departure kept,\nwith the principle and why.\n' "$area"
  } > ".claude/skills/$area-principles/SKILL.md"
}
skill architecture Architecture
skill code Code

cat > CLAUDE.md <<'EOF'
# Presswork

Presswork runs the print shop's orders: a customer orders a job, the shop quotes it, reserves
paper, and plans the press run. Run the tests with `python3 -m pytest -q`.

## Project surfaces

- **CONTEXT.md** — what words mean here.
- **docs/decisions/** — why decisions went the way they did.
- **Architecture work** — load the `architecture-principles` skill (`.claude/skills/architecture-principles/SKILL.md`) before planning, designing, building or reviewing it.
- **Code work** — load the `code-principles` skill (`.claude/skills/code-principles/SKILL.md`) before planning, designing, building or reviewing it.
EOF
ln -s CLAUDE.md AGENTS.md

cat > CONTEXT.md <<'EOF'
# Presswork

The print shop's order system.

## Language

**Job**:
One order to print one document: its pages, copies, stock and finish.

**Stock**:
The paper a job is printed on, named by its catalogue code, such as `uncoated-90` or `card-300`.

**Kind**:
What a job's sheets become: `flat` sheets, or a `booklet` folded and stapled from them.

**Finish**:
The ink coating the press applies as it prints, matte or gloss.
_Avoid_: lamination, which is a film a separate machine adds after printing and is not a finish.

**Customer profile**:
A customer's account and the preferences they set once for all their jobs.
EOF

cat > docs/decisions/0001-finish-is-the-press-coating.md <<'EOF'
# 0001: Finish is the press coating

Status: Accepted
Decided by: Rosa Lindqvist (shop owner)

A job's `finish` names the coating the press lays down while it prints, and the press prices it
per sheet. Anything done to the printed sheets afterwards, on another machine, is not a finish:
it has its own setup cost and its own queue.
EOF

cat > src/presswork/__init__.py <<'EOF'
EOF
cat > src/presswork/catalogue.py <<'EOF'
"""The paper the shop stocks, with its price per sheet in cents."""

STOCKS = {
    "uncoated-90": 4,
    "silk-130": 7,
    "card-300": 15,
}


def price_per_sheet(stock: str) -> int:
    return STOCKS[stock]
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
    kind: str = "flat"
    proof: bool = False

    def sheets(self) -> int:
        """Sheets of stock the job uses: two pages per sheet, printed on both sides."""
        return -(-self.pages // 2) * self.copies
EOF
cat > src/presswork/customers.py <<'EOF'
"""Customer profiles and the preferences a customer sets once for all their jobs."""
import hashlib
import json
from dataclasses import dataclass, field


@dataclass
class Customer:
    customer_id: str
    name: str
    preferences: dict[str, str] = field(default_factory=dict)

    def profile_hash(self) -> str:
        """Changes whenever a preference changes; caches keyed on it go stale with the profile."""
        encoded = json.dumps(self.preferences, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()[:12]


CUSTOMERS: dict[str, Customer] = {}


def get(customer_id: str) -> Customer:
    return CUSTOMERS[customer_id]
EOF
cat > src/presswork/pricing.py <<'EOF'
"""Quotes a job, caching each quote by the customer's profile and the job's paper and size."""
from presswork import catalogue, customers
from presswork.jobs import Job

FINISH_PER_SHEET = {"matte": 1, "gloss": 2}
_cache: dict[tuple[str, str, int, int, str], int] = {}


def quote(job: Job) -> int:
    customer = customers.get(job.customer_id)
    key = (customer.profile_hash(), job.stock, job.pages, job.copies, job.finish)
    if key not in _cache:
        sheets = job.sheets()
        _cache[key] = sheets * (catalogue.price_per_sheet(job.stock) + FINISH_PER_SHEET[job.finish])
    return _cache[key]
EOF
cat > src/presswork/inventory.py <<'EOF'
"""Reserves the paper a job needs before it is printed."""
from presswork.jobs import Job

on_hand: dict[str, int] = {"uncoated-90": 20000, "silk-130": 8000, "card-300": 3000}
reserved: dict[str, int] = {}


def reserve(job: Job) -> None:
    sheets = job.sheets()
    if on_hand.get(job.stock, 0) - reserved.get(job.stock, 0) < sheets:
        raise ValueError(f"not enough {job.stock} for job {job.job_id}")
    reserved[job.stock] = reserved.get(job.stock, 0) + sheets
EOF
cat > src/presswork/press.py <<'EOF'
"""Plans the press run for a job: which stock to load and how many sheets."""
from dataclasses import dataclass

from presswork.jobs import Job


@dataclass(frozen=True)
class Run:
    stock: str
    sheets: int
    finish: str


def plan_run(job: Job) -> list[Run]:
    return [Run(job.stock, job.sheets(), job.finish)]
EOF
cat > tests/conftest.py <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
EOF
cat > tests/test_jobs.py <<'EOF'
from presswork import customers, inventory, press, pricing
from presswork.customers import Customer
from presswork.jobs import Job

JOB = Job("j1", "c1", pages=8, copies=10, stock="silk-130")


def setup_function() -> None:
    customers.CUSTOMERS["c1"] = Customer("c1", "Harbour Choir")
    pricing._cache.clear()
    inventory.reserved.clear()


def test_quote_prices_sheets_of_the_job_stock() -> None:
    assert pricing.quote(JOB) == 320


def test_reserve_takes_the_job_stock() -> None:
    inventory.reserve(JOB)
    assert inventory.reserved == {"silk-130": 40}


def test_plan_run_loads_the_job_stock() -> None:
    assert press.plan_run(JOB) == [press.Run("silk-130", 40, "matte")]
EOF
git add -A
git commit -qm 'Presswork: quotes, paper reservations and press runs'
