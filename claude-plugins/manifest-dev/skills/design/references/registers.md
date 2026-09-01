# Registers beyond the web page

The register layer for every genre past the five web/app registers in `SKILL.md`: what each genre must do to achieve its purpose, where generated output fails it, and the behavior probe that verifies it.

## The cross-genre taxonomy

Purpose picks the metric; the metric picks the design; decoration is what survives when you forget the metric.

| Genre | Job | Design center | Success metric | Failure smell |
|---|---|---|---|---|
| Landing page | Persuade → one action | Message clarity in the visitor's vocabulary; anxiety removed at the call to action | Conversion on the one goal | Beautiful hero, vague promise; three equal calls to action |
| Form / checkout | Enable a transaction | Fewest *considered* fields; forgiving inputs; validate late, reward early | Completion and error-recovery rate | Looks clean, punishes typing; an error wipes input |
| Dashboard | Monitor and decide | The 3–5 decisions it serves; deviation visible at a glance | Time to detect the deviant number | Wall of tiles, everything equally loud |
| Report / memo | Persuade a decision-maker | Answer first; evidence beneath; stable page references | Decision made from page 1 | Conclusion on page 6; no page numbers |
| Talk deck | Persuade or teach a room | One assertion per slide, visual evidence, legible in a 3-second glance | Audience can restate the argument | Slides used as speaker notes; 40-bullet slides |
| Slidedoc (reading deck) | Inform without a presenter | 50–150 words per page, full sentences, reading hierarchy | Reader acts on it alone | The projected/emailed hybrid that serves neither |
| Infographic | One takeaway spreads | A title that states the finding; one governing metaphor; plain data marks | Takeaway recalled correctly | Icon soup; ten facts, no message |
| Data story | Walk a reader through evidence | Author-driven sequence; everything load-bearing always visible | Story lands without interaction | Load-bearing tooltips; exploration instead of narrative |
| Poster / one-pager | Inform at a glance | One plain-language finding legible at distance; three-layer read | Message received in 3 seconds at 3 meters | Paragraphs on a poster |
| Explainer / explorable | Build a mental model | Worked example; parts before mechanism; the static state carries the story | Reader predicts the system's behavior | Sliders that demonstrate nothing; content behind hover |
| Game / toy | Delight → re-engagement | Input answered under 100ms; rich feedback on a working core; teach by doing | Unprompted second session | One spectacle, identical the tenth time |

## Genre rules and probes

### Presentations

The genre split is the whole game: a projected talk deck (~10–40 words per slide), a standalone reading deck (50–150), and a dense leave-behind carry different word budgets, and the hybrid that tries to be both is the canonical failure. The strongest generation rule: **outline first as full-sentence assertions, one per slide, and refuse to lay out a slide whose claim-sentence cannot be written.** A sentence headline stating the slide's claim plus visual evidence beats a topic phrase plus bullets. Never mirror the narration as on-screen prose — spoken and identical written words compete.

Generated decks reproduce documented bad practice — evenly-weighted bullets, topic headlines, stock imagery in the evidence slot, genre blindness. *Probe:* read only the headlines, in order; they must state the whole argument.

### Infographics, data stories, posters

Name what the reader must be able to *do*, then hold the order truthful → functional → beautiful. Pipeline: one-sentence big idea → simple familiar chart forms → declutter → gray everything plus one accent → annotate the takeaway. **Keep data marks plain and honest; spend richness on the frame** — subject imagery, one governing metaphor, and above all the title: titles are the most-looked-at element and determine what is recalled, so the title states the finding, with a verb and a direction. Pictogram-style encodings are fine; unrelated decoration measurably distracts. Nothing load-bearing lives behind hover — most readers never touch tooltips. The artifact travels alone: finding, source, and data date answerable from the artifact itself.

Generated failures: icon soup, unmoored numbers, decoration-first ordering, topic titles, emphasis everywhere, text rasterized inside images. Hard gates: every number traces to a supplied source or does not render; all text typeset in the layout layer (HTML/SVG), never inside a generated image; one accent, enforced. *Probe:* cover everything but the title — does it state the finding? Ask what the reader would repeat to a colleague.

### Conversion surfaces and forms

A landing page is an argument: motivation and value-proposition clarity dominate conversion; polish is a minor term. The first screenful gets ~57% of viewing time — its job is clarity plus a reason to scroll. Treat every "best practice" as a hypothesis: moving the call to action *down* has won on complex offers; shorter forms have lost when they cut a clarifying field. Two near-universal negatives: auto-rotating carousels, and links or buttons that do not look clickable.

Forms are the settled genre: cut fields that need justification (most checkouts can cut 20–60%, but never a field that builds clarity or trust); single column; labels above fields; a placeholder is never a label; validate on leaving the field, not on every keystroke — and never eagerly mark half-typed input wrong; errors adjacent with input preserved; guest checkout mandatory; total cost early (late-revealed cost is the top abandonment reason).

Generated forms ship placeholder-as-label, eager validation, errors that clear input, and multi-column field grids — each a tested conversion killer, none visible in a screenshot. *Probe:* a generated form is judged by its worst error path; submit it wrong, twice, and watch what survives.

### Games and playful interactives

Feel is real-time control: input answered under 100ms, and polish that sells the interaction. Rich feedback on every action ("juice") is **additive on a working core** — it cannot rescue a mechanic that does not read. Build the boring working loop first, add feedback in a second pass, gate all motion behind `prefers-reduced-motion`. Onboard by doing: a safe first room, one mechanic at a time, instruction inside the world — never a text-wall tutorial. Feedback must never block input or obscure state.

Generated failures: juicing before the core works, the same confetti on every event, animation that blocks input, no reduced-motion path. *Probe:* remove the feedback layer in your head — is a game still there? Is the tenth repetition still pleasant?

### Print-shaped documents and email

Fixed layout earns its place only when the artifact will be printed, needs stable page references, or *is* its layout (poster, certificate); everything else reflows. Structure outranks typography: **the answer first, about three grouped reasons, evidence beneath** — a report whose conclusion arrives on page 6 has an ordering defect, not a length problem. Typography levers: 10–12pt print body, line-height 120–145%, 45–90 characters per line — line length sets the margins. Email is its own constraint set: ~600px single column, button styles that survive client rewriting, colors that survive forced dark-mode inversion.

Generated documents write background → analysis → conclusion, the inverse of what a decision-maker needs; fix ordering first. *Probe:* read page 1 alone — can the decision be made from it?

### Explorables

Animation per se teaches nothing once information is equal, and most readers never interact. What survives: reader-controlled **pacing** (advance-on-click beats autoplay) and **guided one-variable sweeps** with instant feedback. Prefer small multiples over animation unless motion is the content. **The zero-interaction state must carry the whole story**; interaction is pacing and guided sweeps, never a hiding place.

Generated explorables over-produce decorative interactivity and hide load-bearing content in tabs, accordions, and tooltips *because* it looks sophisticated. *Probe:* print it. Does the story survive on paper?

## The feeling budget

Felt quality runs on two independent axes: the pragmatic axis is the floors; the hedonic axis — novelty, identity — raises attractiveness once the floors hold and never buys back a broken basic.

- **Spectacle-positive surfaces:** marketing and launch pages, portfolios, campaign pieces, brand homepages for expert audiences. The visitor evaluates *the maker*, grants seconds, and expert audiences tolerate a higher novelty dose.
- **Spectacle-negative surfaces:** tools, dashboards, forms, docs, checkout — anything visited repeatedly or mid-task. Repetition converts any surprise into pure latency, and control-stealing effects (scroll hijacking, forced reveals) read as bugs.
- **Middle band:** product landing pages for lay audiences — keep the first frame simple and recognizable, with at most one signature move.

Even where spectacle is licensed, sequencing governs: **the first painted frame stays fluent** — a recognizable skeleton for the category, complexity erring simple (overshooting complexity is punished about three times harder than undershooting) — and novelty is what the second look finds. Deviate from the genre's convention on one or two salient dimensions while the category stays recognizable within one second; every deliberate strangeness needs a designed resolution within seconds. Never gate meaningful pixels behind a loader or an orchestrated reveal: appeal is judged in well under a second. And never imitate a famous signature look — by the time it is famous enough to copy, its novelty is spent and its association is someone else's.

Craft rules for delight moments once a register licenses them — endings, celebration, personality — are in `craft.md` (emotion section).

## Editorial machinery

Only for editorial treatments — utilitarian pages skip all of it:

1. **Philosophy, then expression.** Name a 1–2-word direction drawn from the subject's world, write two or three sentences of the aesthetic worldview, then build it. Derivation grounds distinctiveness; skipping to "make it beautiful" samples the monoculture.
2. **One signature element; everything else quiet.** Spend the boldness in one place. Before coding, privately name the layout this category would default to, then compare two materially different compositions — change topology, density, and evidence placement, not merely palette.
3. **The non-transplant test.** The signature move must belong to its material: if it could be transplanted unchanged onto an unrelated artifact, it is decoration, not identity.
4. **Refine what exists; don't add.** The refinement pass sharpens the chosen direction — it never introduces a second one.

One honest bound: this machinery improves a single artifact's fit. It does not make your *body of output* diverse — run-to-run variety requires state outside the session (a project memory of past directions, real subject data, the user's choice), so where a portfolio must vary, ask for or record that state rather than trusting the procedure.

## The ten rules under every genre

1. Declare the purpose — comprehension, retention, persuasion, or action — and apply its column; they conflict.
2. Design for the partial read: title + headings + bold phrases + figure titles must carry the whole argument alone.
3. Verdict first, key claim also last; nothing load-bearing buried mid-list or mid-document.
4. Every element earns its place; cut decoration and interesting-but-irrelevant asides.
5. Labels in the figure, explanation beside it, never "see above".
6. Say it once, in the best medium — prose or figure or caption, not all three.
7. One visual channel for the one thing that must pop; comparisons on a common aligned scale, where the eye reads differences precisely.
8. Parts before mechanism, worked example before exercise, chunk when more than ~4 things interact.
9. Calibrate to reader expertise — for experts, strip the scaffolding the other rules add.
10. The static state tells the story; interaction is pacing and guided sweeps, never a hiding place.
