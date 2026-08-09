# ADR: Shape Up adoption boundary — what is deliberately not imported

## Status
Accepted

## Area
Positioning

## Context

Shape Up (Basecamp) was read in full and mapped systematically against the workflow suite. The convergence is deep: Deliverables as exercisable slices match scopes and "get one piece done"; least-proven-first ordering matches "push the scariest work uphill first"; `/do`'s bound-repairs-by-subject escalation matches the circuit breaker's kernel (non-convergence means the shaping had a hole — reframe, don't grind); the figure-out/define track beside `/do` matches the shaping/building two-track split; the Summary for Approval matches the pitch-presentation moment. Where real gaps existed, concepts were adopted — Problem, Appetite, and Out of bounds in the manifest (`20260727-manifest-intent-leads-with-problem-appetite-and-bounds`), rabbit-hole probe fuel, breadboarding as a one-shot-probe form.

The remainder was considered and deliberately excluded. Without a record, each excluded concept invites re-derivation the next time the book crosses someone's desk.

## Decision

The following Shape Up machinery is not imported, on these grounds:

- **Betting table, six-week cycles, cool-down, uninterrupted-time policy**: these solve scarce human team capacity and calendar coordination — Calendar Tetris, C-suite attention, human momentum and burnout. Agent executions are cheap, parallel, and retryable; none of the scarcities these mechanisms ration exist here.
- **Hill charts**: their job is status-without-asking across a multi-week human team. The execution log already records unknown-versus-solved state as it moves; a plotted hill position for an agent run is ceremony.
- **Backlog abolition ("bets, not backlogs")**: there is no backlog to abolish — manifests are per-task and nothing accumulates between them.
- **Pitches as a replacement for figure-out Reads**: a Read is an understanding deliverable carrying confidence, an Evidence Ledger, and overturn conditions, and can conclude "build nothing"; a pitch presupposes a solution worth selling to a betting table that does not exist here. The pitch's ingredients map onto the Read and the Manifest jointly; no third artifact is added.
- **"Rough is good" applied to gates**: Shape Up leaves shaped work rough because talented humans under deadline pressure fill the roughness with taste and trade-off judgment. Manifest gates exist precisely because the executor has no such backstop. The import is "don't over-specify the how" — which lands as gate altitude in `20260727-define-encodes-for-full-do-autonomy` — never "loosen the what."

The boundary is dated to the current architecture: a single operator driving agent executions.

## Alternatives Considered

- **Import the method wholesale**: — Rejected: most of its machinery rations scarcities (team-weeks, calendar, senior attention) that have no referent in an agent workflow; importing it would be form without function.
- **Leave exclusions unrecorded and re-evaluate case by case**: — Rejected: the mapping work is expensive to redo and the conclusions non-obvious; an unrecorded "no" gets re-litigated from scratch.

## Consequences

### Positive
- Future proposals to add cycles, betting rituals, or hill charts meet recorded grounds instead of a fresh debate.
- The limit of the Shape Up analogy is explicit, so adopted concepts don't drag their neighbors in by association.

### Negative
- If the workflow ever coordinates scarce human capacity — multi-person teams sharing agent fleets, genuinely rationed review bandwidth — several exclusions (cycles, betting, cool-down) would need revisiting under that changed premise.

## Source
- Related: [20260727-manifest-intent-leads-with-problem-appetite-and-bounds](20260727-manifest-intent-leads-with-problem-appetite-and-bounds.md)
- Related: [20260727-define-encodes-for-full-do-autonomy](20260727-define-encodes-for-full-do-autonomy.md)
- Related: [20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty](20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty.md)
