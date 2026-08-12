# ADR: A ticket's type is a rollout selector, not a classification

## Status
Accepted — per-Deliverable type assignment now applies only in explicit split mode after 20260812-tickets-follow-independently-schedulable-work-units; single-valued type semantics are unchanged

## Area
Ticketing

## Context

Turning unattended automation on across a ticket store is all-or-nothing. The only thing an automation can select on is the Auto grant, and [20260810-auto-is-an-opt-in-grant-to-unattended-automation](20260810-auto-is-an-opt-in-grant-to-unattended-automation.md) makes that a per-ticket yes/no the author sets at write time, with absence as the fence.

Absence already carries three meanings: the author doesn't trust this ticket, the ticket has a designed-in human step, or the item was never a ticket at all. An operator who wants automation to start on bug work only has no way to say so except by withholding the grant everywhere else — which adds a fourth meaning, *not yet*, indistinguishable from the other three once written. Widening the rollout later then requires re-opening every ungranted ticket and re-deciding, from prose, why each one was withheld.

The gap is narrower than "tickets need categories". Human filtering is already served: the effort label, the ready rule, and the priority rule answer "what should I work on". What nothing provides is a stable, cold-start-queryable property an *operator's* policy can range over — so that policy lives in the query rather than being frozen into the tickets.

The obvious source for such a property is `/define`'s task taxonomy, which already sorts work into Coding, Feature, Bug, Refactor, PR lifecycle, Prompting, Writing, Document, Tech design, Research, and Blog. It is the wrong instrument: that taxonomy is explicitly non-exclusive because its job is loading several gate files at once.

## Decision

**A ticket may carry a type — one of `bug`, `feature`, `refactor`, `docs`, `chore` — naming what kind of work it is. It exists so an operator's automation policy can select granted work without re-reading it.**

**The type is optional and single-valued.** Exactly one value applies, or none. Optionality is what makes a closed set of five safe: work that fits nothing carries no type, and no type query matches it — the same fail-closed shape the Auto grant's silence already has. That also settles hand-written tickets nobody typed, and means the set need only name the stages operators actually roll out by rather than cover all work.

**Type and grant answer different questions and neither reads the other.** The grant says whether automation may touch a ticket at all and is the author's call. The type says what the work is, which is what lets an operator's query say which granted work runs today. Keeping them apart is the whole point: it stops rollout schedule from becoming a fourth meaning riding on the grant's silence.

**The vocabulary is a default a project may replace**, recorded in the same place the store's venue is recorded, so a store that thinks in different terms is not forced into these five.

**No risk ordering ships.** Nothing in the convention or the venue references says which types are safer to automate or which to enable first. That is the operator's policy, and putting it in the ticket would freeze one operator's judgment into work everyone reads.

**`ticket-up` assigns the type per ticket from that Deliverable's own work**, not once per manifest — a manifest can hold a refactor Deliverable beside a new-capability one. `next-ticket` reports the type with its pick but never ranks by it, the posture it already holds for the grant.

## Alternatives Considered

- **Withhold the Auto grant instead of adding a type** — express a narrow rollout by granting Auto only on the tickets in scope. — Rejected: it works today and produces identical behaviour, but it overloads the grant's silence, which already carries three meanings. The ticket then no longer records *why* it is ungranted, so widening the rollout means re-judging every ungranted ticket by hand instead of editing one query.
- **Roll out by the existing `effort:<slug>` label** — automate one effort at a time; the label is already on every ticket and already queryable from a cold start. — Rejected: it needs no new machinery and remains the better dial when rollout stages are bodies of work, but the stages this decision serves are kinds of work, which cut across efforts. An effort is also a coherent thing to judge as a whole, where a rollout that widens by kind cannot be expressed as a set of efforts.
- **Mirror `/define`'s task taxonomy** — reuse the eleven-value set the manifest workflow already computes. — Rejected: it is composable by design ("domains aren't mutually exclusive — a bug fix that refactors uses both"), because its job is loading several gate files at once. Carried onto tickets, enabling automation for one value sweeps in tickets carrying another, so the query stops being predictable — which was the whole reason for moving policy into the query. Several of its values (PR lifecycle, Prompting, Tech design, Blog) are gate-loading concerns nobody stages a rollout by.
- **Include `research` as a type value** — as originally proposed alongside bug, feature, and request. — Rejected: it restates the question kind established by [20260810-shaped-means-the-decision-space-is-closed](20260810-shaped-means-the-decision-space-is-closed.md). Declaring both produces two fields that can contradict each other about the same ticket, and the kind is the one a picker already reads to know which tool to bring. `request` was rejected on a different ground: it names where work came from, and once acted on, a request is a bug or a feature anyway.
- **Make the type multi-valued** — let a ticket carry every type that applies, avoiding the awkward call on mixed work. — Rejected: enabling one type then sweeps in tickets carrying others, unless the operator remembers to require that *every* type on a ticket be enabled — a rule that has to be re-applied correctly on each widening. The single-valued form costs one judgment at write time and buys a query whose result is predictable without that rule.
- **Do nothing** — accept that rollout is all-or-nothing. — Rejected: it is the honest answer only if the rollout never widens. Once it widens even twice, the re-judgement cost of the withhold route exceeds the authoring cost of the field. That trade is the boundary this decision sits on, and it is recorded as an assumption rather than an established fact — no automation consuming the type exists yet.

## Consequences

### Positive

- Rollout policy becomes a query the operator edits, so widening costs one line instead of a pass over every ungranted ticket.
- The Auto grant keeps a single meaning, and its silence keeps the three it already carried.
- A closed vocabulary stays safe against work it does not describe, because untyped means unselected rather than unclassified.
- Filtering a store by kind of work comes along free, though it was not the reason for the field.

### Negative

- Every emitted ticket now carries a judgment that did not exist before, and single-valued means mixed work forces a call that will sometimes be arbitrary.
- A closed default vocabulary will be wrong for some project, which is why it is overridable — but an overriding project loses the portability of a query written against the defaults.
- The field is authoring cost until an automation consumes it, and none does yet. If rollout stages turn out to be bodies of work rather than kinds, the effort label already provided the dial and this is dead weight.
- Two taxonomies now name overlapping words for different jobs — this one, and `/define`'s composable task types. Confusing them is the failure mode to watch, which is why the glossary pins them against each other.

## Source
- Session: figure-out session, 2026-08-11
- Related: [20260810-auto-is-an-opt-in-grant-to-unattended-automation](20260810-auto-is-an-opt-in-grant-to-unattended-automation.md), [20260810-shaped-means-the-decision-space-is-closed](20260810-shaped-means-the-decision-space-is-closed.md), [20260809-group-github-tickets-by-sub-issue-membership-and-effort-label](20260809-group-github-tickets-by-sub-issue-membership-and-effort-label.md), [20260807-trim-the-manifest-schema-to-fields-that-are-read](20260807-trim-the-manifest-schema-to-fields-that-are-read.md)
