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
- Its seed also offers a few Taste entries (steering preferences the owner already explained in the project's history) for the user to accept. A project set up earlier is offered them once, as the v13 item of its update, and never again.
- figure-out's docs mode offers it: no surfaces at all, a missing or older surfaces version, or a broken surface met on the way.
- On a project recording an older surfaces version it follows that version's upgrade guide: from v13, the ADR-conventions rule that deleting or retargeting a draft record gives back the Status it changed; from v12, also a few Taste entries drawn from reasons the owner already stated, offered once; from v11, also the harness's time lines removed — the tool update, recipes' `Line:` and `Workload:` fields, the `headroom:` and `raise:` settings and text about lines; from v10, also decision records giving grounds rather than a veto and the North Star fit check; from v9, also scoped instructions and bounded delegated maintenance with optional coordination preparation; from v8, the North Star's *Purpose* proposed to open with the end the owner names and its measures tested against it, each on the owner's ruling, the `Revisit when` signpost and the outside-Purpose note in the ADR conventions, and the check that rebuilds the index and the strategy list; from v7, also the North Star reshaped into six sections with each chosen option moved to a decision record on the owner's ruling, and the `Strategy` area in the ADR conventions; from v6, also committed evidence removed and its directory ignored, and context-file lines that commit evidence rewritten; from v5, also a recipe for the checks run across the whole tree and one way in; from v4, also control commands, the tool update and the ask-first marks narrowed to cost; from earlier, moving an existing verification surface, feature map and reader tasks into one harness of recipes. A repository with nothing gets the wiring only.

## Scenarios

### update-from-v13
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-update-one-behind.md --scaffold claude-plugins/manifest-dev/evals/53-update-offer-from-v13 --max-turns 80`
Proves: it follows the v13 guide: it offers, and on acceptance adds to `docs/adr/CONVENTIONS.md`, the rule that deleting or retargeting a draft record gives back the Status it changed; the version line reaches v14 only after the offer has an answer. Nothing from v13 or earlier is offered as new — not the Taste entries, not the time-line removal — and no record, North Star position or code is rewritten.
Check: read

### update-from-v3
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-update-one-behind.md --scaffold verification/scaffolds/project-at-v3 --max-turns 80`
Proves: the report lists what it offered, applied and declined; the context file ends at the newest version with one verification bullet; the summary's files include `scripts/verify`, `verification/harness.md`, a recipe per former feature-map entry and reader task (the checkout recipe keeps its *Club notes*), a recipe for the checks run across the whole tree, no committed evidence with its directory ignored, and the removal of `docs/features/` and `docs/reader-tasks/`. Nothing was written that the run did not offer and accept.
Check: read

### update-from-v1
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-update-one-behind.md --scaffold verification/scaffolds/project-at-v1 --max-turns 80`
Proves: it follows the v1 guide straight to the harness — the loose `verify/` feature map becomes recipes without first taking v2's fixed map shape — and adds the records-in-effect rule.
Check: read

### seed-from-the-end
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-seed-end.md --scaffold verification/scaffolds/app-without-surfaces --max-turns 80`
Proves: the seeded `NORTH_STAR.md` opens its *Purpose* with the end the prompt's owner names — every lent book coming back and the club staying a pleasure to run — keeps any barrier the README or the prompt names as one thing in its way rather than as the purpose, and its *How we know* holds a measure of that end, `empty` with what would fill it where nothing counts it; the project gets a check that rebuilds the ADR index beside its tests.
Check: read

### taste-from-history
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-taste-from-history.md --scaffold verification/scaffolds/taste-from-history --max-turns 80`
Proves: with the owner away, setup's seed reports Taste candidates drawn only from reasons the owner stated and only where they lean away from a shipped default, and writes none. Graders, applied by a grader session that sees the run under a letter label only: (1) it reports as candidates an entry for the ballot-settings reversal in the commit body (decisions that make a vote valid are set explicitly by the organizer rather than defaulted) and one for the guest-poll refusal in the review notes (nothing that sends to other people before a verified account), each stated as a principle that carries beyond its case, built on the owner's stated reason, with when it yields; (2) it puts forward none for asking only the email at sign-up, which a shipped default already says, none for SQLite storage, which `docs/adr/0001` settles, and none for the export-button revert, which gives no reason; (3) it writes no `## Taste` section or entry to any file; (4) it opens no past session record of the owner; (5) its report names what it left out and why. PASS when all five hold.
Check: read

### app-project
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-install.md --scaffold verification/scaffolds/app-without-surfaces --max-turns 80`
Proves: the harness it seeds runs the existing `python3 -m pytest tests/` and the CLI commands, marks none of them ask-first, and `scripts/verify check` passes; one context-file verification bullet.
Check: read

### audit-current
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-audit-current.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing --max-turns 80`
Proves: it offers gaps item by item though the version is current, and backfills `Enforced by` only on records in effect.
Check: read

### upgrade-this-repository-from-v3
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-upgrade-this-repository.md --scaffold verification/scaffolds/this-repository-at-v3 --max-turns 300`
Proves: on this repository's last commit at v3, the update offers the move to one harness and applies it: a recipe per skill, walk and eval suite, committed evidence removed and its directory ignored, `docs/features/` and `docs/reader-tasks/` removed, the version line at the newest. The run's `scratch.diff` is what the later hand-completed commit started from.
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
- `tests/test_setup_project_versions.py` (a change to an emitted file ships a new version) and `tests/test_project_conventions_forks.py` (this repo's copies match the defaults) also check it; behavior cases `30`, `45` and `53` cover figure-out's offer of it (all `unmeasured`). The eval suites cover `figure-out` and `define` only, so setup-project's own runs are checked here: the v1, v3 and app scaffolds live under `verification/scaffolds/`.
- Not yet driven: the description phrases, figure-out's offer.
