# ADR: ADR conventions ship into the repo as project knowledge, and the repo copy governs

## Status
Accepted

## Area
ADR conventions

## Context

ADR conventions lived entirely inside the plugin: `ADR_FORMAT.md` carried the write-time mechanics and `WITH_DOCS.md` carried the bar for what deserves a record. That works for a session running figure-out and for nobody else. A teammate who does not run manifest-dev has no way to learn the project's ADR practice, and the practice is exactly the kind of thing a team needs to hold in common — the value of a decision corpus comes from everyone contributing to it, not from one member's tooling.

The split between the two files also cut in the wrong place for a reader outside the workflow. `ADR_FORMAT.md` assumed the bar had already fired and pointed at `WITH_DOCS.md` for it, so a plugin-less reader following the format file reached a pointer they could not open.

Separately, this repo's own index had drifted five rows in three days despite the sole maintainer authoring the conventions himself — evidence that conventions living only where the tooling can see them do not hold even for the person who wrote them.

## Decision

The conventions become a file in the repository: `docs/adr/CONVENTIONS.md`, self-contained, covering both whether a decision deserves a record and how to write one. `init-context` emits it into any project it sets up.

The cut runs between **criteria and cadence**. Criteria travel into the repo — the worth-recording and not-worth-recording categories, the Decision Test, the template and its fields, naming, lifecycle, immutability, cross-references, granularity, retroactive records, and the index rebuild rules. Cadence stays in the skill — when a session offers to record a decision, and how the offer is phrased — because that is workflow behavior a project has no stake in.

**Where a project's conventions file exists, it governs.** A team may edit its template, fields, lifecycle or index format, and the tooling follows rather than overriding. figure-out loads that file at Bootstrap, which is both what makes the precedence real and the first time anything in the workflow reads the ADR directory rather than only writing to it. The plugin's `ADR_FORMAT.md` remains the shipped default for projects that have no conventions file of their own, and states the precedence rule.

## Alternatives Considered

- **Keep conventions plugin-only and point at them from the project context file**: No duplication, one source — Rejected: a pointer into a plugin file is unopenable for the readers this is for, which is the entire population that motivated the change.
- **Emit the conventions but let the plugin reference win on conflict**: Protects against a badly edited repo copy — Rejected: a project's written convention losing to a tool's default is backwards, and it would make editing the emitted file pointless. The narrower risk is handled by scoping precedence to conventions and keeping cadence with the skill.
- **Emit a short pointer file naming the conventions rather than the conventions themselves**: Smaller artifact in the user's repo — Rejected: same failure as the first option, one indirection later.
- **Split the emitted file in two, mirroring the current `ADR_FORMAT` / `WITH_DOCS` boundary**: Preserves the existing structure — Rejected: that boundary exists for progressive disclosure inside a session, not for a human reader, and it is precisely the split that stranded plugin-less readers at a dead pointer.

## Consequences

### Positive
- A teammate with no tooling can decide and write ADRs correctly from one file in the repo.
- A team can change its own ADR practice by editing a file it owns.
- figure-out now reads the ADR directory at Bootstrap, so the corpus stops being write-only.

### Negative
- The conventions exist in two places — the plugin default and each project's copy — and must be kept in step.
- A project copy frozen at setup time will not pick up later improvements to the shipped default unless someone refreshes it.

## Source
- Session: figure-out session, 2026-08-09
- Related: 20260703-progressive-disclosure-triggers-live-in-loading-layer
- Related: 20260809-adr-index-is-derived-from-the-records
- Related: 20260809-init-context-skill-lives-in-core
