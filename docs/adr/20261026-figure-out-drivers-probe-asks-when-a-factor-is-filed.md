# ADR: figure-out's drivers probe asks its question when a factor is filed, not only when an aim is judged

## Status
Accepted

## Area
Task guidance

## Decided by
An agent, with no review — under the user's delegation to test whether *Drivers across
branches* catches the vote case and a harder one, to improve it where it misses, and to merge
the change. The wording is the agent's.

## Context

`20261025-figure-out-counts-each-driver-against-every-aim-it-moves` added *Drivers across
branches* to `figure-out/tasks/DECISION.md`. Its evidence was single-turn: `DECISION.md` was read
at the moment the cross-branch factor mattered. In a real session the file is read at the first
turn, a factor is filed under one aim a few turns later, and the aim it also moves comes up after
that.

In-session simulations tested that order on three fictional decisions: the vote between parties
A, B and C, a clinic-software "Lite" plan whose email-only support was filed as a cost saving,
and a laptop choice with no cross-branch factor (a control). The session's own model wrote the
filing turn, then continued to the next aim. Each variant produced three replies per turn, and
two graders per batch graded them blind, on graders written before the results. They agreed on
every reply. These are not eval-suite results.

| Case, turn | no probe | probe as shipped | this wording |
|---|---|---|---|
| vote, filing turn: says settlements also move another aim | 0/3 | 0/3 | 3/3 |
| vote, economy turn: counts the economic effect of settlements | 0/3 | 0/3 | 3/3 |
| Lite plan, filing turn: says email-only support also moves revenue | 1/3 | 1/3 | 3/3 |
| Lite plan, revenue turn: links support to churn or onboarding | 0/3 | 2/3 | 3/3 |
| laptop control, price turn: raises no cost or saving the user did not state | 3/3 | 3/3 | 1/3 |

The shipped probe missed the vote case once the session ran over several turns. That the new
wording names the settlements' budget cost every time rules out a reading where the model avoids
a politically loaded link; the miss was the probe not firing when the factor was filed.

The eval suite then ran `86` (vote), `87` (Lite plan) and `88` (laptop control) with this wording.
The suite has no scripted second turn, so it tests the single-turn condition only. Three runs per
arm, `sonnet` judge: `86` passed 3 of 3 with the plugin and 0 of 3 without; `87` 3 of 3 and 2 of
3; `88`, plugin arm only, 1 of 3. One `88` failure adds a battery-aging line under price that
concludes it changes nothing; the other names no added cost, and its grader is not yet checked
against it (suite README, *Drivers across branches — 2026-10-26*).

## Decision

Reword *Drivers across branches* so it asks at two moments. When a factor is weighed or set aside
under one aim, as "a low weight" or "neutral", it asks which other aims the factor also moves, and
says so then. When the session turns to a new aim, before judging options on it, it asks what
drives that aim — factors already filed under other branches included, low-weight ones too — how
each option reaches it, and roughly how large each effect is. It still counts each factor against
every aim it moves. `87-decision-driver-filed-in-passing` and the plugin-only guard
`88-decision-no-driver-to-carry` join `86` as its eval cases.

## Alternatives Considered

- **Keep the shipped wording**: it missed the vote case in every multi-turn reply (0 of 6).
  Rejected.
- **Move the probe to `SKILL.md`'s spine**: rejected by
  `20261025-figure-out-counts-each-driver-against-every-aim-it-moves` because it made small asks
  heavier; this miss is about when the probe fires, which the probe's own wording can fix.

## Consequences

### Positive
- A factor filed under one aim is flagged against the other aims it moves at the moment it is
  filed, so a later turn does not have to recall it from far back.

### Negative
- On a choice with no cross-branch factor, the probe can add a short check of an earlier factor
  under the new aim. The laptop control showed one such line in simulation and in `88`.
- The multi-turn evidence is simulation only.

## Enforced by
partly — `86-decision-driver-in-another-branch` and `87-decision-driver-filed-in-passing` (`counts-the-driver-from-another-branch`) and `88-decision-no-driver-to-carry` (`carries-no-false-driver`) in the figure-out eval suite; whether a factor reaches an aim stays judgment

## Revisit when
`88-decision-no-driver-to-carry` fails on most runs for an added link or cost the reader agrees is padding, or a session's log shows the probe adding analysis to a small choice — read in the suite README's results and figure-out logs.

## Source
- Session: a figure-out investigation of the debt PR #397 left, 2026-10-26; simulation batches and blind keys kept outside the repository.
- Related: Amends 20261025-figure-out-counts-each-driver-against-every-aim-it-moves
