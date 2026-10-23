# ADR: Projects advance toward assigned outcomes within delegated authority

## Status
Accepted

## Area
Strategy

## Decided by
The user

## Context
A ready queue describes deliverable work, but its completion does not show whether people made the progress the project exists to support. A coordinator that only drains that queue cannot choose an investigation when the next useful work is still unknown. Product intent and evidence must remain available after an artifact is delivered.

## Decision
The project serves worthwhile progress with less repeated context restoration and avoidable human intervention. Standalone inquiry, finite Manifest work, direct Ticket work, and optional outcome coordination remain complete adoption choices. Teams and noncommercial projects are included; ongoing business operation is an ambition within explicit authority, not a demonstrated capability.

Extend the existing orchestrator to pursue an explicitly assigned outcome. It can commission inquiry and delivery, inspect designated evidence, and choose to continue, wait for evidence, ask for a retained decision, complete, or stop at an operating limit. A queue invocation stays finite. Each independently assigned or resumable job gets a Ticket before dispatch; routine reasoning and internal steps do not. Existing effort records hold the assignment, compact evidence, and continuation, with bounded active state and incremental source reads. No scheduler or separate discovery role is added.

Product inquiry considers circumstances, actual alternatives, adoption, use, and the whole experience. It preserves useful rationale through the existing handoffs without imposing interviews or another document. The North Star measures intended outcomes and remaining necessary human involvement alongside quality, changeability, and cost. Unmeasured positions stay empty; completed Tickets are delivery evidence only.

## Alternatives Considered
- **Queue execution as the destination:** useful and preserved as a mode of use, but cannot pursue outcomes whose next work is unknown.
- **A permanent discovery agent or new operating platform:** adds coordination machinery before actual use shows it is necessary.
- **One mandatory workflow chain:** would make standalone adoption and team use needlessly costly.

## Consequences
### Positive
- Inquiry, delivery, and evidence can serve one outcome without losing intent.
- People can start with an individual skill and delegate only useful work.
### Negative
- Outcome decisions need evidence and explicit continuation when that evidence is absent.
- Repeated autonomous operation remains unproven; isolated runs cannot establish sustained effectiveness.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` pins the separate queue and outcome paths; `tests/test_orchestrate_status_page.py` holds the compatible outcome-state schema; existing browser checks exercise waits on a finished empty plan. Product judgment and sustained outcome achievement remain judgment and actual-use evidence.

## Revisit when
Actual project records repeatedly show that coordinator-owned inquiry misses material opportunities or contrary evidence that a separate review discovers; read the linked coordination records and inquiry results.

## Source
- Amends 20261015-projects-drive-themselves-as-far-as-each-user-climbs
- Amends 20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep
- Amends 20260821-winning-is-our-own-projects-running-the-full-loop
- Related: 20261023-assignment-bounds-delegated-decisions-and-retained-acceptance
