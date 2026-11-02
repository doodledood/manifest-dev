#!/usr/bin/env bash
# A small studio-booking app: the booking sheet a person meets before paying, and the step its Pay
# button leads to. The sheet's promise is false only for someone who follows it to that step.
set -euo pipefail
mkdir -p src/booking src/checkout docs
cat > NORTH_STAR.md <<'EOF'
# North Star — Stretchday

## Purpose

People who work long days can book a yoga or pilates class in the gap between meetings, from
their phone, in under a minute, and trust what they booked.

For: office workers aged 25–50 who book one to three classes a week, usually on the same day.
— hypothesis 2026-09
EOF
cat > src/booking/BookingSheet.html <<'EOF'
<!-- The sheet that slides up when a person taps "Book" on a class. Paying books the place. -->
<section class="booking-sheet">
  <h2>Vinyasa Flow · Today 18:30 · 60 min</h2>
  <p class="teacher">with Ines · Studio 2, Harbour Street</p>
  <p class="price">£14.00</p>
  <p class="reassurance">Book in one tap — no account needed.</p>
  <aside class="gift-banner">
    <strong>Gift this class to a friend</strong>
    <span>Send it by message — they pay nothing.</span>
    <button class="secondary">Gift it</button>
  </aside>
  <button class="primary" data-next="/checkout/details">Pay £14.00 and book</button>
</section>
EOF
cat > src/checkout/Details.html <<'EOF'
<!-- Shown after "Pay £14.00 and book" to anyone not signed in. Payment opens once this is done. -->
<section class="details">
  <h2>Create your Stretchday account</h2>
  <label>Full name <input name="name" required></label>
  <label>Email <input name="email" type="email" required></label>
  <label>Password <input name="password" type="password" minlength="10" required></label>
  <label>Date of birth <input name="dob" type="date" required></label>
  <label>How did you hear about us? <select name="source" required><option></option><option>Friend</option><option>Instagram</option><option>Walked past</option></select></label>
  <button class="primary">Create account and continue to payment</button>
</section>
EOF
cat > docs/analytics-notes.md <<'EOF'
# Booking sheet, last 90 days

- Sheet opened: 41,200. Paid: 30,900.
- "Gift it" tapped: 160.
- Most bookings are made on the day of the class, 2 to 6 hours before it starts.
- 7 in 10 people who open the sheet are not signed in.
EOF
