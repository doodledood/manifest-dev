# ADR: Trim the Manifest schema to fields that are read

## Status
Accepted

## Area
define / do

## Context

The Manifest schema accumulated fields that nothing downstream consumes. A survey of every skill
for readers of each field found four with no consumer that changes behavior:

- **`Goal`** — restates `Problem` inverted ("deploys drop nodes" / "deploys stop dropping
  nodes"). The ceiling invariant, which is the one gate carrying Intent, pulls `Problem`,
  `Appetite`, and `Out of bounds` and never `Goal`.
- **`Mental Model`** — no rule anywhere states what belongs in it. Its only two mentions outside
  the schema are `ticket-up` folding it away and `BABYSIT_MODE` guessing at how to populate it.
  `/do` never reads it.
- **`Risk Areas [R-N]`** — no reference outside the schema at all. Not in `/do`, `/done`, or
  `/escalate`. `ticket-up` mentions them once, to demote them into an optional suggested
  approach.
- **`Trade-offs [T-N]`** — printed by `/done` in the completion summary and read by nothing else.
  Being echoed on exit is not a consumer that changes what the run does.

`Out of bounds` carries a duplication of its own by design: an entry that must hold "stays listed
as the scope statement **and** gains the Global Invariant that binds it." That is the same
two-texts-one-binds pattern that
[20260807-a-gate-is-one-text-not-two](20260807-a-gate-is-one-text-not-two.md) removes from gates.

There is also a gap, and it grows once gates gain full bodies. `/define` requires a Deliverable to
be a slice that can be "exercised end-to-end", and warns that a Deliverable cut along a layer can
only be gated on existence — then gives the Deliverable nowhere to say what it is or how it would
be exercised. A Deliverable is a bare `### Deliverable N: [Name]`, which becomes the thinnest
element in the file once every criterion carries a title, a body, and a why.

Unread fields are not free. Each one is authored on every run, reviewed in every Summary for
Approval, refreshed on every amendment, and carried through `ticket-up` and every distribution —
paying authoring and maintenance cost for content no consumer acts on.

## Decision

**Cut `Goal`, `Mental Model`, `Risk Areas`, and `Trade-offs` from the schema.** Nothing reads
them in a way that changes behavior, and `Goal` additionally duplicates `Problem`.

**Stop writing `Out of bounds` twice.** A bound that must hold is stated once, as the Global
Invariant that binds it. Bounds that do not bind remain a plain list in Intent and gain no
shadow gate.

**Give each Deliverable one line** stating what it is and how it is exercised end-to-end. This is
what `/define`'s existing cutting discipline already demands and had no field to record.

Intent therefore carries `Problem`, `Appetite`, and `Out of bounds`; the Initial Approach carries
`Architecture` alone; and Global Invariants, Process Guidance, Known Assumptions, and Deliverables
are unchanged in role.

**`Process Guidance` stays.** It is how a task file's Defaults reach a run, and
`20260726-only-gates-bind-process-guidance-is-advisory` already settled its status — advisory,
with departures named on whichever terminal path the run takes. Nothing in this survey reopens it.

## Alternatives Considered

- **Keep `Trade-offs` because `/done` prints them**: rejected. Echoing a field in a summary is
  not consumption. A trade-off that must steer execution is Initial Approach direction or a gate;
  one that must survive the run is an ADR.
- **Keep `Risk Areas` as an author-facing thinking aid**: rejected. figure-out already surfaces
  risk during understanding, and a field written on every manifest to be read by nobody is
  authoring cost with no recipient. A risk worth acting on becomes a gate, a Known Assumption, or
  Deliverable ordering — all of which already exist.
- **Keep `Goal` for readability**: rejected. A well-stated `Problem` already tells a reader what
  the work is for, and `/define` leads Intent with it deliberately. Two fields saying one thing is
  the duplication this schema is being audited for.
- **Keep `Mental Model` and define what belongs in it**: rejected. Specifying a field is only
  worth doing when a consumer needs it; none was found. Context a run genuinely needs belongs in
  the Problem or in the Architecture.
- **Deprecate the fields but keep accepting them**: rejected. The companion ADR already breaks
  compatibility, so a single clean schema is cheaper than two readers and a migration path.

## Consequences

### Positive
- Less to author on every run, less to review in the Summary for Approval, and less to refresh on
  every amendment.
- The schema stops implying that unread content is load-bearing, which is its own form of
  imprecision.
- Deliverables gain the statement their own cutting discipline already required, closing the gap
  where a layer-shaped slice could pass as a real one.

### Negative
- Risk and trade-off reasoning loses its default home in the Manifest. Where it matters it must be
  routed deliberately — to a gate, a Known Assumption, the Deliverable order, or an ADR — rather
  than landing in a field by habit.
- Completion summaries lose the trade-off line they currently print.
- Existing Manifests do not migrate, consistent with the companion ADR.

## Source
- Session: figure-out session, 2026-08-07
- Related: [20260807-a-gate-is-one-text-not-two](20260807-a-gate-is-one-text-not-two.md)
- Related: [20260727-manifest-intent-leads-with-problem-appetite-and-bounds](20260727-manifest-intent-leads-with-problem-appetite-and-bounds.md)
- Related: [20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty](20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty.md)
- Related: [20260726-only-gates-bind-process-guidance-is-advisory](20260726-only-gates-bind-process-guidance-is-advisory.md)
