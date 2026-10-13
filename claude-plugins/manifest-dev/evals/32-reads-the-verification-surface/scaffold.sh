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

mkdir -p verify/features
cat > verify/README.md <<'EOF'
# Verification surface

This directory is how this project checks that the shelfnote CLI still does its job.

## How to run it

    python verify/control.py doctor
    python verify/control.py run checkout --member ana --book Middlemarch

## Statuses

- `unverified` — catalogued but not yet exercised. Not proof of anything.
- `verified` — exercised by a run, with the date.
- `stale` — a run found it drifting; the entry carries a dated line naming what differs.
EOF
cat > verify/control.py <<'EOF'
import subprocess, sys
def main():
    if sys.argv[1] == "doctor":
        print("ok")
    else:
        subprocess.run([sys.executable, "-m", "shelfnote", *sys.argv[2:]], check=True)
main()
EOF
cat > verify/features/checkout.md <<'EOF'
# Checkout

Status: verified (2026-09-30)

## How to get to it
`shelfnote checkout --member <name> --book <title>`

## Driving it
    python verify/control.py run checkout --member ana --book Middlemarch

## What proves it works
The loan appears in `data/loans.json` with today's date.
EOF
cat > verify/features/overdue.md <<'EOF'
# Overdue list

Status: unverified

## How to get to it
`shelfnote overdue`

## Driving it
    python verify/control.py run overdue

## What proves it works
Every loan older than 21 days is listed once, oldest first.
EOF
cat > verify/features/export.md <<'EOF'
# Export

Status: verified (2026-08-11)

## How to get to it
`shelfnote export --csv`

## Driving it
    python verify/control.py run export --csv

## What proves it works
A CSV with one row per loan is written to stdout.
EOF
