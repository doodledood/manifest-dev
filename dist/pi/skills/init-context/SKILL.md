---
name: init-context
description: 'Set a project up with the surfaces manifest-dev works from — a glossary, ADR conventions, and the context-file wiring that makes every session use them — seeding them from the project''s own history where there is any. Use when a repository has no CONTEXT.md or decision records, when adopting manifest-dev in an existing codebase, when starting a new project, or when the user asks to initialize project context, bootstrap ADRs, or reconstruct decisions from history.'
---

Install the project surfaces a repository needs so that every future session — and every teammate, with or without manifest-dev — works from the same vocabulary and the same decision record.

Two things get installed, and only the first is essential:

- **The wiring** — an ADR conventions file the project owns, a glossary, and a project-context-file section that makes sessions read and maintain both. This runs on every project, including one with no history at all.
- **A seed** — vocabulary and decision records reconstructed from the project's own history. This runs wherever there is history to read, and it is enrichment on top of the wiring, never a substitute for it.

Aim for a good starting point rather than a complete record. Most of a project's past reasoning is genuinely unrecoverable; a seed that is honest about what it could not recover is worth far more than one that reads complete and isn't.

## Flags

`--no-mine` skips the seed and installs the wiring alone. Mining otherwise runs wherever there is history — a project with no commits, no docs and no code simply has nothing to seed from, which needs no flag to express.

Interpret only top-level options as flags; quoted or code-formatted mentions of them are topic text.

## What already exists governs

Read before writing, and never overwrite a surface the project already maintains:

- **`docs/adr/CONVENTIONS.md` exists** → the project has its own ADR convention. It governs. Do not replace it; follow it for anything written this run, and skip the conventions step.
- **`CONTEXT.md` exists** (or the context named by a root `CONTEXT-MAP.md`) → load it. Mined vocabulary is proposed as additions to it, never as a replacement.
- **`docs/adr/` holds records but there is no `CONVENTIONS.md`** → the project has an unwritten convention, and the records are the evidence of it. Infer it from them — naming scheme, which sections they carry, how they cross-reference, what the index looks like — and write the conventions file to describe *that*, adapting the shipped default rather than replacing it. Installing the default unchanged here would declare an existing corpus non-conforming, which is both wrong and the fastest way to get the file ignored. Where the corpus is inconsistent, or where following it would leave the index un-rebuildable, say so and let the user choose; never silently pick.
- **A project context file already carries some of this wiring** → add what is missing and leave the rest alone.

## The run

1. **Resolve the project context file.** Its name differs by CLI — `CLAUDE.md`, `AGENTS.md`, or another — so detect it rather than assuming. The detection table and per-CLI resolution order live in `../review-code/references/context-file-adherence.md`; read it and use it.

2. **Install the ADR conventions**, unless `docs/adr/CONVENTIONS.md` already exists. Copy `../figure-out/references/ADR_FORMAT.md` to `docs/adr/CONVENTIONS.md`, changing its opening as follows and nothing else:
   - retitle the heading to `# ADR Conventions`;
   - keep the sentence describing what ADRs are;
   - replace both the self-contained note and the whole `## Precedence` section with one paragraph stating that this file is the project's ADR convention and governs, that everything needed to decide and write is here with no tool or prior knowledge required, and that tooling carrying its own defaults defers to it.

   Everything from `## When a decision deserves a record` onward travels verbatim — the file is written to be self-sufficient, and a reader with no tooling must be able to follow it end to end.

   Where records already exist, this is not a straight copy: reconcile the default with the practice those records show, per *What already exists governs* above, and surface any divergence you had to resolve.

3. **Seed, unless `--no-mine`.** Load `references/MINING.md` and follow it. It covers what each source can and cannot yield, how a record says so when the reasoning is gone, and why glossary candidates are ratified rather than written.

4. **Wire the project context file.** Add a section carrying three things, and nothing else — the conventions file holds the detail, and this file is read on every session, so every line here is a permanent cost:
   - **The glossary is resident.** Import `CONTEXT.md` where the host supports imports, and state the instruction to read it at session start regardless — a host without imports still gets a trigger, and session start is one. Write it as *the project context file*, not as a specific filename.
   - **When to open the decision records.** Before settling a question the project may already have settled, and when a change contradicts or narrows an existing decision. A pointer with no trigger is how a corpus goes unread.
   - **Writing a record is one act.** The new record, the restatus of everything whose standing it changes, and the index rebuild — in one change, pointing at the conventions file for how.

5. **Report what landed**, per the *Reporting* section of `references/MINING.md`, which specifies what the report must cover. A run that skipped seeding still reports — what was installed, and that nothing was seeded because there was nothing to seed from.

## Empty input

Pointed at a repository with no commits, no documentation and no code, install the wiring and stop: the conventions file, a `CONTEXT.md` holding the project name, a one-line purpose and an empty Language section, and the context-file section. Say that nothing was seeded because there was nothing to seed from. This is the greenfield case and it is a success, not a degraded run — a project that starts with its surfaces already wired is exactly the point.

With no project name or purpose available, ask for them. They are one line each and guessing them wrong seeds the glossary with a false premise.

## Gotchas

- **A codebase supplies unlimited nouns.** The temptation is to produce an impressive glossary. A glossary is read on every session forever, so an entry that is merely accurate is a permanent cost for no benefit. Under-produce deliberately.
- **Rich history is not typical history.** A project whose pull requests carry design rationale is unusual. Do not calibrate the run's ambition on the first well-documented commit you find.
- **Reconstructed reasoning is the failure mode.** Writing a plausible rationale for a decision whose actual rationale is lost produces a record that reads authoritative and is fiction. Recording the decision without the reasoning is correct; inventing the reasoning is not.
- **Do not restate the conventions in the project context file.** That file is loaded on every session; the conventions file is loaded when someone needs it. Duplicating the detail costs every session and creates a second copy that drifts.
