# ADR: Locate the ticket store by convention, not configuration

## Status
Accepted

## Area
Ticketing

## Context

`ticket-up` persists a venue choice to `store-config.md` "inside this skill's directory", falling back to the store root only "if that directory isn't writable (managed plugin installs)". The fallback trigger is writability, not scope — so the same instruction produces a repo-scoped config under a development symlink install and a single config shared across every repository under a marketplace plugin install. In real use the config was written inside the skill, where it cannot describe more than one repository.

The venue is also never asked for. The store section opens with "**Files (default).** No configuration" and branches to GitHub only "when the user chooses GitHub", so a run whose venue was never stated silently writes files. The only instruction to ask is subordinate to a config that does not exist on a first run.

Both gaps surfaced the same way: users hand-added a "this repo tracks work in GitHub" section to each repository's project context file, carrying the fact between repositories themselves.

## Decision

The store is found by convention rather than by a pointer. Skills read one fixed repo-relative path, `tickets/store-config.md`. On the first run in a repository with no config there, the venue is asked for once and the answer written to that path; later runs read it without asking.

The always-loaded project context file is not this fact's home. It serves only as the escape hatch for a project that deliberately keeps its store elsewhere — and needs no mechanism to do so, because it is already in context when the skill runs.

## Alternatives Considered

- **Make the project context file the venue's home**: record "this repository tracks work in GitHub Issues" where every session already reads — Rejected: a fixed conventional path makes the pointer unnecessary, and a custom tracker's operating details would tax every session for something only ticketing runs read.
- **Keep the skill-directory sidecar and fix only its fallback trigger**: swap the writability test for an install-mode test — Rejected: scope is the property that matters, and a location whose repo-scoping depends on install mode is wrong in both modes for different reasons.
- **Detect the venue instead of recording it**: a store is largely self-identifying once it exists — Rejected: the first run has nothing to detect, and a repository holding both a stale `tickets/` directory and live issues is ambiguous.

## Consequences

### Positive
- One lookup location, identical across installs, that cannot leak configuration between repositories.
- No hand-written context-file section per repository.
- A first run can no longer write the wrong venue silently.

### Negative
- A repository whose store is GitHub gets a `tickets/` directory holding only a config file.
- The first run in every repository costs one question.

## Source
- Session: figure-out on ticketing-skills feedback (2026-08-09)
- Related: 20260806-retire-decision-map-for-ticket-up-and-ticket-store
