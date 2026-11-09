---
name: setup-project
description: 'Set a project up with the surfaces manifest-dev works from — a North Star, a glossary, ADR conventions, a recommended verification harness the user may opt out of, principles skills for its high-signal areas, and the context-file wiring that makes every session use them — seeding them from the project''s own history where there is any, and keep a set-up project sound by auditing it against the setup the references describe and offering each gap, marking what changed since the surfaces version it records. Use when a repository has no CONTEXT.md or decision records, when adopting manifest-dev in an existing codebase, when starting a new project, when a set-up project records no surfaces version or an older one, or when the user asks to set up the project, re-run the setup to check it is sound, bootstrap ADRs, or reconstruct decisions from history.'
---

Install the project surfaces a repository needs so that every future session — and every teammate, with or without manifest-dev — works from the same direction, the same vocabulary, and the same decision record.

Four things get installed or offered, and only the first is essential:

- **The wiring** — an ADR conventions file the project owns, a glossary, a North Star (the project's standing statement of what it is for: its purpose and whom it serves, its goal, the principles it holds, how it measures progress, and the bets it rests on), and a project-context-file section that makes sessions read and maintain all three and records the surfaces version the project carries. This runs on every project, including one with no history at all.
- **A verification harness, recommended and installed by default** — the project's one command for checking that what future runs will change still does its job, with a recipe per thing it checks, seeded from what the project already has. Before installing a harness, offering the upgrade to one or auditing one that exists, read `references/VERIFICATION_HARNESS.md`. A project that verifies its own way may opt out; the context file then records that way instead.
- **A seed** — vocabulary and decision records reconstructed from the project's own history, and a few Taste entries (steering preferences its owner already explained) offered for the user to accept. This runs wherever there is history to read, and it is enrichment on top of the wiring, never a substitute for it.
- **Principles skills, offered** — one project skill per high-signal area of the project's work, such as design or prompts, holding how its people want that area's work done, with a pointer line in the context file; and the principles and Taste entries in the context file that only one area's work needs, moved into that area's skill. Before offering, writing or auditing a principles skill, read `references/PRINCIPLES_SKILLS.md`: it is the method. Only the person's yes writes any of it.

All of this is for a project: a repository or working folder holding, or about to hold, work later sessions will change — a new or empty one the user is starting counts, as *Empty input* below says. When this skill runs where there is none — a chat with no workspace, a home or scratch folder, a folder holding one finished artifact, or a question that does not concern the folder the session runs in — say so, ask which folder to set up, and write nothing until one is named.

Aim for a good starting point rather than a complete record. Most of a project's past reasoning is genuinely unrecoverable; a seed that is honest about what it could not recover is worth far more than one that reads complete and isn't.

## Flags

`--no-mine` skips the seed; the wiring and the verification harness install as usual. Mining otherwise runs wherever there is history — a project with no commits, no docs and no code simply has nothing to seed from, which needs no flag to express.

Interpret only top-level options as flags; quoted or code-formatted mentions of them are topic text.

## What already exists governs

Read before writing, and never overwrite a surface the project already maintains:

- **`docs/adr/CONVENTIONS.md` exists** → the project has its own ADR convention. It governs. Do not replace it, and follow it for anything written this run — then compare it, per `references/UPDATE.md` → *Compare, then offer*, which covers this file, `docs/NORTH_STAR_CONVENTIONS.md`, and the context file's surfaces section alike.
- **`CONTEXT.md` exists** (or the context named by a root `CONTEXT-MAP.md`) → load it. Mined vocabulary is proposed as additions to it, never as a replacement.
- **`NORTH_STAR.md` exists** → load it. Seeded content is proposed as additions or as evidence for positions it already carries — never as a rewrite: its positions change only by an authorized ruling within explicit delegation, per the maintenance rules in `references/NORTH_STAR_FORMAT.md`.
- **`docs/adr/` holds records but there is no `CONVENTIONS.md`** → the project has an unwritten convention, and the records are the evidence of it. Infer it from them — naming scheme, which sections they carry, how they cross-reference, what the index looks like — and write the conventions file to describe *that*, adapting the shipped default rather than replacing it. Installing the default unchanged here would declare an existing corpus non-conforming, which is both wrong and the fastest way to get the file ignored. Where the corpus is inconsistent, or where following it would leave the index un-rebuildable, say so and let the user choose; never silently pick.
- **A project context file already carries some of this wiring** → add the wiring it lacks and leave the rest alone; where its surfaces section is present but differs from the template, compare and offer rather than rewrite, per `references/UPDATE.md` → *Compare, then offer*.

### Intended use and scoped adjustments

Read applicable project and personal instructions first. `../ticket-up/references/AUTHORITY.md`
defines assignment, delegated decisions and retained acceptance; use it for any scoped
adjustments. Setup configures how later assignments run. It does not assign project operation.

Infer intended use from the request and existing instructions before asking. Coordination here
means the `orchestrate` skill running the project's Tickets, or an outcome assigned to it, in
sessions of their own. Project-only setup needs no coordination, no Ticket store (where the
project's Tickets live: files in the repository, GitHub Issues or another tracker) and no
notification configuration. For intended coordination, load
`../ticket-up/references/STORE_CONFIG.md` and resolve through it the existing Ticket store, the
tracker it lives on, the account automation acts as, and who is told when a run needs a person,
without authoring Tickets. Discover the evidence the project already names for judging progress
on its outcome, and its notification sources; ask only material unresolved choices, and check
available access. Name any missing capability or access that would prevent starting. Where a
person wants it, use a capability the host already offers for keeping a run going until its work
is done; setup installs no scheduler.

Keep the skills' current defaults. Offer only project-specific adjustments that matter to the
intended use, stating scope, responsible actor, delegated decisions and retained decisions in
plain language. For example, direction may be delegated while acceptance of the rendered result
stays with the user. Show the exact proposed text and destination before persisting a new user
choice: shared rules in the detected project context file or its reachable companion, personal
rules in the existing private instruction mechanism. Reuse decisions already supplied; no empty
policy document or exhaustive permission matrix is required.

When a person accepts coordination, or asks for scoped adjustments, ask which decisions they
retain. Capture each as a principle with an example they give, not a closed list, and show the
proposed text before writing it into the existing scoped-instructions slot. The owner names the
set. Project-only setup gets no such prompt. If the project already
coordinates and its scoped instructions name no retained decisions, offer that same ask as its
own item when a person is present.

A run with no person present does not treat absence as wanted or as an answer. Inference from
existing instructions does not make an optional item wanted when no person is present. Optional
items that write delegated or retained decisions, or that prepare coordination, are owner-judgment
items: only a person's answer, or a choice the project already records, settles them. They are
flagged in the report and not written. Mechanical items, the steps the assignment to run this
setup already covers, may proceed where the assignment authorizes them; the run flags the rest,
and the surfaces version is not written until each flagged item has an answer.

### The surfaces version

The project-surfaces section in the context file records one surfaces version, as the comment the template carries. Read it from the file on disk: a host that loads the context file into the session may strip HTML comments, so the copy already in context can show no version where the file records one. `references/CHANGES.md` lists each version in one line, the last being the newest, and `references/changes/vN.md` holds what version N gives an installed project; read only the files after the recorded version. The line says which surfaces the project carries, so only this skill writes it — when it installs, and when it finishes an update. Content written under the surfaces — a new record, a glossary entry, a recipe — never changes it.

figure-out records a declined update offer on a line of its own, `<!-- setup-project update declined through vN -->`. That decline line only stops figure-out repeating its offer: it says nothing about what the project carries, so this run reads no version from it, and removes it when it writes the surfaces version. A project-surfaces section holding nothing but a version line, with or without decline lines beside it, was left by an earlier figure-out decline, not by this skill: read its version line as a decline line through that version and the project as recording no version, and install the section.

The recorded version also decides which differences in a copy the project owns are offered, per `references/UPDATE.md` → *Compare, then offer*.

### The update pass

When the context file records a surfaces version, or the project already has `docs/adr/CONVENTIONS.md`, `docs/NORTH_STAR_CONVENTIONS.md`, `NORTH_STAR.md` or a project-surfaces section in the context file, the run is an update: read `references/UPDATE.md` before offering or writing anything. It says what the update covers, how each gap is offered and reported, and how a copy the project owns is compared. Which upgrade guides it adds up depends on the version the project records:

| Recorded version | Loads |
|---|---|
| vN, older than the newest `CHANGES.md` lists | `references/upgrades/vN-to-current.md`, then each later `vM-to-current.md` in that folder |
| the newest | no guide |
| none | no version guide |

Whatever version is recorded, the newest included, also load `references/upgrades/MOVE_TO_HARNESS.md` while the project has a feature map, a reader-task list or a verification-surface README to move, and offer the move as one item — the one `v3-to-current.md` names, where that guide loads: the project's shape, not the number it records, says whether the move is owed. Likewise load `references/upgrades/RESHAPE_NORTH_STAR.md` while the project's `NORTH_STAR.md` is still in the older nine-field form, and offer its reshape as one item: an owner who has not yet ruled its lines is offered it again on every run.

## The run

Steps 2 to 6 install what a project lacks. On a project that already carries surfaces, they run only through *The update pass* above: nothing in them is written unless the update offered it and the user accepted it or, for a mechanical item, the assignment authorizes it — or, for the harness step 4 installs by default, the user was told and did not opt out. A surface the project lacks entirely — no conventions file, no North Star, no surfaces section, or no recommended verification harness, whatever the project verifies with now — is installed by its step when accepted, offered as one item of the update whatever version the project records.

1. **Resolve the project context file.** Its name differs by CLI — `CLAUDE.md`, `AGENTS.md`, or another — so detect it rather than assuming. The active-host detection and context-file resolution rules live in `../review-code/references/context-file-adherence.md`; read them and use them. Resolve the glossary through `CONTEXT-MAP.md` where present, otherwise `CONTEXT.md`. Preserve an existing glossary; create a missing one with the known project name, one-line purpose, and empty Language section before mining or wiring. This also runs under `--no-mine`.

2. **Install the ADR conventions**, unless `docs/adr/CONVENTIONS.md` already exists. Copy `../figure-out/references/ADR_FORMAT.md` to `docs/adr/CONVENTIONS.md`, changing its opening as follows and nothing else:
   - retitle the heading to `# ADR Conventions`;
   - keep the sentence describing what ADRs are;
   - replace both the self-contained note and the whole `## Precedence` section with one paragraph stating that this file is the project's ADR convention and governs, that everything needed to decide and write is here with no tool or prior knowledge required, that tooling carrying its own defaults defers to it, and — since that deference makes this copy a fork no sync will update — that keeping it current is the project's job, with re-running the setup that installed it offered as one way to see what a current default carries.

   Everything from `## When a decision deserves a record` onward travels verbatim — the file is written to be self-sufficient, and a reader with no tooling must be able to follow it end to end.

   Where records already exist, this is not a straight copy: reconcile the default with the practice those records show, per *What already exists governs* above, and surface any divergence you had to resolve.

   Where the project keeps automated checks — a test suite, or a verification harness — offer one check that rebuilds the ADR index by the conventions' rebuild rules, and the North Star's *Strategy choices in force* list by its conventions where the North Star keeps one, signposts (each record's `Revisit when` line) included, and fails on any difference from the files. A derived list rebuilt by hand drifts the way a hand-kept index does, and the check is what holds it for contributors who never read the rule. Write it in the project's own test form, or as a harness scenario. A project with no automated checks gets none; the rebuild stays part of writing a record. Where a decision record decides keeping the index or the list, name the check in that record's `Enforced by` line once it is built.

3. **Install the North Star**, unless `NORTH_STAR.md` already exists (then only propose per *What already exists governs*). Load `references/NORTH_STAR_FORMAT.md` — it carries the document skeleton, the six sections, the four kinds of line a North Star may hold, the four position states, and the maintenance rules — and write `NORTH_STAR.md` at the repository root. Seed it per the reference's *Produce it honestly*, which says what may be seeded, what the owner is asked, and which sections wait for their own later investigation; the `empty` positions are the doc's to-do list. Artifact-seeding is mining: under `--no-mine`, write the bare skeleton instead — every section `empty` with its filling condition. Alongside the doc, emit the project-owned conventions copy at `docs/NORTH_STAR_CONVENTIONS.md` unless one exists (then it governs — same rule as the ADR conventions): the reference's content retitled `# North Star Conventions`, its ownership section replaced by one paragraph stating that this file is the project's North Star convention and governs, self-contained with no tooling required, and a fork that no sync will update — keeping it current is the project's job, with re-running the setup that installed it offered as one way to see what the current default carries, and the installer-facing *project-surfaces section* chapter dropped — a project maintainer meets that section in the context file itself.

4. **Install the verification harness** where the project holds something future runs will change and its context file records no verification choice. It is the recommended default, so install it unless the user opts out to keep verifying the project's own way; say so before writing it, with what it adds, so the user can opt out. Where the project already verifies its own way — an own-way bullet, or tests, scripts or a harness of its own making — offer the upgrade to the recommended harness all the same: it adopts those checks by delegation, each becoming a recipe scenario that calls the project's own command, so nothing the project trusts is replaced; name any earlier opt-out, and on a decline leave the bullet and the checks as they are, recording the bullet of a harness found on disk that had none. On install, load `references/VERIFICATION_HARNESS.md` and follow its *What setup creates, and what runs build* section; its *The parts* says how the tool's default language is offered and overridden. On an opt-out, name the project's commands and steps with the user and record them in the own-way form of the verification bullet in step 6, so no figure-out, define or do run offers the harness again. A project with nothing future runs will change gets none; say so in the report. This runs under `--no-mine` too: the catalog comes from the source as it stands, not from history.

5. **Seed, unless `--no-mine` or the project records a surfaces version** (an update mines only as `references/UPDATE.md` says). Load `references/MINING.md` and follow it. It covers what each source can and cannot yield, how a record says so when the reasoning is gone, and why glossary candidates are ratified rather than written. Then, under `--no-mine` too, offer principles skills for the project's high-signal areas per `references/PRINCIPLES_SKILLS.md`: under `--no-mine`, or with no history, only the areas it names for a project with no history to read.

6. **Wire the project context file.** Emit the project-surfaces section per `references/NORTH_STAR_FORMAT.md` → *The project-surfaces section*, whose template is the single source of the emitted text. Include only accepted scoped adjustments, as its optional entry permits — this file is read on every session, so every line here is a permanent cost — and write imports as *the project context file*'s imports rather than a specific harness's filename.

7. **Report what landed**, what needs the person first: which owner-judgment items were flagged unanswered, and any unavailable access or capability with its next step. Then the configured scope and retained decisions, and, where coordination was set up, that setup has started no operations; then what was installed, the surfaces version written, each principles skill offered with the lines written and the context-file sort, what the update offered and what the user chose for each item, the items already in place as one count, whether the project took the harness or kept its own way, and for a harness what it adopted and catalogued, the ask-first choice, and which scenario its proof run drove, and what was seeded. Where seeding ran, the *Reporting* section of `references/MINING.md` specifies what that half must cover. Give the comparison's outcome either way, per `references/UPDATE.md` → *Compare, then offer*: which sections of which copies differ from what the steps would emit today and what the user chose for each, or plainly that the copies were compared and already carry everything the current defaults do — an unreported comparison reads exactly like one that never ran, which is the failure this whole step exists to prevent. A run that skipped seeding reports the actual reason: `--no-mine` skipped it, the project already records a surfaces version, or no history was available.

## Empty input

Pointed at a repository with no commits, no documentation and no code, install the wiring and stop: the conventions file, a `CONTEXT.md` holding the project name, a one-line purpose and an empty Language section, a `NORTH_STAR.md` skeleton whose every section is `empty` with its filling condition, and the context-file section with the surfaces version. There is no artifact yet for a harness to check, so record its form of the verification bullet as the recommended default unless the user opts out here, and the first run that builds something to check builds the harness's first parts, starting with the command that bullet names. Say that nothing was seeded because there was nothing to seed from. This is the greenfield case and it is a success, not a degraded run — a project that starts with its surfaces already wired is exactly the point.

With no project name or purpose available, ask for them. They are one line each and guessing them wrong seeds the glossary with a false premise.

## Gotchas

- **Rich history is not typical history.** A project whose pull requests carry design rationale is unusual. Do not calibrate the run's ambition on the first well-documented commit you find.
- **Do not restate the conventions in the project context file.** That file is loaded on every session; the conventions file is loaded when someone needs it. Duplicating the detail costs every session and creates a second copy that drifts.
