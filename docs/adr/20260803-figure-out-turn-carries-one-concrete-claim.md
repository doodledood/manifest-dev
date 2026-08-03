# ADR: a figure-out turn carries one concrete claim, in plain words, in a skimmable shape

## Status
Accepted

## Context

figure-out's landing half has now been revised five times in six weeks. `20260722-figure-out-firms-low-cognitive-load-directive` firmed an abstract directive's modality; `20260726-figure-out-narrows-presentation-no-trim-clause` narrowed its guardrail; `20260727-figure-out-adopts-a-default-turn-shape` replaced the modality entirely with one point per turn, concise-by-default prose, and the ask alone on the last line.

The failure recurred under that wording. In the session that produced this ADR — running on the post-`20260727` skill — the reader called a turn *"nice but I would want less details unless asked."* Rather than argue, the same turn was rewritten four times against live reaction, which produced three findings the previous four ADRs did not have.

**The dial is claims per turn, not words.** The offending turn carried four separate proofs of one claim. Cutting them was right. But the next draft cut the wrong thing — the substance of the claim — and *"it failed twice with a real reviewer"* turned out both vaguer and barely shorter than the version that lands (*the reviewer said "way too much text at once", twice, even after collapsing more of it*). The reader's response to that draft was that important points had been dropped. **Abstraction was posing as brevity.** No prior ADR names this: `20260722` attacked modality, `20260726` the guardrail, `20260727` structure and length. All three treated length as the axis and none priced the cost of compressing a claim into an abstraction.

**Plain language has a floor.** The reader's next objection was that the language was *"too jargony."* The offenders were invented compounds — "interview-time glance-check", "extract rather than move", "carry the conversation" — not the project's own names. Plainifying `canvas`, `manifest`, `crux`, `fog` would make sentences vaguer, not clearer. And the first attempt at plainness padded: `document` was replaced by *"a page of text with bits you click open"* — plainer-sounding, five words, worse.

**Conciseness had crowded out structure.** After the conciseness rules landed, the same reader asked for formatting back: *"with some structure i can actively choose to skim or skip sections… while paragraphs require me to read the full thing."* The skill already asks for this — *"anchor whatever carries it… with a bold label or short numbered split per part… Skimmable beats compact"* — and the agent had drifted off it while chasing the conciseness note. The two defaults pull against each other, and under pressure conciseness wins and skimmability loses.

Three candidate turn shapes were then rendered over identical content and reacted to: bold labels with prose inside; generic section headers; and top lines that carry the information with detail beneath. The third won, with the reason stated: generic headers say nothing — *"The problem"* is a label, not information.

## Decision

Three rules, replacing the mechanism `20260727` installed for landing while keeping its premise and its one-point-per-turn core.

- **One claim per turn, stated concretely.** Cut the second and third proof of a claim; never cut what the claim says. Where a concrete statement and an abstract summary are close in length, the concrete one wins — abstraction is not a saving.
- **Plain words, with the project's names kept.** Drop invented compounds and abstract register. Keep the vocabulary the project uses for itself. Reach for the short familiar word before the plain-but-longer description.
- **Shape C.** Each part is a bold top line that carries the information, with optional detail beneath, so skimming only the bold lines loses nothing. No generic section headers. The ask stays alone on the last line, in prose, carrying its recommended answer.

And the tension itself is encoded, not just the rules: concise-by-default and the anchored shape pull against each other, and conciseness must not be read as licence to drop structure.

This **supersedes** `20260727-figure-out-adopts-a-default-turn-shape` on the landing mechanism. Its premise stands and is inherited — landing ranks with rigor, one point per turn, the ask alone at the end, and the guardrail that the load comes off how a turn reads and never off what was investigated.

## Alternatives Considered

- **Firm or re-word the existing directive again**: Rejected — this would be the fifth iteration in six weeks, and the fourth failed live against the reader it was written for two days after landing.
- **A word or length budget**: Rejected, consistent with `20260722`, `20260726` and `20260727` — and now with direct evidence, since the shortest draft in this session was the one the reader rejected for dropping the point.
- **Generic section headers per part** (Problem / Meaning / Call): Rejected on reader reaction after being rendered concretely — the headers carried no information and put furniture between the reader and the point.
- **Record it as a Taste entry rather than changing the skill**: Rejected on the same grounds `20260727` rejected it — this is how figure-out should read for every reader, not how one user steers, and a Taste entry would leave the shipped skill unchanged for everyone else.
- **Bundle this with the canvas work**: Rejected — the rules were derived by probing the reader on prose alone and hold whether or not a canvas exists. Keeping them separable means the cheaper half can ship first.

## Consequences

### Positive
- The rule names the axis that four prior ADRs missed: a turn gets shorter by carrying fewer claims, not by making each claim vaguer.
- Shape C makes depth the reader's choice at part granularity rather than turn granularity, which is what the reader actually asked for twice.
- Encoding the concise-versus-structure tension makes the observed drift diagnosable instead of recurring silently.

### Negative
- A fifth revision of the same paragraph. If the sixth failure looks like "turns read as padded to fill the shape," the shape itself is the suspect and this should be reopened rather than firmed.
- Naming a concrete shape reintroduces something a model can pattern-copy, which `20260722` warned about and `20260727` accepted deliberately. The trade is unchanged.
- Evidence is one reader across one session, though gathered by direct probing with four rendered alternatives rather than by argument.

## Source
- Session: figure-out session on a canvas for figure-out (2026-08-03); the prose rules were derived mid-session by rewriting one real turn four times against live reaction, and ratified by the reader.
- Supersedes 20260727-figure-out-adopts-a-default-turn-shape
- Related: 20260722-figure-out-firms-low-cognitive-load-directive, 20260726-figure-out-narrows-presentation-no-trim-clause, 20260803-figure-out-gains-an-optional-canvas
