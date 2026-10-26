#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr notes data
cat > docs/adr/20260212-shelfnote-stays-a-command-line-tool.md <<'EOF'
# ADR: Shelfnote stays a command-line tool, with no web interface

## Status
Accepted

## Area
Interface

## Decided by
The user

## Context
Shelfnote runs on volunteers' own laptops. A web interface would need a server: someone to keep
it running and patched, and a monthly hosting cost the club has no budget for. Volunteers come
and go; nobody can promise to look after a server.

## Decision
Shelfnote is a command-line tool only. No web interface.

## Alternatives Considered
- **A hosted web app.** Rejected: monthly cost, and a server nobody can promise to maintain.
- **A desktop app.** Rejected: more to build than the club needs.

## Consequences
- Nothing to host or patch.
- Only volunteers with the tool can see the loans.

## Source
- Club committee, February 2026.
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-02-12 | [Shelfnote stays a command-line tool, with no web interface](20260212-shelfnote-stays-a-command-line-tool.md) | Accepted | Interface |
EOF
cat > notes/volunteers.md <<'EOF'
Volunteer notes, October 2026.

About 25 messages a month ask "is <book> on the shelf?" before a meeting. Two volunteers answer
them by running `shelfnote list --available` and pasting the result into the club chat.

Loans live in data/loans.json. The club already has a free page on the library's community
site, which hosts static files the club uploads.
EOF
echo '{"loans": []}' > data/loans.json
