#!/usr/bin/env bash
# Pollbox recorded at the newest surfaces version, with a design-principles skill and model work
# that no skill covers: the setup-project recipe's starter-current scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../principles-from-history/scaffold.sh"
newest=$(grep -oE '^- v[0-9]+' "$DRIVE_CHECKOUT/claude-plugins/manifest-dev/skills/setup-project/references/CHANGES.md" | tail -1 | tr -dc 0-9)
sed -i.bak "s/surfaces v[0-9]* -->/surfaces v$newest -->/" CLAUDE.md && rm -f CLAUDE.md.bak
mkdir -p .claude/skills/design-principles src/prompts
cat > .claude/skills/design-principles/SKILL.md <<'EOF'
---
name: design-principles
description: 'Design principles for Pollbox: how its people want design work done, and why. Use before planning, designing, prototyping, building or reviewing design work in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Results go on their own page — organizers share the link with members who did not vote. Yields when a poll has a single option.
- Vote bars use one neutral colour — colour reads as a winner and a loser. Yields when the poll has closed and the winner is announced.
- Forms take one column — organizers fill them on phones. Yields on a page only organizers open on a desktop.

Before calling design work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
EOF
cat >> CLAUDE.md <<'EOF'
- **Design work** — load the `design-principles` skill (`.claude/skills/design-principles/SKILL.md`) before planning, designing, building or reviewing it.
EOF
cat > src/prompts/summary.md <<'EOF'
Summarize the members' comments on this poll in three sentences for the organizer.
EOF
cat > src/summary.py <<'EOF'
"""Ask a model to summarize a poll's comments for its organizer."""
from pathlib import Path

PROMPT = (Path(__file__).parent / "prompts" / "summary.md").read_text()


def summarize(comments: list[str]) -> str:
    raise NotImplementedError("send PROMPT and the comments to the model")
EOF
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example add -A
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -qm "feat: comment summaries; design principles"
