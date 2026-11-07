# ADR: The comment the venue created first decides each Ticket fact

## Status
Accepted; amended by 20261107-a-ready-mark-whose-orchestrator-stopped-is-adopted-not-relaunched: an orchestrator adopting a ready mark another orchestrator's timed-out run left is the mark's one other writer; amended by 20261107-automation-writes-beside-what-a-person-wrote-never-over-it: answer records each count, in the order created, as an exception to the first-created rule

## Area
Ticketing

## Decided by
The user

## Context
20261018-the-tickets-attempt-record-carries-its-manifest-progress-and-run-facts put every run
fact on the Ticket's one attempt record and said a fact counts only when the automation identity
wrote it. Several orchestrators share that identity, and a venue such as GitHub has no
compare-and-set on a comment: an edit replaces the whole comment and the last writer wins. The
protocol relied on a re-read before each write as if it were a lock. A model of the protocol and
an independent reading of the prose found the races that leaves open: two orchestrators that read
a Ticket with no record each create one, after which an escalated Ticket can still be landed; a
ready mark from one run still counts after a relaunch; and a session fact written by both the
launcher and the run.

## Decision
- Where two comments on a Ticket carry the same marker, the comment the venue created first
  decides. A writer whose comment is not the first removes its own and stands down: it skips the
  Ticket, or stops its run. The rule is stated once, in ticket-up's shared automation reference,
  and the skills and venue references point to it. A Manifest continuation comment is the one
  exception, since it continues the first.
- A writer re-reads the Ticket after it writes. The re-read narrows a race to one write; the
  first-created comment settles it.
- A record counts only when the automation identity created the comment and made its last edit.
- Each run fact has one writer. The launcher writes the session only where the host names it
  before the run starts; otherwise the run records its own session on its first write.
- The ready mark and a drafted answer name the run that wrote them, and count only while the run
  facts name that run.
- A takeover writes a fresh start time, so the timeout runs from the takeover.
- A run re-reads the record and the Ticket before each write and each push, and stops when another
  run is named, a person holds the claim, the Ticket is closed, or, unattended, the escalation mark
  is on. git rejects a push that does not build on the branch's head, so a stale run's push either
  fails or becomes a commit the named run builds on.

## Alternatives Considered
- **A lease or lock comment**: needs a compare-and-set the venue lacks, and a renewal no run makes;
  20260812-trigger-adapters-enforce-per-ticket-single-flight already rejected a lease inside
  `run-ticket`.
- **The comment written last decides**: every writer's own re-read then sees itself winning until
  the next write, so two runs can each act on a different record.
- **One automation identity per orchestrator**: ends the shared-identity races, but every setup
  then needs several bot accounts, and a person can no longer tell automation's claims apart from
  one rule.

## Consequences

### Positive
- Every marker kind the protocol writes has one deciding comment, by a rule any venue with
  creation order can apply.
- A loser finds out on its own re-read and stands down before its first effective write.

### Negative
- Each launch costs one more read of the Ticket.
- A venue with no creation order on its comments needs its venue reference to name what decides.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` — `test_where_two_comments_carry_one_marker_the_comment_created_first_decides`
fails if the rule loses its one home or a skill restates it, and
`test_each_ticket_fact_keeps_one_writer` fails if the session or the start time gains a second
writer, or the ready mark a writer beyond the adopting orchestrator
20261107-a-ready-mark-whose-orchestrator-stopped-is-adopted-not-relaunched names; `verification/recipes/ticket-protocol-model.md` model-checks one attempt
record, pushes that build on the head and merges only at the recorded head, and
`tests/test_ticket_protocol_model.py` fails when a sentence the model quotes leaves its file. Which
marker kinds exist stays judgment.

## Source
- Session: figure-out and define reviewing manifest-dev's verification practice, and a model of
  the ticket protocol (2026-10-19).
- Related: amends 20261018-the-tickets-attempt-record-carries-its-manifest-progress-and-run-facts;
  see also 20260812-trigger-adapters-enforce-per-ticket-single-flight,
  20261019-a-model-checks-the-ticket-protocol-against-the-prose-it-quotes
