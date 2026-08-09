# ADR: The ADR index is derived from the records, not authored alongside them

## Status
Accepted

## Area
ADR conventions

## Context

`docs/adr/README.md` was a hand-maintained table and no document instructed maintaining it — `ADR_FORMAT.md` had no index section and `WITH_DOCS.md`'s accept path stopped at writing the record. It drifted accordingly: four of the most recent ADRs were absent entirely, and one row still read `Accepted` for a decision its own file recorded as superseded.

Measurement removed the obvious alternative response. The index costs roughly 45 tokens per row and about 3k tokens in total at 66 records; it is not auto-loaded, and it is smaller than `CONTEXT.md`, which is. A hierarchical split by theme would not bound growth either — 19 of 62 rows sat in a single Area while a dozen Areas held one record each, so a theme tree yields one branch that keeps growing and ten branches of one.

The index also held information no record carried, which is why it drifted in both directions. Every row's Area existed only in the table. And relationships were being recorded there instead of in the records — one row read "deferral lifted by …" while the record itself read plain `Accepted` — because editing a published ADR feels like breaking immutability, even though the lifecycle rule already requires exactly that when a decision's standing changes.

## Decision

The index holds nothing the records don't, and is rebuilt from them rather than edited alongside them.

Two write-backs make that true. An `Area` field joins the ADR template and is backfilled across every existing record. And a decision's changed standing is written into the record it changes, in the same act as writing the new one — which the immutability rule already permitted and now states as an explicit third step.

The conventions file specifies the rebuild tightly enough that two rebuilds produce the same bytes: which files are rows, ascending-filename order, where each column's value comes from, and the rule that a cross-reference renders as a link labelled with the referenced filename. That last rule replaces editorially worded link labels such as "consolidated default ADR", which appeared in no record and therefore could not be derived by anything.

No tooling ships. The value of a derived index is recoverability — the information is never lost, so a stale table is a cosmetic lag any agent can repair from the specification — and a markdown-parsing script would add a fragile, untested artifact to every repository the skill touches in exchange for determinism the specification already supplies.

When size eventually justifies a split, it is live records versus superseded ones — superseded accumulates monotonically while standing decisions plateau — and not theme or date.

## Alternatives Considered

- **Keep the index authored, add a maintenance trigger**: A curated one-line summary per row is genuinely better to skim than a filename — Rejected: curation was already failing in the repo that invented the convention, and authored content cannot be recovered once it rots, where derived content always can.
- **Split the index into a theme tree now**: The original proposal, aimed at context cost — Rejected on measurement: the cost is ~3k tokens and not auto-loaded, and theme buckets are too unevenly distributed to bound the hot branch.
- **Split by date or date range**: Deterministic bucketing — Rejected: nobody looks up a decision by when it was taken, so it optimizes the one access path that is never used.
- **Ship a shell command or script to regenerate the index**: Deterministic output, runnable without an agent — Rejected: parsing multi-line prose Status values across a directory is not a one-liner but a brittle parser shipped into every user's repo, and for a project whose users all drive an agent CLI the human it serves is close to nobody.
- **Leave `Area` out and drop the column**: Makes the index derivable with no template change — Rejected: Area is the only column that groups the corpus usefully, and losing it to avoid one field is a poor trade.

## Consequences

### Positive
- A stale index is repairable by anyone at any time, because nothing is lost when it rots.
- Records carry their own standing, so reading one no longer requires cross-checking the table.
- The rebuild rules are precise enough to check by rebuilding and diffing.

### Negative
- Every record now carries a field that must be filled, and Area labels have to be kept stable by hand.
- Rebuilding is a derivation someone must actually perform; nothing enforces freshness, and this repository runs no CI that could.
- Link labels in the index are filenames rather than readable phrases, which is more literal and less graceful to read.

## Source
- Session: figure-out session, 2026-08-09
- Related: 20260809-adr-conventions-ship-as-project-knowledge
- Related: 20260809-glossary-stays-resident-with-an-under-produced-seed
