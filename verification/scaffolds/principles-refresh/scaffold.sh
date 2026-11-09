#!/usr/bin/env bash
# The principles-from-history project with a design-principles skill already written: one
# principle stated loosely, one decision line, one history note. New review notes restate that
# principle more sharply and add one new principle: the create-principles-skill refresh scenario.
set -euo pipefail
bash "$(dirname "$0")/../principles-from-history/scaffold.sh"
commit() { git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example add -A && git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -q "$@"; }
mkdir -p .claude/skills/design-principles
cat > .claude/skills/design-principles/SKILL.md <<'EOF'
---
name: design-principles
description: 'Design principles for Pollbox: how its people want design work done, and why. Use before planning, designing, prototyping, building or reviewing design work in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Results go on a page, not a modal — people share the results link. Yields when nothing about the view is ever shared.
- We use Tailwind utility classes for all styling.
- Added in March after the results-page review on pull request #12.

Before calling design work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work — fix what departs, and repeat until nothing does.
Name any departure you keep, with the principle and why.
EOF
cat >> CLAUDE.md <<'EOF'
- **Design work** — load the `design-principles` skill (`.claude/skills/design-principles/SKILL.md`) before planning, designing, building or reviewing it.
EOF
cat > docs/reviews/pr-21-poll-settings.md <<'EOF'
# Review notes exported from pull request #21 (poll settings)

**Dana:** Settings can't be a popover either. It's the same reason as results: anything a member
or organizer might send to someone else needs its own address, or the link they send lands on the
wrong thing.

**Dana:** And no colour on the vote bars here either — keep them in one neutral colour. Colour
reads as a winner and a loser before the poll even closes, and members take it personally.

**Sam:** Moved settings to /polls/<id>/settings; bars are grey.
EOF
commit -m "docs: keep the poll-settings review notes"
