# ADR: figure-out firms the low-cognitive-load directive to match rigor's modality

## Status
Accepted

## Context

figure-out's goal is *shared* understanding. Two things serve it: getting the answer right — rigor: evidence discipline, crumb and fog tracking, rival management, independent re-derivation — and making it land for the reader — presentation: low cognitive load. A turn that is correct but arrives as a dense wall the reader has to re-read has not produced shared understanding; the "shared" half failed even though the "understanding" half held.

The spine did not weight those two halves equally. Its rigor instructions are hard, unconditional imperatives ("verify before asserting," "close every crumb before naming a read"). The single landing directive was soft and self-cancelling:

- it asked for visible shape only "when a turn carries more than a few load-bearing points" — a self-assessed threshold that a model rarely trips, because the bloated turn is exactly the one the model believes is a single nuanced argument;
- it left how much shape to apply entirely to model judgment and closed on "how much shape ... never a fixed amount," a re-softener that was the last word the paragraph left;
- its two guards ("never a fixed layout stamped on every turn," "never ... a pick-from-options prompt") defend against over-structuring and rubber-stamp menus.

Net, the paragraph granted more license to skip structure than requirement to apply it. The imbalance is one of **modality and conditionality, not word count** — presentation already had a full paragraph.

The observed failure matches this. Strong models produce turns that are information-dense, scattered, with the actual question buried inside long paragraphs — the precise failure the directive already names ("dense scattered prose that loses the reader fails the turn even when every sentence in it is right"). A short, plain, in-conversation instruction to lower cognitive load corrects it reliably, while the elaborate standing directive does not prevent it: the correction is unconditional and salient where the standing directive is hedged and conditional.

A prior restructuring ADR (20260709) audited the spine's density as "load, not bloat," rejected a full rewrite as maximum nuance-loss risk against battle-tuned prose, and explicitly noted that **no live-session presentation failure had been observed** — that change was preventive. The failure it lacked has now been observed, which grounds the targeted, evidence-gated edit the earlier ADR deliberately withheld.

## Decision

Firm the landing directive's modality to match the rigor directives, anchored to the goal. One paragraph changes; the rest of the spine is untouched.

- **Edge-marking becomes a near-default.** It fires whenever a turn carries more than one point the reader has to hold separately — a claim and its ground, a rival, a live question — not only once a turn has grown to several. Only a genuinely single simple point is exempt. This replaces the mis-calibrated "more than a few load-bearing points" gate.
- **Separate *whether* from *how much*.** Whether to mark the edges of distinct points is a near-default; how much shape a turn takes and what form it uses stays a read of who's reading. The "never a fixed amount" clause is rescoped to form/amount so it no longer reads as permission to drop structure entirely.
- **The lever is structure, not brevity.** The edit adds no length or word-count pressure anywhere; the sole (soft) brevity lever, "the explanation it needs and no more," is unchanged. Cutting length too far removes the explanation that makes a claim land — a loss, not a saving.
- **Scope the directive to presentation.** It marks the edges of reasoning already worked out and never trims or gates the Evidence Ledger, rivals, crumbs, independent re-derivation, or overturn conditions. The load comes off how a turn reads, never off what was investigated. This is also why the change cannot erode rigor: restructuring rearranges content, it cannot delete a crumb or a rival.
- **Keep the guards, scoped.** "Never a fixed layout stamped on every turn" and "never a pick-from-options menu" remain in force against over-structuring; they no longer read as license to under-structure.
- **Foreground the directive** (its own prominent sentence rather than buried after the softeners), hedging a co-cause the evidence could not exclude — that the directive was not only too soft but too buried.

## Alternatives Considered

- **Do nothing; rely on the in-conversation nudge**: Rejected — the correction is real but must be re-issued every session. Low cognitive load is a standing goal, not a per-turn ask; paying the tax repeatedly is the cost this change removes.
- **A hard mechanical rule (always bullet points, or a maximum length)**: Rejected — always-bullets is precisely "a fixed layout stamped on every turn," which the spine forbids and which invites the rubber-stamp menu the other guard forbids; a maximum length attacks the wrong dial and manufactures the nuance loss the change exists to avoid; and a fixed rule cannot tell a single-point turn (a short block is fine) from a multi-point one.
- **A baked-in worked example (a canonical good turn)**: Rejected — a concrete example becomes a shape the model pattern-copies, functionally the fixed layout the spine forbids, and it does not target the defect, which is soft modality rather than missing illustration. The abstract directive already names the right structure ("separable points separated, the question set apart"); the fix is to firm that line, not to illustrate it.
- **A full rewrite of the paragraph or spine for plainness**: Rejected — 20260709 already rejected a rewrite as maximum nuance-loss risk and judged the density load, not bloat. The observed failure is localized to one directive's firmness, so the edit is localized.

## Consequences

### Positive
- The landing half of shared understanding carries weight proportionate to the rigor half, and the directive fires by default on exactly the multi-point turns where the failure occurs.
- The near-default no-ops on genuinely single-point turns, so models that already present well are not pushed into choppy over-structuring.
- Rigor is protected by construction: the directive can only change how content reads, never what is investigated or retained — the guardrail makes "lower the load" un-citable as a reason to skip a crumb, a rival, or the re-derivation pass.

### Negative
- Balance is a judgment the wording installs but cannot fully calibrate; a model can still misjudge how much shape a turn needs. Watch sessions before further tuning.
- The evidence could not cleanly separate "too soft" from "too buried," so the edit both firms the modality and foregrounds the directive; if only one was the true cause, the other change is inert rather than harmful.
- The change edits standing guidance and is reversible (a two-way door): if the firmer default over-structures in practice, a later ADR can retune it.

## Source
- Grounding: an observed live-session presentation failure on strong models (dense, scattered turns with the question buried), read against the spine's uniformly hard rigor directives; corroborated by an independent re-derivation from the evidence with the conclusion withheld, which converged on modality (not word count) as the imbalance and structure (not brevity) as the lever.
- Related: 20260709-figure-out-reweight-by-rehosting-not-extraction
- Related: 20260611-figure-out-spine-owns-epistemics-mode-refs-thin
- Related: 20260714-figure-out-scales-read-depth-with-stakes-and-reversibility
