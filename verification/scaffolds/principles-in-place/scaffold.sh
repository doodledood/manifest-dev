#!/usr/bin/env bash
# The principles-from-history project with a settled design-principles skill and its pointer line:
# the define, figure-out and review-code recipes' principles scenarios.
set -euo pipefail
bash "$(dirname "$0")/../principles-from-history/scaffold.sh"
mkdir -p .claude/skills/design-principles
cat > .claude/skills/design-principles/SKILL.md <<'EOF'
---
name: design-principles
description: 'Design principles for Pollbox: how its people want design work done, and why. Use before planning, designing, prototyping, building or reviewing design work in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Anything a member or organizer might send to someone else gets its own page with its own address, never a modal or popover — people paste links into the club chat, and a link must land on the thing they meant. Yields when the view holds nothing anyone would share, such as a confirm step.
- Vote counts and bars use one neutral colour, never a colour per option or for the leader — colour reads as a winner and a loser, and members take it personally. Yields after a poll closes, where the result may be marked.
- Forms are one column with labels above fields — organizers fill them on phones mid-meeting and two columns made them mistype. Yields on a screen only an admin uses at a desk.

Before calling design work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work — fix what departs, and repeat until nothing does.
Name any departure you keep, with the principle and why.
EOF
cat >> CLAUDE.md <<'EOF'
- **Design work** — load the `design-principles` skill (`.claude/skills/design-principles/SKILL.md`) before planning, designing, building or reviewing it.
EOF
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example add -A
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -qm "docs: design principles"
