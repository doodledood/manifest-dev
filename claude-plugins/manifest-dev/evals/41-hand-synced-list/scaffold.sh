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

mkdir -p docs
sed -i.bak 's/choices=\["csv", "json"\]/choices=["csv"], help="Export format: csv (see docs\/formats.md)"/' src/shelfnote.py && rm -f src/shelfnote.py.bak
cat > docs/formats.md <<'EOF'
# Export formats

| Format | Flag |
|--------|------|
| csv | `--format csv` |
EOF
cat > src/formats.py <<'EOF'
EXPORTERS = {"csv": lambda loans: "\n".join(",".join(map(str, l.values())) for l in loans)}
EOF
