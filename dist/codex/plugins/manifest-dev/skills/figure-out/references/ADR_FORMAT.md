# ADR Format

<!-- Fixed boundary: copying starts below this comment. setup-project reproduces the sentence
     below verbatim in a project's own `docs/adr/CONVENTIONS.md`, under a retitled heading,
     then pauses at the next boundary. Every boundary comment in this file marks where
     copying pauses or resumes, and the comments themselves are dropped from the copy.
     Renaming or rewording the text any boundary comment sits above breaks that copy —
     change the recipe in setup-project/SKILL.md step 2 in the same edit. -->

Architecture Decision Records capture significant decisions with their context, alternatives, and consequences. Based on the MADR (Markdown Any Decision Records) standard.

<!-- Fixed boundary: copying pauses here. The recipe replaces the note below and the
     whole Precedence section with a short paragraph of its own, then resumes at the
     boundary further down. -->

This file is self-contained: it carries both the bar a decision must clear to deserve a record and the mechanics of writing one, so a reader with no tooling installed can follow it end to end.

## Precedence

A project may keep its own copy of these conventions at `docs/adr/CONVENTIONS.md`. **Where that file exists, it governs** — template, field set, naming, status lifecycle, immutability, cross-references, and index format are the project's to set, and a team that has edited them means it. Read it before writing an ADR into that project, and follow it where it differs from this file.

One thing is not the project's to set: **cadence** — when a session raises an ADR and how the offer is made. That is workflow behavior, it lives with the workflow that makes the offer, and a conventions file stating otherwise does not bind it.

<!-- Fixed boundary: copying resumes at the heading below and runs to the end of the file. -->

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

## Decided by
[The user | An agent in an unattended run, with no review]

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

## Enforced by
[The strongest check that holds the decision, and what it pins | partly — <check>; <what stays judgment> | not yet — <the check that would hold it> | none — <why no check can hold it>]

## Revisit when
[Optional; expected on a `Strategy` record. The observable condition that would reopen this choice, and where it is read.]

## Source
- Session: [transcript / conversation reference]
- Related: [Supersedes / Superseded by / See also]
````

**Area** is a single short label — reuse an existing one wherever the decision fits it, and mint a new one only when nothing fits. It is read by the index, so keep it stable: renaming a label means editing every record that carries it.

One label is reserved. A record of a guiding choice — one the project pursues its goal through, and that other decisions derive from — carries the area `Strategy`. Where the project's North Star (its standing statement of what it is for, `NORTH_STAR.md`) keeps a *Strategy choices in force* list, that list is derived from the `Strategy` records in effect — each one's title, with its `Revisit when` where it has one — and holds nothing else, so writing, superseding or retiring such a record, or editing its `Revisit when`, rebuilds that list in the same act, as the index is rebuilt. The exact rebuild rule is in the North Star's own conventions (`docs/NORTH_STAR_CONVENTIONS.md`). A North Star in an older form without that list gains none from it.

**Decided by** names who made the decision, so a later reader can tell a person's ruling from an agent's. Write `The user` when a person decided it or reviewed the record before it was accepted. Write `An agent in an unattended run, with no review` when a run with no person present accepts its own record. When a person later reviews such a record and keeps its decision, change the value to `The user` in place; a person who changes the decision writes a new record instead.

**Context**, where the project keeps a North Star, also carries one check: compare the decision's subject with what the North Star's *Purpose* names (its Diagnosis, in a North Star of the older nine-field form), and where the decision sits outside it, say so in one line of the context. This is how a North Star going stale without contradiction becomes visible: every record is locally consistent with the text, so nobody meets the mismatch. One decision outside the Purpose means nothing, so the line is a note — never a question to the owner, never an edit to the North Star — and what makes it actionable is a run of them across records, which the notes let a later reader see. Every writer of a record applies it, whichever workflow writes the record.

**Enforced by** names what makes the decision hold for contributors who never read the record. Name the strongest rung that applies: a type or structure that makes the wrong code fail to compile; a lint or architecture test that fails the build; an invariant test that states a property; one owning site that every caller goes through. Name the check by file and test or rule, and what it pins. Where a check holds only part of the decision, write `partly —` with the check and the part that stays judgment. Where a check could hold it but none does yet, write `not yet —` with the check that would; the run that implements or touches the decision builds it and replaces the line. Where no check can hold it — metric design, a deliberate non-action, a one-time operational choice — write `none —` with the reason. The check carries a comment citing the record, so someone about to weaken it meets the decision first. The line records current enforcement, not the decision, so it is editable in place.

**Revisit when** is the record's signpost: the observable condition in the world that would reopen the choice, and where it is read — for example, "the second channel brings more than a third of new sign-ups, read on the weekly funnel report". It is optional on any record and expected on a `Strategy` record, since a guiding choice made on today's evidence is the one most worth reopening when the evidence moves. Name a source a reader can open; a condition nobody can read is a reminder, not a signpost. A reader that finds the condition met brings it to the person who owns the choice and changes nothing, since reopening the choice is a new record. The field says when to look again, not what was decided, so it is editable in place.

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

Only an `Accepted` record is in effect, including one a later record narrows or amends. Whatever acts on records reads only those in effect: backfilling `Enforced by`, building a `not yet` check, citing a record as a binding ruling. A `Deprecated` or `Superseded` record is history; its check is retargeted or retired in the change that deprecated or superseded it, and its `Enforced by` line is not backfilled or kept current.

## Writing an ADR is one act, not three

Adding a record means doing all three of these in the same change:

1. **Write the new record** per the template above.
2. **Update every record it changes the standing of** — a superseded decision's Status becomes `Superseded by <filename>`; a decision narrowed, amended, or partly lifted by the new one says so in its own Status line. Retarget or retire the check named in the old record's `Enforced by` so it holds the new decision instead of the old one, and update that line. This is required by the lifecycle above, and it is the step that gets skipped: it means editing a published ADR, which the immutability rule below explicitly permits.
3. **Refresh the index** per *The index* below — and, for a `Strategy` record where the project's North Star keeps a *Strategy choices in force* list, rebuild that list, signposts included, from the `Strategy` records in effect.

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
- Changing `Decided by` to `The user` after a person reviews an unattended record and keeps its decision
- Updating `Enforced by` when the check that holds the decision changes
- Adding or updating `Revisit when`
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
