#!/usr/bin/env bash
# Presswork with a change on feature/cover-stock that meets a need the job's own stock input could
# take: booklets want their cover on another stock than their inner pages. The job takes one stock;
# the change does not let it take more. It adds a named setting on the customer profile instead,
# with its own service, a guard that keeps the setting off proof prints, a glossary term and a
# decision record whose alternatives never mention the job's input. Its caching rides the profile's
# existing hash. The review-code recipe's widen-catch scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../widen-presswork/scaffold.sh"
git switch -qc feature/cover-stock
git config user.name 'Theo Marchetti'
git config user.email 'theo@presswork.example'

cat > src/presswork/cover_stock.py <<'EOF'
"""Cover stock override: a customer profile setting that prints a booklet's cover on its own stock.

A customer who sets `cover_stock_override` gets the first sheet of each copy of every booklet
printed on that stock; the rest of the job stays on the job's stock. Proof prints never use it:
a proof shows the job exactly as ordered.
"""
from presswork import customers
from presswork.jobs import Job

SETTING = "cover_stock_override"


class CoverStockOnProof(Exception):
    """Raised when the override is asked for on a proof print."""


def guard_not_proof(job: Job) -> None:
    if job.proof:
        raise CoverStockOnProof(f"job {job.job_id} is a proof; proofs print as ordered")


def cover_stock_for(job: Job) -> str | None:
    """The cover stock this job's customer set, or None when they set none or the job is a proof."""
    if job.proof:
        return None
    return customers.get(job.customer_id).preferences.get(SETTING)


def cover_sheets(job: Job) -> int:
    """One cover sheet per copy, folded around the inner pages."""
    return job.copies


def set_override(customer_id: str, stock: str) -> None:
    customers.get(customer_id).preferences[SETTING] = stock
EOF

cat > src/presswork/pricing.py <<'EOF'
"""Quotes a job, caching each quote by the customer's profile and the job's paper and size."""
from presswork import catalogue, cover_stock, customers
from presswork.jobs import Job

FINISH_PER_SHEET = {"matte": 1, "gloss": 2}
_cache: dict[tuple[str, str, int, int, str], int] = {}


def quote(job: Job) -> int:
    customer = customers.get(job.customer_id)
    # The cover stock override lives in the profile's preferences, so the profile hash already
    # changes when it does: the existing cache identity covers it with no new key.
    key = (customer.profile_hash(), job.stock, job.pages, job.copies, job.finish)
    if key not in _cache:
        finish = FINISH_PER_SHEET[job.finish]
        cover = cover_stock.cover_stock_for(job)
        if cover is None:
            _cache[key] = job.sheets() * (catalogue.price_per_sheet(job.stock) + finish)
        else:
            covers = cover_stock.cover_sheets(job)
            inner = job.sheets() - covers
            _cache[key] = inner * (catalogue.price_per_sheet(job.stock) + finish) + covers * (
                catalogue.price_per_sheet(cover) + finish
            )
    return _cache[key]
EOF

cat > src/presswork/inventory.py <<'EOF'
"""Reserves the paper a job needs before it is printed."""
from presswork import cover_stock
from presswork.jobs import Job

on_hand: dict[str, int] = {"uncoated-90": 20000, "silk-130": 8000, "card-300": 3000}
reserved: dict[str, int] = {}


def _take(stock: str, sheets: int, job_id: str) -> None:
    if on_hand.get(stock, 0) - reserved.get(stock, 0) < sheets:
        raise ValueError(f"not enough {stock} for job {job_id}")
    reserved[stock] = reserved.get(stock, 0) + sheets


def reserve(job: Job) -> None:
    cover = cover_stock.cover_stock_for(job)
    if cover is None:
        _take(job.stock, job.sheets(), job.job_id)
        return
    covers = cover_stock.cover_sheets(job)
    _take(job.stock, job.sheets() - covers, job.job_id)
    _take(cover, covers, job.job_id)
EOF

cat > src/presswork/press.py <<'EOF'
"""Plans the press run for a job: which stock to load and how many sheets."""
from dataclasses import dataclass, replace

from presswork import cover_stock
from presswork.jobs import Job


@dataclass(frozen=True)
class Run:
    stock: str
    sheets: int
    finish: str


def plan_run(job: Job) -> list[Run]:
    cover = cover_stock.cover_stock_for(job)
    if cover is None:
        return [Run(job.stock, job.sheets(), job.finish)]
    covers = cover_stock.cover_sheets(job)
    return [Run(cover, covers, job.finish), Run(job.stock, job.sheets() - covers, job.finish)]


def plan_cover_run(job: Job) -> Run:
    """The cover run alone, for the operator who loads card first; never for a proof."""
    cover_stock.guard_not_proof(job)
    cover = cover_stock.cover_stock_for(replace(job, proof=False))
    if cover is None:
        raise ValueError(f"job {job.job_id} has no cover stock")
    return Run(cover, cover_stock.cover_sheets(job), job.finish)
EOF

cat > tests/test_cover_stock.py <<'EOF'
import pytest

from presswork import cover_stock, customers, inventory, press, pricing
from presswork.customers import Customer
from presswork.jobs import Job

BOOKLET = Job("j2", "c2", pages=8, copies=10, stock="silk-130")


def setup_function() -> None:
    customers.CUSTOMERS["c2"] = Customer("c2", "Lantern Press Club")
    pricing._cache.clear()
    inventory.reserved.clear()


def test_without_override_the_booklet_prints_on_its_stock() -> None:
    assert press.plan_run(BOOKLET) == [press.Run("silk-130", 40, "matte")]


def test_override_prints_one_cover_sheet_per_copy_on_card() -> None:
    cover_stock.set_override("c2", "card-300")
    assert press.plan_run(BOOKLET) == [
        press.Run("card-300", 10, "matte"),
        press.Run("silk-130", 30, "matte"),
    ]


def test_override_reserves_card_for_the_covers() -> None:
    cover_stock.set_override("c2", "card-300")
    inventory.reserve(BOOKLET)
    assert inventory.reserved == {"silk-130": 30, "card-300": 10}


def test_override_changes_the_quote() -> None:
    plain = pricing.quote(BOOKLET)
    cover_stock.set_override("c2", "card-300")
    assert pricing.quote(BOOKLET) == 30 * 8 + 10 * 16
    assert plain == 320


def test_a_proof_never_takes_the_override() -> None:
    cover_stock.set_override("c2", "card-300")
    proof = Job("j3", "c2", pages=8, copies=1, stock="silk-130", proof=True)
    assert press.plan_run(proof) == [press.Run("silk-130", 4, "matte")]
    with pytest.raises(cover_stock.CoverStockOnProof):
        press.plan_cover_run(proof)
EOF

cat >> CONTEXT.md <<'EOF'

**Cover stock override**:
A customer profile setting naming the stock a customer's booklet covers print on, one sheet per copy; proofs ignore it.
EOF

cat > docs/decisions/0002-cover-stock-override.md <<'EOF'
# 0002: Booklet covers print on a cover stock override set in the customer profile

Status: Accepted
Decided by: Theo Marchetti (author of this change)

## Context
Choirs and clubs order booklets and want the cover on card while the inner pages stay on lighter
paper. Today every sheet of a job prints on the job's stock.

## Decision
Add a cover stock override to the customer profile. A customer sets it once; every booklet they
order prints its first sheet per copy on that stock. A service, `cover_stock`, resolves it for
pricing, inventory and the press, and a guard keeps it off proof prints, which must show the job
as ordered. The quote cache needs no change: the override lives in the profile's preferences, so
the profile hash the cache already keys on changes with it.

## Alternatives considered
- A note on the order that press operators read: nothing prices or reserves the card.
- A second job for the covers, linked to the booklet: two quotes, two reservations, and the
  covers can be printed without their booklet.
- A shop-wide default cover stock: customers want different card.
- A customer flag that moves all their jobs to card: inner pages would print on card too.
- A cover stock catalogue table that jobs look up by customer: a new table for one value per
  customer, which the profile already holds.
EOF

git add -A
git commit -qm 'Print booklet covers on a cover stock override from the customer profile'
