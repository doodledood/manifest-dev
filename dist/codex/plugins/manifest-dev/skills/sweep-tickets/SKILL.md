---
name: sweep-tickets
description: 'Recover or start one unattended Ticket from a configured shared Ticket Store, then stop. Use from a scheduled agent trigger to resume one interrupted automation-owned Auto Ticket or select one ready Auto Ticket and invoke run-ticket. This is the low-frequency correctness path beside issue-event triggers, not a backlog batch runner.'
user-invocable: true
---

# sweep-tickets

Advance unattended Ticket work by at most one Ticket. A scheduled runner invokes this skill; the
selected Ticket still executes through `run-ticket`.

Read `../ticket-up/references/TICKET_CONVENTION.md`, the project's venue reference, and
`../ticket-up/references/AUTOMATED_EXECUTION.md` before reading or changing store state.

## Establish the shared store and runner

Resolve `tickets/store-config.md` or the project-declared equivalent. The venue must provide one
live claim surface every runner reads. A files venue spread across clones, branches, or worktrees
does not: report that it cannot safely sweep and stop without changing a Ticket.

Resolve the adapter's stable automation claim identity and any configured effort or type filter.
The automation identity must be distinguishable from human assignees. Missing or ambiguous store,
identity, or policy context stops before selection.

## Select one Ticket

Build the eligible set before choosing a branch: open Auto Tickets that match every configured
effort or type filter and whose dependencies are all closed. A type filter never treats an untyped
Ticket as a wildcard. Leave closed, ungranted, dependency-blocked, policy-filtered, and
human-assigned items untouched. Ignore tracking items and venue items that are not Tickets.

1. **Recover first.** From the eligible set, find Tickets claimed by this automation identity. The
   adapter's per-Ticket single-flight guarantees that a `run-ticket` invocation waits for any live
   run for that same canonical Ticket before it reaches this state. If any admitted interrupted
   attempt exists, recover one before considering new work. When several recovery candidates exist,
   use the store's explicit override or the convention's delay-loss rule to choose among them.
2. **Otherwise start ready work.** Compare the unassigned Tickets in the eligible set using the
   store's explicit priority override or the convention's expected-delay-loss rule. Judge current
   unattended end-to-end execution and landing time only when its difference materially changes
   what other eligible work loses by waiting. Do not infer days from traditional feature size or
   apply a fixed agent-speed multiplier; when plausible runtimes are all short relative to the
   consequences, treat them as effectively equal and use shorter duration only as a tiebreak.

Human-assigned Tickets are paused, not recovery candidates. Never mutate any claim during
selection, remove Auto, or create a ready/running/retry label. If no Ticket qualifies, report why
and stop without a write.

## Run and stop

Invoke the `manifest-dev:run-ticket` skill with the chosen Ticket's canonical reference and the
complete current venue context. Do not invoke `next-ticket`: it is a human selector, does not
filter on Auto, and stops after presentation.

After `run-ticket` returns, stop. Do not select a second Ticket, even when the first one was already
done, reconciled, escalated, or completed quickly. The next scheduled invocation advances the
graph again.

## Gotchas

- Selection is not execution. Let `run-ticket` own the claim transition, recovery inspection,
  branch, pull request, comments, and terminal Ticket outcome.
- Closing a dependency needs no label pulse or dependent-issue mutation. The next sweep derives
  that the dependent Ticket is ready.
- Two overlapping sweep jobs may initially name the same Ticket. The adapter's canonical
  per-Ticket single-flight serializes their `run-ticket` calls; the later call refreshes state and
  stops when the earlier one finished or handed the Ticket to a person.
- One Ticket per invocation is the simplicity boundary. Throughput comes from issue events and
  independent Ticket keys, not from turning a sweep into a batch orchestrator.
