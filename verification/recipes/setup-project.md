---
kind: skill
covers: claude-plugins/manifest-dev/skills/setup-project
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# setup-project

Installs a project's surfaces — North Star, glossary, ADR conventions, a verification harness, principles skills for its high-signal areas, and the context-file wiring with its surfaces version — seeding them from history, and on a set-up project audits the whole setup against what its references describe and offers each gap.

## How a user reaches it

- `/setup-project [--no-mine]`; `--no-mine` installs the wiring and the verification harness without mining history.
- Phrases its description matches: "set up the project", "bootstrap ADRs", "check whether the setup is sound".
- Its seed also offers a few Taste entries (steering preferences the owner already explained in the project's history) for the user to accept. A project set up earlier is offered them once, as the v13 item of its update, and never again.
- figure-out's docs mode offers it: no surfaces at all, a missing or older surfaces version, or a broken surface met on the way.
- On a project recording an older surfaces version it follows that version's upgrade guide: from v14, principles skills offered for high-signal areas, with the principles and Taste entries only one area needs moved into them and a pointer line for each; from v13, also the ADR-conventions rule that deleting or retargeting a draft record gives back the Status it changed, and the tool update that keeps the summary of the run that finished last; from v12, also a few Taste entries drawn from reasons the owner already stated, offered once; from v11, also the harness's time lines removed — the tool update, recipes' `Line:` and `Workload:` fields, the `headroom:` and `raise:` settings and text about lines; from v10, also decision records giving grounds rather than a veto and the North Star fit check; from v9, also scoped instructions and bounded delegated maintenance with optional coordination preparation; from v8, the North Star's *Purpose* proposed to open with the end the owner names and its measures tested against it, each on the owner's ruling, the `Revisit when` signpost and the outside-Purpose note in the ADR conventions, and the check that rebuilds the index and the strategy list; from v7, also the North Star reshaped into six sections with each chosen option moved to a decision record on the owner's ruling, and the `Strategy` area in the ADR conventions; from v6, also committed evidence removed and its directory ignored, and context-file lines that commit evidence rewritten; from v5, also a recipe for the checks run across the whole tree and one way in; from v4, also control commands, the tool update and the ask-first marks narrowed to cost; from earlier, moving an existing verification surface, feature map and reader tasks into one harness of recipes. A repository with nothing gets the wiring only.

## Scenarios

### update-one-behind
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-update-one-behind.md --scaffold claude-plugins/manifest-dev/evals/53-update-offer-from-v17 --max-turns 80`
Proves: on a project recording the surfaces version one behind the newest, it follows that version's upgrade guide: it offers what the newest version gives, marked as new, and records the newest version once each offer has an answer. Nothing from that version or earlier is offered as new, and no record, North Star position or code is rewritten.
Check: read

### principles-from-v14
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-update-one-behind.md --scaffold verification/scaffolds/principles-at-v14 --max-turns 100`
Proves: graders, applied to the report and the files written: (1) it offers, as separate items marked new in v15, creating `design-principles` from the stated reasons in the history, moving the design-only Taste entry from `CLAUDE.md` into that skill, and its pointer line; (2) on acceptance `.claude/skills/design-principles/SKILL.md` holds the moved entry in principle form and lines for the stated reasons, each with its reason and when it yields, and no line for the Tailwind choice, the blue button or the storage comment; (3) the design-only Taste entry is gone from `CLAUDE.md` while the entry that guides every session stays; (4) `CLAUDE.md` carries one pointer line for the skill and records the newest surfaces version; (5) its *Releases* and *Before PR* sections, which are not principles, are unchanged and offered for no move. PASS when all five hold.
Check: read

### greenfield-principles
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-install.md --scaffold verification/scaffolds/greenfield-page --max-turns 100`
Proves: on a new project with a web page and no history, it offers a design principles skill — putting the shipped design guidance's key trade-offs as questions with that guidance's position as the recommended answer — and offers no skill for an area the project has no work in, such as prompts; with every item accepted, `.claude/skills/design-principles/SKILL.md` exists with a pointer line.
Check: read

### starter-new-project
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-starter-new-project.md --scaffold verification/scaffolds/starter-recipebox --max-turns 150`
Proves: graders, applied to the transcript and the files written: (1) it offers starter principles for code, architecture, agent behavior, design, product, writing, security and privacy, and working practice, and none for evaluation, which this project does not do; (2) no more than three areas' lines are in front of the person at once, and it goes on to the next batch; (3) each offered line is shown word for word before any principles file is written, and the offer says before the yes that an accepted line is then held at review and that any line can be struck; (4) each choice arrives set to a named side with the reason that side fits; (5) no line is offered or written about work run twice or retried, deciding who may see or do what, outside readers of stored data, deleting stored personal data, or several writers of shared state — conditions this project does not meet; (6) a principles skill exists for each accepted area, in the method's shape, with one pointer line each in `CLAUDE.md`, the working-practice one saying to load it before changing anything; (7) the struck line about deleting what a change leaves unused appears in no written file, the choice about problems a change runs into is written on the side the person gave, and no writing skill or pointer exists. PASS when all seven hold.
Check: read

### starter-away
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-starter-away.md --scaffold verification/scaffolds/starter-recipebox --max-turns 100`
Proves: with the person away, it writes no principles skill and no pointer line, and its report lists the starter lines it would offer, by area, as candidates for the person. PASS when both hold.
Check: read

### starter-from-history
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-starter-from-history.md --scaffold verification/scaffolds/starter-from-history --max-turns 150`
Proves: graders, applied to the transcript and the files written: (1) it offers starter principles for design and code with what the history adds; (2) it offers no line of its own for the review note about empty lists, which a starter line already states; (3) it offers the starter line about naming figures and their units honed with this project's reason — the "Rooms: 3" label that led two members to book the same room; (4) it offers a new design line for the one-column booking form, with the reason that members book on their phones in the laundry room; (5) it shows the conflict between keeping the replaced form under `legacy/` as the office's paper fallback and the starter line about deleting what a change leaves unused, with both sides, and writes the project's side and not that starter line; (6) nothing is written to a principles skill before its offer. PASS when all six hold.
Check: read

### starter-from-v16
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-starter-principles-only.md --scaffold verification/scaffolds/starter-from-v16 --max-turns 150`
Proves: on a project at v16, the version before starter principles shipped, with principles skills in place, graders applied to the transcript and the files written: (1) it offers starter principles marked as new since v16: a whole starter set for model work, which no skill covers, and for `ui-principles` and `engineering-principles` the starter lines each lacks, reading which starter area each covers from what it says it is for; (2) it offers the empty-list line of `ui-principles` sharpened rather than a starter line beside it; (3) it shows the conflict between keeping replaced templates under `legacy/` and the starter line about deleting what a change leaves unused, with both sides, and keeps the project's line; (4) it offers no starter line restating the context file's principle against skipping or loosening tests; (5) it offers splitting `engineering-principles` into a code skill and an architecture skill as its own item, and makes the split with each pointer line; (6) no second skill for design appears beside `ui-principles`; (7) the newest version is recorded. PASS when all seven hold.
Check: read

### starter-current
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-starter-principles-only.md --scaffold verification/scaffolds/starter-current --max-turns 100`
Proves: on a project at the newest surfaces version, it offers the whole starter set for model work, which has work and no skill, and writes it with its pointer line; it offers no starter line for `design-principles`, whose area a skill covers; it does not change the recorded version. PASS when all three hold.
Check: read

### starter-empty-project
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-starter-empty.md --max-turns 120`
Proves: on an empty folder whose purpose the person states, it offers the starter sets for the areas that purpose implies — design, product, code, architecture, agent behavior, and security and privacy for signed-in members' bills — at most three areas at a time, offers none for evaluation, writes the accepted skills with their pointer lines beside the wiring, and tells the person how to get a set for another area later. PASS when all four hold.
Check: read

### working-practice-in-use
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-working-practice-in-use.md --scaffold verification/scaffolds/starter-working-practice --no-plugins --max-turns 40`
Proves: an agent with none of this repository's plugins, asked for a small change in a project that accepted the working-practice starter set, reads `.claude/skills/working-practice-principles/SKILL.md` before its first edit. Graded on the host's record of the session's tool calls. PASS when it does.
Check: read

### widen-plan
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-widen-plan.md --scaffold verification/scaffolds/widen-presswork --no-plugins --max-turns 60`
Proves: an agent with none of this repository's plugins, in Presswork on main, whose principles skills are the architecture and code starter sets, is asked to plan a cover stock override on the customer profile so booklet covers print on card. Grader, on PLAN.md: the plan puts the covers on the job's existing stock input (a job that takes one stock per part, or more than one stock), or names that input and says why letting it take more could not serve. Recorded as shown or not shown. With `STARTER_SETS_AT` set to a revision before the starter line about widening before adding a concept, the line's effect on planning is the difference between the two plans.
Check: read

### fit-parts
Run: `scripts/drive-skill.sh setup-project verification/prompts/setup-project-starter-principles-only.md --scaffold verification/scaffolds/starter-fit-parts --max-turns 150`
Proves: on Pollbox one surfaces version behind the plugin's newest, whose `architecture-principles` skill holds a reuse line and a fewest-moving-parts line that each carry only a part of the starter line "A new need is met by extending what already does that job", and a third line that states the one-authoritative-home starter line whole. Graders, on the transcript and the files written: (1) it offers that extending starter line, as a sharpening of one of the project's lines or as an addition, and does not report it as held; (2) it does not offer the one-authoritative-home starter line as a second line; (3) nothing is written to a principles skill before its offer. PASS when all three hold. Run with `DRIVE_PLUGINS_AT` set to a revision before the stricter fit rule, the same scaffold records the version one behind that revision's newest; on an earlier form of this fixture the earlier rule did not mark the line held either, so this scenario does not by itself tell the stricter rule from the earlier one.
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
