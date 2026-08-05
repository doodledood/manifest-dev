# ADR: Judgment Gates re-verify by Ratchet, not by re-sampling

## Status
Accepted

## Context

`/do` evaluates every Acceptance Criterion and Global Invariant each round until all
hold a fresh PASS. Two gate kinds sit behind that uniform loop, and they behave
differently under repetition.

A **Deterministic Gate** returns a verdict from a command or check: the same artifact
state yields the same result, so re-running it costs little and settles the same
question every time. A **Judgment Gate** returns a model's judgment over an open
finding space. A fresh evaluation samples that space again, and reliably surfaces
findings the previous one did not — on an unchanged subject as well as a changed one.
Its PASS therefore means "this round's sample came up empty", not "the subject is
settled".

That difference decides whether a gate can converge. A defect-finder's supply
contracts across rounds: real, trigger-nameable defects deplete as they are fixed,
and the defects a repair introduces shrink with the size of the repairs. The nine
advisory review dimensions have no such contraction. Each round re-reads the whole
change; repairs add new surface to read; and taste findings are generated rather than
enumerated, so a capable reviewer can produce one more defensible Medium on any
non-trivial diff. Terminating on an empty sample across nine such bars is luck, and a
stronger, more willing model makes that draw rarer — which is why round counts rose
as executing models improved rather than falling.

Two shipped dampers reach neither the sampling nor the termination structure.
`20260728-bound-the-acceptance-contract-from-above` bounds executor over-delivery with
a ceiling invariant and anchors defect-finder reportability with a required `Trigger`
field, which covers four dimensions. `20260730-consolidated-default-verification-mode`
cuts artifact reads per round and explicitly accepts lower per-round recall; it changes
who evaluates, not how often the finding space is re-opened. Observed behavior after
both: rounds continued, and the findings were new each round rather than the same
verdict flipping — the signature of re-sampling rather than instability.

## Decision

Classify every gate and bind re-verification to the class.

**Kind is a property of the gate, declared in `verify.kind`.** The field is required on
every Acceptance Criterion and Global Invariant and takes `judgment` or `deterministic`.
There is no default and nothing is inferred: a gate that omits it makes the Manifest
invalid, and `/do` rejects it by the same route it rejects any other schema violation.
A gate mixing a command check with a judgment declares `judgment`; instructions naming
explicit commands always run those commands in full whatever the declared kind.

*(This paragraph was amended after the decision first shipped — see **Amendment:
kind becomes a required schema field** below, which records why the original
kind-as-instructions-prose form was reversed.)*

**Deterministic Gates re-run freely and fully.** Narrowing what they read buys nothing.

**Judgment Gates re-verify by Ratchet.** The first evaluation reads the full change.
Every later evaluation judges only two things: whether the findings it last reported
were repaired, and whether the delta since that evaluation introduces anything the
criterion catches. The evaluator still reads as widely as it needs to; it reports only
within that scope. The gate ledger and the execution log carry the state this rests
on — per Judgment Gate, whether the full look happened, the artifact state it read,
the findings issued, and the repairs verified — so a run that resumes after context
compaction delta-checks rather than silently taking a second full look.

**The whole-change quality sweep runs late and once.** `/define` phases the nine
advisory dimensions after the defect-finders and the project's mechanical gates, so
their one full look lands on a change those gates have already settled. Their findings
bind exactly as before: repaired in the run, never handed to the user as unfixed
homework. The trust boundary stays at `/done`.

**`--exhaustive-verification` restores full re-sampling** as run-level policy, behind
progressive disclosure, for a run that wants maximum recall and accepts the round
count. Like the verification mode it is fixed at launch and never written into the
Manifest.

**Advisory severity gains an auditable floor.** A Medium-or-higher finding on an
advisory dimension must name the concrete cost that earns the grade — the change it
makes harder, the task it defeats, the condition under which behavior degrades. This
is the `Trigger` move applied to the tier where Medium is the blocking grade: it holds
the bar in one place across reviewers and models instead of letting it drift with the
reader. Thresholds themselves do not move.

## Alternatives Considered

- **Hand the advisory findings to the user as a report at the end**: rejected. A
  terminal list of unfixed findings is homework, and `/do`'s output is meant to be
  final — the user's stated success condition and this project's own
  ("trust the output enough to ship it with minimal review").
- **Move the advisory tier to the PR boundary, running `review-pr` instead**:
  rejected, though `review-pr` is already ratcheted at that boundary (it bounds
  findings to the reviewed range and prunes what prior threads cover). It moves the
  trust boundary from `/done` to merge-ready and leaves non-PR work — prose,
  local runs — with no taste enforcement at all.
- **Make `self` the default verification mode**: rejected. The executor grading its
  own work is the self-attestation collapse that independent verification exists to
  prevent (`20260606`, `20260722`).
- **A raw round cap**: rejected. It drops findings a verifier already reported.
  The Ratchet bounds rounds by closing the sample space instead, so everything found
  is still repaired and only unsampled ground is forgone.
- **Late phase for the advisory tier without the Ratchet**: rejected as insufficient.
  Phasing moves when the first sample happens; the gate still re-samples after each
  repair, so the termination structure is unchanged.
- **Raise the advisory threshold from no MEDIUM+ to no HIGH+**: rejected. It lowers
  the quality floor to catch only egregious findings, and under the Ratchet the
  MEDIUM bar costs one repair round rather than an unbounded number.
- **Add a `verify.kind` schema field**: initially rejected — it buys explicitness at the
  price of a migration, a validation change in `/do`, and version skew between executors
  and manifests, when the instructions text already carries the fact and inference covers
  what it omits. **This rejection was reversed; see the amendment below.**

## Consequences

### Positive

- Round count becomes a property of the contract rather than of sampling luck, and
  stops rising as executing models get stronger.
- The advisory tier keeps binding: findings are still repaired in-run, so `/done`
  remains the trust boundary.
- Kind is visible in the schema rather than buried in prose, so a reader can tell from
  the Manifest alone how each gate will re-verify (as amended).
- Ratchet state is durable in the execution log, so long or compacted runs resume
  without re-opening settled ground.
- Advisory severity is auditable from a written finding, matching what the `Trigger`
  field already does for defect-finders.

### Negative

- Findings a second or third full look would have surfaced on ground already judged
  once are forgone. That is the deliberate trade, priced against a standard that
  ended on an empty draw rather than on completeness; `--exhaustive-verification`
  buys it back for a run that wants it.
- Correct scoping now depends on ledger and log state surviving the run. A log that
  loses a gate's last-read artifact state costs that gate a fresh full look — the old
  behavior, not a correctness failure, but the reason the log requirement is explicit.
- Misclassification risk moves from the reader to the author (as amended). Nothing is
  inferred any more, so a gate is exactly the kind it declares — and a mixed gate
  labelled `deterministic` puts its judgment half back on a full re-sample every round,
  which is the churn this decision exists to remove. The commands-always-run rule does
  not reach that case, since it governs whether commands run rather than how widely the
  gate re-reads. `/define` names it as the error to watch for, but no check detects it.
- Requiring a stated cost will drop some true advisory Mediums whose reviewer sensed
  the problem but could not name what it costs. That is the same trade the `Trigger`
  field made, with the same honest loss.

## Source
- Related: `20260728-bound-the-acceptance-contract-from-above`,
  `20260730-consolidated-default-verification-mode`,
  `20260722-state-verification-sufficiency-not-only-necessity`,
  `20260606-figure-out-process-trust-vs-define-do-artifact-trust`,
  `20260728-move-verification-execution-policy-to-do`
- Manifest: `~/.manifest-dev/manifests/manifest-20260805-200316.md`

## Amendment: kind becomes a required schema field

Accepted the same day, superseding this ADR's rejection of a `verify.kind` field and
its no-schema-change consequence. The rest of the decision — the Ratchet itself, the
late single-sample sweep, `--exhaustive-verification`, the ledger and log state, the
advisory severity floor — is unchanged.

**Why.** Kind decides a gate's entire re-verification behaviour, and as instructions
prose it was invisible in the schema, inferred when unstated, and silently wrong in the
one direction that costs most: a judgment gate read as deterministic re-runs "freely and
fully", which for a judgment gate means re-sampling every round — precisely the churn
this ADR exists to remove. Reading a Manifest, you could not tell what any gate would
do. A load-bearing property should be declared, not guessed.

**What changed.** `verify.kind` is required on every gate, taking `judgment` or
`deterministic`, with no default and no inference. `/do` and `/define` validate it like
any other schema requirement; `/define` emits it on every gate it authors, the ceiling
included; the kind-as-prose guidance is removed rather than left as a second mechanism;
and a mixed gate declares `judgment`.

**Cost accepted.** Manifests written before the field are invalid rather than migrated,
and an older `/do` rejects a Manifest carrying it. Both were weighed and accepted
deliberately — no migration machinery is provided. Requiring the field also removes the
safety net the old inference default supplied: previously an unmarked judgment gate
still ratcheted, where now an unmarked gate is simply refused. That is the intended
trade, refusal being preferable to a wrong guess.
