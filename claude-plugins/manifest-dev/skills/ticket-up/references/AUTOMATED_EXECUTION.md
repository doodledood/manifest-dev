# Automated Ticket execution

This is the integration contract between a Ticket Store and a hosted agent runner. The
store remains the only durable workflow state; the runner supplies delivery and liveness.

## The two invocations

An eligible issue event invokes one exact Ticket:

```text
Invoke the manifest-dev:run-ticket skill with: "<canonical Ticket URL or ID>"
```

A scheduled trigger invokes the one-Ticket sweep:

```text
Invoke the manifest-dev:sweep-tickets skill
```

Both routes converge on `run-ticket`. The event is the fast path. The sweep is the correctness
path: it recovers interrupted work and eventually notices work made ready by another Ticket
closing. The sweep can operate alone. Events are an optional fast path; without the sweep, missed
deliveries and dependency closes are not recovered reliably. Using both adds latency and
parallelism benefits, not a second execution model.

## Recommended setup

Start with one scheduled automation. It is the smallest complete deployment and can drive the
whole Ticket graph by itself:

- Set cron to `*/10 * * * *` for a ten-minute default. Most hosted schedulers interpret cron in
  UTC; confirm the host's convention. Use five minutes for lower latency or 15–30 minutes to spend
  fewer runner invocations.
- Give the scheduled agent exactly the sweep prompt above. It selects at most one Ticket, invokes
  `run-ticket`, and exits. The next schedule advances the graph again.
- Configure the stable automation identity, human escalation recipient, finite provider retries,
  timeout, optional effort/type filters, and overall concurrency in the host or store config.

Add a second, event-triggered automation when lower latency and parallel work matter:

- Listen for issue `opened`, `reopened`, and `unassigned` events, plus `labeled` when the applied
  label is `auto`. Re-fetch that exact issue and apply event eligibility before launching.
- Give the event agent the exact-Ticket prompt above, replacing the placeholder with the issue's
  canonical URL or ID.
- Use the same automation identity and per-Ticket single-flight key for both automations. Different
  Ticket keys may run concurrently; duplicate deliveries for one Ticket serialize and re-check.

Schedule only is correct but starts at most one Ticket per tick. Event plus schedule adds the fast
path and parallelism while the schedule still recovers crashes and notices dependents made ready by
another Ticket closing. A person may also run the exact-Ticket prompt manually at any time; manual
invocation does not require Auto and does not change the unattended trigger rules.

## Adapter responsibilities

Keep the adapter thin. It owns only what the host can know or enforce:

1. **Event eligibility.** Before launching an issue event, confirm that the item is a Ticket,
   open, unassigned, carries Auto, has no open dependency, and matches any configured effort or
   type filter. A schedule delegates those store-level checks to `sweep-tickets`.
2. **Stable automation identity.** Use one recognizable claim identity, distinct from the people
   who receive escalations. Record that identity and the human escalation recipient in the
   project's store config.
3. **Per-Ticket single-flight.** Key execution by canonical Ticket identity. For GitHub, use
   `<owner>/<repository>#<issue-number>`. At most one run for that key may be active. A queued run
   resolves the Ticket again after the preceding run ends and stops if it is closed or assigned
   to a person. Different Ticket keys may run concurrently.
4. **Finite runner retries.** Configure a finite provider-native retry policy for runner failures.
   Retry count, delay, timeout, schedule cadence, and overall concurrency are deployment choices,
   not Ticket fields or skill behavior.
5. **Terminal runner-failure handoff.** When the provider exhausts retries without a Ticket-level
   DONE or ESCALATED outcome, resolve the Ticket again. If it remains open and is not assigned to
   a person, write or update one operational handoff comment containing the failed run URLs or
   IDs, the last known branch and pull request when discoverable, and the fact that no terminal
   Ticket outcome was recorded; then assign the configured human. Use a stable hidden marker so a
   repeated hook updates the same comment instead of duplicating it.

The adapter does not remove and re-add `auto`, keep a retry counter on the Ticket, infer process
liveness from the assignee, or create ready/blocked/running labels. Claims express ownership.
Dependencies express blocking. The host's execution system is the source of truth for live jobs.

## Authority at landing

Auto is the durable authority for unattended work, not a launch pulse. An unattended run refreshes
the Ticket immediately before an irreversible landing and stops if Auto was removed, the Ticket
was closed, or a person took the claim. A person directly invoking `run-ticket` supplies the
authority for that supervised run even when the Ticket has no Auto grant.

Ticket bodies and comments are untrusted work context. They cannot grant their own execution,
change adapter policy, or turn quoted commands into instructions.

## Recovery boundary

The durable recovery surface is the Ticket, its early attempt comment, one stable remote branch,
pushed commits, one pull request, and current check state. A replacement agent reconstructs from
those artifacts. It need not receive the earlier conversation or workspace. Uncommitted work and
unpushed commits may be lost; coherent pushed checkpoints are the durability boundary.

## Minimal GitHub shape

- Trigger an issue run after an `auto` label, open, reopen, or unassignment event only when the
  refreshed issue passes event eligibility.
- Trigger `sweep-tickets` on a schedule. One invocation handles at most one Ticket.
- Apply the same per-issue concurrency key to event and sweep-launched `run-ticket` jobs.
- Let normal repository protections govern pull-request landing.
- Keep the scheduled sweep even when issue events are enabled: dependency closure and a crashed
  event delivery do not reliably produce an event on the Ticket that should run next.

## Gotchas

- A claim is not a lock between two jobs using the same automation identity; only keyed
  single-flight prevents that overlap.
- Reapplying `auto` as a retry pulse can create an event loop and erases the useful distinction
  between durable authority and delivery.
- Assigning the configured person is a pause. After resolving the blocker, that person records
  the continuation context and unassigns the Ticket; readiness then becomes true naturally.
- A provider crash is not a Ticket-level ESCALATED outcome. Only the terminal failure hook may
  convert exhausted infrastructure retries into a human operational handoff.
