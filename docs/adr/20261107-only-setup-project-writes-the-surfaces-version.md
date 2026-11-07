# ADR: Only setup-project writes the surfaces version; figure-out records a declined offer apart

## Status
Accepted

## Area
Project context

## Decided by
An agent, under the owner's delegation to fix the state-machine audit's findings that are not nits; no review

## Context
20261013-set-up-projects-receive-updates-through-a-version-marker let figure-out write the newest surfaces version when the user declined its whole update offer, appending a project-surfaces section holding only that line where the project had none, so the same offer was not made again. That record's premise was that the version line records what was offered. 20261014-setup-project-audits-the-whole-setup-when-run changed that premise: a setup-project run audits the whole setup, re-offers declined items, and attributes every difference in a project-owned copy by the recorded version — content gained after it is offered, anything else is the project's own choice. The line therefore has to say which surfaces the project carries.

A decline written into it breaks that. In a project that was never set up, a glossary capture creates `CONTEXT.md`; the next session finds a glossary and no version, offers the update, and on a decline appends a section that claims the newest version and holds no wiring. A later setup-project run then finds a section and a recorded version, so it offers only content gained after the newest version — nothing — never offers the North Star, glossary, records or verification bullets, and skips seeding, which runs only where no version is recorded. A project set up at an older version loses the same way: content between its version and the newest is attributed to the project and never offered, and a pre-v4 project's move into the harness, which loads by version, is skipped.

## Decision
- The surfaces version line says which surfaces the project carries, and only setup-project writes it — when it installs, and when it finishes an update.
- figure-out records a decline of its whole update offer on a line of its own, `<!-- setup-project update declined through vN -->`, beside the version line or, with no section, at the end of the context file. It never creates the section. The line only stops figure-out repeating its offer: figure-out offers when neither the recorded nor the declined version is the newest, and lists what the versions after the later of the two give.
- setup-project reads no version from a decline line and removes it when it writes the version. A project-surfaces section holding nothing but a version line, with or without decline lines beside it, was left by an earlier figure-out decline: setup-project and figure-out read its version line as a decline line through that version, with no version recorded, so setup-project installs the section and runs as it does wherever no version is recorded.
- A version line inside a full section may also have been advanced by such a decline. Where the project's history shows the number last changed in a commit that changed nothing else in the section or in the copies setup-project emits, setup-project reads the number from before that commit and says so; where no history shows how the number was set, it takes the line as written and says the project can remove it for a full comparison. Reading too old a version only offers again what the project may have ruled out; reading too new hides gaps as the project's choice.
- This amends 20261013-set-up-projects-receive-updates-through-a-version-marker: its bullets that let figure-out write the version line on a decline, and that let a decline advance the recorded version, no longer hold. A declined item is not offered again by figure-out; setup-project offers it again, as 20261014-setup-project-audits-the-whole-setup-when-run already decides.

## Alternatives Considered
- **Keep the decline in the version line, but never create a section**: closes the never-set-up case, but a project at an older version still loses everything between its version and the newest from setup-project's attribution.
- **Treat any section without the template's bullets as unrecorded**: repairs the symptom in setup-project only, and leaves the version line meaning two things that a reader cannot tell apart.
- **Write nothing on a decline**: figure-out would repeat the offer every session in a project that has turned it down.

## Consequences

### Positive
- A setup-project run after any number of figure-out declines installs the wiring a project lacks, seeds a project never set up, and offers every change the project does not carry.
- Legacy sections a decline left behind are recognized by their shape and repaired on the next setup-project run.
- A version a decline advanced inside a full section is read back from history where history shows it.

### Negative
- Where a setup-project update changed only the version line, a later run reads the version before it, so it marks that version's items new again and repeats a once-only offer that version made.
- Without history, an advanced version stays hidden until a person removes the line.
- One more line can appear in a project's context file.
- A project whose version line is older than the newest keeps saying so after a decline, and define's report names the older version.

## Enforced by
partly — `tests/test_setup_project_versions.py::test_only_setup_project_writes_the_surfaces_version` fails when a shipped skill other than setup-project names the version line's form, the project-surfaces section heading or a write into the version line, and when figure-out and setup-project name the decline line differently; whether a run reads the lines as written stays judgment.

## Source
- Session: state-machine audit of setup-project and figure-out's docs mode, with a model of the surfaces-version machine.
- Amends 20261013-set-up-projects-receive-updates-through-a-version-marker
- Related: 20261014-setup-project-audits-the-whole-setup-when-run
