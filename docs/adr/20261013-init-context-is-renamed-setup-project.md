# ADR: init-context is renamed setup-project

## Status
Accepted

## Area
Project context

## Decided by
The user

## Context
The skill installs and later compares a project's durable surfaces: the ADR conventions, the North Star, the glossary, the context-file wiring, and now the verification surface. Its name described less than that. "context" covered one of the surfaces and already meant three things in this repository — the project context file, the glossary file, and an agent's context window. "init" suggested a one-time step, while the skill also runs again to compare a project's copies against what it would emit today. Users reach the skill through figure-out's offer rather than by typing it, so the name appears mostly in that offer's text and to maintainers.

## Decision
- The skill is renamed `setup-project`.
- Every reference in shipped skills, READMEs, plugin metadata, the glossary, the context file, tests, and the generated distribution copies changes in the same change.
- The change is breaking for anyone who invokes the old name, so the plugin takes a major version bump.
- Decision records that name `init-context` keep the old name; they describe what was decided at the time.
- Installed projects carry no reference to the old name: it appears only in maintainer comments above the copy boundaries of the shipped formats.

## Alternatives Considered
- **Keep `init-context`**: the name keeps describing a fraction of the job.
- **`project-surfaces`**: matches the glossary term, but "surface" reads as a metaphor to a newcomer.
- **`project-memory`**: easy to confuse with harness memory files and Taste.
- **`bootstrap-project`**: suggests a one-time step again.

## Consequences

### Positive
- The name says what the skill does in words a newcomer knows.

### Negative
- A major version bump for a rename.
- Older records and outside links use the old name.

## Enforced by
none — a one-time rename; decision records keep the old name on purpose.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20260809-init-context-skill-lives-in-core
