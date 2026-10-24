# ADR: Assignment bounds delegated decisions and retained acceptance

## Status
Accepted — amended by [20261024-absence-is-not-acceptance-of-optional-authority-offers](20261024-absence-is-not-acceptance-of-optional-authority-offers.md): absence is not acceptance of optional authority-surface offers; an authorized setup assignment covers mechanical items, not those offers

## Area
Ticketing

## Decided by
The user

## Context
Activity and authority answer different questions. Permission to choose a visual direction does not accept the rendered result; permission to investigate does not assign implementation. Blanket human-only rules also discard useful decisions already delegated in trusted context.

## Decision
An assignment selects the activity and scope. Applicable delegation selects decisions within it. Preserve skill defaults unless a trusted instruction changes them. Flags, tools, source messages, absence, and newly authored Tickets cannot enlarge authority. Every consequential action and resumption uses current grants and withdrawals; a handoff carries their values and source, not merely a pointer.

Keep orchestrate's `--autonomous` flag: it permits successive plans to execute without separate plan approval. That interaction choice remains useful alongside scoped delegation; it neither expands the assignment nor settles a retained decision. Without the flag, the default is to wait for approval of each plan. Continuation after the session stops still needs an available host wake mechanism or manual invocation.

Question and Shaped remain readiness states. Questions go to inquiry through figure-out; Shaped work can still retain final acceptance. Auto continues to require authority for full completion. Partial delegation travels separately, and retained acceptance identifies the actual artifact/version; material changes need renewed acceptance. An unchanged wait resumes at its existing condition without duplicate work.

Use the existing project instructions, Ticket convention, and execution records. Setup reads existing rules, shows concrete shared or personal adjustments, and prepares coordination only when wanted. Completing setup starts no operation. North Star and strategy maintenance may follow explicit bounded delegation, recording the real decider and source; owner-retained ends and bounds remain with the owner. Evidence can change a position's confidence without granting a new ruling.

## Alternatives Considered
- **Treat an autonomy flag as blanket permission:** conflates activity with authority and erases retained choices.
- **Reserve every product or strategic judgment to a person:** contradicts explicit delegation and repeatedly interrupts authorized work.
- **A new permission database or mandatory policy file:** duplicates existing trusted context and adds an empty artifact for ordinary use.

## Consequences
### Positive
- Standalone and coordinated sessions share the same boundary without a required hierarchy.
- Work can advance to a retained decision, then resume with its evidence intact.
### Negative
- Instruction consistency cannot guarantee every model follows the boundary.
- Acceptance and current authority must be checked again after material changes or interruption.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` pins inquiry-only Question dispatch and authority/acceptance propagation; `tests/test_shared_blocks.py` keeps the user-call blocks aligned; setup-version, glossary, and conventions-fork checks hold the distributed contract; `tests/test_owner_judgment_offers.py` pins the amendment that absence is not acceptance of optional authority-surface offers. The existing Ticket protocol model covers claims, retries, landing, and deferred work, not general delegated decisions. Actual judgment remains outside those checks.

## Source
- Amends 20260810-shaped-means-the-decision-space-is-closed
- Amends 20260812-run-ticket-owns-attempt-not-dispatch
- Amends 20261018-a-ticket-without-auto-runs-until-it-needs-a-person-and-never-lands-on-its-own
- Amends 20261018-orchestrate-tickets-up-debt-and-grants-auto-where-the-criterion-holds
- Amends 20260820-north-star-lines-carry-states
- Amends 20261021-the-north-star-holds-what-decisions-are-judged-against
- Amends 20261021-the-north-star-opens-with-its-end-and-signposts-reopen-choices-and-deferred-work
- Related: 20261023-projects-advance-toward-assigned-outcomes-within-delegated-authority
