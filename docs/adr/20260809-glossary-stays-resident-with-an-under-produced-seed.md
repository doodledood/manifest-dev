# ADR: The glossary stays resident, and setup seeds it deliberately short

## Status
Accepted

## Area
Project context

## Context

`CONTEXT.md` is imported into every session through the project context file. Measured against the surfaces around it, it is the largest always-on document in this repository — 13,838 characters against the ADR index's 12,240 — and the index is paid only when something opens it. Per item the glossary is worse: roughly 74 tokens per term against 45 per index row. The unbounded always-on cost sits here, not on the ADR corpus, which was where the concern started.

The obvious response was to drop the import and reference the file instead. That fails for a reason the same change set had just measured elsewhere: a glossary defends against *misreading*, and nobody opens a glossary for a term they already believe they understand. A pointer with no trigger is exactly what left `docs/adr/` unread for the entire life of the workflow.

The second pressure comes from setup. `init-context` can mine vocabulary from a codebase, and a codebase supplies effectively unlimited nouns. The existing entry bar in `WITH_DOCS.md` transfers — project-specific meaning, ambiguity reduction, workflow boundary, load-bearing relationship — but its trigger signals are all conversational ("the user used a term and stated what they mean by it"), and a mining pass has no user turns. A bar makes each entry earn its place; it does not cap how many entries can.

## Decision

The glossary stays resident. Hosts with an import directive get `@CONTEXT.md`; hosts without one get an instruction to read it at session start, which is a real trigger because session start is observable. The wording is generic "project context file" language, so the existing per-CLI substitution in sync-tools carries it to the `AGENTS.md` harnesses.

Residency is affordable only if the file stays small, so setup **under-produces on purpose**. Mining ranks candidates rather than sweeping, admitting only terms whose misreading would change what someone builds, and presents them to the user as one batch for approval before anything is written. figure-out's inline no-offer write is warranted because the user just spoke the term; a miner has no such warrant.

Should residency stop being affordable, the fallback is splitting `CONTEXT.md` into a resident core and a deferred appendix — a threshold move on the same footing as the index's live-versus-superseded split, and not warranted at present size.

## Alternatives Considered

- **Drop the import, keep a reference**: Removes the always-on cost outright — Rejected: silent misreading is an unbounded, invisible failure, and trading a measured 3.5k tokens for it is a bad exchange. It is the same pointer-without-a-trigger shape that left the ADR corpus unread.
- **Split `CONTEXT.md` into resident core and deferred appendix now**: Bounds the resident cost while keeping the full glossary — Deferred rather than rejected: genuinely viable, but it reintroduces two places to look and requires judging which terms are hot, which is not worth paying at current size.
- **Rely on the entry bar alone to keep the glossary small**: The rule already exists and is good — Rejected: all 47 existing terms cleared that bar and the file is still the largest always-on document. Necessary, not sufficient.
- **Let the miner write glossary terms directly, as figure-out does**: Consistent with existing behavior, no approval step — Rejected: figure-out's warrant is that the user just said the thing, which a mining pass does not have, and the cost of a wrong entry is paid by every future session.

## Consequences

### Positive
- Vocabulary is present before anyone can misread it, on every harness rather than only those with imports.
- A human stands between an unlimited noun supply and a file every session pays for.
- The residency rule is stated portably, so distributions inherit it without special handling.

### Negative
- Every glossary entry is a permanent per-session cost, which makes the bar's enforcement a standing obligation rather than a one-time judgment.
- Setup deliberately leaves vocabulary uncaptured, so a freshly initialized project's glossary is thinner than the codebase could support.
- Non-import harnesses depend on an instruction being followed rather than a mechanism, which is weaker.

## Source
- Session: figure-out session, 2026-08-09
- Related: 20260709-gate-figure-out-project-docs-by-topic-relevance
- Related: 20260809-adr-index-is-derived-from-the-records
