---
kind: skill
covers: claude-plugins/manifest-dev/skills/setup-project
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# setup-project

Installs a project's surfaces — North Star, glossary, ADR conventions, a verification harness, and the context-file wiring with its surfaces version — seeding them from history, and on a set-up project audits the whole setup against what its references describe and offers each gap.

## How a user reaches it

- `/setup-project [--no-mine]`; `--no-mine` installs the wiring and the verification harness without mining history.
- Phrases its description matches: "set up the project", "bootstrap ADRs", "check whether the setup is sound".
- figure-out's docs mode offers it: no surfaces at all, a missing or older surfaces version, or a broken surface met on the way.
- On a project recording an older surfaces version it follows that version's upgrade guide, moving an existing verification surface, feature map and reader tasks into one harness of recipes. A repository with nothing gets the wiring only.

## Scenarios

### update-one-behind
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-update-one-behind.md --scaffold claude-plugins/manifest-dev/evals/50-update-moves-v3-into-harness --max-turns 80`
Proves: the report lists what it offered, applied and declined; the context file ends at the newest version with one verification bullet; the summary's files include `scripts/verify`, `verification/harness.md`, a recipe per former feature-map entry and reader task (the checkout recipe keeps its *Club notes*), the moved evidence, and the removal of `docs/features/` and `docs/reader-tasks/`. Nothing was written that the run did not offer and accept.
Check: read

### update-from-v1
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-update-one-behind.md --scaffold claude-plugins/manifest-dev/evals/47-update-offer-from-previous-version --max-turns 80`
Proves: it follows the v1 guide straight to the harness — the loose `verify/` feature map becomes recipes without first taking v2's fixed map shape — and adds the records-in-effect rule.
Check: read

### app-project
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-install.md --scaffold claude-plugins/manifest-dev/evals/51-setup-offers-harness-for-app --max-turns 80`
Proves: the harness it seeds runs the existing `python3 -m pytest tests/` and the CLI commands, marks none of them ask-first, and `scripts/verify check` passes; one context-file verification bullet.
Check: read

### audit-current
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-audit-current.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing --max-turns 80`
Proves: it offers gaps item by item though the version is current, and backfills `Enforced by` only on records in effect.
Check: read

### upgrade-this-repository-from-v3
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-upgrade-this-repository.md --scaffold verification/scaffolds/this-repository-at-v3 --max-turns 300`
Proves: on this repository's last commit at v3, the update offers the move to one harness and applies it: a recipe per skill, walk and eval suite, the evidence moved with an Outcome line, `docs/features/` and `docs/reader-tasks/` removed, the version line at the newest. The run's `scratch.diff` is what the later hand-completed commit started from.
Check: read

### this-repository
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-this-repository.md --scaffold verification/scaffolds/this-repository --max-turns 200`
Proves: on this repository, set up at the newest version, the audit offers nothing and writes nothing; the summary shows no files written.
Check: read

### install
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-install.md --max-turns 80`
Proves: `docs/adr/CONVENTIONS.md`, `CONTEXT.md`, `NORTH_STAR.md` and `docs/NORTH_STAR_CONVENTIONS.md` exist, and the context file carries the newest version line.
Check: read

## Gotchas

- It writes many project files and changes every later session's context. Scratch directory only.
- It never overwrites a project-owned copy: differences are offered, not applied.
- It writes scenarios only as far as existing commands reach; drive work beyond that comes from the change that needs it.
- `this-repository` copies the last commit, not the working tree: commit before driving it.
- Each prompt file except the two `setup-project-*-repository.md` ones starts `/manifest-dev:setup-project`, followed by whether the user accepts every item.
- `tests/test_setup_project_versions.py` (a change to an emitted file ships a new version) and `tests/test_project_conventions_forks.py` (this repo's copies match the defaults) also check it; behavior cases `30`, `45`, `47`, `49` cover figure-out's offer of it, and `50`, `51` a setup run (all `unmeasured`).
- Not yet driven: the description phrases, figure-out's offer.
