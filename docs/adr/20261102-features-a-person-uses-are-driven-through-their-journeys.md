# ADR: A feature a person uses is gated on being driven through that person's journeys, which the evaluator derives

## Status
Accepted

## Area
define

## Decided by
The user — the user approved the Manifest that added a journeys gate to define's feature task file and the probe that mirrors it in figure-out; the agent that ran it chose the wording and the fixture that tests it, under that Manifest's delegation.

## Context

define's feature task file gates that the new path runs (*Behavioral exercise*) and leaves which
journeys get walked to the specification. In replays of one owner's product sessions, kept outside
this repository, a page passed its interface checks, its tests and four code reviews and failed
the next morning on journeys its specification never named: a signed-out visitor from a shared
link met a blank page, sign-in did not return them to the page, a second added item replaced the
first, and a mode ignored its own setting. Each review read the specification's cases; none was
asked to arrive as the person from outside.

A fixed list of journeys in the task file would overfit: the journeys that matter come from the
person and the feature, and the kinds that recur — first arrival from outside, coming back, what
goes wrong, the feature's own modes and quantities — are the part that generalizes.

This decision sits inside what the North Star's *Purpose* names: work trustworthy enough to use
with minimal review.

## Decision

- `define/tasks/FEATURE.md` gains the Quality Gate **Journeys driven as the person**: no MEDIUM+
  when the built feature is driven, as the person it is for, through journeys the evaluator
  derives from that person and this feature — how they first arrive from outside, how they come
  back, what goes wrong, and the journeys only this feature has — with evidence of what the person
  met in each. It is emitted when the feature has a runnable surface a person uses, and skipped for
  a library, an API change or internal work nobody meets directly.
- `figure-out/tasks/FEATURE.md` gains its mirror probe, *Driven as the person*, asked before a
  Manifest exists; this repository's context file lists the pair.
- The `define` recipe carries a fixture, a small trip-planner app with five planted journey defects
  and a fixed twin (`verification/fixtures/journeys-app/`, checked by
  `tests/test_journeys_fixture.py`), so the gate can be driven against known defects.

## Evidence at decision time

Driven once per arm through the `define` recipe, graded where a rubric applies by a grader
session that saw each output under a letter label only.

| Check | Result |
|---|---|
| `d29` a shared trip page, Manifest after / before | PASS / FAIL — after, a gate has the evaluator derive the person's journeys; before, one fixed two-friend script |
| `d30` a library option (guard), after / before | PASS / PASS — no journeys gate in either |
| journeys gate on the seeded fixture | FAIL, naming all five planted defects and four more |
| journeys gate on the fixed fixture | FAIL — none of the five planted defects; seven other defects the fixed twin has |
| the before Manifest's own gates on the seeded fixture | FAIL, naming all five planted defects |

The Manifest written before this change already carried an end-to-end gate that had two friends
plan one trip, and that gate found all five planted defects. On this fixture the journeys gate
found the same five and four more — an unknown trip with no way out, a rejected name with no
message, an add that fails offline with no help, and the empty and crowded trips it could not
reach — so it widened what was walked, but the planted defects alone show no uplift.

On the fixed twin the gate walked signed-out arrival, the return after sign-in, the day-start
setting and two friends adding at once, found each working, and still returned FAIL on defects
the twin has: with about 30 places the plan lists times such as "25:00", and an add sent with no
session is saved while the page asks the person to sign in. Both are in
`verification/fixtures/journeys-app/server.js` (`tripPage` adds two hours per place with no cap;
`addPlace` checks no session). So the gate raised no false alarm; the twin is not free of the
defects an open gate walks into, and a PASS arm needs a twin hardened against them.

## Alternatives Considered

- **A fixed list of journeys in the gate** — not chosen: it is the overfit the Context names, and
  an evaluator would walk the list instead of the person.
- **Leave journeys to the specification and the review gates** — not chosen: the replays show
  every review reading the specification's cases and none arriving from outside.
- **Put the journeys in figure-out only** — not chosen: what figure-out names before building is
  not walked after it; the gate is where the built thing meets the person.

## Consequences

### Positive
- A runnable feature is walked as its person before it is reported done, including the journeys
  nobody wrote down.
- The fixture lets a later change to the gate be driven against known defects.

### Negative
- The gate drives many browser journeys by hand and is the slowest gate on a feature's Manifest.
- An open gate can find defects outside the work's scope; `/do` records those below the bar
  rather than repairing them.
- No uplift measured on planted defects: an end-to-end gate the specification already asks for
  catches them too.
- The fixture's fixed twin fails the gate on defects of its own, so the recipe's
  `journeys-gate-on-the-fixed-app` scenario cannot pass until the twin is hardened.

## Enforced by
partly — `tests/test_journeys_fixture.py` proves the fixture's five defects exist and its twin fixes them; whether `/define` emits the gate and whether an evaluator finds them is judgment, measured by the `define` recipe's drives.

## Revisit when
A drive of the `define` recipe's `todays-gates-on-the-seeded-app` and `journeys-gate-on-the-seeded-app`, or a fixture whose defects no specified case reaches, shows the journeys gate finding nothing the Manifest's other gates miss; read in the `define` recipe's evidence for those scenarios.

## Source
- Session: a `/define` session and a `/do` run on the resulting Manifest, 2026-11-02 (logs kept locally). Drive summaries and blind grades are in the pull request that adds this record.
- Related: 20261102-figure-out-looks-from-the-persons-seat-in-a-fresh-pass, 20261102-the-seat-pass-judges-against-default-product-stances
