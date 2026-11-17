#!/usr/bin/env bash
# A Shelfnote project with no surfaces: the setup-project recipe's app-project scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
mkdir -p src tests
cat > CLAUDE.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed. Run the tests with
`python3 -m pytest tests/`.
EOF
cat > README.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed.

    python3 src/shelfnote.py checkout --member ana --book "Middlemarch"
    python3 src/shelfnote.py return --book "Middlemarch"
    python3 src/shelfnote.py overdue
    python3 src/shelfnote.py export --format csv
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
cat > tests/test_cli.py <<'EOF'
import subprocess, sys

def run(*args):
    return subprocess.run([sys.executable, "src/shelfnote.py", *args], capture_output=True, text=True)

def test_overdue_runs():
    assert run("overdue").returncode == 0
EOF
