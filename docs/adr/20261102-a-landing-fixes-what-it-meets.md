# ADR: A landing fixes what it meets — a cross-cut extends the run, and a red base gets one repair Ticket

## Status
Accepted

## Area
Ticketing

## Decided by
The user

## Context
20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges makes `/do` fix
the pre-existing issues its work meets, and leave as debt only what is a project of its own, needs
a person, or a project's own rules keep out. The landing protocol in `ticket-up`'s
`AUTOMATED_EXECUTION.md` → *Landing*, with `run-ticket` and `orchestrate`'s check-in, still worked
to an older rule in two places:

- **A cross-cut at landing.** When the base moved and landed one more instance of something the
  Ticket's change reshapes, the run extended its work only when the extension "fits its Ticket",
  and otherwise wrote a follow-up for a person. This was set in
  20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep. Its premise was that a
  follow-up for a person is the only home for work outside the Ticket. Since then, `orchestrate`
  tickets up the debt runs leave, so work outside the Ticket has a home that needs no person.
- **A red base.** When a required check failed the same way on the base, every run named the cause
  and finished, and `orchestrate` paused the effort once and raised one item for the person. This
  was set in 20261019-one-cause-failing-several-runs-pauses-the-effort-once. Its premise was that a
  base failure is one no run can fix. A CI or venue outage fits that premise. An ordinary broken
  test on the base does not: one run could fix it, yet the effort stayed stopped until a person
  did.

## Decision
- **Cross-cut.** A landing run that finds a cross-cut extends its own work to cover it, unless the
  extension is a project of its own, needs a decision a person retains, or the project's own rules
  keep it out. Then the run names the cross-cut as debt in the completion record, which
  `orchestrate` tickets up with the rest of the run's debt. An extension changes the pull request's
  own patch, so every gate re-runs, as step 3 already requires.
- **Red base.** A run still names a base failure and finishes, without repairing it inside
  another Ticket, and `orchestrate` still pauses the effort once on it. A cause no code change can
  fix waits for the person, as before. A base check a code change can fix gets one repair Ticket,
  in either mode:
  - Whenever a `Paused:` line an orchestrator wrote names no repair Ticket for such a cause, an
    orchestrator writes one through `ticket-up`, in that effort, scoped to making that check pass
    on the base. `ticket-up` reuses an open Ticket that already covers it. The orchestrator then
    names the repair Ticket in the line. When the line already names another one, or is gone, it
    closes the one it just wrote as a duplicate.
  - While the pause holds, only the repair Ticket the line names may launch or land.
  - The repair Ticket takes the mode's grant step like any Ticket an agent wrote, so its Auto comes
    from a person or from `orchestrate --autonomous` under its criterion, never from the run that
    found the failure.
  - Its own run repairs the failure, as the one exception to the rule that a base failure is not a
    Ticket's to repair.
  - Once the base check passes, any orchestrator removes the line, as before.
  - A `run-ticket` started by hand, with no orchestrator, names the cause and finishes.

## Alternatives Considered
- **Keep "fits its Ticket" and a follow-up for a person**: rejected. It sends a person small work
  the run could do, while the same run fixes larger unrelated issues on its own path.
- **The first run that meets a red base repairs it inside its own pull request**: rejected. That
  pull request then carries an unrelated repair, and every other run in the effort races to make
  the same repair.
- **Keep the pause for a person on every base failure**: rejected for failures a code change can
  fix. Kept for outages.
- **Commission the repair Ticket before writing the pause line**: rejected. Runs would keep
  launching onto a red base until the Ticket existed.

## Consequences

### Positive
- An unattended effort recovers from a broken base without a person, under the same gates and Auto
  rules as any Ticket.
- Small cross-cut work lands with the change that caused it, rather than waiting on a follow-up.

### Negative
- A landing can grow beyond what the Ticket text named. Bounded by the same three exceptions `/do`
  uses, and by every gate re-running.
- An orchestrator that stops between writing a repair Ticket and naming it in the line leaves a
  second repair Ticket open. Its run finds the check already passing and has nothing to change.
  A scratch model of two orchestrators, one of which may stop at any step, found no other
  duplicate, no stuck state, and no second repair landing.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` — `test_a_red_base_gets_one_repair_ticket`
fails, on the source and the Codex copy, if the repair Ticket, its deduplication, its sole right to
launch during the pause, its grant step or its exception to the base-failure rule leaves the text;
`test_orchestrate_orders_cross_cutting_pairs_and_checks_them_at_landing` fails if the cross-cut
rule goes back to "fits its Ticket". Judging whether an extension is a project of its own, and
whether a cause is one a code change can fix, stays judgment.

## Source
- Related: amends 20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep and
  20261019-one-cause-failing-several-runs-pauses-the-effort-once; follows
  20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges; see also
  20261019-every-way-a-landing-cannot-merge-relaunches-or-escalates
