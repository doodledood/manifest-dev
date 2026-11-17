#!/usr/bin/env bash
# Branchline on main: a visit log that a decision made the one record of checkouts, then a later
# commit with no record narrowed it to item ids. A principles skill, pointed to in the project's own
# words under an area word no reviewer carries, holds a reuse line. Run inside an empty repository.
set -euo pipefail
git branch -M main
git config user.name 'Rui Santos'
git config user.email 'rui@branchline.example'
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p .agents/skills/foundations-principles .claude docs/decisions src/branchline tests
ln -s ../.agents/skills .claude/skills
cat > tests/conftest.py <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
EOF
cat > AGENTS.md <<'EOF'
# Branchline

Branchline records checkouts at the library and builds the monthly reports from them.

## Before you work here

- Anything that touches code: read `.agents/skills/foundations-principles/SKILL.md` first. It is
  how the team wants new work to fit the system, and why.
- Decisions live in `docs/decisions/`.
EOF
ln -s AGENTS.md CLAUDE.md
cat > .agents/skills/foundations-principles/SKILL.md <<'EOF'
---
name: foundations-principles
description: 'Foundations principles for Branchline: how the team wants new work to fit the system, and why. Use before planning, designing, building or reviewing code in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Reuse what already owns the behavior: before building a second store, path or job for a kind of data, extend the module that already records it, or restore what an earlier change narrowed — two records of one thing drift, and every report then has to know which one is true. Yields when the owner cannot carry the new need without changing what it means.

Before calling work done, check it against these principles from a fresh start. Name each
departure kept, with the principle and why.
EOF
cat > docs/decisions/0001-the-visit-log-is-the-record-of-checkouts.md <<'EOF'
# 0001: The visit log is the record of checkouts

Status: Accepted
Decided by: Rui Santos (maintainer)

Every checkout is written to the visit log with the full item record at that moment: title,
format, branch and the borrower's age band. Reports and audits read the visit log and nothing else,
so there is one answer to "what went out".
EOF
cat > src/branchline/__init__.py <<'EOF'
EOF
cat > src/branchline/catalog.py <<'EOF'
"""The live catalog. Records change over time: items move branches, formats are recatalogued."""
CATALOG: dict[str, dict] = {}


def item(item_id: str) -> dict:
    return dict(CATALOG[item_id])
EOF
cat > src/branchline/visit_log.py <<'EOF'
"""The record of checkouts (decision 0001)."""
from datetime import datetime

from branchline.catalog import item

LOG: list[dict] = []


def record_checkout(item_id: str, age_band: str, at: datetime) -> None:
    LOG.append({"at": at, "age_band": age_band, **item(item_id)})
EOF
cat > tests/test_visit_log.py <<'EOF'
from datetime import datetime

from branchline import catalog, visit_log


def test_checkout_keeps_the_item_as_it_was():
    catalog.CATALOG["b1"] = {"id": "b1", "title": "Dune", "format": "paperback", "branch": "east"}
    visit_log.record_checkout("b1", "18-25", datetime(2026, 3, 1, 10))
    assert visit_log.LOG[-1] == {"at": datetime(2026, 3, 1, 10), "age_band": "18-25",
                                 "id": "b1", "title": "Dune", "format": "paperback", "branch": "east"}
EOF
git add -A
git commit -qm 'Visit log records each checkout with the full item'
cat > src/branchline/visit_log.py <<'EOF'
"""The record of checkouts (decision 0001)."""
from datetime import datetime

LOG: list[dict] = []


def record_checkout(item_id: str, age_band: str, at: datetime) -> None:
    # Store the id only: copying the catalog record made checkout writes slow at the desk.
    LOG.append({"at": at, "age_band": age_band, "id": item_id})
EOF
cat > tests/test_visit_log.py <<'EOF'
from datetime import datetime

from branchline import visit_log


def test_checkout_is_recorded():
    visit_log.record_checkout("b1", "18-25", datetime(2026, 3, 1, 10))
    assert visit_log.LOG[-1] == {"at": datetime(2026, 3, 1, 10), "age_band": "18-25", "id": "b1"}
EOF
git add -A
git commit -qm 'perf: keep only item ids in the visit log'
