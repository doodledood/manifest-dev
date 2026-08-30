# ADR: the rendering contract judges the whole turn, not the element

## Status
Superseded by 20260830-rendering-contract-folds-into-figure-out — the contract's home is retired; its whole-turn re-entry principle and set-completeness rule survive as figure-out's folded turn contract

## Area
Prompt architecture

## Context

`chat-surface`'s rendering contract could not detect the failure it existed to prevent, because nothing in it looked at a whole turn.

Six of its eight rules judged one element at a time — whether *this* form beat prose, whether *this* caption added, whether *this* interactive control answered something static could not. Two rules did address a turn as a whole. One was a permission to expand: "a session's deliverable ... gets the fullest treatment the destination offers". The other measured a single layer: "reading only the claim lines and the asks, top to bottom, must tell the session's story". The body between the claim lines was licensed to grow by the first and measured by neither.

A wall of serial prose therefore passed all eight rules with every individual sentence defensible. That is not a hypothetical: a turn written under this contract rendered an eight-item audit as a paragraph and carried six of the eight items, omitting two that had verdicts behind them. Nothing in the output looked incomplete, and the omission was invisible to the reader and to the author.

Two properties of prose produce that, and neither is reachable by a per-element test:

- **Prose runs serially.** A sentence means what it means only while the reader still holds the ones before it, so an interrupted reader pays a restart rather than a glance. A claim line, a table, or a diagram can be entered at any point.
- **Prose has no empty slot.** A set rendered as a sentence can lose a member with nothing looking wrong. A form with one slot per member shows the gap.

The second is the more consequential. It makes this a completeness defect rather than a matter of reading comfort, which puts it in the same class as the evidence discipline elsewhere in these workflows. That discipline is not traded away for convenience.

The per-element rules also had a second weakness: "earns its place" is a justification an author can always construct. A test asking whether a reader can resume the turn is checked against the artifact instead.

Separately, most of the eight did not survive a provenance audit. "Captions must add" and "choose form per point" describe what a capable model already does unprompted. A rule that only restates the model's own default spends context load on every invocation to say nothing.

`20260818-surface-skill-owns-the-rendering-contract` named the earning rule as "the only thing holding that line" against decorative forms, and set its reopening condition as turns beginning to carry a decorative table or diagram apiece. That condition has not been met; the observed failure runs the other way, toward walls of prose. Replacing the rule therefore has to say what now holds the line it held.

## Decision

**Replace the eight per-element rules with one test applied to the whole turn: a reader must be able to leave it and resume without re-reading.**

- The test is two-sided, and both sides are needed. A reader must be able to re-enter the turn, *and* everything in the turn must be something they would need on re-entry. The second half is what now holds `20260818`'s line. An element carrying nothing to return to fails the same test a wall of prose fails, so the guard against decorative forms is preserved rather than dropped.
- **A set is rendered as a set** — several things of one kind get a form with one slot each, so a missing member shows as a gap. This is the completeness half of the test, stated as its own rule because it is the part a reader cannot audit after the fact.
- **Rules survive only on provenance.** A rule stays where it carries a ruling, knowledge outside what a run reading these files already has, or a model default that has actually been observed. Five rules remain: the re-entry test, the ceiling that is its other side, the set-rendering rule carrying its completeness half, the ask set apart with its recommendation, and tool output rendered as meaning. The ask rule stays because burying the question is an observed default, and because `chat-surface` is independently invocable and cannot lean on `figure-out`'s spine to carry it.
- **A mode reference carries only rules that would be meaningless at another destination.** `references/HTML.md` keeps its accessibility floor and its verbatim user messages — there is no viewport in a terminal, and a terminal already shows the user their own words — and loses its bar on interactive elements, which was the per-element pattern specialized to one destination. Setup, wire format, and failure handling are mechanics and are unaffected.

Two rulings from the replaced text are folded into the re-entry rule rather than kept as rules of their own. Bolding that decorates makes the re-entry path untrustworthy. And each point picks its own form: the cut rule "choose form per point, not per turn" was re-derivable in its first half, but its second half carried `20260722`'s ruling against a fixed layout stamped on every turn, and `figure-out` has since delegated form selection here entirely, so nothing else would carry it.

## Alternatives Considered

- **Add a re-entry rule beside the existing eight**: Rejected — it leaves six rules that judge the wrong unit, and leaves the specialized copy of the replaced pattern standing in the mode reference. `20260818`'s implementing commit already made this mistake in the opposite direction, adding rules without removing what they replaced, which is what `tests/test_rendering_contract_single_home.py` was written to catch.
- **Shorten the contract without changing what it measures**: Rejected, and it would contradict `20260722-figure-out-firms-low-cognitive-load-directive`, which ruled the lever is structure rather than brevity and explicitly refused a word-count dial. The contract does come out shorter, but as a consequence of cutting rules that failed the provenance audit — not as the mechanism. What fixes the defect is the change of unit.
- **A rule preferring diagrams and tables over prose**: Rejected — that is a fixed-layout lever of the kind `20260722` refused, and it is unnecessary: the re-entry test recruits a spatial form wherever one helps without mandating one where prose already passes. A paragraph whose first sentence carries its point is re-enterable.
- **Record this as a personal preference in a memory file rather than changing the skill**: Rejected — `figure-out`'s taste-capture reference rules it out directly. The opposite of a re-enterable turn is the skill failing its own stated goal, not a rival preference. Capturing it as taste would also make weighable something that binds.
- **Keep "weight follows information"**: Rejected — it is the permission that licensed the unmeasured body. A compact exchange is trivially re-enterable, so the useful half needs no rule.

## Consequences

### Positive
- The contract can detect the failure it exists to prevent, because it now measures the unit that failure belongs to.
- Presentation gains a completeness argument rather than only a comfort one, which is what makes it non-negotiable under pressure.
- The test is checked against the artifact instead of argued for, so it is harder to satisfy by rationalization than "earns its place" was.
- Five rules instead of eight, with each survivor traceable to a ruling, out-of-reach knowledge, or an observed default.

### Negative
- "Can a reader re-enter this" is still a model's own judgment about its own output, so it remains partly self-graded. It is more checkable than its predecessor, not fully external. If turns start passing it while still reading as walls, this needs an external check rather than firmer wording.
- Cutting to five rests on a provenance audit of what current models do unprompted. That premise ages: a rule cut as redundant today would have to be restored if the default it assumed stops holding.
- Whether the contract's reduced length contributes to the effect independently of the changed test was not separated by the evidence behind this record. If length turns out to matter on its own, the remaining five are a further candidate for cutting.

## Source
- Session: figure-out investigation of why a short ad-hoc presentation instruction outperformed the standing contract (2026-08-21), with the contract's defect established by rendering a real in-session turn under it and recounting what it carried.
- Related: 20260818-surface-skill-owns-the-rendering-contract — narrows its earning rule, which this record replaces.
- Related: 20260722-figure-out-firms-low-cognitive-load-directive
- Related: 20260817-prompt-lines-earn-their-place-by-provenance
- Related: 20260818-chat-surface-replaces-the-crux-map-canvas
