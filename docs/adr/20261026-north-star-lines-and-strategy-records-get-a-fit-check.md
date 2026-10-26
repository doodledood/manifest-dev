# ADR: North Star lines and Strategy records get a fit check, and an unattended run follows one that applies and raises the challenge

## Status
Accepted

## Area
North Star

## Decided by
The user

## Context
Sessions cut options because a North Star line seems to cut against them. Often the line does not
cover the case: it is read wider than it was written. For example, "Each piece stands alone" rules
out requiring one piece to use another. It does not rule out an optional offer that a person can
decline.

North Star ends and principles are different from a chosen option. A principle is written to hold
even when evidence says crossing it would pay, and
`20261023-assignment-bounds-delegated-decisions-and-retained-acceptance` keeps owner-retained ends
and bounds with the owner. `Strategy` records are the guiding choices that the North Star lists as
*Strategy choices in force*. Other decisions derive from them, and their signposts already go to
the owner when met.

## Decision
A North Star line gives grounds for a second look, never a silent veto. When a line seems to cut
against an option, the session first checks that the line covers this case. Where it does not, the
option stands, and the session says why the line does not apply. Where it does, a person decides.
A run with no person present follows the line and brings the challenge to the owner, and its run
continues. It never departs from an end or a principle by itself, and it never drops an option
unseen because a line cuts against it.

`Strategy` records follow the same rule, not the record rule in
`20261026-decision-records-give-grounds-not-a-veto`, except that a run whose assignment
explicitly delegates that decision, such as orchestrate pursuing an assigned outcome within
delegated authority, may reopen a `Strategy` record that covers its case. No delegation lets a run
depart from an end or a principle. The North Star's update asymmetry is unchanged: its text changes only on an authorized
ruling.

The rule lives in the North Star conventions (`docs/NORTH_STAR_CONVENTIONS.md` and the shipped
`setup-project/references/NORTH_STAR_FORMAT.md`), beside "It informs; it never binds". A short form
lives at the end of the North Star skeleton's opening paragraph and in the North Star bullet of the
context-file section.

## Alternatives Considered
- **The same rule as other records.** An unattended run departs from a North Star line or a
  `Strategy` record when the need makes sense, and reports it afterwards. Rejected by the user for
  North Star lines: a principle is meant to survive a run's judgment in the moment. Rejected for
  `Strategy` records too: it would change the signpost rule in six files (the North Star format,
  figure-out's docs mode, orchestrate, next-ticket, the ADR conventions and the glossary's
  *Signpost*), for choices that other decisions derive from.
- **Surface only, without a fit check.** The run follows any line that seems to apply. Rejected:
  most false blocks come from a line read too wide, and this keeps them.

## Consequences

### Positive
- Lines read wider than they were written stop cutting options.
- An unattended run is never left waiting for a ruling on a North Star line. It follows the line
  and keeps going, and the owner sees the challenge.

### Negative
- A line that does apply still binds an unattended run until the owner rules, even when the run
  judges it wrong for the case.
- The fit check is judgment, and a run can misjudge it in either direction.

## Enforced by
partly — eval cases driven through `verification/recipes/figure-out.md`:
`claude-plugins/manifest-dev/evals/24-ruled-position-holds` pins that an unattended run keeps a line
that covers the case and looks for a design that keeps it, and
`90-north-star-line-read-too-wide` pins that a line read wider than its words and reason does not
cut the option and that the line's text is left unchanged; the fit judgment stays judgment

## Source
- Session: a figure-out session on records and North Star lines treated as blockers, 2026-10-26.
- Related: 20261026-decision-records-give-grounds-not-a-veto, 20261023-assignment-bounds-delegated-decisions-and-retained-acceptance, 20260820-north-star-lines-carry-states
