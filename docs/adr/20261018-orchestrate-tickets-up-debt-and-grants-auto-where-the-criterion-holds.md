# ADR: orchestrate tickets up the debt runs leave and grants Auto where the criterion holds

## Status
Accepted — amended by 20261019-the-first-grant-decision-stands-and-a-persons-decline-removes-the-grant: an orchestrator gathers only the debt of landings it recorded, the first grant decision created decides, and a person's decline removes the grant

## Area
Strategy

## Decided by
The user

## Context
A run names the debt it leaves in three places: its report, its pull request's "Debt left" section
and its Ticket's completion record. `/done` then offers `ticket-up` for any item a person wants
worked. Under 20261013-debt-is-paid-on-the-path-of-work, items become Tickets only when the user
accepts that offer, and debt off the path of later work stays recorded. An unattended run has no
one to answer the offer. So the debt of every Ticket `orchestrate --autonomous` lands sits on
closed Tickets and merged pull requests, and a person meets it only if later work reaches that
area. That record also rejected a periodic cleanup pass because "it needs infrastructure or someone
to remember it", and `orchestrate` is now that infrastructure.

Under 20261015-only-a-person-grants-auto-to-a-follow-up, a Ticket an agent writes carries Auto
only when a person grants it. The North Star stated this as a Never on agents granting themselves
work. The owner treats `orchestrate` as acting for them while it runs, and ruled that it grants
Auto wherever the grant criterion holds.

## Decision
- At each check-in, `orchestrate` gathers the debt named on the Tickets that landed since its last
  check-in. It checks each item against the current code and groups what still stands by area. It
  skips what an open Ticket already covers, and writes the rest as Tickets through `ticket-up`,
  each linked to its source.
- In `--autonomous`, `orchestrate` applies the grant criterion to every Ticket an agent wrote: the
  debt Tickets it writes and the follow-ups runs write. It grants Auto, through `ticket-up`, to
  each Ticket that passes. The run that found the work never grants it.
- In default mode, `orchestrate` asks the person instead, alongside the next plan. Whatever the
  person grants or approves joins that plan.
- A grant names its grantor on the Ticket, so a person can tell a grant `orchestrate` made from
  their own and withdraw it. `orchestrate` re-reads a Ticket before it launches it.
- When one area keeps producing debt across runs, `orchestrate` proposes a structural refactor to
  the person, with the count. Its direction is the person's call under
  20261013-debt-is-paid-on-the-path-of-work, so the proposal fails the grant criterion and never
  carries Auto.
- The North Star's Never on agents granting themselves work is removed.

## Alternatives Considered
- **The person grants every agent-written Ticket in one batched answer**: keeps the Never, at the
  cost of one answer per batch. The owner chose to delegate the choice to `orchestrate`.
- **`orchestrate` grants within bounds**: only when a person granted the source Ticket, only for
  debt in the paths that run changed, and never for debt found while running a Ticket `orchestrate`
  granted. This limits the chain, but needs a rule that tracks who granted what across
  generations. The owner chose the criterion alone.
- **Debt shown only on the person's waiting list**: no Tickets until the person says so, so the
  debt still waits on someone.
- **Leave debt for the path of later work**: the standing design, under which unattended landings
  leave debt unseen.

## Consequences

### Positive
- Debt from unattended runs becomes Tickets that anyone can see, schedule and close.
- Unattended work continues on what runs find without waiting on a person.

### Negative
- The chain can feed its own queue. Work that runs find is granted and run without a person having
  judged it worth doing now, and debt off the path of any change is paid for in quota. The North
  Star judges cost per unit of merged work, so this counts against it whenever the added work is
  not worth merging.
- The grant criterion is necessary, never sufficient. `orchestrate` now makes the choice a person
  used to make.

## Enforced by
`tests/test_ticket_automation_prompts.py` — `test_orchestrate_tickets_up_debt_and_grants_only_where_it_may` fails if `orchestrate`
stops gathering debt at check-in, grants Auto in default mode or without the criterion, re-grants a
withdrawn grant, lets the run that found the work grant it, or drops the grantor from a grant;
`test_ticket_up_preserves_auto_authority_boundary` is retargeted to the new grant path in
`ticket-up` and the convention: two grantors, the grantor recorded, and never the finder.

## Source
- Session: define on running unattended Ticket work with many agents at once (2026-10-18).
- Supersedes 20261015-only-a-person-grants-auto-to-a-follow-up
- Related: amends 20261013-debt-is-paid-on-the-path-of-work,
  20261015-projects-drive-themselves-as-far-as-each-user-climbs; see also
  20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep,
  20260810-auto-is-an-opt-in-grant-to-unattended-automation
