# North Star — manifest-dev

What this project is for, for whom, and how it measures progress — the base every session and
contributor decides from. This document informs; it never binds: a boundary that must be
enforced on a piece of work is encoded in that work's own binding contract (for manifest-dev
users: `/define` routes a principle whose violation would be unsafe or irreversible to a Global
Invariant). The choices made along the way live in `docs/adr/`, never here.

Every position below carries a state, rendered as a dated provenance note:

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — the owner decided it; only the owner moves it.
- **empty** — nobody has answered yet, written with what would fill it.

New evidence may lower a position's state. The position text itself changes only by the
owner's ruling, and each change is remembered as a decision record in `docs/adr/`. The full
form — sections, states, maintenance — is `docs/NORTH_STAR_CONVENTIONS.md`, which governs and
needs no tooling.

## Purpose

Agents can write almost anything, and projects still drift. What a project is becoming, what is
worth doing next and what done means live in whoever is working, so every session and every
teammate works them out again, and the agent's speed multiplies work nobody can tell was worth
doing. manifest-dev keeps that understanding in the project and makes an agent's output
trustworthy enough to ship with minimal review.

— hypothesis: 2026-08-20. Records: The project is the unit the workflows serve, not the single task.

For: quality-first developers — five-plus years of experience, already working with an agentic
coding CLI, willing to spend tokens and up-front effort for output they can trust — in a team of
any size, on a project of their own or inside a codebase where most colleagues do not use
manifest-dev. Secondary: teams standardizing how AI-assisted development is done.

Not for: cost optimizers, speed-first shippers, tinkerers who want to tweak everything, hype
chasers, and people not using a coding agent at all.

— ruled: 2026-10-15. Records: Projects drive themselves as far as each user climbs, and manifest-dev fits inside teams that do not use it.

## Goal

*"I can give the agent a complex task and trust the output enough to ship it with minimal review
— and come back to the project weeks later and find it still knows what it's becoming, what's
next, and what done means — and find the codebase easier to change correctly than when I started
— and, as far up the autonomy ladder as I choose to go, find the project moving forward on its
own, taking its next work from its queue and asking me only when it needs my judgment, taste or
authority."*

— ruled: 2026-10-15. Records: Projects drive themselves as far as each user climbs, and manifest-dev fits inside teams that do not use it; The promise includes a codebase that gets easier to change correctly.

For the project itself: our own projects run end to end on all three tiers — a North Star that
stands, work pulled from a Ticket store, and execution against a Manifest with gate evidence —
and drive themselves wherever they can. Outside recognition is welcome as a consequence of that,
never a target traded against it.

— ruled: 2026-10-15. Records: Winning is our own projects running the full loop; recognition is a consequence.

## Principles

- **Quality decides.** Cost and speed bind second to it: a workflow stays practically affordable
  on high-end models and its verification fast enough that many agents at once are not held up,
  and neither is ever bought with quality. A run that keeps verifying and repairing after its
  gates hold is a defect in the workflow, never a meter the user has to watch.

  — ruled: 2026-10-15. Records: Cost is a binding constraint, second to quality; Verification speed binds like cost, second to quality.

- **Simple to use.** Workflows may be sophisticated inside; the experience stays minimal steps,
  nothing to memorize — follow along and it works.

  — ruled: standing since the project's first strategy document, before 2026-07-28.

- **Each piece stands alone.** Nothing has to be adopted whole to be useful. The autonomy ladder
  is the levels a user may adopt — one skill on its own; one piece of work understood, defined
  and verified; a project that keeps its direction, vocabulary, decisions and checks; a shared
  queue of Tickets; and unattended runs that take work from that queue — and each level works
  without the ones above it. What a user adds to a shared repository reads as plain files and
  plain instructions, so a colleague who does not use manifest-dev keeps working as before.

  — ruled: 2026-10-15. Records: Projects drive themselves as far as each user climbs, and manifest-dev fits inside teams that do not use it.

- **Claim only what holds.** No hype register and no superlative promising what models cannot
  reliably do, on any surface we write; no commentary on this repository's own adoption or
  popularity.

  — ruled: standing since the project's first strategy document, before 2026-07-28.

- **Free and open.** No monetization intended; the workflows are built for our own projects
  first, and distribution stays second to getting them right.

  — ruled: standing since the project's first strategy document; reaffirmed 2026-07-28.

## How we know

- **Our own projects running all three tiers at once** — a count; up.

  — ruled: 2026-08-21. Records: Winning is our own projects running the full loop; recognition is a consequence.

- **Merged work that needed a person only for judgment, taste or authority** — a share; up.

  — empty: no count chosen. What would fill it: the owner's choice, once our own projects run unattended work. 2026-10-15

- **Shipped work that had to be reworked** — a rate; down.

  — empty: the trust part of the goal has no measure. What would fill it: the eval baseline or our own projects reporting rework. 2026-10-21

- **A codebase that gets easier to change correctly** — corrections that became checks, and debt
  paid on the path of later changes; up.

  — empty: nothing counts it. What would fill it: real projects reporting the checks and debt their runs leave. 2026-10-21

- **Cost per merged change** — down, never at quality's cost; judged per unit of merged work once
  runs go unattended, so cheap runs that escalate count against it.

  — ruled: 2026-10-15. Records: Projects drive themselves as far as each user climbs, and manifest-dev fits inside teams that do not use it.

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

- Gates that carry evidence can stand in for a person reviewing each change, so work can land
  unattended wherever it needs no one's judgment, taste or authority.

  — hypothesis: no project has yet run unattended work at volume against reviewed work. 2026-10-15

## Open

- Does the project-level half of the goal hold for anyone but its author? What would fill it:
  someone who is not the maintainer keeping a project's direction, its queue, and its definition
  of done in these surfaces. The owner assumes it does; no one else has tried it. 2026-08,
  owner's assumption 2026-10-15
- Does this wording say what the owner means? Every position above was reshaped into this form
  by an agent on 2026-10-21, from a draft the owner accepted; the states are those of the lines
  each replaces, and the wording awaits the owner's line-by-line ruling. What would fill it: the
  owner ruling each line. Records: The North Star holds what decisions are judged against, and chosen options live in decision records.

## Strategy choices in force

- The project is the unit the workflows serve, not the single task
- Positioning drops the conversion funnel; the standalone shape stays on honest grounds
- One skill per beat, built up from the lean body
- An orchestrating skill runs the queue in parallel and replaces the sweep and event triggers
- orchestrate tickets up the debt runs leave and grants Auto where the criterion holds
