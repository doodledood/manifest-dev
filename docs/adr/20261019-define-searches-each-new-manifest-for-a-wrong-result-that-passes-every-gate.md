# ADR: define searches each new Manifest for a wrong result that passes every gate

## Status
Accepted

## Area
define

## Decided by
The user

## Context
define's fresh review (20261018-define-reviews-each-new-manifest-in-a-fresh-context) checks each
gate on its own: for every gate it names a plausible wrong result the gate would fail. A wrong
result can still pass every gate at once, because each gate covers its own part and nothing
covers the space between them. Under orchestrate no person reads a Manifest before `/do` holds the
work to it, so such a hole reaches the code.

In one experiment, define wrote a Manifest from a read of an invoice worker — several workers,
atomic claims, the email provider's idempotency key, a reclaim timeout — whose design a TLA+
model had already checked. Its own review, self-graded in that run, found none of the holes
below. Two separate searches of that Manifest for wrong results that pass every gate then found
holes:

- A judgment search, in about 10 minutes, found among others an invoice sent twice when the old
  worker is stopped mid-send during the switch to the new workers, a job marked sent but never
  delivered when an overlapping send gets the provider's "in progress" answer, and a retry loop
  when an email's body changes under a reused key.
- A TLA+ model of the Manifest, with the implementation left free wherever the Manifest was
  silent and the gates as constraints, took about 42 minutes. It found the same switch-over double
  send and holes judgment missed, mostly long event sequences: a retry after a provider error
  receives the provider's stored answer and the job is marked sent with nothing delivered, and a
  rollback whose reclaim lets the old worker send again.

20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks decided that nothing
model-checks a Manifest's own text, because translating prose into logic is unreliable and a
proof over a wrong translation looks like strong evidence while proving nothing. That objection
is to certifying a Manifest. A search for holes is the other way round: each hole it reports is a
concrete scenario anyone can judge, so a faulty encoding costs a false alarm, not false
confidence.

## Decision
- define's fresh review, after its per-gate question, searches the new Manifest as a whole for
  holes: wrong results its owner would reject that pass every Acceptance Criterion and Global
  Invariant at once. What the owner would reject is judged against the Manifest's own intent and
  the session record, not the reviewer's taste, and behavior a Known Assumption or Process
  Guidance entry already accepts is not a hole.
- The search is by judgment on every new Manifest. A model is used only by extending one already
  built for the design the Manifest encodes — such as the one figure-out builds for a design whose
  correctness depends on the order of events — or when the user asks for one. None is built from
  scratch by default, and rebuilding a model the session only describes counts as from scratch.
  define hands the fresh context the path of any such model so the review can extend it.
- Each hole is reported with its scenario and the gates that pass it. A hole is a result the
  stated Intent already rejects, so define closes it with a gate or a design decision, attended
  or unattended. Only a fix that would change the Intent or the scope is the user's call: asked
  when attended; unattended, recorded as an assumption that names the hole as still open. An
  entry that merely accepts a hole the Intent rejects does not settle it. Each ambiguity — two
  readings of a gate's text that change what passes — is settled by writing one reading into the
  gate. The digest names the holes found and how each was settled.
- A search that finds nothing is no evidence that the Manifest is sound, and a model is never
  offered as proof of it. Translating a Manifest into a formal language to prove it stays
  rejected.
- The search runs inside the one fresh review, names no required tool, and does not run on
  amendments, which get no review.

## Alternatives Considered
- **A model built from scratch for every Manifest whose core is states and events over time**:
  finds long event sequences judgment misses — Not chosen: it took about 42 minutes on the one
  Manifest tried, against about 10 for the judgment search, which found most of the costly holes;
  the user ruled that define must not take that long.
- **Judgment only, never a model**: cheapest — Not chosen: where a design model already exists,
  adding the Manifest's gates to it is a small step that reaches what judgment misses.
- **The search in a second fresh context**: keeps the review's two questions apart — Not chosen:
  one review per new Manifest is the decided shape, and a second context reads the same rules and
  Manifest again.
- **Prove the Manifest in a formal language**: Not chosen, as in
  20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks.

## Consequences

### Positive
- Holes that pass every gate are caught before `/do` runs, while closing one is a line in a gate.
- Ambiguities are settled before an executor picks a reading for itself.

### Negative
- Each new Manifest's review takes longer; the judgment search took about 10 minutes in the one
  experiment.
- Where no design model exists, long event-sequence holes a model would find still get through;
  test-quality's question at review
  (20261019-test-quality-asks-whether-a-kept-test-reaches-the-case-that-breaks-a-guarantee) catches
  part of them later.
- The evidence is one Manifest, in the kind of design formal methods suit best.

## Enforced by
partly — the `hole-search` scenario of `verification/recipes/define.md` drives define on the
invoice read and checks that the review searched for holes and settled them, and the define eval
case `d26-holes-that-pass-every-gate` grades, on the self-graded path, whether the spec closes two
holes the experiment found; how deep a search goes stays judgment.

## Source
- Session: figure-out and define on formal verification in manifest-dev's workflow, with a
  judgment search and a TLA+ search of one Manifest (2026-10-19).
- Related: amends 20261018-define-reviews-each-new-manifest-in-a-fresh-context and
  20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks; see also
  20261019-test-quality-asks-whether-a-kept-test-reaches-the-case-that-breaks-a-guarantee
