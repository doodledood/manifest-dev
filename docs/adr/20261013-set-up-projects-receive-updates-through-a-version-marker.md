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
- setup-project records the version of the surfaces it installed or last updated as one line in the project-surfaces section of the project context file. That section is already the index every session reads, so it also gains one entry pointing at the project's verification surface: where it lives and which form it takes. No separate file holds the version or the paths.
- Each shipped version carries a short list of what it added or changed for installed projects. A test in this repository fails when a shipped template changes without a new version and a change-list entry, so a release cannot change what projects receive without saying so.
- Only setup-project writes the version line, when it installs or finishes an update, plus figure-out when the user declines the whole update offer. Content written under the surfaces — a new record, a glossary entry, a map entry — never changes it.
- At bootstrap, figure-out's docs mode reads the version line. When the project has surfaces but no version line, or its version is behind the shipped one, it offers setup-project's update and lists only what changed since the recorded version. A project with no surfaces at all still gets the full setup offer. An unattended run flags the offer and does not run it.
- define, which runs without figure-out on a direct request, makes the same check and names a missing or old version in its report, without stopping to run the update.
- Accepting or declining an item both advance the recorded version, so a declined item is not offered again.
- With a recorded version, a difference can be attributed: content the shipped text gained since that version is offered as new; anything else that differs is the project's own choice and stays.
- The update covers the surfaces (conventions, North Star conventions, context-file wiring, glossary additions); the editable fields of existing records — `Enforced by` candidates drawn from code that cites a record and from lint and test configuration, Area, and the index; and the verification surface, where existing verification assets are adopted and extended rather than duplicated. Record bodies are never rewritten.
- A project with no recorded version falls back to the neutral comparison: each difference is offered as what the current default says.

## Alternatives Considered
- **A separate tool-owned file such as `.manifest-dev.json`**: it repeats the paths the project-surfaces section already lists, so the two lists drift, and it marks shared project ground as belonging to one tool.
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

## Enforced by
`tests/test_setup_project_versions.py` — `test_latest_version_matches_what_setup_project_emits` and `test_surfaces_template_carries_the_latest_version` fail when an emitted template changes without a new surfaces version and change-list entry.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20261013-init-context-is-renamed-setup-project
- Related: 20260809-adr-conventions-ship-as-project-knowledge
- Related: 20261013-new-capabilities-live-inside-the-four-workflow-entry-points
