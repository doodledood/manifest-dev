# ADR: Gate figure-out project docs by topic relevance

## Status
Accepted

## Context

`figure-out` is intentionally topic-general: it can investigate any problem, idea, or decision, including subjects unrelated to the repository in the current working directory. Its default docs mode currently resolves and loads that repository's `CONTEXT.md` before pressing the topic, and may later write glossary entries or ADRs there.

The working directory is useful evidence for locating project context, but it does not establish that the user's topic belongs to that project. Treating it as sufficient can anchor an unrelated investigation on irrelevant vocabulary, delay the first substantive question with project-doc bootstrap, or write a non-project decision into the repository.

## Decision

Keep `figure-out` topic-general. Project documentation participates only when the investigation is relevant to the active project or one of its mapped contexts.

Topic relevance gates project-doc bootstrap, `CONTEXT.md` loading and glossary capture, and project ADR capture. The repository working directory identifies where relevant project documentation would live; it does not by itself make that documentation relevant. If project relevance emerges later in the investigation, docs mode may activate at that point.

Default investigation logging remains independent of this decision because the log is an out-of-repo session artifact rather than project documentation.

## Alternatives Considered

- **Always use the working directory's project context**: Preserve the current behavior unless the user passes `--no-docs`. — Rejected because repository location is not evidence that an arbitrary topic belongs to that repository, and irrelevant context can distort or delay the investigation.
- **Restrict figure-out to project topics**: Narrow the skill's activation and public promise so every invocation is assumed to belong to the active project. — Rejected because topic-general adversarial understanding is part of the skill's intended role; project documentation should adapt to that boundary rather than narrowing it.

## Consequences

### Positive

- Non-project investigations remain free of unrelated repository vocabulary and writes.
- The first substantive interaction is not displaced by irrelevant project-doc setup.
- `figure-out` can retain both its broad topic promise and its project-memory behavior when that behavior is actually relevant.

### Negative

- The agent must make a topic-relevance judgment before loading project documentation.
- A topic whose project relationship is initially unclear may load project context later than an always-on policy would.
- Mid-session activation adds a small mode transition that must preserve the normal bootstrap and capture rules.

## Source

- Grounding: cross-skill prompt audit of `figure-out`'s topic-general activation against default docs-mode bootstrap and write behavior.
- Related: 20260705-front-figure-out-as-door-define-do-loop-as-house
