#!/usr/bin/env bash
set -euo pipefail
mkdir -p src/wallbook tests
cat > README.md <<'EOF'
# Wallbook

Class booking for Quillon Climbing Wall: beginner courses, technique classes and yoga for climbers.
Members book in the app; each class has a fixed number of places. Python, no framework yet; the
web layer calls `src/wallbook/classes.py`. Charges go through `src/wallbook/billing.py`.
Run the tests with `python3 -m unittest` from the repository root.
EOF
cat > src/wallbook/__init__.py <<'EOF'
EOF
cat > src/wallbook/billing.py <<'EOF'
CHARGES: list[tuple[int, int, str]] = []


def charge(member_id: int, pence: int, reason: str) -> None:
    """Charge the member's card on file. Recorded here; the real call is made by the web layer."""
    CHARGES.append((member_id, pence, reason))
EOF
cat > src/wallbook/classes.py <<'EOF'
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from wallbook import billing

LATE_CANCEL_HOURS = 12
LATE_CANCEL_FEE_PENCE = 500


class ClassFull(Exception):
    pass


@dataclass
class GymClass:
    id: int
    name: str
    starts_at: datetime
    capacity: int
    booked: list[int] = field(default_factory=list)  # member ids, in booking order


def book(gym_class: GymClass, member_id: int) -> None:
    if member_id in gym_class.booked:
        return
    if len(gym_class.booked) >= gym_class.capacity:
        raise ClassFull(gym_class.name)
    gym_class.booked.append(member_id)


def cancel(gym_class: GymClass, member_id: int, now: datetime) -> None:
    gym_class.booked.remove(member_id)
    if gym_class.starts_at - now < timedelta(hours=LATE_CANCEL_HOURS):
        billing.charge(member_id, LATE_CANCEL_FEE_PENCE, f"late cancel: {gym_class.name}")
EOF
cat > tests/__init__.py <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
EOF
cat > tests/test_classes.py <<'EOF'
import unittest
from datetime import datetime

from wallbook import billing
from wallbook.classes import ClassFull, GymClass, book, cancel


def make_class(capacity=2):
    return GymClass(1, "Lead technique", datetime(2026, 11, 21, 18, 0), capacity)


class ClassesTest(unittest.TestCase):
    def setUp(self):
        billing.CHARGES.clear()

    def test_full_class_refuses_a_booking(self):
        c = make_class(1)
        book(c, 10)
        with self.assertRaises(ClassFull):
            book(c, 11)

    def test_cancel_inside_twelve_hours_charges_the_fee(self):
        c = make_class()
        book(c, 10)
        cancel(c, 10, datetime(2026, 11, 21, 9, 0))
        self.assertEqual(billing.CHARGES, [(10, 500, "late cancel: Lead technique")])

    def test_cancel_a_day_ahead_is_free(self):
        c = make_class()
        book(c, 10)
        cancel(c, 10, datetime(2026, 11, 20, 9, 0))
        self.assertEqual(billing.CHARGES, [])
EOF
