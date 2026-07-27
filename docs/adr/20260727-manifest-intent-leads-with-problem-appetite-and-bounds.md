# ADR: Manifest Intent leads with a required Problem, plus Appetite and Out of bounds

## Status
Accepted

## Context

The manifest schema's Intent & Context carried two fields: Goal and Mental Model. Everything downstream of `/define` steers by them.

The workflow suite is problem-first at both ends but not in the middle. figure-out opens solution-shaped topics at the problem behind them (per `20260714-figure-out-roots-crux-tree-above-solution-shaped-topics`), and review-pr's Judgment Layer weighs a change against the pain it solves (per `20260708-judgment-layer-is-a-review-time-premise-check`) — but the contract between them dropped the problem the understanding started from. `/do` makes judgment calls that need it — weighing Process Guidance departures, triaging external review comments against "does it serve this PR's intent," deciding what stays below a gate's threshold — with only a one-line Goal to steer by, and the Judgment Layer must re-infer the pain the manifest never recorded.

A systematic mapping of Shape Up (Basecamp) against the suite made the gap precise: of the pitch's five ingredients, Solution elements, Rabbit holes, and (via gates) boundaries all have manifest addresses; Problem, Appetite, and No-gos have none. A second gap compounds the first: with no notion of what a problem is worth, `/define` encodes the best-supported solution rather than the best solution within what the problem deserves, and nothing bounds complexity before solutioning starts. Scope discipline here serves quality and prioritization — a chopped-down first solution leaves room for the next high-impact change — not cost: this repo's positioning explicitly rejects cost optimization, so a time- or token-denominated appetite would be the wrong import.

## Decision

Intent & Context is reordered and extended; no new top-level sections are added.

- **Problem** leads the section and is **required**: a compact baseline story — what specifically breaks or grates today, the status quo this work challenges. The reading order encodes the epistemic order: nobody meets the Goal before the pain that justifies it. A `/define` session that cannot name the pain does not fill the field with boilerplate; the empty field is a stop signal — return to figure-out, or conclude there is nothing to do. This is the grab-bag guard: work defined without a single driving pain has no test of doneness.
- **Appetite** follows, per the CONTEXT.md definition: the size of change the problem is worth — a scope bound on complexity and surface set before solutioning, independent of time and token cost. This deliberately diverges from Shape Up's time-budget form to stay consistent with quality-first positioning.
- **Goal** is derived from the Problem rather than standing alone.
- **Out of bounds** lists what the work deliberately does not do. Entries that must bind route to Global Invariants exactly as before; the listed form exists for legibility, not enforcement.

Each field is justified by a consumer, not by pitch symmetry: `/do` gains a fitness test for its trade-off calls and Shape Up's honest stop rule — compare down to the baseline story, not up to an ideal; review-pr's Judgment Layer gains the pain record it currently infers; `/define` gains an encoding criterion for what to gate and how many Deliverables to cut; a blown appetite during execution reads as evidence of a shaping hole rather than a reason to push harder.

figure-out and `/define` split these fields the way they split understanding itself: figure-out is where boundaries arise and get pressed when a topic turns solution-bound (an appetite is a constraint to classify), `/define` is where they are settled and recorded, asking only what is still unset when encoding starts.

The Problem field records settled understanding; it is not a place where `/define` re-litigates it. Its best form is Shape Up's: a single specific story of the status quo failing.

## Alternatives Considered

- **Status quo (Goal-only Intent)**: — Rejected: it is the broken link in an otherwise problem-first chain; every downstream consumer of the pain either infers it or does without.
- **New pitch-shaped top-level sections, including a solution narrative**: mirror Shape Up's pitch structure fully — Rejected: a pitch is a sales document for a betting table, and there is no betting table; the user is the sole bettor and the Summary for Approval already serves the presentation moment. A section with no consumer is dead weight in every manifest.
- **Pitches replace figure-out Reads**: — Rejected: a Read is an understanding deliverable carrying confidence, evidence, and overturn conditions, and can legitimately conclude "build nothing" — a shape the pitch cannot take, since it presupposes a solution worth selling. The pitch's ingredients map onto Read + Manifest jointly; no third artifact is needed.
- **Problem as an optional field**: — Rejected: optionality forfeits the stop signal. The field must be required for its emptiness to mean anything.

## Consequences

### Positive
- `/do`'s judgment calls and review-pr's Judgment Layer work from a recorded pain instead of an inferred one.
- "Better than the baseline story" replaces "as good as possible" as the honest completion comparison, giving scope-hammering a target.
- Grab-bag work ("redesign X", "2.0") is stopped at define time by a field it cannot fill.
- Appetite gives `/define` a sizing criterion before solutioning, keeping high-impact breadth prioritized over expanding one solution.

### Negative
- `/define` interviews gain required elicitation — slightly more upstream friction, accepted per the cost asymmetry recorded in `20260727-define-encodes-for-full-do-autonomy`.
- Manifests written before this change lack the fields; they still execute, and their `/do` runs simply steer by Goal as they always did. No migration.
- A Problem field invites over-writing. The guard is its stated form: one specific baseline story, not a requirements essay.

## Source
- Related: [20260714-figure-out-roots-crux-tree-above-solution-shaped-topics](20260714-figure-out-roots-crux-tree-above-solution-shaped-topics.md)
- Related: [20260708-judgment-layer-is-a-review-time-premise-check](20260708-judgment-layer-is-a-review-time-premise-check.md)
- Related: [20260727-define-encodes-for-full-do-autonomy](20260727-define-encodes-for-full-do-autonomy.md)
- Related: [20260727-shape-up-adoption-boundary](20260727-shape-up-adoption-boundary.md)
