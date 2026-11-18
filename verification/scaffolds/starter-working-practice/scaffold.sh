#!/usr/bin/env bash
# A small project that accepted the shipped working-practice starter set: its skill holds the
# set's lines, each choice at its default side, and its context file carries the pointer line
# setup writes. The setup-project recipe's working-practice-in-use scenario asks an agent with
# none of this repository's plugins for a small change here.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
set_file="$DRIVE_CHECKOUT/claude-plugins/manifest-dev/skills/setup-project/references/starter-principles/working-practice.md"
[ -f "$set_file" ] || { echo "no working-practice starter set at $set_file" >&2; exit 1; }
mkdir -p .claude/skills/working-practice-principles src tests
python3 -B - "$set_file" > .claude/skills/working-practice-principles/SKILL.md <<'PY'
import re, sys
text = open(sys.argv[1]).read()
lines = text.split("## Lines", 1)[1].splitlines()
out = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("- Only where "):
        out.append("- " + line.split(": ", 1)[1])
    elif line.startswith("- Choice — "):
        default = next(l for l in lines[i + 1:] if l.lstrip().startswith("- Default side: "))
        out.append("- " + default.split("- Default side: ", 1)[1])
    elif line.startswith("- "):
        out.append(line)
    i += 1
print("""---
name: working-practice-principles
description: 'Working-practice principles for Ledgerline: how its people want any change made, and why. Use before changing anything in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.
""")
print("\n".join(out))
print("""
Before calling a change done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.""")
PY
cat > CLAUDE.md <<'EOF'
# Ledgerline

Command-line tool that keeps a household's shared expenses in a CSV file.

## Project surfaces

- **Working practice** — load the `working-practice-principles` skill (`.claude/skills/working-practice-principles/SKILL.md`) before changing anything in this project.
EOF
cat > src/ledger.py <<'EOF'
"""Read the shared-expenses CSV and work out who owes what."""
import csv


def total(path: str) -> float:
    with open(path, newline="") as f:
        return sum(float(row["amount"]) for row in csv.DictReader(f))
EOF
cat > src/report.py <<'EOF'
from ledger import total


def report(path: str) -> str:
    return f"Spent so far: {total(path):.2f}"
EOF
cat > tests/test_ledger.py <<'EOF'
import sys
sys.path.insert(0, "src")
from ledger import total


def test_total(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text("who,amount\nana,2.50\nbo,1.50\n")
    assert total(str(f)) == 4.0
EOF
git -c user.name="Ravi Patel" -c user.email=ravi@ledgerline.example add -A
git -c user.name="Ravi Patel" -c user.email=ravi@ledgerline.example commit -qm "feat: totals and report"
