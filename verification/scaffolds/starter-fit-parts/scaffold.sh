#!/usr/bin/env bash
# Pollbox one surfaces version behind the newest that the drive's plugin snapshot lists (this
# checkout, or DRIVE_PLUGINS_AT when set), with an architecture-principles skill from an earlier
# setup. Two of its lines each carry only a part of the starter line "A new need is met by
# extending what already does that job": one says to reuse what already owns a behavior, one to
# question a requirement and take the fewest moving parts. A third line states another starter
# line whole. The setup-project recipe's fit-parts scenario.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../principles-from-history/scaffold.sh"
changes=claude-plugins/manifest-dev/skills/setup-project/references/CHANGES.md
if [ -n "${DRIVE_PLUGINS_AT:-}" ]; then
  listed=$(git -C "$DRIVE_CHECKOUT" show "$DRIVE_PLUGINS_AT:$changes")
else
  listed=$(cat "$DRIVE_CHECKOUT/$changes")
fi
newest=$(printf '%s\n' "$listed" | grep -oE '^- v[0-9]+' | tail -1 | tr -dc 0-9)
sed -i.bak "s/surfaces v[0-9]* -->/surfaces v$((newest - 1)) -->/" CLAUDE.md && rm -f CLAUDE.md.bak
mkdir -p .claude/skills/architecture-principles
cat > .claude/skills/architecture-principles/SKILL.md <<'EOF'
---
name: architecture-principles
description: 'Architecture principles for Pollbox: how its people want the app structured and its data kept, and why. Use before planning, designing, building or reviewing how Pollbox is structured.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Reuse what already owns a behavior instead of building a second path beside it — two paths for one job drift apart, and fixes land in only one. Yields when the owner would have to change what it means to take the new case.
- Question a requirement before building for it, then take the design with the fewest moving parts — every part is one more thing to keep right. Yields when the fewer parts would not meet the requirement.
- Each fact has one authoritative home, and any other copy is derived from that home — two copies can drift apart without a sound, and only one of them ever gets checked. Yields when measured cost demands a stored copy, which is then a cache verified against its home, or when the copies are supposed to evolve separately.

Before calling architecture work done, check it against these principles from a fresh start — a
new session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
EOF
cat >> CLAUDE.md <<'EOF'
- **Architecture work** — load the `architecture-principles` skill (`.claude/skills/architecture-principles/SKILL.md`) before planning, designing, building or reviewing it.
EOF
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example add -A
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -qm "docs: architecture principles"
