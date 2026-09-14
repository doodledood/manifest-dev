# ADR: A North Star field is applied only by a consumer at its decision point; `Who it's for` gets one in figure-out

## Status
Accepted

## Area
North Star

## Context

A feature shaped through the full loop — figure-out, define, do — came out directionally right, and its niche flow branches were not adapted to the person the project is for. The project carried a North Star, resident in every session, whose `Who it's for` named that person. The gaps surfaced only afterwards, when the maintainer asked for every user story that person would ideally want and held the built feature against them.

Nothing in the loop had a line that took that person's seat — reasoned from their position as the one who will use the thing, through every use they would make of it — while the work was being shaped. figure-out's feature probes walk the *what* (the slow-motion walk) and the *seen surface* (the undiscussed-surface sweep); `/define`'s feature gate checks that every *specified* use case is implemented, without asking who specified them; the design skill and `/define`'s writing gates take their audience from the brief or from "the reader the deliverable names". Reading the shipped skills for what consumes each North Star field: `Promise`, `Never`, `How they arrive`, and `Money` are read by `/define`'s marketing task file; `Winning` and `Never` by `next-ticket`; `Diagnosis` by figure-out's docs mode when a decision is recorded. `Who it's for` is read by nothing. The record that introduced the North Star (`20260820-manifest-dev-owns-a-project-north-star`) listed "every session by residency" among its consumers and, in its own consequences, named the risk this fills: "a field nothing consults is possible; the admission bar for future fields stays 'a consumer that changes behavior'."

Residency, then, is what "keep the person the project is for in mind at all times" looks like as a prompt, and it did not make the field bite on flow details. A *consumer* here is a line in a skill that reaches into the North Star at the moment a specific decision is being made and lets the field steer it — as the marketing gates do for `Promise`, or `next-ticket` does for `Winning`.

This decision sits inside what the North Star's Diagnosis names — direction that was written down and still lived only in whoever was at the keyboard at the moment of shaping.

## Decision

A North Star field is applied only by a concrete consumer at the decision point it bears on; being resident in the session is not enough. `Who it's for` gets its first consumer in figure-out's spine — the always-on core of its prompt, loaded on every invocation — as a widening beside the line that fires when the read implies making something:

> Whatever the read implies making is for someone: the person the project's North Star names under *Who it's for*, or find out who. Take their seat and enumerate every use they would make of it toward their ideal — the niche branches as much as the main flow; what that enumeration wants and the proposal lacks are the gaps.

The line is conditional on an artifact, so a session whose read implies making nothing carries only the condition. Where the project keeps no North Star, the seat still exists and the session finds out who sits in it. figure-out's feature probe file gains one clause naming user stories as the feature-shaped rendering of the same walk, pointing at the spine rule rather than restating it. Docs mode changes nothing: its bootstrap already loads the North Star, so the person is in context when the spine line asks for them, and a second statement there would be one rule in two files.

Three grounds fix the placement:

- **Generality.** The seat exists for every artifact — a feature's user, a document's reader, a design's operator — and figure-out has no probe file for writing or design shapes. A probe-file home would cover only features. This is the same ground `20260824-undiscussed-surface-sweep-lives-in-read-naming-checkpoint` used to place its sweep in the spine.
- **Timing.** That person's uses have to shape the design while it is still soft. The read-naming checkpoint fires too late; a line that holds throughout fires as soon as an artifact comes into view.
- **Independence from docs mode.** Docs mode loads only once the investigation is project-relevant, and not under `--no-docs` or `--team`. A team deliberation about a feature still has a person it is for.

## Alternatives Considered

- **A probe in figure-out's feature task file alone**: a default-press probe naming user stories from the seat of the person the project is for — rejected. figure-out's probe files cover code, diagnosis, research, and technical-design shapes, and none covers writing or design artifacts, so those would keep shaping for nobody; and probe files load as optional awareness, the posture the surface-sweep record found under-weighted.
- **A lens line in figure-out's docs mode** ("read the topic through the North Star's `Who it's for`") — rejected. It fires only with project relevance and never under `--no-docs` or `--team`; and a general lens over a resident document is residency restated, which is the mechanism that had already failed.
- **A taste entry** in the maintainer's harness memory — rejected. Taste is for preferences another maintainer could hold the opposite of. A session that never checks an artifact against the person it is for is the skill working badly, owed by every session rather than preferred by this one.
- **A `/define`-side gate as the whole fix** (an acceptance criterion that every flow branch serves the person the project is for) — rejected on the surface-sweep record's grounds: a gate catches the mismatch after it is built, while the criterion surfaces cheapest during figuring-out, where the design can still absorb it. A define-side gate remains possible as a complement for sessions that enter at `/define` without a figure-out session; this record does not decide it.

## Consequences

### Positive

- `Who it's for` has a consumer that changes behavior, meeting the admission bar the North Star record set for its own fields.
- Every artifact-shaping session — feature, document, design, under any mode — names the person the artifact is for and walks the niche branches from their seat before anything binds.
- Where the project keeps a North Star, that person costs nothing to source; where it does not, the line makes the missing answer visible instead of letting a builder's picture of them fill it in.

### Negative

- The spine grows by one bullet that every figure-out session carries, including sessions whose read implies making nothing; the conditional opening keeps that cost to the condition itself.
- The placement rests on one project's observed failure plus the verified absence of any consumer of the field. A later session that carries the line and still skips the niche branches is evidence the wording does not force the enumeration, and would reopen the placement.

## Not decided here

- Whether any other North Star field should gain a consumer in figure-out. `Never` already binds through `/define`'s Global Invariant route, `Promise` has its consumer in `/define`'s marketing gates, and `Winning` in `next-ticket`; the rest wait for their own observed failure.
- A `/define`-side gate for sessions that never pass through figure-out.
- Any convention for how a project writes or deepens the description of the person it is for. The `Who it's for` paragraph proved enough to walk from.

## Source
- Session: figure-out session, 2026-09-14 (investigation log kept locally).
- Related: 20260820-manifest-dev-owns-a-project-north-star — whose consequences anticipated an unconsumed field; this record fills it and leaves that record's standing unchanged.
- Related: 20260824-undiscussed-surface-sweep-lives-in-read-naming-checkpoint — precedent for the placement grounds; not superseded or narrowed.
