---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/handoff
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# handoff

Writes a self-contained context payload a fresh agent can continue from without re-deriving what this session established.

## How a user reaches it

- `/handoff <what the next session is for>`; given an earlier handoff's path, it writes a fresh one from it.
- Phrases its description matches: "hand this off", "switching tools", "start a clean session".
- No other skill calls it.

## Scenarios

### write
Run: `scripts/drive-skill.sh handoff verification/prompts/handoff-write.md --tools`
Proves: the drive's summary lists a new `handoffs/handoff-*.md` among what the session wrote under `.manifest-dev`, and the reply names its path. A fresh session given only that file can state the goal, the state and the next step.
Check: read

### cross-host-contract
Run: `scripts/drive-skill.sh handoff verification/prompts/acceptance/handoff-contract.md --tools --scaffold verification/fixtures/acceptance-contract`
Proves: The payload carries the essential acceptance and continuation state when the original files cannot reach the receiver. It keeps the reachable versioned reference, supported rejection and reopening condition, first-look state, pending amendment, approval and cleanup. It grants no merge or deployment right.
Check: read

## Gotchas

- Needs a session with some work to hand over.
- The file is outside the repository.
- Passing an earlier handoff rewrites it into a new file; it does not append.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
