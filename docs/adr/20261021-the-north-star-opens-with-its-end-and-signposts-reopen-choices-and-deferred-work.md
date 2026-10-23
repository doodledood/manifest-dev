# ADR: The North Star opens with its end, and signposts reopen strategy choices and deferred work

## Status
Accepted; amended by 20261023-assignment-bounds-delegated-decisions-and-retained-acceptance: assignment scope, delegated decisions and retained acceptance

## Area
North Star

## Decided by
The user

## Context
A project upgraded to surfaces v8 showed three gaps the v8 form left open.

Its *Purpose* named only the barrier its first feature removes, as the form asked: "what is going on and what is in the way, then who the project is for". Later features served the same end by other means and sat outside that Purpose for weeks. The one note meant to catch this lived only in figure-out's docs mode, so records written by other workflows never carried it, and the project's records carried none. Rewritten later, the same project's *Goal* stated three features as outcomes, and *How we know* filled with counts of their use while the end those features serve had no measure.

A deferred Ticket carried its reopen condition in prose. The condition held for weeks and nothing noticed: the ticket convention had no way to say "wait for a condition in the world", and no picker read one. A `Strategy` record gated on a reopen condition had the same problem, and the *Strategy choices in force* list showed titles only, so a session reading the North Star could not see what would reopen a choice.

That project's strategy list was also rebuilt by hand, and setup-project never offered the check that holds it, although this repository keeps one.

## Decision
- **The *Purpose* opens with the end.** The person's end comes first, found by asking "why does that matter?" until the document has no deeper answer. Then come the barriers in its way, then *For* and *Not for*. The *Purpose* trap names a purpose stated as the problem the project's first feature solves. The *Goal* and *How we know* rows carry the same test. Their trap is features written as outcomes and measured by counts of use while the end's own measure is missing. *Produce it honestly*, setup-project's seeding and the reshape from the nine-field form ask the owner for the end first.
- **Every record writer applies the outside-Purpose note.** The note moves from figure-out's docs mode into the ADR conventions' guidance for *Context*, so define, do, orchestrate and a person writing by hand apply it too.
- **Signposts.** A decision record may carry a `Revisit when` field: an observable condition and where it is read. It is expected on a `Strategy` record and editable in place. The same line on a Ticket marks it deferred. The convention's readiness rule reads it at its source: a deferred Ticket is ready only once its condition reads as met, and a source the picker cannot read puts the Ticket in front of the person rather than out of sight. next-ticket and orchestrate apply the rule on every sort, read every strategy signpost on every run whatever their scope, bring a met or unreadable one to the owner, and change no line, record or list. figure-out's docs mode brings a signpost its findings show met to the person.
- **The strategy list shows signposts.** The list amends 20261021-the-north-star-holds-what-decisions-are-judged-against, which kept titles only. It now has one line per `Strategy` record in effect, in filename order: the title, then ` — revisit when: ` and the signpost where the record has one. The North Star conventions state this rule exactly enough that two rebuilds produce the same bytes.
- **setup-project offers the check.** In a project that keeps automated checks, setup-project offers one check that rebuilds the ADR index and the strategy list and fails on a difference.
- **Release.** These ship as surfaces v9, with a v8 upgrade guide. The guide proposes *Purpose*, *Goal* and measure changes and signposts only for the owner's ruling, line by line. An unattended run flags them and writes nothing.

## Alternatives Considered
- **Signposts on Strategy records only**: leaves deferred work, where the missed condition was observed, with no field and no reader. Not chosen.
- **Pickers load the Strategy records instead of the list showing signposts**: every picker would read a corpus to learn what a resident list can show in a line. Not chosen.
- **A gated reopen Ticket per Strategy record**: two artifacts for one condition, which can disagree. Not chosen.
- **The signpost check in next-ticket alone**: orchestrate's runs, which take most unattended work, would never read it. Not chosen.
- **A per-turn end probe in figure-out**: a session-level interruption for a document-level property. Seeding and the upgrade guide reach the same Purpose at the moment it is written or reshaped. Not chosen.
- **A change to update cadence**: the v8 sort already offers an update only when an end, measure, principle or bet moves. No change.

## Consequences

### Positive
- A Purpose seeded from a README no longer narrows the project to its first feature, and the end gets a measure of its own.
- A reopen condition is read at its source on every pick, so its coming true is noticed without anyone remembering it.
- A condition nobody can read stays visible to the person instead of keeping work out of sight.
- The strategy list says what would reopen each choice, and a check keeps it equal to the records.

### Negative
- Every pick now reads one source per deferred Ticket and per strategy signpost, which costs time when sources are slow.
- A signpost whose source is permanently unreadable puts the same item on the person's list at every pick until someone rewrites it.
- Projects at v8 must ask their owner for the end before their *Purpose* changes, so the old shape stays until the owner rules.

## Enforced by
partly — `tests/test_north_star_strategy_list.py` rebuilds this repository's strategy list, signposts included, and fails on any difference; the `LaunchedOnlyWhenMet` property of `verification/models/ticket-protocol/TicketProtocol.tla`, driven by the `deferred` and `prefix` scenarios of `verification/recipes/ticket-protocol-model.md`, checks that a deferred Ticket is launched only once its condition reads as met. Whether a *Purpose* opens with the end, and whether readers bring signposts to the person, stays judgment.

## Source
- Session: (none recorded)
- Related: Amends 20261021-the-north-star-holds-what-decisions-are-judged-against
- Related: 20261019-a-model-checks-the-ticket-protocol-against-the-prose-it-quotes
