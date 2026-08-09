# ADR: a figure-out turn carries one concrete claim, in plain words, in a skimmable shape

## Status
Accepted

## Area
figure-out

## Context

The prior landing contract evolved through `20260722-figure-out-firms-low-cognitive-load-directive`, `20260726-figure-out-narrows-presentation-no-trim-clause`, and `20260727-figure-out-adopts-a-default-turn-shape`. It settled one point per turn, concise-by-default prose, and the ask alone on the last line, but it still treated length as the main control.

Three distinct failure modes remain.

**The dial is claims per turn, not words.** Several proofs of one claim create excess load, but removing the claim's substance produces a vague summary without meaningful savings. A turn gets shorter by carrying fewer claims and proofs, not by compressing its one claim into abstraction.

**Plain language has a floor.** Invented compounds and abstract register make the prose harder to parse. The project's own names—`canvas`, `manifest`, `crux`, `fog`—remain because replacing precise shared vocabulary with longer descriptions makes the sentence less clear, not more plain.

**Conciseness can crowd out structure.** A compact paragraph can still force linear reading. Information-bearing top lines let the reader skim or choose depth, while generic headers add shape without carrying meaning. The concise and skimmable defaults therefore need an explicit rule for their tension.

## Decision

Three rules, replacing the mechanism `20260727` installed for landing while keeping its premise and its one-point-per-turn core.

- **One claim per turn, stated concretely.** Cut the second and third proof of a claim; never cut what the claim says. Where a concrete statement and an abstract summary are close in length, the concrete one wins — abstraction is not a saving.
- **Plain words, with the project's names kept.** Drop invented compounds and abstract register. Keep the vocabulary the project uses for itself. Reach for the short familiar word before the plain-but-longer description.
- **Shape C.** Each part is a bold top line that carries the information, with optional detail beneath, so skimming only the bold lines loses nothing. No generic section headers. The ask stays alone on the last line, in prose, carrying its recommended answer.

And the tension itself is encoded, not just the rules: concise-by-default and the anchored shape pull against each other, and conciseness must not be read as licence to drop structure.

This **supersedes** `20260727-figure-out-adopts-a-default-turn-shape` on the landing mechanism. Its premise stands and is inherited — landing ranks with rigor, one point per turn, the ask alone at the end, and the guardrail that the load comes off how a turn reads and never off what was investigated.

## Alternatives Considered

- **Firm or re-word the existing directive again**: Rejected because the existing wording does not name whether to cut claims, proofs, or claim substance.
- **A word or length budget**: Rejected, consistent with `20260722`, `20260726`, and `20260727`, because a shorter abstract sentence can carry less meaning without lowering reading effort.
- **Generic section headers per part** (Problem / Meaning / Call): Rejected because the headers carry no information and put furniture between the reader and the point.
- **Record it as a Taste entry rather than changing the skill**: Rejected on the same grounds as `20260727`: this is a property of figure-out's output, not a local steering preference, and a Taste entry would leave the shipped skill unchanged.
- **Bundle this with the canvas work**: Rejected — the rules were derived by probing the reader on prose alone and hold whether or not a canvas exists. Keeping them separable means the cheaper half can ship first.

## Consequences

### Positive
- The rule names the axis that four prior ADRs missed: a turn gets shorter by carrying fewer claims, not by making each claim vaguer.
- Shape C makes depth the reader's choice at part granularity rather than turn granularity.
- Encoding the concise-versus-structure tension makes the observed drift diagnosable instead of recurring silently.

### Negative
- A named shape can invite padding. If turns read as padded to fill it, the shape itself is the suspect and this should be reopened rather than firmed.
- Naming a concrete shape reintroduces something a model can pattern-copy, which `20260722` warned about and `20260727` accepted deliberately. The trade is unchanged.
- Validation coverage is narrow. The rule should be reopened if it lowers load for one reading style while adding padding for others.

## Source
- Origin: figure-out investigation of turn load and session-state visibility (2026-08-03).
- Supersedes 20260727-figure-out-adopts-a-default-turn-shape
- Related: 20260722-figure-out-firms-low-cognitive-load-directive, 20260726-figure-out-narrows-presentation-no-trim-clause, 20260803-figure-out-gains-an-optional-canvas
