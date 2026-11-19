#!/usr/bin/env bash
# Presswork with a change on feature/cover-stock that meets a need the job's own stock input could
# take: booklets want their cover on another stock than their inner pages. The job takes one stock;
# the change does not let it take more. It adds a named setting on the customer profile instead,
# with its own service, a guard that keeps the setting off proof prints, a glossary term and a
# decision record whose alternatives never mention the job's input; it extends the customer profile.
# The change is otherwise sound: one function owns the sheet split, the setting is checked where it
# enters, the cache keys on what is priced, and planning re-reserves paper. The review-code recipe's
# widen-catch scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../widen-presswork/scaffold.sh"
git switch -qc feature/cover-stock
git config user.name 'Theo Marchetti'
git config user.email 'theo@presswork.example'

cat > src/presswork/cover_stock.py <<'EOF'
"""Booklet cover stock: the card a customer's booklet covers print on, set once in their profile.

A customer who sets it gets the cover sheet of every booklet they order (one per copy) on that
stock, and the inner pages on the job's stock. Flat jobs never use it. The guard: proofs never use
it either, since proofs run on the proof press, which takes one stock; the customer approves the
card from a sample.
"""
from presswork import catalogue, customers
from presswork.jobs import Job

SETTING = "booklet_cover_stock"


def set_cover_stock(customer_id: str, stock: str) -> None:
    if stock not in catalogue.STOCKS:
        raise ValueError(f"unknown stock {stock!r}; the catalogue holds {sorted(catalogue.STOCKS)}")
    customers.get(customer_id).preferences[SETTING] = stock


def sheets_by_stock(job: Job) -> list[tuple[str, int]]:
    """Each stock the job prints on, with its sheets. Pricing, inventory and the press read this."""
    cover = None
    if job.kind == "booklet" and not job.proof:
        cover = customers.get(job.customer_id).preferences.get(SETTING)
    if cover is None or cover == job.stock:
        return [(job.stock, job.sheets())]
    inner = job.sheets() - job.copies
    return [(cover, job.copies)] + ([(job.stock, inner)] if inner else [])
EOF

cat > src/presswork/pricing.py <<'EOF'
"""Quotes a job, caching each quote by the stocks and sheets it prints on and its finish."""
from presswork import catalogue, cover_stock
from presswork.jobs import Job

FINISH_PER_SHEET = {"matte": 1, "gloss": 2}
_cache: dict[tuple[tuple[tuple[str, int], ...], str], int] = {}


def quote(job: Job) -> int:
    # Keyed on what is priced, so any input of the stock split, the profile's cover stock
    # included, reaches the key without being listed here.
    needs = tuple(cover_stock.sheets_by_stock(job))
    key = (needs, job.finish)
    if key not in _cache:
        finish = FINISH_PER_SHEET[job.finish]
        _cache[key] = sum(sheets * (catalogue.price_per_sheet(stock) + finish) for stock, sheets in needs)
    return _cache[key]
EOF

cat > src/presswork/inventory.py <<'EOF'
"""Reserves the paper a job needs before it is printed; a job holds one reservation at a time."""
from presswork import cover_stock
from presswork.jobs import Job

on_hand: dict[str, int] = {"uncoated-90": 20000, "silk-130": 8000, "card-300": 3000}
reserved: dict[str, int] = {}
_held: dict[str, list[tuple[str, int]]] = {}


def reset() -> None:
    reserved.clear()
    _held.clear()


def release(job_id: str) -> None:
    for stock, sheets in _held.pop(job_id, []):
        reserved[stock] -= sheets
        if not reserved[stock]:
            del reserved[stock]


def reserve(job: Job) -> None:
    """Reserve what the job prints on now, replacing any reservation it held; on a shortage the
    old reservation stays."""
    needs = cover_stock.sheets_by_stock(job)
    held: dict[str, int] = {}
    for stock, sheets in _held.get(job.job_id, []):
        held[stock] = held.get(stock, 0) + sheets
    for stock, sheets in needs:
        if on_hand.get(stock, 0) - reserved.get(stock, 0) + held.get(stock, 0) < sheets:
            raise ValueError(f"not enough {stock} for job {job.job_id}")
    release(job.job_id)
    for stock, sheets in needs:
        reserved[stock] = reserved.get(stock, 0) + sheets
    _held[job.job_id] = needs
EOF

cat > src/presswork/press.py <<'EOF'
"""Plans the press run for a job: which stock to load and how many sheets."""
from dataclasses import dataclass

from presswork import cover_stock, inventory
from presswork.jobs import Job


@dataclass(frozen=True)
class Run:
    stock: str
    sheets: int
    finish: str


def plan_run(job: Job) -> list[Run]:
    """Plan the run and re-reserve its paper, so the reservation matches what will be loaded."""
    if not job.proof:
        inventory.reserve(job)
    return [Run(stock, sheets, job.finish) for stock, sheets in cover_stock.sheets_by_stock(job)]
EOF

cat > tests/test_cover_stock.py <<'EOF'
import pytest

from presswork import cover_stock, customers, inventory, press, pricing
from presswork.customers import Customer
from presswork.jobs import Job

BOOKLET = Job("j2", "c2", pages=8, copies=10, stock="silk-130", kind="booklet")


def setup_function() -> None:
    customers.CUSTOMERS["c2"] = Customer("c2", "Lantern Press Club")
    pricing._cache.clear()
    inventory.reset()


def test_without_the_setting_a_booklet_prints_on_its_stock() -> None:
    assert press.plan_run(BOOKLET) == [press.Run("silk-130", 40, "matte")]


def test_the_setting_prints_one_cover_sheet_per_copy_on_card() -> None:
    cover_stock.set_cover_stock("c2", "card-300")
    assert press.plan_run(BOOKLET) == [
        press.Run("card-300", 10, "matte"),
        press.Run("silk-130", 30, "matte"),
    ]


def test_the_setting_reserves_card_for_the_covers() -> None:
    cover_stock.set_cover_stock("c2", "card-300")
    inventory.reserve(BOOKLET)
    assert inventory.reserved == {"card-300": 10, "silk-130": 30}


def test_the_setting_changes_the_quote() -> None:
    assert pricing.quote(BOOKLET) == 320
    cover_stock.set_cover_stock("c2", "card-300")
    assert pricing.quote(BOOKLET) == 10 * 16 + 30 * 8


def test_flat_jobs_ignore_the_setting() -> None:
    cover_stock.set_cover_stock("c2", "card-300")
    flyer = Job("j3", "c2", pages=2, copies=100, stock="uncoated-90")
    assert press.plan_run(flyer) == [press.Run("uncoated-90", 100, "matte")]


def test_proofs_ignore_the_setting_and_are_quoted_apart() -> None:
    cover_stock.set_cover_stock("c2", "card-300")
    proof = Job("j4", "c2", pages=8, copies=10, stock="silk-130", kind="booklet", proof=True)
    assert press.plan_run(proof) == [press.Run("silk-130", 40, "matte")]
    assert pricing.quote(proof) == 320
    assert pricing.quote(BOOKLET) == 400


def test_a_changed_setting_moves_the_reservation_when_the_run_is_planned() -> None:
    cover_stock.set_cover_stock("c2", "card-300")
    inventory.reserve(BOOKLET)
    cover_stock.set_cover_stock("c2", "silk-130")
    press.plan_run(BOOKLET)
    assert inventory.reserved == {"silk-130": 40}


def test_a_cover_on_the_booklet_stock_is_one_run() -> None:
    cover_stock.set_cover_stock("c2", "silk-130")
    assert press.plan_run(BOOKLET) == [press.Run("silk-130", 40, "matte")]


def test_a_shortage_on_re_reserving_keeps_the_old_reservation() -> None:
    cover_stock.set_cover_stock("c2", "card-300")
    inventory.reserve(BOOKLET)
    inventory.on_hand["uncoated-90"], saved = 5, inventory.on_hand["uncoated-90"]
    try:
        cover_stock.set_cover_stock("c2", "uncoated-90")
        with pytest.raises(ValueError, match="uncoated-90"):
            inventory.reserve(BOOKLET)
        assert inventory.reserved == {"card-300": 10, "silk-130": 30}
    finally:
        inventory.on_hand["uncoated-90"] = saved


def test_an_unknown_stock_is_refused_where_it_is_set() -> None:
    with pytest.raises(ValueError, match="card300"):
        cover_stock.set_cover_stock("c2", "card300")
EOF

cat >> CONTEXT.md <<'EOF'

**Booklet cover stock**:
A customer profile setting naming the stock the covers of that customer's booklets print on, one sheet per copy; flat jobs and proofs ignore it.
EOF

cat > docs/decisions/0002-booklet-cover-stock.md <<'EOF'
# 0002: Booklet covers print on a cover stock set in the customer profile

Status: Accepted
Decided by: Theo Marchetti (author of this change)

## Context
Choirs and clubs order booklets all season and want every cover on the same card while the inner
pages stay on lighter paper. Today every sheet of a job prints on the job's stock.

## Decision
Add a booklet cover stock to the customer profile, the place a customer's standing choices
already live. A customer sets it once; every booklet they order prints its cover sheet on that
stock, and an open booklet follows a change to it until it prints, which is what a club changing
card mid-season wants. One function, `cover_stock.sheets_by_stock`, says which stocks a job uses
and is what pricing, inventory and the press read. A guard in it keeps the setting off proofs,
which run on the proof press with one stock. Planning a run re-reserves its paper, so a changed
setting moves the reservation with it. The quote cache keys on the stocks and sheets a job prints
on, so the setting reaches it with no new identity.

## Alternatives considered
- A note on the order that press operators read: nothing prices or reserves the card.
- A second job for the covers, linked to the booklet: two quotes, two reservations, and covers can
  print without their booklet.
- A shop-wide default cover stock: customers want different card.
- A customer flag that moves all their jobs to card: inner pages and flat jobs would print on card.
- A cover stock catalogue table that jobs look up by customer: a new table for one value per
  customer, which the profile already holds.
EOF

sed -i.bak 's/inventory.reserved.clear()/inventory.reset()/' tests/test_jobs.py && rm tests/test_jobs.py.bak

git add -A
git commit -qm 'Print booklet covers on a cover stock set in the customer profile'
