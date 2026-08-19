# The North Star — format and maintenance rules

A North Star is a project's standing strategy surface: one short document holding why the
project exists, who it is for, what it promises, and what winning means, kept in the
project's own repository so every session and every contributor — with or without any
particular tooling — anchors on the same direction. It is the project-level counterpart
of a task-level spec: a task contract governs one piece of work and resets when it ends;
the North Star persists across all of them and is edited on purpose.

**It informs; it never binds.** A boundary that must be enforced on a piece of work is
encoded in that work's own binding contract (for manifest-dev users: `/define` routes a
"never" whose violation would be unsafe or irreversible to a Global Invariant). Keeping
that line is what stops the document becoming a rulebook nobody reads.

## Where it lives

`NORTH_STAR.md` at the repository root, made resident so sessions meet it without being
told to look: import it from the project context file where the host supports imports,
and state the instruction to read it at session start regardless. One document per
repository; comparisons *across* projects belong to whoever owns the portfolio, not to
any one repo.

Keep it standalone-first: detail moves to an adjacent linked document only when a section
outgrows the page, never pre-emptively.

## The four states

Every line carries one state, rendered as a dated provenance note under its section
(e.g. `— hypothesis: matches ourselves; no outside user has confirmed it. 2026-08`).
Without the state, a measurement, a guess, and a decision all read as equally settled.

| State | Means | What moves it |
|-------|-------|---------------|
| `evidence` | Something happened in the world, dated | new evidence |
| `hypothesis` | Best current thinking, untested | a test |
| `ruled` | The owner decided it | only the owner |
| `empty` | Nobody has answered — written **with what would fill it** | whoever answers it |

`ruled` is separate from `evidence` because evidence is about the world and a ruling is
a choice: one is falsifiable, the other is not, and a form that calls both "evidence"
cannot say which lines a measurement could ever move. An `empty` line is never left
bare — without its filling condition it reads as an oversight instead of an open
question.

**The update asymmetry — the one rule every maintainer needs:** new evidence may *lower*
a line's state (an `evidence` line whose grounding stops holding drops to `hypothesis`,
with one line naming what would settle it). The position text itself changes only by the
owner's explicit ruling, and each position change is remembered in the project's
decision records — the North Star states current truth; the records remember why it
moved. A session that finds a contradiction surfaces it and asks; it never rewrites.
Unattended automation may lower states or flag, never change a position.

## The nine fields

| Field | What it holds | The trap |
|-------|---------------|----------|
| **Diagnosis** | What is going on and what is in the way, plus the one sentence that changes everything if false | Writing the user's complaint instead of the barrier behind it |
| **What this rests on** | The handful of live, falsifiable assumptions under the diagnosis — one line each | Letting it grow past a handful, or filling it with task-level facts, which belong in the task's own spec and reset with it |
| **Who it's for** | A person with a situation, named narrowly enough to exclude someone, plus an explicit not-for | A segment name so broad it cannot be wrong |
| **Promise** | The sentence a stranger reads at the moment they decide to try it | A feature list, or a quality claim no stranger can check |
| **How they arrive** | What the person was doing when they got here, not only which channel | Naming channels alone — an offer matched to one arrival and shown to another measures nothing |
| **Money — or what it feeds** | The mechanism and price; where there is none, what the project compounds instead | Leaving it at "free", which hides what justifies the effort |
| **Winning, and the number watched** | The destination, and the single count that tracks it | Treating them as one — a destination with no number is unwatchable, a number with no destination tracks nothing |
| **Never** | The standing boundaries, in checkable form — trade-off stances included, phrased as the prohibition they imply | Stating a stance and its prohibition as two entries; one rule split in two means only one copy gets read |
| **Open** | Questions no field holds, each with what would fill it | Duplicating `empty` fields, which already carry their own filling condition |

Belief height is the ruler between the first two fields and everything below them: if
this line turned out false, how much dies? The diagnosis false means pivot or stop; an
assumption false means one lane of the product dies; anything smaller is a task fact and
does not belong here.

## What it anchors, and what it never holds

The North Star is what a decision is checked against, never where work is done. Who
it's for sets who copy is written to — the copy is not in here. The promise bounds what
marketing may claim — the campaigns are not in here. Live metric readings never enter
the document: states carry dates, and staleness is read from them.

## Document skeleton

```markdown
# North Star — {project}

Why this project exists, for whom, and what winning means — the standing answers every
session and contributor anchors on. This document informs; it never binds: a boundary
that must be enforced on a piece of work is encoded in that work's own binding contract.

Every line below carries a state, rendered as a dated provenance note:

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — the owner decided it; only the owner moves it.
- **empty** — nobody has answered yet, written with what would fill it.

New evidence may lower a line's state. The position text itself changes only by the
owner's ruling, and each change is remembered as a decision record.

## Diagnosis
{— state: grounding. date}

## What this rests on
{one assumption per line, each with its state}

## Who it's for
{including "Not for: …"}

## Promise

## How they arrive

## Money — or what it feeds

## Winning, and the number watched

## Never

## Open
```

## The project-surfaces section

The project context file carries this section so every session — and every contributor
on any stack — knows the surfaces exist and how to treat them. Emit it (adapted to what
the project actually has; extend an existing section rather than duplicating one):

```markdown
## Project surfaces

This project keeps its direction, vocabulary, and decision memory in the repo — shared
ground for every contributor and agent, regardless of tooling.

- **NORTH_STAR.md** — why this project exists, who it's for, what winning means. Anchor
  scope, priority, and marketing calls on it. Each line carries a dated state
  (evidence / hypothesis / ruled / empty): new evidence may lower a state, but a
  position changes only by the owner's call, recorded as a decision record.
- **CONTEXT.md** — what words mean here. Read it before naming things; add a term when
  the project settles one.
- **docs/adr/** — why decisions went the way they did. Before settling a question the
  project may already have settled, open `docs/adr/README.md`. Write new records per
  `docs/adr/CONVENTIONS.md` — it is self-contained.
```

## Producing it honestly

Seed only what the repository's own artifacts evidence — a README's stated audience, a
pricing page's price, a published tagline — each seeded line carrying `hypothesis` or
`evidence` per its actual grounding, with the artifact named in the provenance note. A
field no artifact answers stays `empty` with its filling condition; a strategy line the
artifacts don't support is fiction with a state on it, and inventing it wrongs every
session that later anchors there. Fields that need working out rather than stating —
who it's really for, the promise, the money mechanism — are one investigation each,
run when the owner chooses; the `empty` and `hypothesis` lines are the doc's own to-do
list.
