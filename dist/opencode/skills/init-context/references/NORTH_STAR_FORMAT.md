# The North Star — format and maintenance rules

A North Star is a project's standing strategy surface: one short document holding why the
project exists, who it is for, what it promises, and what winning means. It lives in the
project's own repository so every session and every contributor — with or without any
particular tooling — anchors on the same direction. It is the project-level counterpart
of a task-level spec: a task contract governs one piece of work and resets when it ends;
the North Star persists across all of them and is edited on purpose.

**It informs; it never binds.** A boundary that must be enforced on a piece of work is
encoded in that work's own binding contract (for manifest-dev users: `/define` routes a
"never" whose violation would be unsafe or irreversible to a Global Invariant). Keeping
that line is what stops the document becoming a rulebook nobody reads.

## Ownership and precedence

This file is the shipped default. When a repository is set up, a self-contained copy is
emitted as `docs/NORTH_STAR_CONVENTIONS.md`, owned by the project — so a contributor
with no tooling can learn how the document looks and functions from the repo alone,
the same way the project's ADR conventions work. **Where a project's conventions file
exists, it governs the document's form**, and tooling carrying this default defers to
it. That deference makes the copy a fork from the moment it is written: improvements to
this default never reach it, and no sync carries them, because a project's own file is
precisely what tooling must not overwrite. Keeping it current is the project's job —
port what the project wants from a later default, and keep what it has ruled for itself.
Only cadence — when a session offers an update — stays with the workflow; a project's
file has no say in that.

## Where it lives

`NORTH_STAR.md` at the repository root, made resident so sessions meet it without being
told to look: import it from the project context file where the host supports imports,
and state the instruction to read it at session start regardless. One document per
repository; comparisons *across* projects belong to whoever owns the portfolio, not to
any one repo.

Keep it standalone-first: detail moves to an adjacent linked document only when a section
outgrows the page, never pre-emptively.

## Positions and their states

A **field** is one of the nine sections below. A **position** is one claim carrying one
state: most fields hold a single position, and a field written as a list holds one per
entry. Every position carries its state as a dated provenance note — for example,
`— hypothesis: matches ourselves; no outside user has confirmed it. 2026-08` or
`— empty: no audience named. What would fill it: a person with a situation. 2026-08`.
Without the state, a measurement, a guess, and a decision all read as equally settled.
The following table defines the four states:

| State | Means | What moves it |
|-------|-------|---------------|
| `evidence` | Something happened in the world, dated | New evidence |
| `hypothesis` | Best current thinking, untested | A test |
| `ruled` | The owner decided it | Only the owner |
| `empty` | Nobody has answered — written **with what would fill it** | Whoever answers it |

`ruled` is separate from `evidence` because evidence is about the world and a ruling is
a choice: one is falsifiable, the other is not, and a form that calls both "evidence"
cannot say which positions a measurement could ever move. An `empty` position is never
left bare — without its filling condition it reads as an oversight instead of an open
question.

**The update asymmetry — the one rule every maintainer needs:** new evidence may *lower*
a position's state (an `evidence` position whose grounding stops holding drops to
`hypothesis`, with one line naming what would settle it). The position text itself
changes only by the owner's explicit ruling, and each position change is remembered in
the project's decision records — the North Star states current truth; the records
remember why it moved. A session that finds a contradiction surfaces it and asks; it
never rewrites.
Unattended automation may lower states or flag, never change a position.

## The nine fields

Throughout these fields, *they* is the person the project serves — never the tooling,
agents, or sessions that operate it. Where a project's users are its own maintainers, the
machinery is the most visible thing arriving and is still not the audience.

The following table names each field, what it holds, and the trap that most often ruins it:

| Field | What it holds | The trap |
|-------|---------------|----------|
| **Diagnosis** | What is going on and what is in the way, plus the one sentence that changes everything if false | Writing the user's complaint instead of the barrier behind it |
| **What this rests on** | The handful of live, falsifiable assumptions under the diagnosis — one line each | Letting it grow past a handful, or filling it with task-level facts, which belong in the task's own spec and reset with it |
| **Who it's for** | A person with a situation, named narrowly enough to exclude someone, plus an explicit not-for | A segment name so broad it cannot be wrong |
| **Promise** | The sentence that person reads at the moment they decide to rely on it | A feature list, or a quality claim they cannot check |
| **How they arrive** | What the person was doing when they got here, not only which channel | Naming channels alone — an offer matched to one arrival and shown to another measures nothing |
| **Money — or what it feeds** | The mechanism and price; where there is none, what the project compounds instead | Leaving it at "free", which hides what justifies the effort |
| **Winning, and the number watched** | The destination, and the single count that tracks it — or the owner's ruling that this project carries no number | Treating them as one — a destination with no number is unwatchable; a number with no destination tracks nothing |
| **Never** | The standing boundaries, in checkable form — trade-off stances included, phrased as the prohibition they imply | Stating a stance and its prohibition as two entries; one rule split in two means only one copy gets read |
| **Open** | Questions no field holds, each with what would fill it | Duplicating `empty` fields, which already carry their own filling condition |

Belief height decides what may enter the first two fields: if this position turned out
false, how much dies? The diagnosis false means pivot or stop; an assumption false means
one lane of the project dies; anything smaller is a task fact and belongs in that task's
own spec.

## What it anchors, and what it never holds

The North Star is what a decision is checked against, never where work is done. Who
it's for sets who copy is written to — the copy is not in here. The promise bounds what
marketing may claim — the campaigns are not in here. Live metric readings never enter
the document: states carry dates, and staleness is read from them.

Position text carries no details: a change in an example, a name, a number, or a path
must never force this document to change. Write positions at the altitude that survives
such changes, and let provenance notes carry compact pointers to where the specifics
live.

## Document skeleton

```markdown
# North Star — {project}

Why this project exists, for whom, and what winning means — the standing answers every
session and contributor anchors on. This document informs; it never binds: a boundary
that must be enforced on a piece of work is encoded in that work's own binding contract.

Every position below carries a state, rendered as a dated provenance note:

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — the owner decided it; only the owner moves it.
- **empty** — nobody has answered yet, written with what would fill it.

New evidence may lower a position's state. The position text itself changes only by the
owner's ruling, and each change is remembered as a decision record.

## Diagnosis
{what is going on, what is in the way, and the sentence that changes everything if false}
{— state: grounding. date}

## What this rests on
{one assumption per entry, each with its own state}

## Who it's for
{the person this project serves, not the machinery that operates it; plus "Not for: …"}

## Promise
{what that person gets, in the sentence they read when deciding to rely on it}

## How they arrive
{what that person was doing at the moment they came to this project}

## Money — or what it feeds
{the mechanism and price, or what the project compounds where there is neither}

## Winning, and the number watched
{the destination and the one count that tracks it, or the ruling that there is no number}

## Never
{one standing boundary per entry, each phrased as the prohibition it implies}

## Open
{one question per entry, each with what would fill it}
```

## The project-surfaces section

The project context file carries this section so every session — and every contributor
on any stack — knows the surfaces exist and how to treat them. The template below is the
single source of the emitted text. Emit it adapted to what the project actually has, and
extend an existing section rather than duplicating one; where the host supports imports,
the session-start reads become imports.

```markdown
## Project surfaces

This project keeps its direction, vocabulary, and decision memory in the repo — shared
ground for every contributor and agent, regardless of tooling. Read `NORTH_STAR.md` and
`CONTEXT.md` at the start of every session.

- **NORTH_STAR.md** — why this project exists, who it's for, what winning means. Anchor
  scope, priority, and marketing calls on it. Each position carries a dated state
  (evidence / hypothesis / ruled / empty): new evidence may lower a state, but a
  position changes only by the owner's call, recorded as a decision record. The full
  form is `docs/NORTH_STAR_CONVENTIONS.md` — it is self-contained.
- **CONTEXT.md** — what words mean here. Read it before naming things; add a term when
  the project settles one.
- **docs/adr/** — why decisions went the way they did. Open `docs/adr/README.md` before
  settling a question the project may already have settled, and when a change
  contradicts or narrows an existing decision. Write new records per
  `docs/adr/CONVENTIONS.md` — it is self-contained, and writing one is one act: the
  record, the restatus of what it changes, and the index rebuild together.
```

## Produce it honestly

Seed only what the repository's own artifacts evidence — a README's stated audience, a
pricing page's price, a published tagline. Each seeded position carries `hypothesis` or
`evidence` per its actual grounding, with the artifact named in the provenance note. A
field no artifact answers stays `empty` with its filling condition; a strategy position
the artifacts don't support is fiction with a state on it, and inventing it wrongs every
session that later anchors there.

*Diagnosis* and *Who it's for* are the two fields the rest are derived from, so a seed
narrower than the project propagates into all of them. Read what the project does — its
practice, its live work — alongside what it says about itself, and where the stated
purpose and the practice diverge, put both to the owner rather than picking one.

Fields that need working out rather than stating — who it's really for, the promise, the
money mechanism — are one investigation each, run when the owner chooses. The `empty` and
`hypothesis` positions are the doc's own to-do list.
