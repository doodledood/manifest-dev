# ADR: Debt is paid on the path of work, so a codebase converges through normal runs

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
The goal is a codebase that, over time, can be maintained by the workflow itself, with no work asked of the user outside figure-out, define, do, and auto. Several pieces already move it that way: locks keep a corrected class of mistake from returning; each change gets a sketch screened against red flags and reshapes the area it touches instead of patching it; the verification surface grows along the features work touches; and the debt a run leaves is reported at the end. Two gaps remained.

Each change keeps to one concern, which keeps a fix from turning into a bundle of experiments. On its own, that also means a feature run never makes the structural change that would make its area easy to work in, so the architecture improves only at the edges. figure-out already asks whether to fix in place or refactor first, but define had no way to encode the answer. And reported debt went nowhere unless the user acted on it; nothing connected it to later work in the same area.

## Decision
- When the sketch shows that the area a change touches resists it — a value threaded through layers, state with more than one writer, a missing seam, a workaround the change would extend — define encodes a behavior-preserving preparatory Deliverable first: make the change easy, then make the easy change. It is scoped to what this change needs, pinned by existing or characterization tests, and stays its own slice, which can land as its own pull request.
- While recalling earlier sessions, figure-out and define look for recorded debt on the change's path — debt reported by earlier runs, open debt tickets, stale verification entries — and offer to fold the items on the path into that preparatory slice. Debt off the path stays recorded.
- When one area keeps producing debt across runs, the read says so, with the count, and proposes a dedicated topic such as a structural refactor or a paved path for that kind of work. The user rules on it; once accepted, it runs through the same flow.
- Debt a run leaves is written where any runner can read it. Every pull request a run opens or updates carries a "Debt left" section, attended or not. When the user accepts the ticket-up offer, items become tickets, which track whether the debt got paid. The run's local log keeps a copy for that machine only. A repository without pull requests falls back to tickets and local logs.
- Recall reads open debt tickets and the "Debt left" sections of recent pull requests that touched the change's paths, plus local logs where present. Each item is checked against the current code before it is offered, and a ticket's status settles whether it is done. Declines are not recorded; the check keeps a repeated offer real.
- The effect intended: maintenance cost concentrates where change happens, and the flow pays debt exactly there while locks keep known classes from returning. The parts of the codebase that change most become the easiest to change. A part that no run touches costs nothing until one does.

## Alternatives Considered
- **Rely only on the user following up reported debt**: the follow-up stays available inside the flow — the completion report offers ticket-up, and a later auto run can take the tickets — but debt that sits on the path of later work would still wait for someone to pick it, while the run that touches it already has its context loaded.
- **Fold all known debt into every run**: it bundles unrelated work into each change.
- **Keep debt in local logs only**: a cloud runner or a teammate sees none of it, and an unattended run cannot file tickets.
- **A periodic cleanup pass**: it needs infrastructure or someone to remember it.
- **Let the flow start structural refactors on its own**: the direction of the architecture is the user's call; the flow proposes it with evidence instead.

## Consequences

### Positive
- Debt gets paid without separate work, in the places where paying it matters.
- Architecture improves where work keeps happening, not only at the edges.

### Negative
- Some changes grow by one preparatory slice.
- When an area counts as resisting a change, or as a hotspot, is a judgment.
- Whether a codebase actually converges is not measured yet; the signals are debt per run in an area falling, verified verification entries rising, and the share of review findings a check could have prevented falling.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20261013-corrections-become-scoped-locks-and-their-hits-become-reported-debt
- Related: 20261013-figure-out-and-define-recall-earlier-sessions-on-the-same-repo
- Related: 20261013-design-judgment-moves-to-design-time-as-task-file-probes
