---
name: setup-project
description: 'Set a project up with the surfaces manifest-dev works from — a North Star, a glossary, ADR conventions, a verification harness, and the context-file wiring that makes every session use them — seeding them from the project''s own history where there is any, and keep a set-up project sound by auditing it against the setup the references describe and offering each gap, marking what changed since the surfaces version it records. Use when a repository has no CONTEXT.md or decision records, when adopting manifest-dev in an existing codebase, when starting a new project, when a set-up project records no surfaces version or an older one, or when the user asks to set up the project, re-run the setup to check it is sound, bootstrap ADRs, or reconstruct decisions from history.'
---

Install the project surfaces a repository needs so that every future session — and every teammate, with or without manifest-dev — works from the same direction, the same vocabulary, and the same decision record.

Three things get installed, and only the first is essential:

- **The wiring** — an ADR conventions file the project owns, a glossary, a North Star (the project's standing strategy surface: who it is for, what it promises, what winning means), and a project-context-file section that makes sessions read and maintain all three and records the surfaces version the project carries. This runs on every project, including one with no history at all.
- **A verification harness** — the project's one command for checking that what future runs will change still does its job, with a recipe per thing it checks, seeded from what the project already has, per `references/VERIFICATION_HARNESS.md`.
- **A seed** — vocabulary and decision records reconstructed from the project's own history. This runs wherever there is history to read, and it is enrichment on top of the wiring, never a substitute for it.

All of this is for a project: a repository or working folder holding, or about to hold, work later sessions will change — a new or empty one the user is starting counts, as *Empty input* below says. When this skill runs where there is none — a chat with no workspace, a home or scratch folder, a folder holding one finished artifact, or a question that does not concern the folder the session runs in — say so, ask which folder to set up, and write nothing until one is named.

Aim for a good starting point rather than a complete record. Most of a project's past reasoning is genuinely unrecoverable; a seed that is honest about what it could not recover is worth far more than one that reads complete and isn't.

## Flags

`--no-mine` skips the seed and installs the wiring alone. Mining otherwise runs wherever there is history — a project with no commits, no docs and no code simply has nothing to seed from, which needs no flag to express.

Interpret only top-level options as flags; quoted or code-formatted mentions of them are topic text.

## What already exists governs

Read before writing, and never overwrite a surface the project already maintains:

- **`docs/adr/CONVENTIONS.md` exists** → the project has its own ADR convention. It governs. Do not replace it, and follow it for anything written this run — then compare it, per *Compare, then offer* below, which covers this file, `docs/NORTH_STAR_CONVENTIONS.md`, and the context file's surfaces section alike.
- **`CONTEXT.md` exists** (or the context named by a root `CONTEXT-MAP.md`) → load it. Mined vocabulary is proposed as additions to it, never as a replacement.
- **`NORTH_STAR.md` exists** → load it. Seeded content is proposed as additions or as evidence for positions it already carries — never as a rewrite: its positions change only by the owner's ruling, per the maintenance rules in `references/NORTH_STAR_FORMAT.md`.
- **`docs/adr/` holds records but there is no `CONVENTIONS.md`** → the project has an unwritten convention, and the records are the evidence of it. Infer it from them — naming scheme, which sections they carry, how they cross-reference, what the index looks like — and write the conventions file to describe *that*, adapting the shipped default rather than replacing it. Installing the default unchanged here would declare an existing corpus non-conforming, which is both wrong and the fastest way to get the file ignored. Where the corpus is inconsistent, or where following it would leave the index un-rebuildable, say so and let the user choose; never silently pick.
- **A project context file already carries some of this wiring** → add the wiring it lacks and leave the rest alone; where its surfaces section is present but differs from the template, compare and offer rather than rewrite, per *Compare, then offer* below.

### The surfaces version

The project-surfaces section in the context file records one surfaces version, as the comment the template carries. Read it from the file on disk: a host that loads the context file into the session may strip HTML comments, so the copy already in context can show no version where the file records one. `references/CHANGES.md` lists what each version gives an installed project. Only this skill writes that line — when it installs, and when it finishes an update — plus figure-out when the user declines a whole update offer. Content written under the surfaces — a new record, a glossary entry, a recipe — never changes it.

Where the project records a version, a difference in a copy the project owns can be attributed: content the shipped text gained since that version is new and is offered, and any other difference is the project's own choice and stays. Where the project records no version, compare as *Compare, then offer* below describes.

### The update pass

On a project that already carries surfaces, the run is an update, and it aims for the best setup the references describe, not only for what changed since the recorded version. Someone running this skill is asking whether their setup is sound, so a recorded version — even the newest — never ends the run on its own. The best setup is the one this project needs now, not every piece the references describe: each offer names the need it serves today — a surface the project's work relies on, a check that already exists, a term in use — and an item with no such need is not a gap, however the references read. Surfaces grow with the work that needs them. It covers:

- **What changed since the recorded version** — marked as new, and offered as the upgrade guide for that version says. A guide goes straight to the newest version, so a project never passes through a shape a later version replaced. With no recorded version, nothing is offered by version: the comparison against what the steps emit today finds the gaps, and no shape a later version replaced is offered. Which guide loads:

  | Recorded version | Loads |
  |---|---|
  | vN, older than the newest in `CHANGES.md` | `references/upgrades/vN-to-current.md` |
  | the newest | no guide |
  | none | no version guide; `references/upgrades/MOVE_TO_HARNESS.md` when the project has a feature map, a reader-task list or a verification-surface README to move |

- **The conventions, the North Star conventions, and the surfaces section** — by comparison, per *Compare, then offer* below.
- **The records written under the conventions** — only their editable fields, and only on records in effect, as the conventions' lifecycle defines them. Add `Enforced by` where a check already holds the record's decision: code that cites the record, or a lint or test configuration that pins what it decided — one that would fail if the decision were reversed. Where that check has no comment citing the record, offer one. Leave a record with no check found without the line. Add a missing `Area`. Rebuild the index per the conventions. Never change a record's body.
- **The verification harness** — one, where the project holds something future runs will change, seeded by step 4 where it is missing; for one that exists, only its parts: the tool's subcommands, settings with the ask-first choice, recipes for what users reach that have none, the repository check, and its bullet in the project-surfaces section. Adopt the verification assets the project already has by delegation rather than building a second set beside them. How much of the product its scenarios can drive grows with the work that needs it, so the update offers no new scenario, drive or proof improvement: when work touches a recipe it cannot trust, figure-out raises it and that work's Manifest builds the missing piece.
- **The glossary** — additions only, ratified as mining describes.

Offer each gap as its own item: what the reference asks for, the need it serves here, what the project has, and what accepting writes. Show each backfilled line and each harness change, and write only what the user accepts. A missing surface is seeded by step 4 when accepted. Report an item the project already satisfies as in place, without offering it. Nothing records a decline, so an item declined on an earlier run is offered again; say so when the project's history shows it. Mine only where the project records no version, and offer only candidates its glossary and records do not already settle. Once every offered item has an answer, write the newest surfaces version and report what was offered, applied and declined.

### Compare, then offer

A conventions file this skill emitted is a copy the project owns, so nothing overwrites it — which makes it a fork that no later improvement reaches on its own. Re-running here is the moment someone is deliberately asking whether their setup is current, so compare rather than skip, for each surface already present: the ADR conventions, the North Star conventions, and the surfaces section in the project context file.

Compare the project's copy against **what this skill's own steps would emit today** — steps 2, 3, and 6 below — never against the raw reference. A correct copy already differs from its reference wherever those steps changed something on the way out: a retitled heading, whatever that surface's step replaces, any chapter it drops, and for the context file's section, the adaptation to what the project actually has. Comparing against the raw file reports every one of those on every run and buries the real difference. **Both reference files mark the spans a copy reproduces verbatim with a fixed-boundary comment** naming what the steps replace or drop at that point; read those to derive what a correct copy looks like rather than reconstructing it from prose. Compare section by section and by meaning rather than line by line — a project that reworded or reflowed its copy has not fallen behind.

Without a recorded surfaces version, a project holds no record of what the reference said when its copy was written, so a difference cannot be attributed: the reference may have gained something, or the project may have removed it deliberately. Present each difference as what the current default says, each accepted or declined on its own, for the user to take or leave — never as a defect, a staleness, or a non-conformance, and never as a single take-it-all offer, since one accepted batch can quietly overwrite a rule the project ruled for itself. Write only what the user accepts. A project is entitled to keep its own wording permanently, and its copy governs whether or not it matches.

Porting a conventions file is rarely a one-file edit: it governs the documents written under it, so when an accepted difference changes what something is called or how it is written, say which of those documents now read as out of step.

## The run

Steps 2 to 6 install what a project lacks. On a project that already carries surfaces, they run only through *The update pass* above: nothing in them is written unless the update offered it and the user accepted. A surface the project lacks entirely — no conventions file, no North Star, no surfaces section, no verification harness — is installed by its step when accepted, offered as one item of the update whatever version the project records.

1. **Resolve the project context file.** Its name differs by CLI — `CLAUDE.md`, `AGENTS.md`, or another — so detect it rather than assuming. The active-host detection and context-file resolution rules live in `../review-code/references/context-file-adherence.md`; read them and use them. Resolve the glossary through `CONTEXT-MAP.md` where present, otherwise `CONTEXT.md`. Preserve an existing glossary; create a missing one with the known project name, one-line purpose, and empty Language section before mining or wiring. This also runs under `--no-mine`.

2. **Install the ADR conventions**, unless `docs/adr/CONVENTIONS.md` already exists. Copy `../figure-out/references/ADR_FORMAT.md` to `docs/adr/CONVENTIONS.md`, changing its opening as follows and nothing else:
   - retitle the heading to `# ADR Conventions`;
   - keep the sentence describing what ADRs are;
   - replace both the self-contained note and the whole `## Precedence` section with one paragraph stating that this file is the project's ADR convention and governs, that everything needed to decide and write is here with no tool or prior knowledge required, that tooling carrying its own defaults defers to it, and — since that deference makes this copy a fork no sync will update — that keeping it current is the project's job, with re-running the setup that installed it offered as one way to see what a current default carries.

   Everything from `## When a decision deserves a record` onward travels verbatim — the file is written to be self-sufficient, and a reader with no tooling must be able to follow it end to end.

   Where records already exist, this is not a straight copy: reconcile the default with the practice those records show, per *What already exists governs* above, and surface any divergence you had to resolve.

3. **Install the North Star**, unless `NORTH_STAR.md` already exists (then only propose per *What already exists governs*). Load `references/NORTH_STAR_FORMAT.md` — it carries the document skeleton, the nine fields, the four position states, and the maintenance rules — and write `NORTH_STAR.md` at the repository root. Seed only what the repository's own artifacts evidence, per the reference's *Produce it honestly* rules: each seeded position carries `hypothesis` or `evidence` with the artifact named, every unanswered field stays `empty` with its filling condition, and nothing is invented. The interview asks nothing beyond name-and-purpose-grade statables — the hard fields are their own later investigations, and the `empty` positions are the doc's to-do list. Artifact-seeding is mining: under `--no-mine`, write the bare skeleton instead — every field `empty` with its filling condition. Alongside the doc, emit the project-owned conventions copy at `docs/NORTH_STAR_CONVENTIONS.md` unless one exists (then it governs — same rule as the ADR conventions): the reference's content retitled `# North Star Conventions`, its ownership section replaced by one paragraph stating that this file is the project's North Star convention and governs, self-contained with no tooling required, and a fork that no sync will update — keeping it current is the project's job, with re-running the setup that installed it offered as one way to see what the current default carries, and the installer-facing *project-surfaces section* chapter dropped — a project maintainer meets that section in the context file itself.

4. **Seed the verification harness** where the project holds something future runs will change. Load `references/VERIFICATION_HARNESS.md` and follow its *What setup creates* section, which also says how the tool's default language is offered and overridden. A project with nothing future runs will change gets none; say so in the report. This runs under `--no-mine` too: the catalog comes from the source as it stands, not from history.

5. **Seed, unless `--no-mine` or the project records a surfaces version** (an update mines only per *The update pass*). Load `references/MINING.md` and follow it. It covers what each source can and cannot yield, how a record says so when the reasoning is gone, and why glossary candidates are ratified rather than written.

6. **Wire the project context file.** Emit the project-surfaces section from `references/NORTH_STAR_FORMAT.md` — its template is the single source of the emitted text; adapt it to what the project has, extend an existing section rather than duplicating one, and add nothing beyond it, because this file is read on every session and every line here is a permanent cost. The template covers the surfaces version, the North Star's residency and maintenance asymmetry, the glossary's residency, the decision-record triggers, the one-act write rule, and the verification command with when to run it; where the host supports imports, the session-start reads become imports, written as *the project context file*'s imports rather than a specific harness's filename.

7. **Report what landed** — what was installed, the surfaces version written, what the update offered and what the user chose for each item, what the harness adopted and catalogued, the ask-first choice, and which scenario its proof run drove, and what was seeded. Where seeding ran, the *Reporting* section of `references/MINING.md` specifies what that half must cover. Give the comparison's outcome either way, per *Compare, then offer* above: which sections of which copies differ from what the steps would emit today and what the user chose for each, plainly that the copies were compared and already carry everything the current defaults do, or that there was nothing to compare because none of these surfaces existed yet — an unreported comparison reads exactly like one that never ran, which is the failure this whole step exists to prevent. A run that skipped seeding reports the actual reason: `--no-mine` requested wiring only, or no history was available.

## Empty input

Pointed at a repository with no commits, no documentation and no code, install the wiring and stop: the conventions file, a `CONTEXT.md` holding the project name, a one-line purpose and an empty Language section, a `NORTH_STAR.md` skeleton whose every field is `empty` with its filling condition, and the context-file section with the surfaces version. There is no artifact yet, so there is no verification harness; the first run that builds something to check creates it. Say that nothing was seeded because there was nothing to seed from. This is the greenfield case and it is a success, not a degraded run — a project that starts with its surfaces already wired is exactly the point.

With no project name or purpose available, ask for them. They are one line each and guessing them wrong seeds the glossary with a false premise.

## Gotchas

- **A codebase supplies unlimited nouns.** The temptation is to produce an impressive glossary. A glossary is read on every session forever, so an entry that is merely accurate is a permanent cost for no benefit. Under-produce deliberately.
- **Rich history is not typical history.** A project whose pull requests carry design rationale is unusual. Do not calibrate the run's ambition on the first well-documented commit you find.
- **Reconstructed reasoning is the failure mode.** Writing a plausible rationale for a decision whose actual rationale is lost produces a record that reads authoritative and is fiction. Recording the decision without the reasoning is correct; inventing the reasoning is not.
- **Do not restate the conventions in the project context file.** That file is loaded on every session; the conventions file is loaded when someone needs it. Duplicating the detail costs every session and creates a second copy that drifts.
