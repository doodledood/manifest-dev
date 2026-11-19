#!/usr/bin/env bash
# Pollbox recorded at v16, the version before starter principles shipped, with principles skills from an earlier
# setup: ui-principles covers design under another name and holds a line that nearly covers a
# general one about empty states; engineering-principles spans code and architecture and holds a
# line that conflicts with a general one about deleting what a change leaves unused. Its context
# file states a principle a general code line would restate, and it has model work with no skill:
# the setup-project recipe's starter-one-behind scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../principles-from-history/scaffold.sh"
sed -i.bak "s/surfaces v[0-9]* -->/surfaces v16 -->/" CLAUDE.md && rm -f CLAUDE.md.bak
mkdir -p .claude/skills/ui-principles .claude/skills/engineering-principles src/prompts
cat > .claude/skills/ui-principles/SKILL.md <<'EOF'
---
name: ui-principles
description: 'UI principles for Pollbox: how its people want screens to look and behave, and why. Use before planning, designing, building or reviewing a Pollbox screen.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Show a message when a list of polls or votes is empty — an empty table reads as a broken page. Yields when the list sits inside a section whose heading already says it is empty.
- Results go on their own page — organizers share the link with members who did not vote. Yields when a poll has a single option.

Before calling UI work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
EOF
cat > .claude/skills/engineering-principles/SKILL.md <<'EOF'
---
name: engineering-principles
description: 'Engineering principles for Pollbox: how its people want code written and the system structured, and why. Use before planning, building or reviewing Pollbox code or its structure.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Keep a replaced template under `src/templates/legacy/` for one release after a change — organizers roll back by hand by copying it over. Yields when the replaced template held no organizer-facing text.
- Store each poll's tally in one place and compute every view from it — two counts of the same votes drift apart. Yields when a count is only displayed and never stored.

Before calling engineering work done, check it against these principles from a fresh start — a
new session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
EOF
cat >> CLAUDE.md <<'EOF'
- **UI work** — load the `ui-principles` skill (`.claude/skills/ui-principles/SKILL.md`) before planning, designing, building or reviewing it.
- **Engineering work** — load the `engineering-principles` skill (`.claude/skills/engineering-principles/SKILL.md`) before planning, designing, building or reviewing it.

## Principles

- Never make a test pass by skipping, loosening or deleting it — a green run that hides a failure is worse than a red one. Yields when the test itself is wrong; then say so in the pull request.
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
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -qm "feat: comment summaries; principles from the earlier setup"
