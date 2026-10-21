# North Star Conventions

A North Star is a project's standing statement of what it is for: one short document holding
its purpose, its goal, the principles it holds, how it measures progress, and the bets it rests
on. It lives in the project's own repository so every session and every contributor — with or
without any particular tooling — starts from the same base when it decides anything a task's
own contract does not settle. It is the project-level counterpart of a task-level spec: a task
contract governs one piece of work and resets when it ends; the North Star persists across all
of them and is edited on purpose.

**It holds what decisions are judged against, never what they chose.** A decision weighs the
project's ends (what it is for), measures, principles and bets and picks an option; that chosen option is the
decision's output, and it lives in the project's decision records. Kept to those inputs, the
document changes only when the purpose, a principle or a bet changes, and a later session never
mistakes a tactic for the mission.

**It informs; it never binds.** A boundary that must be enforced on a piece of work is
encoded in that work's own binding contract (for manifest-dev users: `/define` routes a
"never" whose violation would be unsafe or irreversible to a Global Invariant). Keeping
that line is what stops the document becoming a rulebook nobody reads.

## Ownership

**This file is this project's North Star convention, and it governs.** Everything needed
to read, fill, and maintain `NORTH_STAR.md` is here — no tool, plugin, or prior knowledge
required. Tooling that carries its own North Star defaults defers to this file. That
deference makes this copy a fork: improvements to any shipped default never reach it, and
no sync carries them, because a project's own file is precisely what tooling must not
overwrite. Keeping it current is this project's job — port what the project wants from a
later default, and keep what it has ruled for itself; re-running the setup that installed
this file is one way to see what a current default carries.

## Where it lives

`NORTH_STAR.md` at the repository root, made resident so sessions meet it without being
told to look: import it from the project context file where the host supports imports,
and state the instruction to read it at session start regardless. One document per
repository; comparisons *across* projects belong to whoever owns the portfolio, not to
any one repo.

Keep it standalone-first: detail moves to an adjacent linked document only when a section
outgrows the page, never pre-emptively.

## Positions and their states

A **section** is one of the six below. A **position** is one claim carrying one
state: a section written as prose holds one position per claim, and a section written as a
list holds one per entry. Every position carries its state as a dated provenance note — for example,
`— hypothesis: matches ourselves; no outside user has confirmed it. 2026-08` or
`— empty: no audience named. What would fill it: a person with a situation. 2026-08`.
Without the state, a measurement, a guess, and a decision all read as equally settled.
A provenance note is short: the state, its grounding (for an `empty` position, what would fill
it), its date, and the titles of any records behind it. How a position came to read as it does
is history, and history lives in those records.
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

A position also goes stale without anything contradicting it. When the work a project
actually does drifts away from what a position says — every piece of it defensible on its
own, none of it contradicting the text — the position keeps steering at a shape the project
has left. Divergence is as much staleness as contradiction, and it is quieter: nobody meets
it, because no single session is inconsistent with the text. A session that notices a
mismatch notes it — a note, never a question — and leaves the position alone; what makes it
actionable is a run of them, which no one session can see. Treat the accumulation as a signal
for the owner to weigh, not as something anyone repairs on the spot, and do not answer it with
a scheduled review.

**The update asymmetry — the one rule every maintainer needs:** new evidence may *lower*
a position's state (an `evidence` position whose grounding stops holding drops to
`hypothesis`, with one line naming what would settle it). The position text itself
changes only by the owner's explicit ruling, and each position change is remembered in
the project's decision records — the North Star states current truth; the records
remember why it moved. A session that finds a contradiction surfaces it and asks; it
never rewrites.
Unattended automation may lower states or flag, never change a position.

## What a line may be

Every position in *Purpose*, *Goal*, *Principles*, *How we know* and *What this rests on* is one
of four kinds, and nothing else; *Open* holds questions, and the strategy list holds titles:

- **An end** — what the project is for, or whom it serves. Asked "why does this matter?", it
  has no deeper answer inside the document.
- **A measure** — how the project measures progress on one part of its goal: what is counted,
  which way it should move, and a floor where the floor is itself something the owner holds,
  such as "never worse than what people do by hand today".
- **A principle** — a limit or a trade-off the owner holds even when evidence says crossing it
  would pay. That is what separates it from a choice.
- **A bet** — a belief about the world that, if false, would change the goal or end one part
  of the project. A bet the owner states is still a `hypothesis` until something tests it.

**The test for any line.** Would the owner re-tune it when evidence moves? Then it is a chosen
option, not one of the four: it belongs in a decision record, and a dated target — a value a
measure should reach by a date — belongs with the work pursuing it: the destination of the effort
(the named body of work) that pursues it, where the project tracks work that way, or else the
decision record of the choice it serves. A bet differs: evidence tests it and may lower its
state, but nobody tunes it for a better result, the way a price or a channel is tuned. The
choices themselves can matter a great deal; they leave because they are outputs of the
document's inputs, and a copy here would make a later session protect a tactic as if it were
the purpose. A line that names one example, setting, number or path is nearly always a choice,
however stable it has been; name the shape it serves instead, and let the provenance note
point to the record that holds the specifics.

Live metric readings never enter the North Star: states carry dates, and staleness is read
from them.

## The sections

Throughout these sections, *they* is the person the project serves — never the tooling,
agents, or sessions that operate it. Where a project's users are its own maintainers, the
machinery is the most visible thing arriving and is still not the audience.

The following table names each section, what it holds, and the trap that most often ruins it:

| Section | What it holds | The trap |
|---------|---------------|----------|
| **Purpose** | What is going on and what is in the way, then who the project is for — a person with a situation, named narrowly enough to exclude someone — and an explicit not-for | Writing the user's complaint instead of the barrier behind it, or a segment so broad it cannot be wrong |
| **Goal** | Where the project is headed, in the sentence that person reads when deciding to rely on it, and what reaching it means for the project itself | A feature list, or a quality claim nobody can check |
| **Principles** | The limits and trade-offs held even against evidence — what the project never does, what it never trades away, and what it feeds instead of money where money is not the point — one per entry, each phrased as what it rules out | A tactic phrased as a principle: if evidence would move it, it is a choice |
| **How we know** | One measure for each part of the goal, with its direction and any floor; a part nothing measures yet is `empty` with what would fill it | One number for a goal with several parts, which lets the unmeasured part drop out of every decision |
| **What this rests on** | A handful of live, falsifiable bets, the main one first: the sentence that changes everything if false | Letting it grow past a handful, or filling it with task facts, which belong in that task's own spec |
| **Open** | Questions none of the sections above holds, each with what would fill it | Repeating an `empty` position, which already carries its own filling condition |

After the sections comes **Strategy choices in force**: the titles of the decision records in
effect that carry the area `Strategy` — the few guiding choices the project pursues its goal
through, which other decisions derive from. The list holds titles only and is rebuilt from
those records in the same act that writes, supersedes or retires one; the record holds the
choice and its reasons.

Belief height decides what may enter *What this rests on*: if this bet turned out false, how
much dies? The purpose false means pivot or stop; a bet false means one part of the project
ends; anything smaller is a task fact and belongs in that task's own spec.

## What it anchors

The North Star is what a decision is checked against, never where work is done. Who it is for
sets who copy is written to — the copy is not in here. The goal and the principles bound what
marketing may claim — the campaigns are not in here. The measures say which way to push — the
dated targets live with the work that pursues them.

## Document skeleton

```markdown
# North Star — {project}

What this project is for, for whom, and how it measures progress — the base every session and
contributor decides from. This document informs; it never binds: a boundary that must be
enforced on a piece of work is encoded in that work's own binding contract.

Every position below carries a state, rendered as a dated provenance note:

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — the owner decided it; only the owner moves it.
- **empty** — nobody has answered yet, written with what would fill it.

New evidence may lower a position's state. The position text itself changes only by the
owner's ruling, and each change is remembered as a decision record.

## Purpose
{what is going on and what is in the way; then "For: …" and "Not for: …"}
{— state: grounding. date}

## Goal
{where the project is headed, in the sentence the person reads when deciding to rely on it}
{what reaching it means for the project itself}

## Principles
{one limit or trade-off per entry, held even against evidence}

## How we know
{one measure per part of the goal: what is counted, its direction, any floor}

## What this rests on
{one bet per entry, the main bet first, each with its own state}

## Open
{one question per entry, each with what would fill it}

## Strategy choices in force
{titles of the decision records in effect with area Strategy — rebuilt from them, never edited alone}
```

## Produce it honestly

Seed only what the repository's own artifacts evidence — a README's stated audience, a
published tagline, a stated principle. Each seeded position carries `hypothesis` or
`evidence` per its actual grounding, with the artifact named in the provenance note. A
section no artifact answers stays `empty` with its filling condition; a strategy position
the artifacts don't support is fiction with a state on it, and inventing it wrongs every
session that later anchors there.

Put every candidate line through the test in *What a line may be* before it is seeded. The
history of a project is full of choices — a price, a launch plan, a chosen integration — and
each one that matters is seeded as a decision record, or left out, never as a position.

*Purpose* is the section the rest are derived from, so a seed narrower than the project
propagates into all of them. Read what the project does — its practice, its live work —
alongside what it says about itself, and where the stated purpose and the practice diverge,
put both to the owner rather than picking one.

Sections that need working out rather than stating — who it's really for, the goal, the
measures — are one investigation each, run when the owner chooses. The `empty` and
`hypothesis` positions are the doc's own to-do list.
