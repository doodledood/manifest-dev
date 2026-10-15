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
- It loads medium-specific guidance as the artifact needs, and takes optional measurements through `claude-plugins/manifest-dev/skills/design/scripts/design-tools.mjs` (see design-instruments).

## Scenarios

### guide
Run: `scripts/drive-skill.sh design verification/prompts/design-guide.md`
Proves: guidance that names the person, the moment and the chosen direction. It produced guidance and did not claim to have built or verified anything.
Check: read
Workload: varies

## Gotchas

- "It didn't build the page" is intended.
- Its instruments measure; they do not score quality.
- `tests/test_design_standalone.py` keeps it self-contained and free of delegation; the instruments have their own recipe.
