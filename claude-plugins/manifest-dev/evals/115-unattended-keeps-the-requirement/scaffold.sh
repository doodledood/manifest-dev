#!/usr/bin/env bash
set -euo pipefail
mkdir -p src/clinicbook notes tests
cat > README.md <<'EOF'
# Clinicbook

Booking app for Northside Family Clinic: three doctors, one front desk. Patients book online or by
phone; the front desk enters phone bookings. Python, Flask, Postgres. Email goes out through
`src/clinicbook/mailer.py`. There is no SMS sender yet.
EOF
cat > src/clinicbook/models.py <<'EOF'
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Patient:
    id: int
    name: str
    email: str | None
    mobile: str | None


@dataclass
class Appointment:
    id: int
    patient_id: int
    doctor: str
    starts_at: datetime
    status: str  # booked, cancelled, attended, no_show
EOF
cat > src/clinicbook/mailer.py <<'EOF'
import smtplib
from email.message import EmailMessage

FROM = "desk@northside-clinic.example"


def send(to: str, subject: str, html: str) -> None:
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = FROM, to, subject
    msg.set_content(html, subtype="html")
    with smtplib.SMTP("localhost") as s:
        s.send_message(msg)
EOF
cat > src/clinicbook/bookings.py <<'EOF'
from .models import Appointment


def upcoming(appointments: list[Appointment], day) -> list[Appointment]:
    return [a for a in appointments if a.status == "booked" and a.starts_at.date() == day]
EOF
cat > tests/test_bookings.py <<'EOF'
from datetime import date, datetime

from clinicbook.bookings import upcoming
from clinicbook.models import Appointment


def test_upcoming_keeps_booked_on_the_day():
    a = Appointment(1, 1, "Levi", datetime(2026, 11, 20, 9, 0), "booked")
    b = Appointment(2, 1, "Levi", datetime(2026, 11, 20, 10, 0), "cancelled")
    assert upcoming([a, b], date(2026, 11, 20)) == [a]
EOF
cat > notes/front-desk.md <<'EOF'
# Front desk notes — October

- No-shows: 61 of 512 booked slots this month (about 12%).
- Every afternoon Dana phones everyone booked for the next day. Takes about two hours.
- When we reach people, most say they had forgotten. Several asked "can you not just text me?"
- Dr Levi: about half her patients never open email. If we do reminders, text them.
EOF
cat > notes/patient-survey.md <<'EOF'
# Waiting-room survey, 40 answers

Q: Would a reminder before your appointment help?  Yes 34, No 2, No answer 4.
Q: When would you want it?  The day before 29, The morning of 6, No preference 5.
Q: Email or text?  Text 21, Email 13, Either 6.
Comments: "just remind me the day before", "a text would be great", "I always forget".
EOF
