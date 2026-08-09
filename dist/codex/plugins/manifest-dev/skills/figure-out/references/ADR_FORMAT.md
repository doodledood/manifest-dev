# ADR Format

Architecture Decision Records capture significant decisions with their context, alternatives, and consequences. Based on the MADR (Markdown Any Decision Records) standard.

This file is self-contained: it carries both the bar a decision must clear to deserve a record and the mechanics of writing one, so a reader with no tooling installed can follow it end to end.

## Precedence

A project may keep its own copy of these conventions at `docs/adr/CONVENTIONS.md`. **Where that file exists, it governs** — template, field set, naming, status lifecycle, immutability, cross-references, and index format are the project's to set, and a team that has edited them means it. Read it before writing an ADR into that project, and follow it where it differs from this file.

One thing is not the project's to set: **cadence** — when a session raises an ADR and how the offer is made. That is workflow behavior, it lives with the workflow that makes the offer, and a conventions file stating otherwise does not bind it.

<!-- The heading below is a fixed boundary: init-context copies this file from here to the end
     verbatim, replacing only what sits above it. Renaming it breaks that copy — change the
     recipe in init-context/SKILL.md step 2 in the same edit. -->

## When a decision deserves a record

The threshold is **downstream architectural impact** — decisions that shape the system's structure, constrain future options, or would be costly to reverse.

**Worth recording:**

| Source | What to capture |
|--------|----------------|
| **Architecture choices** | Technology, patterns, component structure, integration approach |
| **Trade-off resolutions** | When competing concerns were weighed and one was preferred |
| **Scope decisions with rationale** | Deliberate inclusion/exclusion that shapes the system boundary |
| **Key constraint decisions** | Invariants established from multiple valid options |
| **Approach pivots** | When implementation adjusts architecture based on reality |

**Not worth recording:**

| Category | Why not |
|----------|---------|
| **Verification configuration** | Which checks run, and at what bar — not architecture |
| **Ways of working** | Process preferences, not system structure |
| **Mechanical choices** | Obvious implementations with no meaningful alternatives |
| **Defaults nobody weighed** | Chosen without deliberation — no alternatives to record |
| **Bug fixes** | Corrections, not decisions, unless the fix involves an architectural choice |

**Decision Test** (when uncertain): *"Would someone joining in six months benefit from knowing WHY this was decided this way?"* If yes, write one. If they would just accept it as obvious, skip it.

## Template

````markdown
# ADR: [Decision Title]

## Status
Accepted

## Area
[One short label naming the part of the system this decision governs.]

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
- Related: [Supersedes / Superseded by / See also]
````

**Area** is a single short label — reuse an existing one wherever the decision fits it, and mint a new one only when nothing fits. It is read by the index, so keep it stable: renaming a label means editing every record that carries it.

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

## Writing an ADR is one act, not three

Adding a record means doing all three of these in the same change:

1. **Write the new record** per the template above.
2. **Update every record it changes the standing of** — a superseded decision's Status becomes `Superseded by <filename>`; a decision narrowed, amended, or partly lifted by the new one says so in its own Status line. This is required by the lifecycle above, and it is the step that gets skipped: it means editing a published ADR, which the immutability rule below explicitly permits.
3. **Refresh the index** per *The index* below.

Doing one or two of these leaves the corpus asserting something untrue. Treat them as a single act.

## Immutability

ADRs are append-only by convention. Once an ADR is **Accepted** and published, do not rewrite the body — the whole point is to capture what we decided, when, and why. Editing the decision destroys the historical record.

Immutability begins at publication, not at drafting: an ADR that has merged (or is otherwise visible outside the branch that authored it) is the historical record. An ADR still on its own open branch is a draft — edit, amend, or delete it in place as the decision evolves there; do not spawn supersede-chains or stack amendment ADRs for a decision that hasn't merged yet.

When reality shifts, write a new ADR and update the old one's Status:

1. Write a new ADR capturing the new decision and its context.
2. Update the old ADR's Status to `Superseded by [new-filename]`.
3. The new ADR's Source field lists `Supersedes [old-filename]`.

**Editable in place** (no new ADR needed):
- Typo fixes, broken-link repairs, formatting
- Status changes and cross-references (e.g., `Related: 20260518-foo`)
- Adding or correcting the `Area` field
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

This is unambiguous, matches the actual filename exactly, and is what lets the index render the reference as a link without anyone inventing a label for it. Don't use numeric-only IDs, slug-only forms, or date-only references — they collide or hide the chronology.

## Granularity

**One decision per ADR.** Don't bundle related decisions into a single record. If two decisions share context but are independently reversible, give each its own ADR and link them with `Related:` in the Source field.

## Retroactive ADRs

Recording a decision that was already made informally — in chat, in code, in a pull request — is permitted. The Status remains `Accepted`. Mark the retroactivity in the Source field:

```
## Source
- Retroactive — decision was made implicitly in PR #142 / commit d8ffab7
- Session: (no session — captured post-hoc)
```

### When the rationale could not be recovered

A retroactive record reconstructed from history often preserves *what* was decided while the *why* is gone. That is worth recording anyway — but the record must say so, in the body, where a reader meets it before drawing conclusions:

```markdown
## Context
**Rationale not recovered.** This record was reconstructed from <sources>. The decision and its
date are evidenced; the reasoning behind it, and the alternatives weighed at the time, were not
found and are not reconstructed here.

## Alternatives Considered
_Not recovered._
```

Never leave `Alternatives Considered` merely empty. An empty section reads as *there were none*, which tells a future reader the decision was uncontested — the opposite of what an unrecovered rationale means, and precisely the misreading that would let someone overturn it without knowing what it cost.

## The index

The ADR directory carries an index at `docs/adr/README.md`. **It holds nothing the records don't** — every column is derived, so a stale index is a cosmetic lag rather than lost information, and anyone can rebuild it from the records at any time.

Refresh it in the same change that adds or restatuses a record.

**Rebuild rules** — following these twice produces the same bytes:

- **Rows**: every `*.md` file in the ADR directory except `README.md` and `CONVENTIONS.md`. Derive the list from the directory; never from a list written down elsewhere.
- **Order**: ascending by filename. The `YYYYMMDD-` prefix makes that chronological, and the slug breaks ties within a date.
- **Date** column: the filename's `YYYYMMDD` prefix, rendered `YYYY-MM-DD`.
- **ADR** column: the record's `# ADR: ` heading with that prefix stripped, as a link to its filename.
- **Status** column: the record's `## Status` line verbatim, with every `YYYYMMDD-kebab-title` token in it rendered as a link to `YYYYMMDD-kebab-title.md`. Do not invent a shorter label for the link — the filename is the label, which is what keeps this derivable.
- **Area** column: the record's `## Area` value verbatim.

**The index file is exactly a title, a blank line, and the table** — no preamble prose, so a rebuild from an empty directory listing produces the same bytes as a rebuild over an existing file. Anything worth saying about the corpus belongs in this conventions file, which is where a reader looks for it anyway.

```markdown
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
```

The file ends with the last table row and a single trailing newline.

An ADR records why a direction was chosen at the time it was chosen; current implementation state may lag a record when it describes a staged rollout. That is expected, and not a reason to edit the record.

A record missing `## Area` is a defect in that record, not a blank cell to paper over — add the field rather than leaving the column empty.
