# North Star — manifest-dev

Why this project exists, for whom, and what winning means — the standing answers every
session and contributor anchors on. This document informs; it never binds. A boundary that
must be enforced on a piece of work is encoded in that work's own binding contract (for
manifest-dev users: `/define` routes an unsafe "never" to a Global Invariant).

Every position below carries a state, rendered as a dated provenance note:

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — the owner decided it; only the owner moves it.
- **empty** — nobody has answered yet, written with what would fill it.

New evidence may lower a position's state. The position text itself changes only by the
owner's ruling, and each change is remembered as a decision record in `docs/adr/`. The
full form — fields, states, maintenance — is `docs/NORTH_STAR_CONVENTIONS.md`, which
governs and needs no tooling.

## Diagnosis

Agents can write almost anything now, and projects still drift. What the project is
trying to become, what's worth doing next, and what done means live in whoever happens to
be working — so every session and every teammate re-derives them from scratch, and the
agent's speed just multiplies work nobody can tell was worth doing. Understanding and
verification demo worse than generation, so tools compete on generation and overpromise.
The one sentence that changes everything if false: spending more tokens and more up-front
process — on understanding, on what's worth doing next, and on what done means — leaves a
project better off than moving faster without them.

— hypothesis: the unit ruled 2026-08-20, after half of one month's decision records
  turned out to sit above the single task the previous text named; the bet sentence ruled
  2026-08-21, moving the stop condition from market adoption to the practice itself.
  Grounded in our own daily use and the frustration list carried since the first strategy
  doc; untested beyond ourselves. See
  docs/adr/20260820-the-project-is-the-unit-not-the-task.md and
  docs/adr/20260821-the-bet-is-about-the-practice-not-the-market.md.

## What this rests on

- Understanding-first workflows — investigate, define what done means, execute and
  verify every criterion — produce fewer reworked results than direct prompting.

  — hypothesis: strong lived support across our own projects; never measured. 2026-08

- Skills are a durable, harness-agnostic distribution surface: the same prompts serve
  Claude Code, OpenCode, Codex, and Pi.

  — evidence: shipped and maintained as per-CLI packages under `dist/` since 2026-06.

## Who it's for

Quality-first developers: five-plus years of experience, already driving an agentic
coding CLI, solo or small-team, willing to spend tokens and up-front effort for output
they can trust. Secondary: small teams standardizing how AI-assisted development is done.

Not for: cost optimizers, speed-first shippers, tinkerers who want to tweak everything,
hype chasers, and people not using a coding agent at all.

— hypothesis: matches ourselves; no user beyond the maintainer has confirmed the
  segment. 2026-08

## Promise

First-principles workflows that make an agent's output trustworthy enough to ship with
minimal review, on work you can tell was worth doing — invest upfront, ship with
confidence. Trustworthy output is what gets felt first, and it is not the whole of it: an
agent can be exactly right about the wrong work. The bar a user should hold us to: *"I can
give the agent a complex task and trust the output enough to ship it with minimal review —
and come back to the project weeks later and find it still knows what it's becoming,
what's next, and what done means."*

— hypothesis: both halves ruled to stand together 2026-08-21; neither has been put in
  front of a stranger as the reason to try the project. See
  docs/adr/20260821-positioning-drops-the-conversion-funnel.md.

## How they arrive

However they find it. The project is built in public and shared as it is used; no channel
is worked and no funnel is maintained. Whatever someone meets first stands alone, so
nothing has to be adopted whole to be useful.

— ruled: 2026-08-21, arrival is not pursued; the standalone shape is kept because it is
  the honest entry to the method, not because it converts. See
  docs/adr/20260821-positioning-drops-the-conversion-funnel.md. Only the owner moves
  this.

## Money — or what it feeds

Free, open source, no monetization intended. What it feeds instead: these workflows are
built for our own projects first, so every improvement pays there — and they build
public credibility for the first-principles approach. Distribution stays secondary to
getting the workflows right.

— ruled: standing since the first strategy doc; last reaffirmed 2026-07-28. Only the
  owner moves this.

## Winning, and the number watched

Winning is our own projects running end-to-end on all three tiers — a North Star that
stands, work pulled from a Ticket store rather than from whoever is at the keyboard, and
execution against a Manifest with gate evidence. Outside recognition is welcome as a
consequence of that working; it is never a target traded against it. The number watched:
how many of our own projects are running all three tiers at once.

— ruled: 2026-08-21, the owner's choice between the two candidates the empty field named,
  grounded in the standing ruling that distribution stays secondary to getting the
  workflows right. See docs/adr/20260821-winning-is-our-own-projects-running-the-full-loop.md.
  Only the owner moves this.

## Never

- Hype registers on any surface we write: no "revolutionary", "game-changing", "magic",
  "10x faster", "the only tool you'll ever need", or any superlative promising what
  LLMs cannot reliably do.
- Trading quality away for token cost or speed — quality stays the deciding axis. Cost
  is a binding constraint now, not a non-goal: workflows must stay practically affordable
  on high-end models, which is why the leaner paths exist (the `just-*` executors; the
  consolidated and self verification modes beside per-gate) — and the mirror still holds:
  a run that keeps verifying and repairing past the point its gates are satisfied is a
  defect in our workflow, never a meter the user should have to watch.
- Commentary on this repository's own adoption or popularity (stars, usage, traction)
  anywhere in the repo.
- User-facing complexity: workflows may be sophisticated inside, but the experience
  stays minimal steps, nothing to memorize, "just follow along and it works".

— ruled: each enforced in practice today — the messaging boundaries since the first
  strategy doc, the bounded-not-cheap boundary added 2026-07-28 and revised 2026-08-20
  (cost promoted from non-goal to binding constraint, second to quality, after high-end
  model pricing forced leaner execution and verification paths into the suite out of
  necessity — see docs/adr/20260820-cost-is-a-binding-constraint-second-to-quality.md),
  the traction rule in the repository's contributor instructions. Only the owner moves
  these.

## Open

- Does the project-level half of the promise hold for anyone but its author? What would
  fill it: someone who is not the maintainer keeping a project's direction, its queue,
  and its definition of done in these surfaces. 2026-08
