---
kind: skill
covers: claude-plugins/manifest-dev/skills/manifest-dev-help
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# manifest-dev-help

Answers any question a person has about manifest-dev, with the why, in English close to ASD-STE100: what it is for, the workflow, the autonomy ladder, every term a user meets, how the parts relate, good practice, and what an artifact the user points at means — reading the owning skill when its own text does not answer.

## How a user reaches it

- `/manifest-dev-help [question]` in Claude Code, `$manifest-dev-help` in Codex, `/skill:manifest-dev-help` in Pi.
- Phrases its description matches: "what is a recipe", "why is this verification folder here", "how do the manifest-dev skills fit together".
- No workflow skill calls it; it is an optional extra.

## Scenarios

### term
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-term.md`
Proves: the answer says what a recipe and the verification harness are and why each exists, that ask-first marks a run with a cost a person accepts, and how an Acceptance Criterion differs from a Global Invariant, from the glossary, in short plain sentences.
Check: read

### hill-climb
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-hill-climb.md`
Proves: the answer says what a hill-climb is and why it needs a measure shown good and a stop rule, that it is quick by default and thorough when asked or when the stakes call for it, that `/hillclimb` from the tools plugin starts one over figure-out, define and do, that nothing is pushed unless asked, and when it stops, from the glossary, in short plain sentences.
Check: read

### agent
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-agent.md`
Proves: the answer gives both uses of the word from the glossary — the AI model that does work for a person, such as the "person or agent" a Ticket is written for, and the separate execution context a host can run one in — in short plain sentences.
Check: read

### judgment
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-judgment.md --tools`
Proves: the answer explains project-consequence judgment, including advice against a correct requested change, and keeps advisory judgment separate from contract results and merge authority. It explains that an informed trade-off can settle discussion without reviewer endorsement, from the glossary or owning review skill, in plain short sentences.
Check: read

### ladder
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-ladder.md`
Proves: the answer names the five levels, says each works without the ones above it and without the team, and gives what each adds and costs and where to start.
Check: read

### why-beyond
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-why-beyond.md`
Proves: for a why that the skill's own text does not carry, the answer reads the skill that owns the behavior (`do` and its log reference), names that file, and gives the reason; it invents nothing that file does not say.
Check: read

### walk-a-pull-request
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-walk-a-pull-request.md`
Proves: asked for a job only a tools-plugin skill does, with the tools plugin not installed, the answer names `/walk-pr`, says it is in the tools plugin, which installs separately, and names the guide as its source, in short plain sentences. The prompt names no skill; the manifest-dev plugin before the guide covered the tools plugin mentions `walk-pr` nowhere, so the answer comes from the guide.
Check: read

### overview
Run: `scripts/drive-skill.sh manifest-dev-help verification/prompts/manifest-dev-help-overview.md`
Proves: with no question, the answer gives what manifest-dev is for, the workflow and the autonomy ladder, and stops there.
Check: read

## Gotchas

- `tests/test_manifest_dev_help_skill.py` holds the term set and each entry's fingerprint against `CONTEXT.md`, the skill list against both plugins, and STE's counted limits. Whether an answer is right stays a read.
- An answer that no file supports is a failure, even when it is true: the skill reads the owning skill or the artifact the user points at, names it, and says so when no file answers.
