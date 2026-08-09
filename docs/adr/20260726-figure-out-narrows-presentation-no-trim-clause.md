# ADR: figure-out narrows the presentation no-trim clause to its guardrail

## Status
Accepted

## Area
figure-out

## Context

`20260722-figure-out-firms-low-cognitive-load-directive` firmed figure-out's landing directive so that edge-marking became a near-default on multi-point turns. That change carried a deliberate guardrail, so firming the presentation directive could not be read as license to cut rigor. The guardrail shipped in commit `3360836` (#234) as:

> This is presentation of thinking already done: it marks the edges of the reasoning that stays and never trims or gates the evidence, rivals, crumbs, re-derivation, or overturn conditions the turn owes — the load comes off how the turn reads, never off what was investigated.

The guardrail's job, as that ADR states it, is to make "lower the load" un-citable as a reason to skip a crumb, a rival, or the re-derivation pass.

The shipped sentence is wider than that job. Its enumeration is qualified by "the turn owes", and the referent of that phrase is defined nowhere in the prompt. A five-noun list sitting inside the *per-turn* presentation paragraph, with no stated referent, is readily read as a per-turn content floor — a checklist a turn is expected to discharge. That reading collides with three narrowings the same file states explicitly:

- the per-turn contract carries **two** things and is "what a turn must earn, not slots to fill in a fixed sequence";
- read-depth discipline "bites where the ground is large or the call is hard to take back, not as ceremony to perform on every turn";
- the read anatomy is "a principle, not a form to pad", and is scoped to naming the read — independent re-derivation is a pre-read pass, and overturn conditions ship with the read, neither being a per-turn obligation.

So the prompt states a per-turn floor in one place and denies it in three others. Whichever reading a given model settles on, one of the two is dead text, and the ambiguity is load-bearing: it sits on the boundary between what a turn prints and what an investigation owes.

The enumeration is also the only part of the sentence carrying this risk. The second half — "the load comes off how the turn reads, never off what was investigated" — discharges the guardrail's stated job on its own. Skipping a crumb, dropping a rival, or omitting the re-derivation pass are all reductions in what was investigated, which that half forbids outright.

## Decision

Delete the enumeration, keeping the guardrail. The sentence becomes:

> This is presentation of thinking already done: it marks the edges of the reasoning that stays — the load comes off how the turn reads, never off what was investigated.

Nothing else in the paragraph or the file changes.

This **narrows** the directive recorded in `20260722-figure-out-firms-low-cognitive-load-directive`; it does not reverse or supersede it. That ADR's decision — that edge-marking is a near-default and that the lever is structure rather than brevity — stands unchanged, as does its guardrail. Only the enumeration that over-stated the guardrail is removed.

Two points of scope are worth stating plainly, because they bound what this change claims:

- **This is correctness hygiene, not a length fix.** The expected effect on figure-out's turn length is approximately zero. The change removes an ambiguity; it does not add brevity pressure, and none should be inferred from it.
- **Nothing leaves the investigation.** The change alters what a turn is ambiguously implied to owe, not what an investigation must do. The Evidence Ledger, belief register, crumb-and-fog tracking, rival management, and the pre-read re-derivation pass are all untouched, and the read still ships with its full anatomy.

Deleting only the qualifier "the turn owes" was rejected as a smaller edit: it would leave the enumeration **unrestricted**, which is a stronger content floor than the current text, not a weaker one. The enumeration has to go as a unit.

## Alternatives Considered

- **Do nothing**: The ambiguity is real but has no demonstrated behavioural cost, and the directive is recent. Rejected because the edit moves the shipped text toward the intent its own ADR records rather than away from it, making it cheap and reversible; and because an unresolved contradiction between four statements in one prompt is a defect regardless of whether a measurement has caught it.
- **Replace the clause with a log-vs-chat routing rule** — route evidence, rivals, crumbs, re-derivation, and overturn conditions to the investigation log, and print only the answer, its load-bearing ground, and the likeliest breaker: Rejected on three counts. It contradicts the read anatomy, which requires the read to ship with the Evidence Ledger it rests on. It contradicts the sentence three lines earlier, which explicitly keeps a load-bearing claim's provenance on the surface. And it makes rigor conditional on the investigation log, which is opt-out-able and lives outside the repo — leaving `--no-log` sessions with nothing carrying the ledger. The log serializes what the investigation already carries; it was never designed as the exclusive home for it.
- **Delete the whole sentence, guardrail included**: Rejected — it removes a deliberate rigor guard recorded in an accepted ADR, and the guard's second half is doing real work that nothing else in the paragraph does.
- **Add a word or length budget to force convergence in output length**: Rejected — `20260722` already rejected a maximum length as attacking the wrong dial, and that reasoning is unchanged: cutting length too far removes the explanation that makes a claim land. Stacking a second, differently-motivated patch onto the same paragraph would also obscure which change produced any observed effect.

## Consequences

### Positive
- The prompt states the per-turn contract once, in one place, instead of stating it in one place and contradicting it in another.
- The guardrail keeps its full force: reducing what was investigated remains forbidden outright, in plainer words than before.
- The paragraph gets 16 words shorter (411 to 395), in a passage whose subject is not making the reader work through dense blocks.

### Negative
- The guardrail is now stated once rather than twice. If a model needed the enumeration's specificity to connect "what was investigated" to crumbs and rivals concretely, the shorter form gives it less to hold onto. The surrounding sections state each of those obligations as hard imperatives in their own right, which is why this is judged an acceptable trade.
- No measurement accompanies this change, and none is claimed. The change is argued from the prompt's internal consistency, not from observed behaviour.
- Two-way door: if the shorter guardrail proves too thin in practice, a later ADR can restore a bounded form of the enumeration scoped explicitly to the read.

## Source
- Grounding: internal inconsistency between the presentation paragraph's no-trim enumeration and the per-turn, read-depth, and read-anatomy scoping stated elsewhere in the same prompt; read against the guardrail's stated job in `20260722-figure-out-firms-low-cognitive-load-directive`. Corroborated by an independent re-derivation from the same evidence with the conclusion withheld, which converged on narrowing and independently rejected the routing replacement.
- Related: `20260722-figure-out-firms-low-cognitive-load-directive` — this ADR narrows that directive's guardrail wording; that ADR remains Accepted and in force.
- Related: `20260709-figure-out-reweight-by-rehosting-not-extraction`
- Related: `20260611-figure-out-spine-owns-epistemics-mode-refs-thin`
