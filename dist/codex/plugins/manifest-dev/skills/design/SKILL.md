---
name: design
description: 'Design and build digital artifacts whose audience can understand, engage with and use them: interfaces, documents, presentations, charts, media and interactive experiences. Use for creating or restyling artifacts, including disposable prototypes. Combine art direction, information design and interaction design, then verify the delivered experience. Finished-artifact evaluation belongs to review-design.'
user-invocable: true
---

# Design the audience's experience

Make what matters understandable, the relationships coherent, and engagement compelling in a way suited to the purpose. Use art direction, information design and interaction design together. Visual work should be striking and memorable; neither a usable layout nor an impressive first frame alone finishes the design.

## Understand the experience before choosing its form

Use the brief, existing artifact and available evidence. Briefly record who this is for, what they need to understand or do, the intended feeling, and the delivery medium. Name the path they take or the loop they repeat, the context they need together, and how frequency and consequential moments affect that work. Keep this task model beside the artifact so the arrangement can be checked against it; revise it when evidence changes the work.

Information needed together should be available without avoidable memory work. Preserve those relationships across small screens and nonvisual alternatives. A once-read presentation and a tool used hundreds of times a day need different pacing, density and interaction.

Respect the user's requirements, then the existing design system, then this skill's defaults. When missing information would change the design, ask the smallest question that distinguishes the plausible directions; use concrete references or a comparison for a visual choice. Avoid a default interview. In autonomous work, state permitted assumptions and their consequences. Distinguish the creator's preference from evidence about the audience: apparent fluency, activity or approval does not establish understanding.

## Give the experience a coherent idea

Choose a creative direction specific to the subject and the audience's encounter with it. Decide what carries that idea—typography, imagery, data, material, interaction, motion—and compose them together. Attention may need a focal point, a comparison field or an unfolding sequence. Let the task decide; different regions can have different jobs within one coherent whole.

Choose the representation—prose, table, image, diagram, chart or interaction—that makes the important relationships perceptible. Use copy for meaning the audience still needs, rather than repeatedly explaining what the design already says. Retain labels, evidence, uncertainty and complementary explanations that support understanding and access. Judge the whole composition: individually reasonable panels, summaries and captions can collectively make everything equally loud.

Motion earns its place through what time contributes: feedback, continuity, transformation, rhythm, atmosphere or play. Compare it with what a still view or simultaneous comparison offers. Keep essential orientation and controls available, and preserve meaning and agency when motion is reduced. Judge the sequence and repeated use, not only its strongest frame.

## Build one system, preserve the work

Use the project's components and tokens where they exist. Otherwise declare a compact system appropriate to the medium: visual roles for color, typography, spacing and shape, or conventions for voice, timing and feedback. Carry the creative direction through that system. Use its values and components consistently, checking for accidental drift during refinement.

Applicable functional and accessibility requirements bind; style examples are defaults, not laws. Preserve truthful information, meaningful state and recovery, and equivalent access. Decorative or generated material must not masquerade as evidence. Load the relevant references below before making the choices they govern.

## Verify the encounter and the use

Inspect the artifact in its intended browser, native host, player or device. Exercise the actual path, including consequential state changes and recovery where they exist; repeat interactions whose feel changes with repetition. Check composition and reading hierarchy alongside the behavior: what becomes clear, what competes for attention, where the person must hunt or remember, and whether the creative direction survives active use and endings.

Use established project checks. For HTML, run `scripts/design-check.mjs <artifact.html>` from this skill's directory as bounded triage: exit zero means it ran, NOTE items need judgment, and SKIPPED items remain unverified. A source selector or automated pass does not establish access, motion quality or audience comprehension. Responsive web starting views are 1440×900 and 390×844; test applicable 320 CSS px reflow, text enlargement, keyboard paths and supported themes. Inspect actual motion and its reduced alternative separately from static captures.

For improvements, compare the incumbent and revision at matched content, state, output size and useful fidelity. Identify whether the weak layer is the concept, hierarchy, craft, behavior or adaptation; preserve successful identity and behavior while changing that layer. Keep the stronger result, including the original where the change loses, and recheck affected paths.

State what was observed, what is a design judgment, and what remains unverified. Source inspection can locate a cause; it cannot clear a missing render or behavior check. Real audience understanding, preference, recall and conversion require evidence beyond the creator's or model's reaction. When a finished-artifact verdict is required, invoke `review-design`; building and evaluating remain separate jobs.

## Prototype weight

A disposable prototype concentrates fidelity on the question being tested. Keep the task model and creative direction, a minimal system, truthful content and legibility; leave incidental regions visibly unfinished. Orientation and necessary controls must be available on arrival. A prototype about interaction or pacing must expose that behavior. The reader's reaction is the test, not a shipping verdict; do not spend a full verification cycle polishing an artifact that will be discarded.

Candidate sets vary the unresolved choice, with incidental differences controlled enough to interpret the reaction. Include an incumbent at comparable fidelity where one exists. Preference can select a direction; it does not establish task performance.

## What loads

Load the applicable guidance, not the whole library. These references are shared with `review-design`.

| When the work involves | Read |
|---|---|
| Web interfaces, or web access and interaction requirements | `references/floors.md` — measurements, exceptions and behavioral checks |
| Choosing a representation for structural or quantitative information; charts, diagrams or other information graphics | `references/figures.md` — faithful encoding and equivalent access |
| Stateful or shared work, multi-page journeys, presentations, non-web delivery, temporal, conversational, AI, spatial or unfamiliar media | `references/experience.md` — continuity, consequences and actual-medium verification |
