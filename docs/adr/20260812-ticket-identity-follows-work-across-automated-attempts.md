# ADR: Ticket identity follows the work across automated attempts

## Status
Accepted

## Area
Ticketing

## Context

An Auto-granted Ticket can finish successfully or hit a surprise that requires a person. The ticket convention already gives closure a strong meaning: a closed Ticket is done, and dependent Tickets become ready when their dependencies close.

One proposed escalation flow closed the automated Ticket and created a new ungranted issue for human takeover. That makes the execution attempt terminal, but it also makes the work appear complete. Downstream Tickets can then start against an unmet dependency. Avoiding that false readiness would require moving every dependency edge to the replacement issue, while the work's history and definition of done would be split across two identities.

## Decision

**Ticket identity follows the work; an automated run is one attempt against it.**

A successful attempt records its outcome and landing references on the Ticket, then closes it as done.

An escalated attempt records a detailed handoff on the same Ticket: the blocker, what was tried, why the attempts failed, and any branch, commit, or pull-request references. It identifies the person whose input or authority is needed and leaves the Ticket open for that person to continue. Escalation ends the attempt, not the work.

A follow-up Ticket is created only for genuinely separate work discovered during the attempt. It is linked to the source Ticket under the existing dependency and effort conventions; it never substitutes for the unfinished source obligation.

## Alternatives Considered

- **Close the automated Ticket and create an ungranted human replacement**: Makes the automated attempt visibly terminal and separates the human queue. — Rejected because closing means done, falsely satisfies dependencies, and splits one work obligation across two Tickets.
- **Close the source after rewiring every dependent Ticket to the replacement**: Preserves dependency truth while retaining separate attempt issues. — Rejected because every escalation becomes a multi-item graph migration that can fail partially or race another picker.
- **Keep the source open and also create a duplicate handoff issue**: Leaves dependencies blocked on the source while giving the person a separate queue item. — Rejected because two open items then represent one obligation and can diverge.

## Consequences

### Positive
- A closed Ticket continues to mean that its work is done.
- Dependency readiness remains truthful without edge migration.
- Automated evidence and human continuation stay in one history.
- Follow-up Tickets retain their existing meaning: separate work, not another attempt at the same work.

### Negative
- One Ticket may accumulate several attempt records before completion.
- The automation needs a distinct way to show that an open Ticket is awaiting a person and must not start another attempt without an explicit retry.
- Reporting systems cannot treat every terminated automated run as a closed Ticket.

## Source
- Session: figure-out on unattended ticket automation (2026-08-12)
- Related: 20260810-auto-is-an-opt-in-grant-to-unattended-automation, 20260810-next-ticket-claims-the-ticket-it-picks, 20260806-retire-decision-map-for-ticket-up-and-ticket-store
