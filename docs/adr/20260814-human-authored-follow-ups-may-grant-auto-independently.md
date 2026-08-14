# ADR: Human-authored follow-ups may grant Auto independently of their source

## Status
Accepted

## Area
Ticketing

## Context

The current follow-up rule requires both source authority and local eligibility before a new Ticket may carry Auto: its source Ticket must already carry Auto, and the follow-up must independently pass the normal Auto grant test. That rule prevents an unattended execution chain from expanding its own authority. It also prevents a person who manually runs an ungranted Ticket from indirectly creating unattended work merely because the agent discovers a follow-up.

The absolute source requirement is too broad for the ordinary human-plus-AI shaping flow. A Ticket can be non-Auto precisely because it needs human judgment. The person can work through that judgment with AI, close the decision space, then explicitly author or approve a separate implementation Ticket whose work and done judgment no longer need a person. If source Auto remains a permanent inheritance requirement, safe implementation stays fenced out of unattended execution only because its parent needed a human earlier.

This does not mean Shaped and Auto should collapse. Shaped says the decision space is closed. Auto is the stronger opt-in authority for an unattended worker to take the Ticket end to end, including required landing under the repository's normal protections. A human-supervised `/do` can already carry shaped repository work to a verified, mergeable pull request without Auto and without pressing merge.

## Decision

**The source-Auto requirement applies only when a follow-up is authored without a fresh human Auto grant at the `ticket-up` boundary.**

When `ticket-up` is invoked as part of an unattended or nested Ticket execution and no person explicitly authorizes Auto for the new Ticket, preserve the existing conjunctive rule: the source Ticket must carry Auto, the follow-up must independently satisfy the normal Auto criterion, and the authoring step must choose to grant it. This prevents an execution chain from escalating its own authority.

A person merely invoking `run-ticket` on an ungranted source does not satisfy that boundary. Follow-ups discovered and authored inside that run remain constrained by source Auto unless the person separately and explicitly authorizes the new follow-up's Auto grant.

When a person directly invokes `ticket-up`, or explicitly reviews and authorizes the follow-up at that authoring boundary, judge the new Ticket independently. Its source may be ungranted. Grant Auto only when the new Ticket itself meets the normal unattended-execution criterion and the person chooses to grant it.

**Shaped does not imply Auto.** A shaped Ticket can remain ungranted because trust or authority is intentionally withheld, and supervised AI execution remains available. Conversely, a Question Ticket may carry Auto when its investigation, judgment, and required landing need no human knowledge, taste, or authority.

Do not add a second marker for "AI may implement but not merge." The supervised path already supplies that behavior: after human shaping, AI may execute through `/do` to a mergeable pull request, while the merge remains outside `/do`. Auto remains the single stronger marker for unattended end-to-end authority.

## Alternatives Considered

- **Keep source Auto mandatory for every follow-up**: Preserve a simple hereditary rule. — Rejected because explicit human authoring cannot grant safe unattended authority to newly shaped work whose source needed human judgment.
- **Make every shaped Ticket Auto**: Treat closed decision space as sufficient delegation. — Rejected because Shaped does not express trust, access, approval, or irreversible-action authority, and Auto includes unattended landing.
- **Let any human-invoked `run-ticket` break inheritance**: Treat the source run's supervision as authority for all discovered follow-ups. — Rejected because that would let a nested authoring step create future unattended work without the person actually reviewing that new grant.
- **Add a middle-tier marker for autonomous implementation to PR but no merge**: Separate implementation authority from landing authority. — Rejected because supervised `/do` already provides that path; another durable Ticket state would duplicate an existing execution mode.
- **Judge every follow-up only on its own content**: Remove source authority from unattended chains. — Rejected because an unattended worker could then expand from one narrow grant into arbitrary newly discovered work.

## Consequences

### Positive
- Human judgment can unlock later unattended implementation without carrying the source Ticket's earlier human dependency forever.
- Unattended execution still cannot escalate its own authority.
- Shaped, Auto, and supervised AI execution keep distinct meanings instead of collapsing into one readiness flag.
- The common human flow stays simple: think with AI, shape the work, then let AI execute to a mergeable pull request without inventing a new Ticket marker.

### Negative
- `ticket-up` must distinguish a fresh explicit human grant at its own authoring boundary from mere human provenance elsewhere in the call chain.
- Follow-up Auto behavior is no longer expressible as source inheritance alone; invocation authority becomes part of the authoring context.

## Source
- Session: figure-out on project Ticket prioritization and human/agent allocation, 2026-08-14
- Supersedes 20260812-auto-follow-up-grant-requires-source-and-local-grant
- Related: 20260810-auto-is-an-opt-in-grant-to-unattended-automation, 20260810-shaped-means-the-decision-space-is-closed, 20260812-auto-ticket-completes-after-required-landing
