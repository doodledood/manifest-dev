# ADR: Bound the acceptance contract from above, not only from below

## Status
Accepted

## Context

A Manifest's Acceptance Criteria and Global Invariants all state a floor: what the work must reach before `/do` may call `/done`. Nothing in the contract states a ceiling — that reaching the floor is the whole of what is owed. That asymmetry was invisible while executing models under-reached: a model inclined to stop early fails floors, so every line of pressure in `/define` and `/do` was calibrated against under-delivery, and criteria that check a capability exists were the right defensive shape.

Newer models invert the disposition. Existence-shaped criteria pass without effort, and the failure mode moves to the other side: the executor polishes past what any gate required, repairs findings a passing gate reported beneath its own threshold, and refactors surfaces no criterion named. Each of those is a substantive change to some gate's subject, so each re-stales gates and buys another verification round. The observed effect is manifest runs taking two to four times as long and costing two to four times as much, on the same manifests with the same gate count — the multiplier is repair rounds, not verifier fan-out.

Two distinct mechanisms produce it.

**Executor-side over-delivery.** `/do` already tells the executor that a gate's threshold is a bar rather than a starting point, and that findings below it are handed over rather than worked. That instruction is prose in the executor's prompt, and nothing verifies it. This repo's own doctrine (`20260726-only-gates-bind-process-guidance-is-advisory`) holds that only Acceptance Criteria and Global Invariants bind, so an unverified instruction is exactly the layer a capable executor may legitimately weigh and depart from. The rule has shipped through every distribution and the over-delivery continues.

**Verifier-side bar inflation.** The four defect-finder review dimensions pass only on no LOW-or-higher findings. That bar is defended on the grounds that a defect-finder reports only certain defects, so every LOW there is real signal — sound while the certainty floor holds. But the certainty floor was itself stated as a disposition ("certainty over suspicion"), judged by the same model doing the review. A model more willing to report raises what the gate demands without anyone changing the gate, and the resulting failures are legitimate, so the follow-on repairs are gate-required work.

The two mechanisms need different answers: no ceiling gate can reach the second, because once a gate genuinely fails, the work that follows is required by definition.

## Decision

State both bounds of the acceptance contract, and make each bound independent of the reading model's disposition.

**From above — `/define` emits a ceiling Global Invariant on every manifest.** It fails a change that carries work no Acceptance Criterion, Global Invariant, or Deliverable required, and work that nominally serves one of those while far exceeding the surface the Appetite allows. Four properties are specified with it:

- **Conformance, never necessity.** It asks whether the change exceeded what was agreed, taking the manifest's premise as given exactly as every other criterion does. It never asks whether the work was worth doing.
- **`phase: 1`.** It runs every repair round beside the other gates. Within a round the gates re-verify anyway, so excess caught there is removed alongside that round's other fixes; excess caught once everything is green forces a fresh round against a diff where the extra work has entangled with passing gates.
- **A cheap, fast `verify.model`.** Tracing each change back to the item that asked for it is mostly a lookup, and this gate runs more often than any other; where judgment is needed, the gate's calibration carries it rather than model strength.
- **Intent carried inline in its `verify.prompt`.** A verifier sees only its own prompt, so a ceiling referring to "the manifest" refers to something it cannot read. This makes it the first gate holding a copy of Intent, so amendment must refresh that copy — a stale one judges the work against the scope the amendment replaced and fails what it required. `/define`'s frame-reconciliation rule names it for that reason.

`/do`'s threshold passage is reconciled to defer to that invariant where a manifest carries one, rather than restating the same restraint as prose.

**From below — reportability on defect-finder dimensions becomes a property of the finding's text.** A finding must name the concrete input, state, or sequence that produces the failure; one that cannot name its trigger is not reportable, however strongly the reviewer suspects it. The finding template gains a `Trigger` field so the requirement is checkable by someone reading only the finding. The dimension thresholds do not move.

These are two sides of one decision rather than two decisions. The contract's meaning had been allowed to vary with the disposition of whoever read it — upward on the missing ceiling, upward again on an unanchored bar — and both sides are closed the same way: by stating in the artifact what had been left to the reader's temperament.

Model-independence here is damping, not elimination. A ceiling invariant is still judged by a model, and an eager reader will find more excess just as it demands more of a floor. That is the point: the same disposition inflates both sides, so pairing them makes the *system* less sensitive to disposition than any single gate can be made on its own.

### Relationship to the judgment layer

`20260708-judgment-layer-is-a-review-time-premise-check` rejected a necessity gate in `/define` and confined premise-questioning to review time. This ADR does not reverse that, and the distinction is load-bearing rather than incidental.

That ADR's grounds were that a gate assumes the premise it would need to question, and that a premise question is not a completion condition because it legitimately resolves as "yes, still wanted" — a human judgment no engine can adjudicate. Neither ground reaches a conformance ceiling. "Does this change contain work nothing required?" assumes the premise in exactly the way every Acceptance Criterion does, and resolves against the artifact with no human ruling in the loop. The existing criteria ask whether a change *reaches* what was agreed; the ceiling asks whether it *stops there*. Both are conformance questions about the same contract.

Premise-questioning — whether the change earns its keep at all — remains where that ADR put it: non-binding, author-facing, at review time.

## Alternatives Considered

- **Strengthen the prose in `/do` instead of adding a gate**: rejected. The instruction already exists, has shipped through every distribution, and the behavior persists. Restraint asked of the executor is asked of the one component in the loop whose disposition is to act, inside a prompt otherwise dense with completeness pressure — and by this repo's own doctrine, unverified instruction does not bind. More words in the same layer change nothing.
- **A late `verify.phase` for the ceiling invariant, judging the finished diff once**: rejected. It is cheaper only when it passes. A failure at that point forces an extra full round against a diff where the excess has entangled with passing gates and is expensive to unpick, and the run has already paid for every round of over-delivery it was meant to prevent. Single-shot feedback arriving at the end also cannot recalibrate the rounds that produced the waste. This alternative was initially preferred on the reasoning that a ceiling needs the finished artifact — which turned out to import the judgment layer's evidence requirement onto a gate that does not have it. A conformance comparison is answerable mid-run, because partial work toward a Deliverable is required work.
- **Pair a ceiling with each Acceptance Criterion**: rejected. Over-delivery is a property of the diff as a whole, so one invariant reads it as well as many would, and pairing doubles gate count — spending the cost this decision exists to reduce.
- **Raise the defect-finder threshold from no LOW-or-higher to no MEDIUM-or-higher**: rejected. It would trade real LOW-severity defects for round count, which inverts the product's stated priority. The threshold is not what moved; what qualifies as a finding at that threshold is.
- **Inject each manifest's Appetite and Out of bounds into every verifier's prompt as a wrapper**: rejected as the primary fix. It bounds the *surface* a verifier ranges over, and the observed overreach is a verifier holding too high a bar over the correct surface. The material is still used, but as the body of the ceiling invariant's own prompt rather than as a wrapper on every gate.
- **Batch several Acceptance Criteria into shared verifier subagents to cut fan-out cost**: not adopted here. Verifier fan-out is fixed by a manifest's gate count and did not change when the cost did, so batching cannot explain or repair the regression; it also trades away the independent-verifier property that makes acceptance evidence worth anything. It remains available as a standalone cost question, on its own merits.
- **A user-facing strictness or budget knob**: rejected on the same reasoning as `20260722-state-verification-sufficiency-not-only-necessity` — it leaves the unstated bound in place, shifts a tuning burden onto users, and cannot help unattended runs where nobody is present to turn it.

## Consequences

### Positive

- The acceptance contract states both of its bounds, so what a run owes no longer depends on the executing model's temperament.
- Excess is caught in the round that produced it, when removing it costs almost nothing beyond that round's other repairs.
- Defect-finder reportability can be audited from a written finding, so the bar sits in one place across reviewers and across models.
- No new manifest fields, skills, or runtime surfaces; the ceiling is an ordinary Global Invariant and inherits the whole verifier contract.

### Negative

- Every manifest carries one more gate. On a run with no over-delivery this is pure added cost — one cheap verifier per round — and the saving depends on the gate actually deterring the behavior it names, which is reasoned rather than measured.
- The ceiling's wording is load-bearing in a way most gates are not. Pitched as "minimal diff" it fails legitimately required work and re-stales everything that failure touches, making cost worse rather than better. `/define`'s guidance leans against that, but the failure mode is real and the gate's text is where it would appear.
- Requiring a stated trigger will drop some true findings whose mechanism a reviewer sensed but could not name. That is the intended trade — an empty report beats a false positive on a defect-finder — but it is a genuine loss, not a free one.
- The conformance/necessity distinction is one wording slip away from collapsing. A ceiling prompt that drifts into asking whether work was warranted rebuilds the gate `20260708` rejected, and would halt runs on questions no engine can settle.

## Source
- Related: See also `20260708-judgment-layer-is-a-review-time-premise-check`, `20260726-only-gates-bind-process-guidance-is-advisory`, `20260722-state-verification-sufficiency-not-only-necessity`.
