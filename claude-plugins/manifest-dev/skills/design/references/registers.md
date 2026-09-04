# Registers beyond the web page

Guidance for established visual genres; unfamiliar media and lifecycle conditions route through `experience.md`. These are starting methods, not exhaustive genre coverage or universal numerical requirements: what each genre must do to achieve its purpose, where generated output fails it, and the behavior probe that verifies it.

## The cross-genre taxonomy

Purpose picks the metric and directs the creative ambition. Each genre expresses it through the experience its audience needs.

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
| Explainer / explorable | Build a mental model | Useful initial state; interaction exposes the mechanism where appropriate | Reader predicts the system's behavior | Sliders that demonstrate nothing; content behind hover |
| Game / toy | Delight → re-engagement | Input answered under 100ms; rich feedback on a working core; teach by doing | Unprompted second session | One spectacle, identical the tenth time |

## Genre rules and probes

### Presentations

The genre split is the whole game: a projected talk deck (~10–40 words per slide), a standalone reading deck (50–150), and a dense leave-behind carry different word budgets, and the hybrid that tries to be both is the canonical failure. The strongest generation rule: **outline first as full-sentence assertions, for argument-bearing content slides; agenda, title, transition and activity slides follow their own jobs.** A sentence headline stating the slide's claim plus visual evidence beats a topic phrase plus bullets. Avoid needless competing duplication; retain captions, labels and complementary explanations required by the audience and delivery mode.

Generated decks reproduce documented bad practice — evenly-weighted bullets, topic headlines, stock imagery in the evidence slot, genre blindness. *Probe:* read only the headlines, in order; they must state the whole argument.

### Infographics, data stories, posters

Name what the reader must be able to *do*, then hold the order truthful → functional → beautiful. Pipeline: one-sentence big idea → simple familiar chart forms → declutter → gray everything plus one accent → annotate the takeaway. **Keep data marks plain and honest; spend richness on the frame** — subject imagery, one governing metaphor, and above all the title: for an author-driven data story, use a finding title with a verb and a direction. Pictogram-style encodings are fine; check whether decoration competes with the task. Place essential findings where the intended reader encounters them; hover cannot be the only access path. The artifact travels alone: finding, source, and data date answerable from the artifact itself.

Generated failures: icon soup, unmoored numbers, decoration-first ordering, topic titles, emphasis everywhere, text rasterized inside images. Hard gates: every number traces to a supplied source or does not render; critical text typeset in the medium’s controllable layout layer with equivalent access; color roles appropriate to the data and creative direction. *Probe:* cover everything but the title — does it state the finding? Ask what the reader would repeat to a colleague.

### Conversion surfaces and forms

A landing page communicates an offer and helps the visitor make an informed choice. Test clarity, credibility, visual expression and the resulting action in context. Treat placement, field count and decorative choices as hypotheses, not guaranteed conversion improvements.

Forms need justified fields and forgiving recovery. As starting points: single column; labels above fields; a placeholder is never a label; validate on leaving the field, not on every keystroke — and never eagerly mark half-typed input wrong; errors adjacent with input preserved; guest checkout where an account is not essential; total cost early (late-revealed cost is the top abandonment reason).

Generated forms ship placeholder-as-label, eager validation, errors that clear input, and multi-column field grids — candidate problems whose effects depend on context; error behavior requires interaction. *Probe:* a generated form is judged by its worst error path; submit it wrong, twice, and watch what survives.

### Games and playful interactives

Feel is real-time control: input answered under 100ms, and polish that sells the interaction. Rich feedback on every action ("juice") is **additive on a working core** — it cannot rescue a mechanic that does not read. Build the boring working loop first, add feedback in a second pass, preserve essential feedback while supporting reduced motion. Onboard by doing: a safe first room, one mechanic at a time, instruction inside the world — never a text-wall tutorial. Feedback must never block input or obscure state.

Generated failures: juicing before the core works, the same confetti on every event, animation that blocks input, no reduced-motion path. *Probe:* remove the feedback layer in your head — is a game still there? Is the tenth repetition still pleasant?

### Print-shaped documents and email

Fixed layout earns its place only when the artifact will be printed, needs stable page references, or *is* its layout (poster, certificate); everything else reflows. Structure outranks typography: **the answer first, about three grouped reasons, evidence beneath** — a report whose conclusion arrives on page 6 has an ordering defect, not a length problem. Typography levers: 10–12pt print body, line-height 120–145%, 45–90 characters per line — line length sets the margins. Email is its own constraint set: ~600px single column, button styles that survive client rewriting, colors that survive forced dark-mode inversion.

Generated documents write background → analysis → conclusion, the inverse of what a decision-maker needs; fix ordering first. *Probe:* read page 1 alone — can the decision be made from it?

### Explorables

Use interaction when it carries the learning or exploration task. Provide clear orientation and a useful initial state; avoid hover-only essential facts. Reader pacing and guided sweeps can help; a simulation may require interaction to reveal its behavior. Provide appropriate equivalent access. *Probe:* can the person predict, change and explain the system, including through the supported alternative?

A decorative slider that changes no meaningful relationship is a defect; purposeful interaction is not. A print view can check the narrative fallback, but cannot verify an interactive task.

## Feeling and use context

Choose the emotional effect from the purpose and audience. A launch page may earn attention through an expressive composition; a serious report through authoritative typography and a revealing figure; a daily tool through a beautiful, immediate view of the work. Each needs a deliberate visual identity within the user's requirements and existing design system.

Keep the first frame readable and usable. On repeated-use surfaces, let visual character come from the composition and craft; animation must give useful feedback without delaying the task. On narrative surfaces, story and surprise can carry the central idea, with all load-bearing content visible without interaction. Never gate meaningful pixels behind a loader or an orchestrated reveal.

Refinement strengthens the chosen direction. A different subject may need a different idea; copying a famous look or adding more effects does not establish one. Craft rules for endings, celebration, and personality live in `craft.md` (emotion section).

## The ten rules under every genre

1. Declare the actual outcome and relevant secondary outcomes; common purposes are examples, not exclusive buckets.
2. Support scanning where appropriate with informative headings and summaries; sustained reading may need depth beyond the scan layer.
3. Put the decision-relevant answer early in decision documents; use the sequence the purpose needs elsewhere.
4. Every element earns its place through the purpose or creative direction; cut unrelated effects and asides.
5. Labels in the figure, explanation beside it, never "see above".
6. Avoid needless duplication; retain complementary explanation, labels and accessible equivalents.
7. Make important comparisons clear; redundant text, shape and color can reinforce meaning and access.
8. Provide the concepts and examples the audience needs; externalize memory demands without a fixed visible-item limit.
9. Calibrate to reader expertise — for experts, strip the scaffolding the other rules add.
10. Make entry and orientation understandable; interaction can carry learning, creative and exploratory tasks.
