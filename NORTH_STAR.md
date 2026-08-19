# North Star — manifest-dev

Why this project exists, for whom, and what winning means — the standing answers every
session and contributor anchors on. This document informs; it never binds. A boundary that
must be enforced on a piece of work is encoded in that work's own binding contract (for
manifest-dev users: `/define` routes an unsafe "never" to a Global Invariant).

Every line below carries a state, rendered as a dated provenance note:

- **evidence** — something happened in the world, dated; new evidence moves it.
- **hypothesis** — best current thinking, untested; a test moves it.
- **ruled** — the owner decided it; only the owner moves it.
- **empty** — nobody has answered yet, written with what would fill it.

New evidence may lower a line's state. The position text itself changes only by the
owner's ruling, and each change is remembered as a decision record in `docs/adr/`.

## Diagnosis

Experienced developers don't trust agent output enough to hand off larger tasks, and the
tool market compounds the problem instead of solving it: agents build before the problem
is understood, and nothing verifies the output against a stated intent — because
understanding and verification demo worse than generation, tools compete on generation
and overpromise. The one sentence that changes everything if false: developers who care
about quality will adopt workflows that spend more tokens and more up-front process to
get output they can ship with minimal review.

— hypothesis: grounded in our own daily use and the recorded frustration list carried
  since the first strategy doc; untested as a market claim beyond ourselves. 2026-08

## What this rests on

- Understanding-first workflows — investigate, define what done means, execute and
  verify every criterion — produce fewer reworked results than direct prompting.

  — hypothesis: strong lived support across our own projects; never measured. 2026-08

- Skills are a durable, harness-agnostic distribution surface: the same prompts serve
  Claude Code, OpenCode, Codex, and Pi.

  — evidence: shipped and maintained as per-CLI packages under `dist/` since 2026-06.

- A single standalone skill, met first, converts a newcomer into a user of the full loop.

  — hypothesis: named unmeasured in its own record,
  `docs/adr/20260705-front-figure-out-as-door-define-do-loop-as-house.md`. 2026-08

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
minimal review — invest upfront, ship with confidence. The bar a user should hold us to:
*"I can give the agent a complex task and trust the output enough to ship it with
minimal review."*

— hypothesis: this sentence has never been put in front of a stranger as the reason to
  try the project. 2026-08

## How they arrive

Burned by another overpromising AI coding tool and searching for something grounded:
GitHub discovery (search, trending), agent-CLI communities (Discord, forums, official
docs), developer Twitter/X, blogs and newsletters, word of mouth, Reddit. Each discovery
surface is fronted by one standalone skill so the first minute delivers value without
adopting the whole method
(`docs/adr/20260705-front-figure-out-as-door-define-do-loop-as-house.md`).

— hypothesis: channels named, none instrumented; no arrival has been measured. 2026-08

## Money — or what it feeds

Free, open source, no monetization intended. What it feeds instead: these workflows are
built for our own projects first, so every improvement pays there — and they build
public credibility for the first-principles approach. Distribution stays secondary to
getting the workflows right.

— ruled: standing since the first strategy doc; last reaffirmed 2026-07-28. Only the
  owner moves this.

## Winning, and the number watched

— empty: no success definition or watched number has been chosen. Filling it means the
  owner deciding whether winning is external adoption or the workflows serving our own
  projects end-to-end — and then naming the one count that tracks it. 2026-08

## Never

- Hype registers on any surface we write: no "revolutionary", "game-changing", "magic",
  "10x faster", "the only tool you'll ever need", or any superlative promising what
  LLMs cannot reliably do.
- Optimizing for token cost or speed at quality's expense — and the mirror image holds
  too: a run that keeps verifying and repairing past the point its gates are satisfied
  is a defect in our workflow, never a meter the user should have to watch.
- Commentary on this repository's own adoption or popularity (stars, usage, traction)
  anywhere in the repo.
- User-facing complexity: workflows may be sophisticated inside, but the experience
  stays minimal steps, nothing to memorize, "just follow along and it works".

— ruled: each enforced in practice today — the messaging boundaries since the first
  strategy doc, the bounded-not-cheap boundary added 2026-07-28, the traction rule in
  the repository's contributor instructions. Only the owner moves these.

## Open

- Does the standalone-skill front door actually convert? Its decision record names this
  a hypothesis until measured, and commits to reopening the positioning if it doesn't.
  What would fill it: any real signal from a fronted surface — installs, invocations,
  or a user arriving through one. 2026-08
