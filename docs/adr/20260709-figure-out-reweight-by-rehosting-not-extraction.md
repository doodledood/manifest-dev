# ADR: Re-weight figure-out's SKILL.md by re-hosting — sectioned arc, no extraction, evidence-gated trims

## Status
Accepted

## Context

figure-out's `SKILL.md` body has grown by accretion — 37 commits since 2026-04, each adding an individually justified behavior — into ~2,300 words of 23 flat, equally weighted imperative paragraphs with no headings. An LLM's attention is finite: when every paragraph presents at identical urgency, load-bearing spine instructions compete with 20-word edge guards and nothing is typographically foregrounded. Concretely: ~230 words of task-probe routing mechanics sit at position 2, ahead of the per-turn cadence rule; the epistemic spine is split by a five-paragraph band of guards and calibration, so the crumbs/fog vocabulary (consolidated conceptually in the confidence-spine change, PR #223) spans two paragraphs ~620 words apart.

Two constraints shape the fix. First, the file already practices deep progressive disclosure — seven conditional references and seven task-probe files — and what remains inline is predominantly always-on: the routing table must stay in the loading layer (see 20260703-progressive-disclosure-triggers-live-in-loading-layer), and the latent-criterion probe's sensing trigger is too subtle to survive an indirection. Extraction headroom is exhausted. Second, the body is distributed verbatim to other CLIs, so any structural device must be plain, portable markdown.

The behaviors themselves are battle-tuned. A per-line audit against the prompt-engineering review discipline — run as two independent passes, one from a fresh context with conclusions withheld — converged on the same verdict: genuine fat is ~3% (~50–70 words); the density is load, not bloat. No live-session salience failure has been observed; the change is preventive — the target is regression-by-a-thousand-cuts, where future additions keep landing at uniform weight until the hierarchy is unrecoverable.

## Decision

Re-host, don't rewrite:

1. **Reorder paragraphs verbatim into a six-section arc** under sparse H2 headings: *The loop* → *Evidence & confidence* → *Serving what's true* → *Reading the user* → *Naming the read* → *Setup, modes & loading*. The probe-routing table and flag blocks move to the final loading-layer section; position affects salience only, since the whole file loads at invocation.
2. **No extraction to references** — headroom is exhausted per the Context.
3. **Text edits limited to a converged, evidence-gated trim list**: unify the crux-selection rule split across two paragraphs (the tiebreaker exists in only one copy); canonicalize the definition of *fog* at first use and have the confidence paragraph reference it (the term is currently glossed twice with drift); delete two redundant clauses ("and naming the read still ends the skill" in the artifact-probe paragraph — triple-guarded within its own sentence — and "as you would anyway"); reword the addressee-less scratch sentence to name the caller. Duplications judged intentional emphasis are kept: anti-sycophancy stated at both decision points where it bites (per-turn recommendation; option-set curation), the crumb-gate at its three sites, and the awareness-not-a-script layering that suppresses checklist-walking.
4. **Nuance-loss guard**: the change ships with a sentence-level accounting — every sentence marked kept-verbatim / moved / merged-into / deleted-with-reason. Deletions require individual argument; the default is zero.
5. **Validation**: an identical cold-read battery runs on the pre- and post-restructure files from fresh contexts (recover the top behaviors in priority order; first action on invocation; what ends the skill; rules in tension; first-turn shape on a trivial topic). The restructured file must score ≥ baseline on every probe, plus a review-prompt pass on the result.

## Alternatives Considered

- **Trim/merge only, no structural change**: Cheapest — but leaves both dilution points (routing mechanics hosted at spine altitude; spine split by the guard band) untouched, and does nothing for future accretion.
- **Reorder + bold lead-sentences, no headings**: Preserves the unbroken-prose look — but bolding at this density reads as shouting, and it gives future additions no slot structure to be measured against.
- **Extraction to references**: Rejected on evidence — every candidate fails: the routing table's trigger must live in the loading layer, the artifact-probe's sensing trigger would not survive an indirection, and the prompt-shaped integration is already trigger + inline fallback.
- **Full rewrite**: Maximum nuance-loss risk against dozens of commits of battle-tuning, for no benefit re-hosting doesn't already capture.

## Consequences

### Positive
- The file's hierarchy becomes typographically legible: spine contiguous, guards grouped, loading layer last.
- Future additions face an altitude question at review time — *which section does this belong in, and is it really spine?* — making accretion drift visible in diffs. This write-time payoff holds even if the read-time delta measures nil.
- The most load-bearing term (*fog*) gets a single canonical definition; the only rule split whose copies could diverge (crux selection) is unified.

### Negative
- Headings introduce a structure a model could misread as sequential phases; section names must name concerns, not steps.
- The probe-routing table loses its top-of-file position; the load-at-start cue must be carried by wording and is explicitly checked by the first-action probe.
- Mass reduction is only ~2% — the file stays dense by design; anyone expecting "trim the fat" to shrink it will find the fat was already gone.

## Source
- Grounding: per-line audit under the prompt-engineering review discipline, two independent passes converging on ~3% genuine fat; preventive — no observed live-session salience failure. Lands ahead of the accompanying skill edits.
- Related: 20260611-figure-out-spine-owns-epistemics-mode-refs-thin
- Related: 20260703-progressive-disclosure-triggers-live-in-loading-layer
