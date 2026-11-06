# ADR: The Ticket's attempt record carries its Manifest, its progress and its run facts

## Status
Accepted — amended by 20261019-the-comment-the-venue-created-first-decides-each-ticket-fact: where two comments carry one marker the first created decides, a record counts only when the automation identity created and last edited it, and each run fact has one writer; amended by 20261106-review-evidence-serves-substantive-acceptance: progress also preserves first-look status, supported dispositions, evidence validity and mandatory work

## Area
Ticketing

## Decided by
The user

## Context
Under 20260812-ticket-recovery-uses-coherent-pushed-checkpoints, a fresh attempt rebuilds the work
from the Ticket, its branch, the pushed commits, the pull request and CI. The Manifest the run
wrote and its do log stay in the runner's home directory and are lost with its container. A fresh
runner therefore runs figure-out and define again from the Ticket's prose, and it can arrive at a
different Manifest with different gates; the earlier run's decisions and dead ends are lost.
`orchestrate` also needs facts about each run — which session works a Ticket, how many launches
failed, which base it last checked, whether it is ready to land. An independent re-derivation of
the design showed that keeping those facts anywhere but the Ticket makes two records that can
disagree.

## Decision
- The Ticket's one marked attempt record, already written early and updated in place, also holds
  the run's Manifest and a short progress record: the gates passed and at which commit, what
  remains, the decisions taken, and the dead ends. The run refreshes it with each pushed
  checkpoint; checkpoints still follow coherent work, not a timer.
- A fresh runner resumes do on that Manifest instead of defining the work again. Recorded passes
  only guide the order of work; every gate still needs fresh evidence before done.
- The same record carries the run facts `orchestrate` reads: the run's ID and its session, the
  launch count, the base it last checked, and whether it is ready to land. A fact counts only when
  the automation identity wrote it.
- The Ticket and git are the recovery surface and the surface through which agents follow each
  other. The Manifest is not committed to the repository unless the user asks for it.
- A Manifest too long for one venue comment continues in a second marked comment.

## Alternatives Considered
- **Commit the Manifest and its progress to the Ticket's branch**: it survives with git, but it
  puts working files into the change and its diff. The owner ruled that the Ticket is the surface.
- **Keep run facts in the orchestrator's status page**: fewer reads per check-in, but a second
  record beside the store, which the re-derivation showed can mislead a crashed or second
  orchestrator.
- **Keep recovering from the Ticket's prose alone**: a fresh runner defines the work again and can
  change its gates partway through a Ticket.

## Consequences

### Positive
- An agent with no memory of the run continues the same work against the same gates.
- When an orchestrator stops, nothing is lost: a new one rebuilds its picture from the Tickets.

### Negative
- Each checkpoint costs one comment update.
- A venue without comments needs its own rendering of the record in its venue reference.
- GitHub limits one comment's length (about 65,536 characters; not checked here), so a large
  Manifest spans two comments.

## Enforced by
`tests/test_ticket_automation_prompts.py` — `test_attempt_record_carries_the_manifest_progress_and_run_facts` fails if the attempt
record loses the Manifest, the progress record, a run fact or the second marked comment, or if a
fresh runner stops resuming the recorded Manifest; `test_a_run_fact_counts_only_when_the_automation_identity_wrote_it`
fails if a record counts without the automation identity as its writer, or a fact gains a second
writer; `test_landing_and_the_attempt_record_each_have_one_owner` fails if the record's format gains
a second home.

The 20261106-review-evidence-serves-substantive-acceptance amendment retargets
`test_attempt_record_carries_the_manifest_progress_and_run_facts` to preserve assessed
criteria, actual subject, full-look state, supported dispositions and unfinished mandatory work.

## Source
- Session: figure-out on running unattended Ticket work with many agents at once (2026-10-18).
- Related: amends 20260812-ticket-recovery-uses-coherent-pushed-checkpoints; see also
  20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep,
  20260812-trigger-adapters-enforce-per-ticket-single-flight (its rejected lease inside
  `run-ticket` stays rejected: no run renews a lease, and liveness comes from the host)
