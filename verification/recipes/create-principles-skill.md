---
kind: skill
covers: claude-plugins/manifest-dev/skills/create-principles-skill
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# create-principles-skill

Creates or refreshes one area's principles skill — a project skill named `<area>-principles` holding how the project's people want that area's work done — by running figure-out with a brief that points to the method in `setup-project/references/PRINCIPLES_SKILLS.md`.

## How a user reaches it

- `/create-principles-skill [area] [--autonomous] [--no-log]`; with no area it offers the high-signal areas.
- Phrases its description matches: "create a principles skill", "capture how we do design here", "refresh the design principles".
- figure-out's docs mode reaches the same method when a person states why they want one area's work done differently, and setup-project offers it for high-signal areas.

## Scenarios

### create-from-history
Run: `scripts/drive-skill.sh create-principles-skill verification/prompts/create-principles-skill-design.md --scaffold verification/scaffolds/principles-from-history --max-turns 80`
Proves: graders, applied to the files the run wrote: (1) `.claude/skills/design-principles/SKILL.md` exists, its description on one line; (2) it holds a line for each of the three stated reasons — results on their own page because they get shared, vote bars in one neutral colour because colour reads as a winner and a loser, forms in one column because organizers fill them on phones — each with its reason and when it yields; (3) it does not restate the Tailwind choice that `docs/adr/0002` settles, and has no line for the blue button, which came with no reason, or for the storage comment; (4) its body opens with the edit rule and ends with the self-check; (5) `CLAUDE.md`'s project-surfaces section gains one pointer line naming the skill and its path, and nothing else in `CLAUDE.md` changes. PASS when all five hold.
Check: read

### away-writes-nothing
Run: `scripts/drive-skill.sh create-principles-skill verification/prompts/create-principles-skill-away.md --scaffold verification/scaffolds/principles-from-history --max-turns 60`
Proves: with the person away, the run writes no skill and no pointer line — the summary shows no file written in the project — and reports the candidate lines with their sources.
Check: read

### no-area-offers-high-signal
Run: `scripts/drive-skill.sh create-principles-skill verification/prompts/create-principles-skill-no-area.md --scaffold verification/scaffolds/principles-from-history --max-turns 60`
Proves: it offers design, with a count of its stated-reason corrections and their sources, and does not offer storage or data, which holds one stray comment; it writes nothing.
Check: read

### refresh-sharpens
Run: `scripts/drive-skill.sh create-principles-skill verification/prompts/create-principles-skill-refresh.md --scaffold verification/scaffolds/principles-refresh --max-turns 80`
Proves: graders, applied to `.claude/skills/design-principles/SKILL.md` after the run: (1) the results line is sharpened in place to cover anything a member or organizer might send to someone else, with no second line beside it on the same principle; (2) the Tailwind line is gone, its choice left to `docs/adr/0002`; (3) the history note is gone; (4) lines for the neutral vote bars and the one-column forms are added, each with its reason and when it yields; (5) the edit rule and the self-check still open and end the body, and `CLAUDE.md` still carries exactly one pointer line for the skill. PASS when all five hold.
Check: read

## Gotchas

- It writes into the project and changes later sessions' context. Scratch directory only.
- The prompts that accept every line answer in advance; the `--autonomous` prompt is the only one with no person present.
- `tests/test_principles_skills.py` holds the wrapper's shape and that the method lives in one file.
