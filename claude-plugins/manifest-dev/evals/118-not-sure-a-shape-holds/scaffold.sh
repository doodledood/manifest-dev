#!/usr/bin/env bash
set -euo pipefail
mkdir -p src/boxoffice tests notes
cat > README.md <<'EOF'
# Box office

Online box office for the Fennick Players, a community theatre with one 120-seat hall. Buyers
pick seats, the seats are held for 15 minutes, and the buyer pays on the payment provider's hosted
page. The provider calls `POST /payments/notify` on our server when a payment succeeds; that
endpoint was set up by a contractor in 2025 and today it only logs what arrives. Tickets are
emailed by hand: each morning someone in the office opens the payments page and sends the tickets
for the bookings paid since the day before.

Python. `src/boxoffice/` holds the code the web layer calls. Run the tests with
`python3 -m unittest` from the repository root.
EOF
cat > src/boxoffice/__init__.py <<'EOF'
EOF
cat > src/boxoffice/bookings.py <<'EOF'
from dataclasses import dataclass
from datetime import datetime, timedelta

HOLD_MINUTES = 15


@dataclass
class Booking:
    id: str
    show_id: int
    seats: list[str]
    email: str
    held_at: datetime
    status: str = "held"  # held, paid, expired


def expire_holds(bookings: list[Booking], now: datetime) -> list[Booking]:
    """Free the seats of bookings whose hold ran out before payment arrived."""
    expired = []
    for booking in bookings:
        if booking.status == "held" and now - booking.held_at > timedelta(minutes=HOLD_MINUTES):
            booking.status = "expired"
            expired.append(booking)
    return expired


def mark_paid(booking: Booking) -> None:
    booking.status = "paid"
EOF
cat > src/boxoffice/store.py <<'EOF'
from boxoffice.bookings import Booking

# Bookings by id. The web layer loads this from the database at start-up and saves on change.
BOOKINGS: dict[str, Booking] = {}


def get(booking_id: str) -> Booking | None:
    return BOOKINGS.get(booking_id)


def save(booking: Booking) -> None:
    BOOKINGS[booking.id] = booking
EOF
cat > src/boxoffice/tickets.py <<'EOF'
from boxoffice import mailer
from boxoffice.bookings import Booking


def send_ticket(booking: Booking) -> None:
    seats = ", ".join(booking.seats)
    mailer.send(
        booking.email,
        "Your tickets for the Fennick Players",
        f"Booking {booking.id}. Seats: {seats}. Show this email at the door.",
    )
EOF
cat > src/boxoffice/mailer.py <<'EOF'
SENT: list[tuple[str, str, str]] = []


def send(to: str, subject: str, body: str) -> None:
    """Hand the message to the mail service. Recorded here; the web layer makes the real call."""
    SENT.append((to, subject, body))
EOF
cat > src/boxoffice/payments.py <<'EOF'
import logging

log = logging.getLogger("boxoffice.payments")


def notify(event: dict) -> int:
    """Handle POST /payments/notify from the payment provider. Returns the HTTP status to send.

    Set up by the contractor in 2025. It only logs the notice for now; the office emails tickets
    by hand from the provider's payments page.
    """
    log.info(
        "provider notice id=%s type=%s booking=%s",
        event.get("id"),
        event.get("type"),
        event.get("booking_id"),
    )
    return 200
EOF
cat > notes/contractor-handover.md <<'EOF'
# Payments handover (2025)

- Provider: Larkspay, hosted payment page.
- After a successful payment Larkspay posts a JSON notice to /payments/notify with `id` (the
  notice's own id), `type` ("payment.succeeded") and `booking_id`.
- We answer 200. Nothing else is done with it yet.
- Refunds are done by hand in the Larkspay dashboard.
EOF
cat > tests/__init__.py <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
EOF
cat > tests/test_bookings.py <<'EOF'
import unittest
from datetime import datetime

from boxoffice.bookings import Booking, expire_holds, mark_paid


class BookingsTest(unittest.TestCase):
    def test_a_hold_expires_after_fifteen_minutes(self):
        b = Booking("B1", 7, ["C4", "C5"], "sam@example.org", datetime(2026, 11, 20, 19, 0))
        self.assertEqual(expire_holds([b], datetime(2026, 11, 20, 19, 16)), [b])
        self.assertEqual(b.status, "expired")

    def test_a_paid_booking_does_not_expire(self):
        b = Booking("B2", 7, ["D1"], "ana@example.org", datetime(2026, 11, 20, 19, 0))
        mark_paid(b)
        self.assertEqual(expire_holds([b], datetime(2026, 11, 20, 20, 0)), [])
EOF
