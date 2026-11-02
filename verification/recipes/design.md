---
kind: skill
covers: claude-plugins/manifest-dev/skills/design
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# design

Gives design guidance for a page, app, document, deck, graphic or prototype from the person, their moment and the subject. It guides; building and checking stay with whoever called it.

## How a user reaches it

- `/design <artifact, brief or file>`.
- Phrases its description matches: "restyle this page", "how should this look and feel".
- figure-out when it renders a draft; eli5; walk-pr's canvas mode.
- When an open alternative is an experience choice — where something lives, how the person moves through it, what each step asks — it shows two or three variants that differ on it, made from the product's existing patterns.
- It loads medium-specific guidance as the artifact needs, and takes optional measurements through `claude-plugins/manifest-dev/skills/design/scripts/design-tools.mjs` (see design-instruments).

## Scenarios

### guide
Run: `scripts/drive-skill.sh design verification/prompts/design-guide.md`
Proves: guidance that names the person, the moment and the chosen direction. It produced guidance and did not claim to have built or verified anything.
Check: read

### variants-of-an-experience-choice
Run: `scripts/drive-skill.sh design verification/prompts/design-split-the-bill.md --scaffold verification/scaffolds/tablewise`
Proves: with when and how diners split a bill left open, the session writes two or three prototype variants under `prototype/` that differ on that choice — when splitting happens, or how many steps it takes each person — each built from the product's own patterns in `pages/styles.css` (cards, the bottom bar's one primary action, steppers, the sheet), rather than asking about the choice in prose or varying only the look. A fresh grader reads the files written and the final reply against that sentence.
Check: read

## Gotchas

- "It didn't build the page" is intended.
- Its instruments measure; they do not score quality.
- `tests/test_design_standalone.py` keeps it self-contained and free of delegation; the instruments have their own recipe.
