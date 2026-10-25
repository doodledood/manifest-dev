# North Star — manifest-dev

What this project is for, for whom, and how it measures progress — the base every session and
contributor decides from. This document informs; it never binds: a boundary that must be
enforced on a piece of work is encoded in that work's own binding contract (for manifest-dev
users: `/define` routes a principle whose violation would be unsafe or irreversible to a Global
Invariant). The choices made along the way live in `docs/adr/`, never here.

Every position below carries a state, rendered as a dated provenance note:

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — an authorized choice; its decider and any delegation are named.
- **empty** — nobody has answered yet, written with what would fill it.

New evidence may lower a position's state. Position changes need an authorized ruling,
remembered as a decision record in `docs/adr/`. Explicit delegation can cover specified changes
within an assignment; owner-retained ends and bounds stay with the owner. The full
form — sections, states, maintenance — is `docs/NORTH_STAR_CONVENTIONS.md`, which governs and
needs no tooling.

## Purpose

People can make worthwhile progress on their projects without repeatedly restoring context,
choosing every next step or supervising every action they have already delegated. They can
trust the work enough to use it, return after a break without starting over, and keep control
of the choices they retain. In the way: purpose, evidence, and decision boundaries often live
only in a conversation or one person's head, while faster production can still serve the wrong
need. manifest-dev keeps that understanding available across inquiry, delivery, and learning.

— ruled: 2026-10-23. Records: Projects advance toward assigned outcomes within delegated authority.

For: quality-first developers — five-plus years of experience, already working with an agentic
coding CLI, willing to spend tokens and up-front effort for output they can trust — in a team of
any size, on a project of their own or inside a codebase where most colleagues do not use
manifest-dev. Secondary: teams standardizing how AI-assisted development is done.

Not for: cost optimizers, speed-first shippers, tinkerers who want to tweak everything, hype
chasers, and people not using a coding agent at all.

— ruled: 2026-10-15. Records: Projects drive themselves as far as each user climbs, and manifest-dev fits inside teams that do not use it.

When they reach for it: four situations so far.

- **Too big to prompt.** A change spans several files or decisions, and a wrong result would
  cost more rework than the tokens to get it right. Today they prompt directly and review
  after, do it by hand, or do less.

  — hypothesis: the maintainer's own use; no outside user has described it. Records: Name the situations people reach for manifest-dev in. 2026-10-25

- **Coming back.** They return to a project after a break and need what it is for, what was
  decided and what needs them, without rereading old conversations. Today they rely on memory,
  notes or the history, or start over.

  — hypothesis: the maintainer's own use; no outside user has described it. Records: Name the situations people reach for manifest-dev in. 2026-10-25

- **Away from the desk.** They want work to move toward an outcome while they are elsewhere,
  and to be asked only about the choices they kept. Today they wait until they are back, watch
  every step, or do not hand the work off.

  — hypothesis: the maintainer's own use; no outside user has described it. Records: Name the situations people reach for manifest-dev in. 2026-10-25

- **Thinking it through.** They face a decision or problem they cannot yet state well, and want
  it pressed until it is clear, before anything gets built. Today they use a plain chat, ask a
  colleague, or think it through alone.

  — hypothesis: the maintainer's own use; no outside user has described it. Records: Name the situations people reach for manifest-dev in. 2026-10-25

## Goal

*"My project makes progress that matters to the people it serves. I can use one skill or delegate
an outcome, keep the decisions I care about, and trust the work enough to use it with minimal
review. When I return, it still knows what it is for, what the evidence says, and what needs me.
The code and other project artifacts get easier to change correctly as the work continues."*

— ruled: 2026-10-23. Records: Projects advance toward assigned outcomes within delegated authority; The promise includes a codebase that gets easier to change correctly.

The ambition includes ongoing operation of a business within the authority its owner grants,
and progress on noncommercial projects. It is optional: a standalone investigation, a finite
piece of work, or a contribution inside a team is a complete use. This is a destination for the
workflow, not evidence that an agent can reliably operate a business today.

— ruled: 2026-10-23. Records: Projects advance toward assigned outcomes within delegated authority.

For the project itself: our own projects achieve their intended outcomes with less necessary
human involvement, while preserving quality and the choices their owners retain. Outside
recognition is welcome as a consequence, never a target traded against those ends.

— ruled: 2026-10-23. Records: Projects advance toward assigned outcomes within delegated authority.

## Principles

- **Quality decides.** Cost and speed bind second to it: a workflow stays practically affordable
  on high-end models and its verification fast enough that many agents at once are not held up,
  and neither is ever bought with quality. A run that keeps verifying and repairing after its
  gates hold is a defect in the workflow, never a meter the user has to watch.

  — ruled: 2026-10-15. Records: Cost is a binding constraint, second to quality; Verification speed binds like cost, second to quality.

- **Simple to use.** Workflows may be sophisticated inside; the experience stays minimal steps,
  nothing to memorize — follow along and it works.

  — ruled: standing since the project's first strategy document, before 2026-07-28.

- **Each piece stands alone.** Nothing has to be adopted whole to be useful. A person can use
  one skill, define finite work, share project records, track jobs in a store, or assign outcome
  coordination. Those are adoption choices, not a required pipeline or a project-wide Manifest.
  Shared additions remain plain files and instructions, so colleagues who do not use
  manifest-dev keep working as before. Delegation applies only inside assigned work.

  — ruled: 2026-10-23. Records: Projects advance toward assigned outcomes within delegated authority; Assignment bounds delegated decisions and retained acceptance.

- **Claim only what holds.** No hype register and no superlative promising what models cannot
  reliably do, on any surface we write; no commentary on this repository's own adoption or
  popularity.

  — ruled: standing since the project's first strategy document, before 2026-07-28.

- **Free and open.** No monetization intended; the workflows are built for our own projects
  first, and distribution stays second to getting them right.

  — ruled: standing since the project's first strategy document; reaffirmed 2026-07-28.

## How we know

- **Progress on each project's intended outcome** — observed results for the people it serves;
  up. Completed Tickets and artifacts are delivery evidence, not a substitute for those results.

  — empty: no common measurement has been chosen or run. What would fill it: designated outcome evidence from our own projects, with each project's success terms. 2026-10-23

- **Human involvement still needed to achieve that progress** — decisions, interventions and
  effort that the person has not chosen to retain; down. Chosen involvement is not a failure.

  — empty: no count or collection method chosen. What would fill it: actual-use records that distinguish retained choices from avoidable interruptions. 2026-10-23

- **Shipped work that had to be reworked** — a rate; down.

  — empty: the trust part of the goal has no measure. What would fill it: the eval baseline or our own projects reporting rework. 2026-10-21

- **A codebase that gets easier to change correctly** — corrections that became checks, and debt
  paid on the path of later changes; up.

  — empty: nothing counts it. What would fill it: real projects reporting the checks and debt their runs leave. 2026-10-21

- **Cost of achieving useful project progress** — down, never at quality's cost; count the
  investigation, delivery, rework, and human involvement needed, rather than cheap output alone.

  — empty: no common cost measure chosen. What would fill it: actual-use cost records paired with outcome evidence. 2026-10-23

## What this rests on

- **The bet:** spending more tokens and more up-front process — on understanding, on what's
  worth doing next, and on what done means — leaves a project better off than moving faster
  without them.

  — hypothesis: 2026-08-21; untested beyond ourselves. Records: The bet is about the practice, not about whether a market adopts it.

- Understanding-first workflows — investigate, define what done means, execute and verify every
  criterion — produce fewer reworked results than direct prompting.

  — hypothesis: strong lived support across our own projects; never measured. 2026-08

- Skills are a durable, harness-agnostic distribution surface: the same prompts serve Claude
  Code, OpenCode, Codex, and Pi.

  — evidence: shipped and maintained as per-CLI packages under `dist/` since 2026-06.

- A codebase converges toward one the workflow can maintain on its own when every correction
  becomes a check, debt is paid on the path of the next change, and each long-lived artifact
  keeps a way to verify it that normal runs keep fresh.

  — hypothesis: unmeasured until the eval baseline and real projects run it. 2026-10

- People will choose this workflow over direct prompting, manual coordination, or existing
  project tools when preserving intent and bounded delegation saves enough repeated work to
  justify setup, tokens, and learning. In a team, it must fit existing review and ownership rules.
  The alternative may be doing less or keeping a task manual, not adopting more automation.

  — hypothesis: product direction, not demonstrated adoption evidence. 2026-10-23

- Gates and explicit delegation can let useful work proceed without repeated intervention,
  while evidence about actual use can correct a delivery that met its contract but missed its
  purpose. Whether this remains reliable over repeated rounds is unmeasured.

  — hypothesis: isolated skill observations can find defects, but cannot establish sustained project outcomes. 2026-10-23

## Open

- Does the project-level half of the goal hold for anyone but its author? What would fill it:
  someone who is not the maintainer keeping a project's direction, its queue, and its definition
  of done in these surfaces. The owner assumes it does; no one else has tried it. 2026-08,
  owner's assumption 2026-10-15
- Which circumstances make the workflow worth adopting over the alternatives, and which parts
  cause people to stop? What would fill it: concrete episodes of choice, switching, and continued
  use, including cases where a simpler approach served the same progress better. 2026-10-23

## Strategy choices in force

- The project is the unit the workflows serve, not the single task
- Positioning drops the conversion funnel; the standalone shape stays on honest grounds
- One skill per beat, built up from the lean body
- An orchestrating skill runs the queue in parallel and replaces the sweep and event triggers
- orchestrate tickets up the debt runs leave and grants Auto where the criterion holds
- Projects advance toward assigned outcomes within delegated authority — revisit when: Actual project records repeatedly show that coordinator-owned inquiry misses material opportunities or contrary evidence that a separate review discovers; read the linked coordination records and inquiry results.
