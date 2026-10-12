#!/usr/bin/env bash
set -euo pipefail
mkdir -p cardpress/cardpress
cat > cardpress/cardpress/__init__.py <<'EOF'
EOF
cat > cardpress/cardpress/layout.py <<'EOF'
CARD_WIDTH_MM = 127
CARD_HEIGHT_MM = 76


def layout(recipe: dict) -> list[str]:
    lines = [recipe["title"].upper()]
    lines += recipe["ingredients"]
    lines += recipe["steps"]
    return lines
EOF
cat > cardpress/README.md <<'EOF'
# cardpress

Prints recipe cards (5x3 inch) from saved recipes. `python -m pytest` runs the tests.
EOF
cat > manifest.md <<'EOF'
# Definition: Long recipes print on two cards instead of being cut off

## 1. Intent
- **Problem:** A recipe with more than about 14 lines is cut off at the bottom of the card, so
  cooks lose the last steps.
- **Appetite:** Changes to `cardpress/layout.py` and its tests only.

## 3. Global Invariants

### INV-G1 — Tests pass

Run `python -m pytest` in `cardpress`. PASS when it exits 0.

Deterministic gate.

## 6. Deliverables

### Deliverable 1: Overflow continues on a second card

#### AC-1.1 — Nothing is cut off

Done when a 30-line recipe lays out across two cards with every line present, in order, and the
second card repeats the title marked "(cont.)".

Judgment gate.
EOF
