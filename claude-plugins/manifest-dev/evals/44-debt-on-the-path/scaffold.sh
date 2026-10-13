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

cat > src/reminders.py <<'EOF'
def subject(line): return "Reminder for " + line.split(",")[1]
def body(line): return "Hello " + line.split(",")[1] + ", your book is due."
def footer(line): return "Sent to " + line.split(",")[1]
EOF
git init -q . && git remote add origin https://example.com/club/shelfnote.git
if [ -n "$(ls -A "$HOME/.manifest-dev/logs" 2>/dev/null)" ]; then
  echo "HOME already holds workflow logs; run this scaffold with a scratch HOME" >&2
  exit 1
fi
mkdir -p "$HOME/.manifest-dev/logs"
cat > "$HOME/.manifest-dev/logs/do-manifest-20260920-1a2b3c4d.md" <<'EOF'
# Execution log — manifest-20260920

Repository: https://example.com/club/shelfnote.git

## 2026-09-20T15:00Z — Debt left

- src/reminders.py: the member name is read by splitting the raw CSV line in subject, body
  and footer; one function should own it. Left: outside that change's scope.
EOF
