# ADR: No verifier-model granularity — the lever is round count, not model routing

## Status
Accepted

## Area
do

## Context

`/do` exposes a single run-level `--verifier-model` that applies to every verifier execution
under the independent modes. A proposal to split it — a cheaper model for command-backed gates
and a strong one for judgment gates, or finer routing still — was raised to reduce cost and
latency.

Two records left neighbouring questions open on the same condition.
20260728-move-verification-execution-policy-to-do rejected per-gate `verify.model` routing
because "concrete model selection is execution policy and not portable across hosts. One
run-level verifier model is sufficient until measured use cases justify a more expressive
execution-only policy," and recorded as a negative that "restoring heterogeneous model routing
would require a later execution-policy design."
20260808-restore-per-gate-default-verification-mode rejected selecting the mode per gate by
declared kind, noting it is "where the cost analysis points" and "worth reconsidering later on
measured evidence."

This is that reconsideration. It found the proposal aimed at the wrong mass.

**The cheaper kind is also the smaller count.** A code manifest built from `CODING.md` carries
eleven always-applicable dimension gates plus two conditional ones — thirteen gates whose
evaluator reads and reasons over the whole change — against roughly four command-backed project
gates that run a command and read an exit code. Billing resends the context on every turn, so
the per-gate ratio compounds the count ratio. A split by kind therefore reaches a small
fraction of the bill, estimated at a few percent.

**It reaches none of the latency.** Under the `per-gate` default, executions run concurrently,
so wall clock is set by the slowest single gate, which is always one reading the whole change.
Making the command-backed gates finish sooner changes nothing observable. This half does not
depend on the cost estimate.

**Cheapening the judgment side inverts the saving.** A reviewer's errors are asymmetric against
the run. Missing a finding costs nothing at the time; inventing one costs a repair round plus
re-verification of every gate whose subject that repair re-stales, because `/do` repairs per
head rather than per finding. The gates a cheaper model would be given are the advisory
dimensions — simplicity, design fitness, maintainability, prose value — which are taste
judgments rather than checks against a ground truth, and so the worst place for a weaker
reader's confident wrong answers, not the best.

One prior rejection rested on a ground that has since moved.
20260806-verification-is-bookkeeping-and-a-stop-condition declined a verifier effort selector
because "the existing verifier-model selector already carries effort." Hosts now expose
reasoning effort separately from model choice in some interfaces. The rejection survives on a
different ground: on the subagent interface `/do` actually launches verifiers through, the
model is selectable and effort is not, and `/do` must reject a policy the host cannot honor —
so the flag would always reject where it matters most.

## Decision

Keep the single run-level `--verifier-model`. Add no per-kind, per-tier, or per-gate model
routing, and no separate effort selector.

Record where the lever actually is: **total cost is per-round cost multiplied by round count,
and only round count is multiplicative.** Every routing scheme trims an addend; the executor
determines the multiplier, because how good the first attempt is decides how many repair rounds
follow. The cheapest complete run is the one whose gates pass on the first evaluation, which
argues for spending on the model doing the work rather than shaving the models checking it.
This is the reverse of the intuition the proposal started from, and it is also the reverse of
the usual "checking is easier than doing" asymmetry — that asymmetry holds for gates that run a
command and read an exit code, which are already the cheap ones, and fails for review over an
open finding space, where judging whether a design is the simplest one is the same class of
call as choosing it.

**Cross-family verification is sound in principle and unavailable in practice.** A reviewer
from a different model family than the writer does not share its blind spots and is less likely
to approve code it would have written the same way. Where the host's subagent model selector
offers one family, `--verifier-model` cannot express it at all. It is realizable only on a
multi-provider host, and its cost effect is two-sided even there: a different family also
disagrees about conventions, and a convention disagreement lands as a finding that buys a
repair round like any other.

**The door stays open on measured evidence**, on the terms 20260728 and 20260808 already set
rather than new ones. The cost figures here are reasoned from gate shape and billing mechanics,
not measured — the same standing 20260808 gave its own linear-against-quadratic argument. Two
measurements would reopen this: executor token spend against verifier token spend on a real
run, and how round count actually moves with executor strength. A pricier executor wins if it
takes a run from four rounds to two and loses if it takes it from four to three and a half, and
nobody has that number.

## Alternatives Considered

- **Split the verifier model by declared kind** — cheap model for command-backed gates, strong
  for judgment gates: rejected. Reaches a few percent of cost and no latency, for a flag that
  `/do`, `/auto`, `/babysit-pr`, the terminal helpers, and three distribution targets would all
  have to carry.
- **Split by dimension tier** — cheap model for the nine advisory dimensions, strong for the
  four defect-finders: rejected. This reaches real mass, and it is the worst place to spend it.
  Taste judgments are where a weaker reader's false findings concentrate, and each one costs a
  repair round.
- **A per-gate model map**: rejected on 20260728's original ground, which still holds — model
  selection is host-specific execution policy, and a map makes a Manifest or a launch command
  carry host-specific names for every gate.
- **A verifier effort selector**: rejected. Not honorable on the subagent interface `/do`
  launches verifiers through, which takes a model and no effort setting, and `/do` rejects a
  policy the host cannot honor rather than pretending it applied.
- **Consolidate the nine advisory dimensions into one reader** so the change is read once:
  rejected on 20260808's own analysis, which found that sharing the read "saves approximately
  nothing" — billing resends the context on every turn, so the read is re-billed either way.
  What consolidation does save is the repeated orientation, a fixed amount per gate whose
  orientation was skipped, so it grows linearly; what it costs is every finished gate staying
  in the context of the gates after it, which grows with the square. The crossover requires
  each gate's own work to be nearly nil, which describes a command-backed gate and not a review
  dimension.
- **Skip dimensions that cannot apply to a given change**: rejected as mostly already taken. A
  dimension reports on absence as readily as on presence — a change touching no documentation
  can still fail the docs dimension — so "no files of that type changed" does not make a
  dimension inert. The two dimensions that genuinely carry a precondition, contracts and
  type-safety, are already conditional in `CODING.md`.
- **Pre-load the change into the verifier envelope so executions share a cacheable prefix**:
  rejected. It requires the executor to assemble what each verifier reads, which is exactly what
  20260807-a-gate-is-one-text-not-two removed for gate text — "the party building it is the
  executor, whose interest in how a gate reads is exactly what verification exists to
  neutralize."
- **Drop advisory dimensions from the default gate set**: the one lever with real mass that does
  not return as repair rounds, and rejected by the maintainer as a quality cut this project will
  not take. Recorded because it is the honest price of the position: keeping thirteen
  independent readings is what the bill is buying.

## Consequences

### Positive

- The execution surface does not grow a flag whose reachable saving is a few percent, on five
  skills and three distribution targets.
- The next reader who proposes routing verifier models by gate kind finds the arithmetic and the
  false-finding mechanism already worked through, rather than re-deriving them.
- Naming round count as the multiplier points cost work at the executor, where the leverage is,
  instead of at the verification topology, where three records have now looked and found little.
- A user who wants cheaper verification still has the levers that exist — one model selector
  covering nearly all the spend, and `self` mode — chosen deliberately rather than by a
  mechanism that hides the trade.

### Negative

- The cost figures are reasoned rather than measured, and the false-finding cost in particular
  is an argument from the repair mechanics rather than an observed rate.
- A user who wants a middle setting between "strong everywhere" and `self` has nothing between
  them, and the position offered instead — accept the bill or cut checks — is blunt.
- Cross-family verification, the one idea here that would add recall without trading quality,
  is left unavailable rather than pursued. A multi-provider host makes it reachable, and this
  record does not design for that.
- Leaving the door open on measurement means this question can be raised a fourth time. The
  reasoning is recorded in enough detail to be attacked directly, which is the only defence
  against that.

## Source

- Session: figure-out investigation, 2026-08-10 — `/do`'s verification references, `CODING.md`'s
  default gate set, and the prior verification records read at source; no measured run available.
- Related: 20260728-move-verification-execution-policy-to-do
- Related: 20260808-restore-per-gate-default-verification-mode
- Related: 20260806-verification-is-bookkeeping-and-a-stop-condition
- Related: 20260807-a-gate-is-one-text-not-two
- Related: 20260805-ratchet-judgment-gate-reverification
