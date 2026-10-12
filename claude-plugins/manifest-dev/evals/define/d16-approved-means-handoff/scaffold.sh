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

### INV-G1 — The change stops at what this Manifest authorized

Read this Manifest. This is a conformance check: take its intent as given, and do not judge
whether the work was necessary, motivated, or worthwhile.

Done when the work this run added carries nothing beyond what the Deliverables, Acceptance Criteria, and
Global Invariants — this one excluded — required, and nothing that nominally serves one of
them while far exceeding the surface the Appetite allows.

Read Problem, Appetite, and Out of bounds as the intent. Read the Deliverables and the other
gates as what the work owes. Read the Initial Approach and Process Guidance as mechanisms that
were *authorized rather than owed* — the ones expected, never the only ones permitted, so work
reaching a Deliverable by a route this Manifest does not name is required by that Deliverable.

Required although no criterion names it: work inherited rather than added — the artifact this
Manifest was synthesized over, and anything arriving from outside the run such as a base branch
merged into the head — and work discharging what a criterion required, including sweeping a
changed rule into every copy and surface that holds it.

FAIL only on work none of the above accounts for. Treat an unclear case as required work, and
leave small, incidental, or imperfect changes inside an artifact already in scope alone.

Why: every other gate states a floor, so a contract bounded on one side only gives an executor
disposed to thoroughness nothing to read as a limit.

Judgment gate.

### INV-G2 — Tests pass

Run `python -m pytest` in `cardpress`. PASS when it exits 0.

Deterministic gate.

## 6. Deliverables

### Deliverable 1: Overflow continues on a second card

#### AC-1.1 — Nothing is cut off

Done when a 30-line recipe lays out across two cards with every line present, in order, and the
second card repeats the title marked "(cont.)".

Judgment gate.
EOF
