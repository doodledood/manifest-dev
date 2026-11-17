#!/usr/bin/env bash
# The front-desk handbook: a draft procedure whose context file points, in its own words, to a
# principles skill under the area word "frontdesk". One line departs from general documentation
# defaults and the draft follows it; the other the draft departs from, with no person's choice. The
# draft's own note claims that line's yield, which its steps do not bear out.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
git branch -M main
git config user.name "Sam Okoro"
git config user.email "sam@frontdesk.example"
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p .agents/skills/frontdesk-principles .claude handbook
ln -s ../.agents/skills .claude/skills
cat > AGENTS.md <<'EOF'
# Front-desk handbook

The procedures library staff follow at the front desk. Each one is printed on the desk's receipt
printer.

Before you write or review anything in `handbook/`, read
`.agents/skills/frontdesk-principles/SKILL.md`: it is how we want procedures written, and why.
EOF
ln -s AGENTS.md CLAUDE.md
cat > .agents/skills/frontdesk-principles/SKILL.md <<'EOF'
---
name: frontdesk-principles
description: 'Front-desk principles for the library handbook: how the team wants desk procedures written, and why. Use before writing or reviewing a procedure in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Write a procedure's steps as one paragraph of short sentences, never as a numbered or bulleted list — the receipt printer drops list markup and runs the numbers into the text. Yields for the web edition.
- Every procedure ends with who to call when a step fails, by role and phone extension — staff alone at closing time stalled on a failed step with nobody to ask. Yields for a procedure none of whose steps can fail.

Before calling handbook work done, check it against these principles from a fresh start. Name each
departure kept, with the principle and why.
EOF
cat > handbook/renew-by-phone.md <<'EOF'
# Renewing a loan by phone

Ask the caller for their card number and the title they want to renew. Open the member's record in
the loans system and find the title. Choose Renew. The system sets a new due date three weeks out
and reads it back to you. Tell the caller the new date. If the system refuses the renewal because
someone has reserved the title, tell the caller it must come back by the current due date.

<!-- Author's note: every way this procedure can fail is handled in its steps, so it needs no one to call. -->
EOF
git add -A
git commit -qm 'Draft: renewing a loan by phone'
