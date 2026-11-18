#!/usr/bin/env bash
# Hearth, a co-op's room-booking web app with no project surfaces, whose history states reasons:
# a review note that only restates a general rule about empty states, a fix whose reason is the
# project's own about naming figures, a reason no general line covers (one-column forms), and a
# kept replaced form that conflicts with a general rule about deleting what a change leaves
# unused: the setup-project recipe's starter-from-history scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
commit() { git -c user.name="Ama Boateng" -c user.email=ama@hearth.example add -A && git -c user.name="Ama Boateng" -c user.email=ama@hearth.example commit -q "$@"; }
mkdir -p src/hearth/templates docs/reviews tests
cat > README.md <<'EOF'
# Hearth

Web app where members of a housing co-op book its shared rooms: the laundry, the guest room and
the workshop. Run `python3 -m hearth`; test with `python3 -m pytest tests/`.
EOF
cat > src/hearth/__init__.py <<'EOF'
EOF
cat > src/hearth/rooms.py <<'EOF'
"""Rooms and their bookings."""
ROOMS = {"laundry": [], "guest": [], "workshop": []}


def free_rooms(day: str) -> list[str]:
    return [name for name, booked in ROOMS.items() if day not in booked]
EOF
cat > src/hearth/templates/today.html <<'EOF'
<main><h1>Today</h1><p>Rooms: {{ rooms|length }}</p><table>{% for b in bookings %}<tr><td>{{ b }}</td></tr>{% endfor %}</table></main>
EOF
cat > src/hearth/templates/book.html <<'EOF'
<form class="two-columns"><label>Room <select name="room"></select></label><label>Day <input name="day"></label><button>Book</button></form>
EOF
cat > tests/test_rooms.py <<'EOF'
from hearth.rooms import free_rooms


def test_all_rooms_free_on_an_empty_day():
    assert free_rooms("2026-05-01") == ["laundry", "guest", "workshop"]
EOF
commit -m "feat: book shared rooms"
cat > docs/reviews/2026-03-today-page.md <<'EOF'
# Review notes: today page

- Never leave an empty list blank; say there is nothing and why.
EOF
commit -m "docs: review notes on the today page"
sed -i.bak 's|<p>Rooms: {{ rooms\|length }}</p>|<p>Free rooms: {{ rooms\|length }}</p>|' src/hearth/templates/today.html && rm -f src/hearth/templates/today.html.bak
commit -m "fix: label the count as free rooms" -m "'Rooms: 3' left members guessing whether three rooms were free or booked, and two members booked the same guest room on the strength of it."
sed -i.bak 's/class="two-columns"/class="one-column"/' src/hearth/templates/book.html && rm -f src/hearth/templates/book.html.bak
commit -m "feat: booking form in one column" -m "Members book from their phones while standing in the laundry room; the two-column form wrapped badly and hid the Book button."
cat > src/hearth/templates/book_v2.html <<'EOF'
<form class="one-column"><label>Room <select name="room"></select></label><label>Day <input type="date" name="day"></label><button>Book</button></form>
EOF
mkdir -p src/hearth/templates/legacy && git mv src/hearth/templates/book.html src/hearth/templates/legacy/book.html
commit -m "feat: new booking form; keep the old one under legacy/" -m "The office prints the old form as a paper fallback when the building's wifi is down, so it stays under templates/legacy/ instead of being deleted."
