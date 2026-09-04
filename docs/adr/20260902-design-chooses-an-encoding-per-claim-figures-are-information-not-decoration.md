# ADR: The design skill chooses an encoding per claim; figures are information graphics, never decoration

## Status
Accepted — amended by 20260905-design-obligations-follow-the-medium-and-task: narrows static-on-arrival to orientation and necessary controls where interaction or pacing is judged; equivalent accessible representations remain available.

## Area
Design skills

## Context

Run standalone on a finished research read, the `design` skill built a 2,500-word single-column decision memo with six hairline tables and no figure. Two-lane architectures, three memory systems flowing into one repository, and a phased setup all arrived as paragraphs and definition lists. The output obeyed every rule the skill had. The document register prescribes "decoration: nearly none", the treatment defaults to utilitarian for documents, and the feeling budget marks documents spectacle-negative. The register was right; the encoding was wrong, and nothing in the skill had asked the question.

Three things combined. The skill's six decisions cover purpose, task model, register, tokens, floors, and verification; none chooses, per claim, whether prose, a table, or a figure carries it. The only words the skill had for a diagram on a document were "decoration" in the register table and "no generated diagrams" in the imagery rule — the latter means image-model output, but a cold reader takes both as a ban. And the three rules that would have pulled toward figures ("say it once, in the best medium", "one visual channel for the one thing that must pop", "labels in the figure") sit in `references/registers.md` under the rules for every genre, which the loading table loaded only for genres beyond the five web registers; a report never saw them. Verification could not catch it either: the document probe read headings and bold lines alone, and the machine check had no figure check.

Two skills shipped by a host harness carry the missing piece: one states when a picture earns its place — a cold reader would otherwise assemble a mechanism from prose; if a sentence says it faster, write the sentence — and how to draw it as inline SVG; the other carries fundamentals the skill lacked (honor an existing design system, structure is information, show the page at rest, charts to one scale). Neither is available where the skill runs standalone, and a shipped skill cannot depend on a host loading them.

## Decision

Four coupled choices:

1. **The encoding choice is a fifth line of the task model, not a seventh decision.** Decision 1's written block gains an *Encoding* line: for each claim the reader must take in, whether prose, a table, or a figure carries it, chosen by the cold-reader test. Placing it in the block means it is written before layout, traced to region by region, revised on evidence like the other lines, and runs in full at prototype weight — all without touching the prototype-weight wording or the decision count the earlier records describe. A claim assigned to a figure that arrives as a paragraph is the same defect as a region tracing to nothing.

2. **A figure replaces the prose it encodes.** The line states it and `references/figures.md` repeats it as a check: once a claim is drawn, the paragraph that assembled it in words goes. Without this, adding figures makes documents longer, and the wall-of-text defect survives the fix.

3. **Ornament and information graphics are told apart wherever the skill restricts visuals.** The register table's Decoration column budgets borders, shadows, backgrounds, and mood imagery, and never counts a figure or table the encoding line placed; the imagery rule says plainly it governs image-model output and that a hand-drawn inline SVG figure is an information graphic governed by `figures.md`. The bulk — what a figure depicts, how options are compared, the SVG mechanics that keep a figure legible in both themes, charts to one scale — lives in the new reference, loaded when the encoding line names any figure or chart, with the trigger in the loading table and not in the file. The same table now routes a document or report build to `registers.md` for its genre row and the rules under every genre.

4. **Verification gains the check the class needs, and the verification loop stays.** Decision 5's document probe covers the prose and asks whether the figures and tables carry the mechanism the encoding line assigned them; `design-check.mjs` reports a page that carries structural content (sequences, definition lists, comparison or flow vocabulary in its headings) with no figure at all, with the exposing memo and a figure-bearing page as its two fixtures; `review-design` judges encoding fit inside task fit, grading a structural claim left to prose alone as it grades a broken co-visibility pair. The host skill's "write, look once, publish, no test loop" stance was read and not adopted: the skill's own second failure mode is that stated principles do not survive into output, external evidence is the ADR-backed counter, and prototype weight already skips verification where cost dominates.

The transferable fundamentals land beside the rules they extend, in the same register and under the same distillation boundary as the original research: honoring an existing system before the token block, the page at rest and structure-is-information as floors, repeated things as one object and one owner per property as craft.

## Alternatives Considered

- **A separate seventh decision between task model and register**: makes the step visible by number, as the task-model record argued for its own addition — not chosen because the encoding choice is a property of the same model the layout traces to, so it belongs in the block that carries the trace rule; a new decision would also renumber what two records and the prototype-weight section already count, for a step the block absorbs in one line.
- **Move the ten cross-genre rules inline into `SKILL.md`**: guarantees every build sees them — not chosen because the always-loaded file would grow by a section most invocations use a fraction of; extending the loading trigger to cover documents reaches the same rules at a cost paid only by the builds that need them.
- **Adopt the no-test-loop stance along with the rest**: cheaper per build — not chosen for the reasons under choice 4.
- **Depend on the host's diagramming skill where it exists**: zero new text — not chosen because a shipped skill stands alone; the exposing run had no such skill loaded, which is how the failure was found.

## Consequences

### Positive
- A document build now has a rule that asks, per claim, whether a picture is owed, and a rule that removes the prose the picture replaces.
- Figures on a document are no longer read as decoration by the register that governs them.
- The class has a counter at build time (the line, the reference), at check time (the script), and at gate time (`review-design`), instead of only in the author's reaction.
- The report genre's own rules load for reports.

### Negative
- Every task model now carries a line whose value is lowest on artifacts with no structural claims, where it collapses to "prose" and is written anyway.
- The script's figure check is a heuristic over markup signals; a prose-only page over a genuinely structural subject that uses none of the counted signals passes it, and a page with one figure passes regardless of what the figure shows — the judgment probe is what catches those.
- The effectiveness of the added instruction rests on one behavioral probe on the exposing brief, the same standing gap the earlier design records name; the deferred blind pairwise eval is what would close it.

## Source
- Session: just-figure-out → just-define → just-do run, 2026-09-02, from the owner's report of a wall-of-text decision memo built by the skill standalone.
- Related: 20260901-design-derives-structure-from-a-written-task-model (extended: the task model gains its fifth line), 20260901-design-skill-pair-distills-research-eval-deferred (extended: the distillation boundary now also covers material drawn from host-shipped skills), 20260901-deliberation-renders-run-the-design-skill-at-prototype-weight (extended: the legibility floors held on the judged surface now include the page being at rest at load), 20260703-progressive-disclosure-triggers-live-in-loading-layer (why the trigger sits in the loading table and the bulk in a reference).
