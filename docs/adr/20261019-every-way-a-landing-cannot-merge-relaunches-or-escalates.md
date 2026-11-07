# ADR: Every way a landing cannot merge relaunches the run or escalates

## Status
Accepted; amended by 20261107-a-ready-mark-whose-orchestrator-stopped-is-adopted-not-relaunched: a ready mark an orchestrator that stopped left is adopted for landing, not taken over and relaunched

## Area
Ticketing

## Decided by
The user

## Context
20261018-orchestrate-lands-and-run-ticket-stops-at-a-ready-pull-request gave `orchestrate` one
landing turn at a time and the one landing procedure: refresh, check the base, merge with the head
pinned, record. When the base moved, the run was relaunched to merge it in and re-run every gate.
Any other mismatch — a head a person or GitHub's "Update branch" moved, a required check that went
red, a protection no run can satisfy, a pull request closed without merging — made the lander
"report the current state and stop". Nothing relaunched or escalated the Ticket, it kept the one
landing turn at every check-in, and no other Ticket in scope landed. Re-running every gate after
each base move also meant a busy base could relaunch a ready Ticket again and again.

## Decision
- The landing procedure runs in this order: re-read the Ticket, refresh the authority, check the
  base, refresh the head and checks, merge, record. The base comes before the head, since merging
  the base in moves the head.
- When the base has moved, the run merges it in. Where the pull request's own change is unchanged
  by that merge (the same patch ID) and the cross-cut check finds no overlap, only the
  deterministic gates re-run, through the repository's required checks where it has them, and the
  judgment gates' earlier verdicts stand. Otherwise every gate re-runs.
- A head that is not the recorded one, or a required check that fails, relaunches the run to
  repair it, and only commits after the recorded head are new work; `run-ticket` treats an attempt
  as having nothing to redo only when the head is the recorded one and the base has not moved. A
  relaunched run starts from an earlier run's ready mark, which the launch facts leave in place. A
  required check that fails the same way on the base is the base's failure and is not repaired per
  Ticket. A required check still pending leaves the merge for a later turn, and one still pending a
  run timeout after the head was pushed counts as failing. A merge that
  waits only on a required review holds the pull request on the person's list without an
  escalation mark, so their approval alone lets it land. Another protection that needs what no run
  can give, or a pull request closed without merging, gets an escalation record. No Ticket keeps a
  landing turn while nothing works toward its landing.
- Relaunches at landing count in the launch count; one that would take it past three hands the
  Ticket to a person, so a check that keeps failing or a base that keeps moving cannot relaunch a
  Ticket without end.
- A merged pull request counts as the landing only when the Ticket was not reopened after that
  merge; a reopened Ticket is new work, sorted for a launch rather than a landing turn.
- *To land* holds only Tickets marked ready by the orchestrator's own run; one left by an
  orchestrator that stopped is taken over and relaunched.
- `orchestrate` checks in while a Ticket in scope waits for a landing turn, not only while a run is
  live, and sorts each Ticket into the first category whose conditions hold, so a Ticket holding a
  drafted answer is never launched again.
- An escalation that ends before its run releases the claim still reaches the person; clearing the
  mark clears any automation claim, and the next launch starts its count again.

## Alternatives Considered
- **Re-run every gate after every base move**: the standing rule. On a busy base it can relaunch a
  ready Ticket indefinitely, and the judgment gates read nothing the base changed when the patch is
  the same.
- **Re-run only the gates whose paths the base change touched**: needs a map from gates to paths
  that gates do not carry.
- **Escalate every landing failure**: simple, but sends a person work a relaunch repairs.
- **Escalate a missing required review**: a person would then both approve and clear the mark, two
  actions where one says the same.

## Consequences

### Positive
- Every landing failure ends in a relaunch, an escalation or the landing, so one stuck Ticket no
  longer holds the scope's landing turn.
- A base move costs a deterministic re-check, not a full judgment re-run, when the change is the
  same.

### Negative
- A judgment gate whose verdict a base change could affect without changing the patch, through a
  path no deterministic gate covers, keeps its old verdict.
- A relaunch to repair a person's commit re-runs the run's gates over work it did not write.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` — `test_the_one_landing_procedure_refreshes_checks_the_base_and_closes_after_merge`
fails if the steps leave this order, either branch of the base rule is dropped, or a failure route
is lost, and `test_orchestrate_sorts_each_ticket_into_one_category_and_keeps_checking_in` fails if
the categories stop being first-match or the check-in stops firing while a Ticket waits to land;
`verification/recipes/ticket-protocol-model.md` model-checks that every Ticket marked ready is
landed, escalated or taken by a person within its bound. Whether a cross-cut overlaps stays
judgment.

## Source
- Session: figure-out and define reviewing manifest-dev's verification practice, and a model of
  the ticket protocol (2026-10-19).
- Related: amends 20261018-orchestrate-lands-and-run-ticket-stops-at-a-ready-pull-request; see
  also 20260825-escalation-clears-the-claim-and-carries-its-own-mark,
  20261019-a-model-checks-the-ticket-protocol-against-the-prose-it-quotes
