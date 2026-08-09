# ADR: Per-gate restored as the default `/do` verification mode

## Status
Accepted

## Area
do

## Context

`/do` evaluates every Acceptance Criterion and Global Invariant under a run-level
verification mode selected at launch: `per-gate`, `consolidated`, or `self` (see
20260728-move-verification-execution-policy-to-do). 20260730-consolidated-default-verification-mode
moved the omitted-flag default from `per-gate` to `consolidated`, on two recorded
grounds — stability and economy — and accepted lower per-round recall as the price.

Both grounds have since moved, and the accepted price has risen.

**The stability ground is recorded as unmet.**
20260805-ratchet-judgment-gate-reverification, written six days later, assessed the
consolidated default directly: it "changes who evaluates, not how often the finding
space is re-opened. Observed behavior after both: rounds continued, and the findings
were new each round rather than the same verdict flipping — the signature of
re-sampling rather than instability." The oscillation consolidation was chosen to damp
was damped by the Ratchet instead. That half of 20260730's rationale now describes work
another decision does.

**The economy ground rests on the wrong cost model.** 20260730 reasoned that "a typical
manifest carries 10–15 gates, so every verification round launched that many verifier
executions, each re-reading the same artifact," and counted the saving as the reads not
repeated. That counts unique tokens. Billing is per request over the whole context, and
the conversation is resent in full on every turn, so an artifact read at the start of an
execution is re-billed on each of that execution's subsequent turns. Under per-gate that
is N executions each carrying one copy across its own turns; under consolidated it is one
execution carrying one copy across all of their turns. The totals are the same, and
consolidating a shared read saves approximately nothing.

What consolidation does save is real but different: the repeated orientation — re-reading
the manifest, re-establishing what the change is — paid once instead of once per gate. That
saving is a fixed amount times the number of gates whose orientation was skipped, so it
grows linearly with gate count.

What consolidation costs is that every gate it finishes stays in the shared context for
every gate that follows. That is paid once per ordered pair of gates, so it grows with the
square of the gate count. The two terms cross at a low gate count, and past it the
quadratic one dominates by a widening margin. Estimating a twelve-gate manifest whose gates
do substantial independent work — the shape observed in practice — puts the penalty at
roughly twenty times the saving. Inverting the crossover gives the condition under which
consolidation is the cheaper choice: each gate's own work must be nearly nil, which
describes a Deterministic Gate that runs a command and reads an exit code.

This magnitude is reasoned from billing mechanics and estimated turn counts, not measured.
The direction does not depend on the estimates — one term is linear in gate count and the
other quadratic — but the multiple does.

**The accepted recall price rose after it was accepted.** 20260730 recorded "Lower
per-round recall than `per-gate`" as a known negative, which was affordable while every
round re-opened the full finding space: a miss in one round could be caught in the next.
The Ratchet closed that. A Judgment Gate now reads the full change once and thereafter
judges only its prior findings' repairs and the delta. Under that regime the single full
look is the only full look, and spending it on a context splitting its attention across
ten to fifteen gates converts a per-round discount into permanent loss. The Ratchet ADR
did not revisit the default it inherited.

**Latency is structural rather than tunable.** `/do` requires an evaluator meeting a
skill-activating gate body to activate that skill in its own context and never to spawn a
further agent. A consolidated execution therefore cannot fan out: it pays one orientation
and then N gates of work in sequence. A per-gate round pays one orientation and one gate of
work, concurrently. Consolidation beats *sequential* per-gate evaluation and never beats
the concurrent evaluation `per-gate` actually performs.

## Decision

Move the omitted-flag default back from `consolidated` to `per-gate`. `/do`, `/auto`, and
`/babysit-pr` all resolve an omitted `--verification` to `per-gate`.

`consolidated` and `self` remain selectable exactly as before. No mode is added, renamed,
removed, or merged; no mode's evaluator topology, reference file, provenance string, or
completion-evidence wording changes; `--verifier-model`, `--exhaustive-verification`, the
Ratchet, and the gate ledger are untouched. Only which mode applies in the absence of the
flag changes.

`/do`'s mode-comparison prose changes with it. That list described `per-gate` as "Highest
quality, slowest, dearest" and `consolidated` as "Middle on all three" — claims this
decision's reasoning contradicts on cost, and on speed for any host that runs the
executions concurrently. It now describes per-gate as concurrent with a whole context per
gate, and consolidated as sequential in a shared context, paying orientation once and
carrying each finished gate forward — with the case for choosing it stated where it holds:
many gates that are each slight, or a host where launching many executions at once is
capped or costly.

`self` is unaffected and keeps the standing 20260806-verification-is-bookkeeping-and-a-stop-condition
gave it: available for cost-sensitive runs, rejected as the default on recorded evidence.

## Alternatives Considered

- **Keep `consolidated` as the default**: rejected. Its stability rationale is recorded as
  unmet by the ADR that replaced it, its economy rationale counts unique tokens where
  billing counts context per turn, and the recall discount it accepted became permanent
  under the Ratchet.
- **Remove `consolidated` entirely, leaving `per-gate` and `self`**: rejected. It retains a
  real niche — manifests whose gates are nearly all deterministic, and hosts that cap
  concurrent executions — and removing a documented option is a larger change than
  restoring a default. Kept deliberately, with the expectation that it earns its keep.
- **Select the mode per gate by declared kind**, consolidating Deterministic Gates and
  running Judgment Gates per gate: rejected. This is where the cost analysis points, but it
  hands the run a lever over its own verification topology and adds a mechanism whose
  behaviour a reader cannot predict from the Manifest, for a saving that matters only on
  manifests dominated by cheap gates. 20260806 rejected a neighbouring form of this on the
  ground that under a one-execution-per-round default it would shorten a briefing rather
  than save an execution; under a per-gate default it would save executions, which makes it
  worth reconsidering later on measured evidence rather than adopting alongside a default
  flip.
- **Measure before deciding**: rejected as a precondition, not as an idea. The cost argument
  is directional (linear against quadratic) and the latency and recall arguments stand
  independently of it, so a measurement would refine the magnitude recorded here without
  changing the decision.

## Consequences

### Positive
- A verification round costs about one gate's wall clock rather than the whole set's,
  because the executions run concurrently.
- No gate's reading accumulates in the context another gate is judged from, so token cost
  stops growing with the square of the gate count.
- Each Judgment Gate's single full look under the Ratchet is spent by a reader attending to
  that gate alone, which is where per-round recall matters most now that there is no second
  full look.
- The mode-comparison prose in `/do` no longer asserts a cost and speed ordering this
  project's own reasoning contradicts.

### Negative
- The shared prefix is written to cache once per verifier execution rather than once, so
  per-gate pays N cache writes where consolidated paid one.
- Concurrently launched executions cannot read a cache entry another is still writing, so
  the first round of a fan-out forgoes cache reads that a sequential execution would have
  had.
- A host that caps concurrent executions splits a large gate set into waves, so the latency
  win is bounded by that cap rather than by the gate count.
- The cost argument is reasoned rather than measured. Its direction follows from the
  billing model, but the twenty-fold figure is an estimate and should be read as one.
- This is the second reversal of this default in six weeks. The reasoning here is recorded
  in enough detail to be attacked directly, which is the only defence against a third.

## Source
- Session: figure-out investigation, 2026-08-08 — 20260730 and 20260805 read at source,
  Anthropic prompt-caching and multi-agent guidance read for the billing and parallelism
  mechanics, and the observed run shape confirmed by the maintainer
- Supersedes: 20260730-consolidated-default-verification-mode
- Related: 20260805-ratchet-judgment-gate-reverification,
  20260806-verification-is-bookkeeping-and-a-stop-condition,
  20260728-move-verification-execution-policy-to-do
- Manifest: `~/.manifest-dev/manifests/manifest-20260808-124500.md`
