#!/usr/bin/env bash
set -euo pipefail
mkdir -p src tests
cat > README.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed.

    python -m shelfnote checkout --member ana --book "Middlemarch"
    python -m shelfnote return --book "Middlemarch"
    python -m shelfnote overdue
    python -m shelfnote export --format csv
EOF
cat > src/shelfnote.py <<'EOF'
import argparse, json, pathlib, sys
DATA = pathlib.Path("data/loans.json")
def load():
    return json.loads(DATA.read_text()) if DATA.exists() else []
def main(argv=None):
    p = argparse.ArgumentParser(prog="shelfnote")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("checkout"); c.add_argument("--member"); c.add_argument("--book")
    r = sub.add_parser("return"); r.add_argument("--book")
    sub.add_parser("overdue")
    e = sub.add_parser("export"); e.add_argument("--format", choices=["csv", "json"])
    args = p.parse_args(argv)
    print(args.cmd)
if __name__ == "__main__":
    main()
EOF

git init -q . && git remote add origin https://example.com/club/shelfnote.git
if [ -n "$(ls -A "$HOME/.manifest-dev/logs" 2>/dev/null)" ]; then
  echo "HOME already holds workflow logs; run this scaffold with a scratch HOME" >&2
  exit 1
fi
mkdir -p "$HOME/.manifest-dev/logs"
cat > "$HOME/.manifest-dev/logs/figure-out-log-20260901-101500.md" <<'EOF'
# figure-out: overdue reminders by text message

Repository: https://example.com/club/shelfnote.git

## 2026-09-01T10:30Z — Ruling

**Ruling (user):** reminders never go out on weekends; clubs meet on weekends and members complained.
**Evidence:** two member complaints forwarded by the organizer.
**Out of scope:** push notifications — members don't install apps.
**Dead end:** batching all reminders into one nightly email was tried and rejected: members missed them.
EOF
cat > "$HOME/.manifest-dev/logs/figure-out-log-20260905-090000.md" <<'EOF'
# figure-out: reminder timing

Repository: https://example.com/school/library-desk.git

## 2026-09-05T09:10Z — Ruling

**Ruling (user):** reminders always go out at 7am sharp, including weekends.
EOF
