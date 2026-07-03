# ADR Format

Architecture Decision Records capture significant decisions with their context, alternatives, and consequences. Based on the MADR (Markdown Any Decision Records) standard.

## Template

````markdown
# ADR: [Decision Title]

## Status
Accepted

## Context
[What situation motivated this decision? What constraints, requirements, or tensions existed?]

## Decision
[What was decided and why this option was chosen.]

## Alternatives Considered
- **[Alternative A]**: [Description] — [Why not chosen]
- **[Alternative B]**: [Description] — [Why not chosen]

## Consequences

### Positive
- [What becomes easier or better]

### Negative
- [What becomes harder or is traded away]

## Source
- Session: [transcript / conversation reference]
- Manifest: [manifest file path, if any]
- Related: [Supersedes / Superseded by / See also]
````

## File Naming and Location

Write ADRs to `docs/adr/YYYYMMDD-kebab-case-title.md` — date prefix using the current date. Create `docs/adr/` lazily on the first ADR if it doesn't exist.

Examples: `docs/adr/20260518-decouple-adr-from-workflow.md`, `docs/adr/20260518-use-madr-format.md`.

**Multi-context repos** (where `CONTEXT-MAP.md` exists at root): per-context ADRs live in the relevant module alongside that context's `CONTEXT.md` rather than the root-level `docs/adr/`.

## Status Lifecycle

ADRs follow a four-state lifecycle: `Proposed` → `Accepted` → `Deprecated` → `Superseded`.

- **Proposed**: Decision drafted but not yet committed. Used when an idea is on the table but the team hasn't fully agreed.
- **Accepted**: Default for fresh ADRs. The decision is in effect.
- **Deprecated**: The decision no longer applies but hasn't been replaced. Use when something was true but the world moved on.
- **Superseded**: A newer ADR replaces this one. Always paired with `Superseded by [filename]` in the Status field, and the superseding ADR carries a matching `Supersedes [filename]` line.

## Immutability

ADRs are append-only by convention. Once an ADR is **Accepted** and published, do not rewrite the body — the whole point is to capture what we decided, when, and why. Editing the decision destroys the historical record.

Immutability begins at publication, not at drafting: an ADR that has merged (or is otherwise visible outside the branch that authored it) is the historical record. An ADR still on its own open branch is a draft — edit, amend, or delete it in place as the decision evolves there; do not spawn supersede-chains or stack amendment ADRs for a decision that hasn't merged yet.

When reality shifts, write a new ADR and update the old one's Status:

1. Write a new ADR capturing the new decision and its context.
2. Update the old ADR's Status to `Superseded by [new-filename]`.
3. The new ADR's Source field lists `Supersedes [old-filename]`.

**Editable in place** (no new ADR needed):
- Typo fixes, broken-link repairs, formatting
- Adding cross-references (e.g., `Related: 20260518-foo`)
- Clarifying confusing prose without changing the decision

**NOT editable in place** (requires a new ADR):
- Changing the decision itself
- Retroactively rewriting the context to match current beliefs
- Deleting alternatives that were considered and rejected
- Backdating

**Practical diff test**: if someone reading the diff would think *"they changed their mind"* → new ADR. If they'd think *"they fixed a typo"* → in-place edit is fine.

## Cross-Reference Format

When an ADR supersedes or is superseded by another, reference the **full filename without the `.md` extension**:

```
## Status
Superseded by 20260518-use-event-bus

## Source
- Supersedes 20260301-direct-rpc-calls
- Related: 20260415-message-ordering
```

This is unambiguous and matches the actual filename exactly. Don't use numeric-only IDs, slug-only forms, or date-only references — they collide or hide the chronology.

## Granularity

**One decision per ADR.** Don't bundle related decisions into a single record. If two decisions share context but are independently reversible, give each its own ADR and link them with `Related:` in the Source field.

## Retroactive ADRs

Recording a decision that was already made informally (in chat, in code, in a PR) is permitted. The Status remains `Accepted` — no new lifecycle value. Mark the retroactivity in the Source field:

```
## Source
- Retroactive — decision was made implicitly in PR #142 / commit d8ffab7
- Session: (no session — captured post-hoc)
```

The history matters; the retroactivity tag is honest about how the record entered the system.

## Gate

The offer gate — whether a decision deserves an ADR at all — lives in `WITH_DOCS.md`, the docs-mode layer that runs the per-turn check. This file assumes the gate has already fired: it carries only the write-time mechanics, and loads after an offer is accepted.
