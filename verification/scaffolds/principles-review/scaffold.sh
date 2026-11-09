#!/usr/bin/env bash
# The principles-in-place project plus an architecture-principles skill whose principle departs from
# a default, and an uncommitted change that follows that principle and departs from a design one:
# the review-code recipe's principles scenario.
set -euo pipefail
bash "$(dirname "$0")/../principles-in-place/scaffold.sh"
mkdir -p .claude/skills/architecture-principles src/exports src/notify
cat > .claude/skills/architecture-principles/SKILL.md <<'EOF'
---
name: architecture-principles
description: 'Architecture principles for Pollbox: how its people want code structured, and why. Use before planning, designing, building or reviewing code structure in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Repeat a small helper in each package under `src/` rather than sharing it from a common module — each package is deployed to a different club host on its own schedule, and a shared module ties their releases together. Yields when the helper is more than about ten lines or must change in step everywhere.

Before calling architecture work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work — fix what departs, and repeat until nothing does.
Name any departure you keep, with the principle and why.
EOF
cat >> CLAUDE.md <<'EOF'
- **Code structure** — load the `architecture-principles` skill (`.claude/skills/architecture-principles/SKILL.md`) before planning, designing, building or reviewing it.
EOF
cat > src/exports/__init__.py <<'EOF'
EOF
cat > src/notify/__init__.py <<'EOF'
EOF
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example add -A
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -qm "docs: architecture principles"
cat > src/exports/csv_export.py <<'EOF'
def poll_title(question):
    """Title-case a poll question for display."""
    return question.strip().rstrip("?").title()


def export_row(question, counts):
    return ",".join([poll_title(question)] + [str(c) for c in counts])
EOF
cat > src/notify/email.py <<'EOF'
def poll_title(question):
    """Title-case a poll question for display."""
    return question.strip().rstrip("?").title()


def closing_subject(question):
    return f"Poll closed: {poll_title(question)}"
EOF
cat > src/templates/results.html <<'EOF'
<!-- Live view, shown while the poll is open. -->
<main class="max-w-xl mx-auto"><h1>{{ question }}</h1>{% for o in options %}<p>{{ o.name }}: {{ o.count }} <span class="{% if o.leading %}bg-green-500{% else %}bg-gray-400{% endif %}" style="width: {{ o.pct }}%"></span></p>{% endfor %}</main>
EOF
