# ADR: figure-out adopts a concrete default turn shape

## Status
Accepted

## Context

figure-out's landing half — making a turn land for the reader — has been patched three times in twelve days, each time in the same modality:

- `2ca074e` (#231) removed the positional anchor *"Per turn: lead with one question and your recommended answer"* in favour of "carrying two things in whatever order the conversation wants", and added the guard *"never a fixed layout stamped on every turn"*.
- `89ec03f` (#232) added an organized-presentation default; `3360836` (#234) firmed its modality to a near-default per `20260722-figure-out-firms-low-cognitive-load-directive`.
- `967eaaa` (#236) narrowed the accompanying no-trim guardrail per `20260726-figure-out-narrows-presentation-no-trim-clause`.

Every one of those changes describes *qualities* a good turn has — "edges legible", "separable points separated", "the question set apart from the reasoning", "plain language over a packed block" — and none specifies a shape. The prompt contains no example of a good turn, by deliberate choice: `20260722` rejected a baked-in worked example on the grounds that a concrete example becomes a shape the model pattern-copies, functionally the fixed layout the spine forbids.

The failure persists on current frontier models under the post-`#234` wording. Turns still arrive dense and scattered, with several questions buried mid-paragraph and no clear signal of what a sufficient answer would be — the reader cannot hold the points or tell which one to answer. The evidence is direct rather than recalled: in the session that produced this ADR, a turn composed while consciously following the current directive was read as "a bunch of noise with little high signal hidden inside".

That makes three escalations of one modality, the most recent four days old, failing against the reader it was written for. The natural inference is that the modality itself is wrong rather than still too weak: models comply reliably with a concrete output shape and unreliably with quality adjectives, however firmly those adjectives are stated. The risk `20260722` guarded against — that a shape gets pattern-copied — is, given a shape worth copying, the mechanism doing the work rather than the hazard.

Two further findings widen the diagnosis beyond presentation:

- **Some of the noise is prompt-ordered content, not formatting.** The per-turn contract requires every turn to carry "the thing most likely to break that answer", and the read anatomy encourages voicing confidence limits. On turns where nothing genuinely threatens the answer, discharging those obligations is padding the reader did not ask for and, in this session, explicitly did not want.
- **Marking edges is not the same as sequencing.** The current directive asks that several separable points be *separated* within one turn. A reader who can only hold and answer one thing at a time is served by the next point waiting for the next turn, not by that point being well-labelled inside a crowded one.

Formats were probed concretely rather than argued: three sample turns (minimal anchor, light three-slot shape, heavy labelled sections) were rendered over identical throwaway content and reacted to. The minimal anchor won — free prose whose only fixed rule is that the ask stands alone at the end.

## Decision

Replace the abstract landing directive with a concrete **default turn shape**, and demote the per-turn obligations that pad turns without earning their place.

- **One point per turn.** A turn advances one thing. When the investigation has several findings pending, they queue across turns rather than arriving together — sequencing, not labelling, is what keeps a turn answerable. Points that are trivially inseparable may still travel together.
- **The default shape.** Concise prose carrying the finding and the best-supported recommended answer, closing with the ask as a standalone final line that carries its own recommended answer. Where ratified Taste context exists, the recommendation is taste-informed.
- **Concise by default.** Brevity becomes a stated default posture for the surface, replacing `20260722`'s position that structure is the only lever. It is paired inseparably with the guardrail carried forward from `20260726`: the load comes off how the turn reads, never off what was investigated. Fog clearing, crumb closure, rival management, verification, and re-derivation are untouched, and no numeric budget is introduced.
- **Ballast on demand.** The breaker check and voiced confidence limits ship when something genuinely threatens the answer, not as a per-turn slot to fill. This applies `20260726`'s reasoning — that the per-turn contract is "what a turn must earn, not slots to fill" — to the obligation that was still being read as a slot.
- **Asks stay in prose.** The ask is a line of text, never a harness question-selection primitive.
- **A default, not a template.** The shape follows the precedent already shipped in this skill's `LOG.md` entry shape: a recommended form that is "a default, not a form to pad". The `never stamp a fixed layout` guard is narrowed to what it is actually for — padding a turn to fill a form, and collapsing deliberation into a pick-from-options menu — rather than reading as a prohibition on having a default at all.

This **supersedes** `20260722-figure-out-firms-low-cognitive-load-directive`. That ADR's premise stands and is inherited: landing ranks with rigor, and a correct turn that arrives as a dense wall has not landed. Its *mechanism* is what this replaces — firming an abstract directive's modality, withholding a concrete shape, and treating brevity as the wrong dial. `20260726-figure-out-narrows-presentation-no-trim-clause` remains Accepted: its guardrail wording is carried forward verbatim in force here, and it becomes a narrowing of this ADR's guardrail rather than of the superseded one's.

## Alternatives Considered

- **Firm the abstract directive again**: Rejected — this would be the third iteration of a mechanism whose most recent version, four days old at the time of writing, failed live against the reader it was written for. Repeating a failing modality with more force is the pattern the evidence argues against.
- **Deliver asks through the harness's question-selection primitive** (structured options with the recommendation marked first): Rejected on three grounds. It was demonstrated live in-session and the reader typed a free-text answer through it, so the convenience it buys went unused. It is a harness-bound primitive where the skill's portability doctrine calls for capabilities named in universal language, and it would need mode-conditional wiring — autonomous runs self-answer and never ask, team mode asks in a chat channel — so it could only ever apply to interactive local sessions. And a menu invites the rubber-stamp the spine already forbids.
- **A word or length budget**: Rejected, consistent with `20260722` and `20260726` — a numeric cap attacks the wrong dial and cuts the explanation that makes a claim land. The conciseness adopted here is a default posture with an explicit rigor carve-out, not a cap.
- **A heavier fixed-section format** (labelled Finding / Read / Risk / Question every turn): Rejected on reader reaction — it reads as a form to discharge, invites padding empty sections, and loses the teammate voice `#231` was written to restore.
- **Record the preference as a Taste entry instead of changing the skill**: Rejected by the ratifier — this is how figure-out should behave for every reader, not how one user steers. A Taste entry would also leave the shipped skill unchanged for everyone else.
- **Do nothing and let `#234` bed in**: Rejected — the sessions exhibiting the failure ran under the post-`#234` wording, so the waiting period this would preserve has already elapsed.

## Consequences

### Positive

- The prompt states a shape a model can execute, instead of qualities it must infer a shape from — the modality that three prior iterations lacked.
- One point per turn makes every turn answerable: the reader holds one thing and knows exactly what is being asked, because the ask sits alone at the end with a recommendation attached.
- Removing per-turn ballast cuts noise at its source rather than reformatting it, which no presentation-only change could reach.

### Negative

- This reintroduces a default shape of the kind `#231` removed. If turns start reading as padded or robotic — the motivation for that de-templating — the mitigation is to loosen toward a guard-plus-example rather than to return to unshaped prose, and a later ADR should record it.
- One point per turn spends more turns on the same ground. If sessions come to feel slow, the trivially-inseparable allowance is the dial to widen.
- Conciseness as a default posture sits closer to the rigor boundary than `20260722` was willing to go. The `20260726` guardrail is the only thing holding that line, and it is stated once; sessions should be watched for investigation depth quietly following the surface down.
- Two-way door throughout: every element here is prompt wording and is reversible by a later ADR.

## Source

- Grounding: the skill's own commit trajectory (`2ca074e`, `89ec03f`, `3360836`, `967eaaa`) read against a live session in which a turn written under the current wording was judged noise by its reader; format chosen by reacting to three rendered sample turns rather than by argument; the ask-delivery alternative eliminated by live demonstration.
- Supersedes `20260722-figure-out-firms-low-cognitive-load-directive`
- Related: `20260726-figure-out-narrows-presentation-no-trim-clause` — its guardrail is carried forward in force here.
- Related: `20260709-figure-out-reweight-by-rehosting-not-extraction`
