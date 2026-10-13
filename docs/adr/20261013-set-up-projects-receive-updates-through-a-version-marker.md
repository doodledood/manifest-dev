# ADR: Set-up projects receive updates through a recorded version, offered by figure-out

## Status
Accepted

## Area
Project context

## Decided by
The user

## Context
setup-project writes copies that each project owns — the ADR conventions, the North Star conventions, the context-file wiring — so no later improvement reaches them by itself. Re-running the skill compares the copies, but two gaps remained. figure-out offered the skill only when a project had no glossary and no decision records at all, so a project that was already set up got an update only when someone remembered to ask for one. And because a project recorded nothing about what the shipped text said when its copy was written, a difference could not be attributed: the shipped text might have gained something, or the project might have removed it on purpose. The comparison also stopped at the conventions themselves, not the records written under them or the project's verification surface.

## Decision
- setup-project records, in the project, the version of the surfaces it installed or last updated, as one line.
- Each shipped version carries a short list of what it added or changed for installed projects.
- At bootstrap, figure-out's docs mode compares the recorded version with the shipped one. When the project is behind, it offers setup-project's update and lists only what changed since the recorded version. An unattended run flags the offer and does not run it.
- Accepting or declining an item both advance the recorded version, so a declined item is not offered again.
- With a recorded version, a difference can be attributed: content the shipped text gained since that version is offered as new; anything else that differs is the project's own choice and stays.
- The update covers the surfaces (conventions, North Star conventions, context-file wiring, glossary additions); the editable fields of existing records — `Enforced by` candidates drawn from code that cites a record and from lint and test configuration, Area, and the index; and the verification surface, where existing verification assets are adopted and extended rather than duplicated. Record bodies are never rewritten.
- A project with no recorded version falls back to the neutral comparison: each difference is offered as what the current default says.

## Alternatives Considered
- **Detect missing features with a checklist**: it offers declined items again on every run, and the checklist grows with every release.
- **Rely on someone re-running the skill**: it depends on memory, so set-up projects stop receiving improvements.
- **Overwrite the project's copies**: the project owns them and may have changed them on purpose.

## Consequences

### Positive
- Set-up projects receive improvements through the normal workflow.
- A comparison can tell new shipped content from a deliberate project change.

### Negative
- One line written into each project.
- Every release has to keep the change list current.
- A project that deletes the recorded version loses attribution until the next update.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20261013-init-context-is-renamed-setup-project
- Related: 20260809-adr-conventions-ship-as-project-knowledge
- Related: 20261013-new-capabilities-live-inside-the-four-workflow-entry-points
