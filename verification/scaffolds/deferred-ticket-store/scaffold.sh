#!/usr/bin/env bash
# A Shelfnote project whose file store holds deferred Tickets and whose North Star lists strategy
# choices with signposts: one ready Ticket, and one deferred Ticket and one strategy signpost each
# whose source shows its condition met, shows it unmet, or cannot be read. The next-ticket and
# orchestrate recipes' deferred scenarios.
set -euo pipefail
mkdir -p tickets/club docs/adr signals src
cat > CLAUDE.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed. Read `NORTH_STAR.md` at the start
of every session. Tickets live in `tickets/`.
EOF
cat > tickets/store-config.md <<'EOF'
Venue: files. Tickets live under `tickets/<effort>/`.
EOF
cat > tickets/club/README.md <<'EOF'
# Effort: club

Destination: an organizer runs a club's lending from Shelfnote alone, with nothing kept on paper.
EOF
cat > tickets/club/01-overdue-reminder-text.md <<'EOF'
Kind: shaped
Status: open
Depends on:
Claimed by:

# Print the member's name in the overdue list

## Why
The overdue list prints book titles only, so the organizer still looks up who has each book.

## Definition of done
`python3 src/shelfnote.py overdue` prints each overdue book with the member who has it.
EOF
cat > tickets/club/02-member-recommendations.md <<'EOF'
Kind: shaped
Status: open
Depends on:
Revisit when: three or more clubs ask to record who recommended a book — read `signals/requests.md`
Claimed by:

# Record who recommended each book

## Why
Clubs want to thank the member who suggested a book. Worth building once enough clubs ask.

## Definition of done
A checkout can name the recommending member, and `export` includes that name.
EOF
cat > tickets/club/03-reading-stats.md <<'EOF'
Kind: shaped
Status: open
Depends on:
Revisit when: ten or more clubs use the tool — read `signals/clubs.md`
Claimed by:

# Show each club its reading statistics

## Why
A yearly summary of books read. Only worth it once enough clubs use the tool to ask for it.

## Definition of done
`python3 src/shelfnote.py stats` prints books lent and returned per month for the past year.
EOF
cat > tickets/club/04-email-reminders.md <<'EOF'
Kind: shaped
Status: open
Depends on:
Revisit when: more than half the clubs' organizers open the monthly digest — read the mailing provider's campaign dashboard
Claimed by:

# Email overdue reminders

## Why
Organizers could stop chasing loans by hand, if they read email from the tool at all.

## Definition of done
An overdue loan sends its member one reminder email a week until the book is returned.
EOF
cat > signals/requests.md <<'EOF'
# Requests to record who recommended a book

- Northside readers, 2026-08-02
- Riverside club, 2026-09-14
- Elm Street book circle, 2026-10-03
EOF
cat > signals/clubs.md <<'EOF'
# Clubs using Shelfnote

4 clubs, as of 2026-10-01.
EOF
cat > signals/website-visits.md <<'EOF'
# Visits to the release-notes page

September 2026: 140 visits, 31 from outside the library network.
EOF
cat > NORTH_STAR.md <<'EOF'
# North Star — Shelfnote

## Purpose

Every book a club lends finds its way back, and running the club stays a pleasure for the
volunteer who organizes it. In the way: clubs lose track of who has which book.

For: volunteer organizers of small reading clubs.
Not for: libraries with a catalogue system of their own.

— hypothesis: from the README. 2026-05

## Goal

An organizer knows, at any moment, where every club book is.

— hypothesis: 2026-05

## Principles

- It never asks a member for anything but a name.

— ruled: 2026-05

## How we know

— empty: nothing is counted yet. What would fill it: a measure the owner picks. 2026-05

## What this rests on

— empty: no bet stated. What would fill it: the owner's main bet. 2026-05

## Open

None yet.

## Strategy choices in force

- New releases reach clubs through the library network's newsletter, not a website — revisit when: more than twenty visits a month to the release-notes page come from outside the library network, read in `signals/website-visits.md`
- Loans are kept on the organizer's own machine, never on a server — revisit when: a club asks to share one loan list between two organizers, read in `signals/requests.md`
- Organizers learn of releases from one note a month — revisit when: fewer than a third of organizers open the monthly note, read on the mailing provider's campaign dashboard
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-06-01 | [New releases reach clubs through the library network's newsletter, not a website](20260601-releases-through-the-newsletter.md) | Accepted | Strategy |
| 2026-06-02 | [Loans are kept on the organizer's own machine, never on a server](20260602-loans-stay-local.md) | Accepted | Strategy |
| 2026-06-03 | [Organizers learn of releases from one note a month](20260603-one-note-a-month.md) | Accepted | Strategy |
EOF
for spec in \
  "20260601-releases-through-the-newsletter|New releases reach clubs through the library network's newsletter, not a website|more than twenty visits a month to the release-notes page come from outside the library network, read in \`signals/website-visits.md\`" \
  "20260602-loans-stay-local|Loans are kept on the organizer's own machine, never on a server|a club asks to share one loan list between two organizers, read in \`signals/requests.md\`" \
  "20260603-one-note-a-month|Organizers learn of releases from one note a month|fewer than a third of organizers open the monthly note, read on the mailing provider's campaign dashboard"; do
  IFS='|' read -r file title revisit <<<"$spec"
  cat > "docs/adr/$file.md" <<EOF
# ADR: $title

## Status
Accepted

## Area
Strategy

## Context
A guiding choice for how Shelfnote reaches and serves clubs.

## Decision
$title.

## Alternatives Considered
- **The opposite choice**: more upkeep for a volunteer.

## Consequences
### Positive
- Less for a volunteer to keep running.
### Negative
- Some clubs are served less well.

## Enforced by
none — a guiding choice no check can hold.

## Revisit when
$revisit

## Source
- Session: (none)
EOF
done
cat > src/shelfnote.py <<'EOF'
import sys
print(sys.argv[1:] or "usage: shelfnote <command>")
EOF
