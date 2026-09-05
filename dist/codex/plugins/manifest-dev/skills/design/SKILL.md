---
name: design
description: 'Design and build digital artifacts: interfaces, documents, workbooks, presentations, charts, media, games, conversational tools and spatial experiences. Model the user’s work and delivery context, choose a coherent creative direction, preserve functional and accessibility requirements, and verify the delivered experience. Visual artifacts should be striking and memorable within their purpose and existing design system. Use for creating or restyling artifacts, including disposable prototypes at reduced fidelity. Finished-artifact evaluation belongs to review-design.'
user-invocable: true
---

# design — user-visible artifacts that work and are worth looking at

Create artifacts that excel at their purpose. Visual artifacts should be striking and memorable; a clear, usable layout alone is not finished visual design.

Model the work before choosing its form. Preserve functional behavior while developing a creative direction, and verify the result in its delivered medium. A stated principle is not evidence that the artifact implements it.

So work through six decisions, in order. Each bounds the next; skipping one is where those failures enter.

**Purpose picks the metric, the task model picks the structure, register picks the rules, tokens hold the system, floors guard the layer that collapses, and verification is external evidence per genre — with a strong creative direction derived from the purpose and subject in every genre.**

## Decision 0 — establish the intent

Establish the creator's intent, the audience's intended outcome and experience, and the relevant situation before committing to a design direction. Use the supplied brief, available research and existing artifact; distinguish requirements, observed evidence and assumptions. Identify what prevents the desired result and which constraints or competing priorities could change the design. Preserve explicit creative requirements; predicted audience response remains a hypothesis until observed.

Name what would demonstrate success and what would count as a misleading success. A genre label, more activity or creator approval alone cannot supply the audience outcome. Resolve design-changing uncertainty through the clarification rule below; the brief is sufficient when it supports a defensible direction and a way to judge it, not when every possible question is answered. These are examples, not exclusive categories:

| Purpose | Optimize for | What changes |
|---|---|---|
| Comprehension | Correct understanding | Explanations and representations suited to the actual question; verify interpretation |
| Retention | Successful recall later | Questions before answers, spaced re-exposure — difficulty in the *task*, never in legibility |
| Persuasion | Informed judgment or action | Compelling, credible expression with the evidence and consequences needed to judge the offer |
| Action | Successful, informed completion | Clear next action, necessary choices and recovery |
| Creation, exploration, communication or play | The brief’s actual outcome | Tools and feedback that support the activity; no forced single call to action |

Difficulty belongs in the task, never in the surface: a retention artifact asks the reader to predict before revealing, on a maximally legible page. Hard-to-read styling teaches nothing and costs trust.

## Decision 1 — model the task before any layout

Purpose names what the artifact optimizes for. It does not name what the person at it actually *does*, and the doing is what structure has to follow. Write the model down before any layout — five lines, kept beside the token block and treated the same way:

- **Who** — the person at the artifact, what they know, and relevant access, language, device and input conditions.
- **The loop** — the one sequence they repeat, in verbs: *read the task → judge it → answer three questions → next*. Name the main sequence and any consequential entry, return, recovery or exit path. Frequency shapes efficiency; consequence can make a rare path structurally important.
- **Co-visible** — for each step of the loop, what has to be on screen *at the same time* for that step to happen without the person holding something in their head. This is the line that decides the arrangement: make information needed together available without avoidable memory work. On nonvisual surfaces, preserve equivalent context; on constrained displays, adapt the arrangement without losing the relationship.
- **Rate** — how often the loop runs and how long one pass takes. A loop run three hundred times a day earns keyboard paths and a dense arrangement that a once-a-quarter form must not spend on.
- **Encoding** — choose what carries the information or experience: prose, table, diagram, chart, image, media or interaction. Use a figure to make a relevant structure, pattern or relationship visible; a table for exact values or comparable attributes; prose where language is clearer. Representations can complement each other. Preserve useful labels, explanation and equivalent access. `references/figures.md` governs information graphics; `references/craft.md` covers imagery and motion.

For stateful, shared, multi-page, non-web, temporal, conversational, spatial or unfamiliar artifacts, load `references/experience.md` before settling the model. Name the final delivery format and use its platform guidance; a web preview cannot establish native-file behavior.

The layout traces to this block. Before writing markup, take each region and name the line of the model that put it there; a region tracing to nothing is decoration or a missing model line, and which one it is gets decided on the spot — the same call as a value outside the token system. A claim the encoding line assigned to a figure that arrives as a paragraph is the same defect from the other side. A layout that breaks a co-visibility pair is wrong however well it is made. Revise the model when evidence changes the work; revise the arrangement when it fails a valid model. Regions can also earn their place through the intended visual or emotional experience.

**Clarify what could change the design.** First use the context already available. When purpose, audience, work, priorities or intended expression remain materially ambiguous, ask the smallest question that distinguishes the plausible directions and explain what the answer changes. A complete loop does not settle an unclear goal. For visual ambiguity, concrete references or a small comparison can make the choice inspectable; distinguish the requester's preference from evidence about the audience. Avoid a default interview. In autonomous work, state permitted assumptions and their consequences; unresolved choices belonging to the requester do not become facts. Revisit the brief when new evidence changes it.

## Decision 2 — choose the register and creative direction

A **register** sets the density, typography, and ornament that suit the artifact's use. It shapes how creative ambition is expressed: an everyday tool can impress through composition and information design while keeping repeated actions direct.

First look for what already exists — a project tokens file, a component library, a house style — and hold the precedence: the user's words, then the project's existing system, then this skill's own choices. Develop the direction within those constraints. The web/app starting registers below supply defaults, not universal numerical floors. Task fit, applicable standards, the brief and the existing system govern departures:

| Register | Useful starting treatment | Task priority |
|---|---|---|
| Dashboard / analytics | Structured density, aligned values, meaningful color and regional emphasis | Consequential changes, uncertainty and next investigation discoverable; a rare critical exception can outrank the summary |
| Document / report | Reading hierarchy, deliberate typography, evidence and imagery suited to the subject | Put the decision, answer or unresolved trade-off early; preserve comparable evidence and reading order |
| Tool / app | Regional emphasis within the existing system; controls matched to repeated work | Relevant actions, context and states available; comparison or creation may require several peer actions |
| Landing / marketing | Message-led composition, expressive type and imagery, coherent palette | The offer and relevant next step are understandable; expression supports informed choice |
| Game / playful | Art direction across space, interaction and time | Working feedback and appropriate access; play and expression can be the central experience |

These are task priorities and starting treatments, not limits on visual richness. Information, atmosphere and ornament are judged by their role in the intended experience.

For any other genre — a deck, an infographic, a poster, a data story, a form or checkout, a print-shaped document, an email, an explorable — load `references/registers.md` before proceeding: each has its own job, success metric, and failure smell, and applying a web register to it is the same defect as putting the marketing look on a dashboard.

Two rules that ride with the pick:

- **Hybrid briefs compose; they never average.** Real briefs blend genres (a dashboard with a marketing header). Choose one governing register per *region* by that region's job, plus one page-level treatment read that arbitrates conflicts — never a blend of two registers' values, which produces mush.
- **Commit to a creative direction.** Use the purpose, audience, and task model to choose what will make this artifact compelling and memorable. Choose whether attention needs a focal point, a comparison field or an unfolding sequence, and what carries the idea: type, color, imagery, data, material, interaction or motion. Coordinate those choices; regional emphasis can differ within one system. An elegant decision chart can carry a serious report; a vivid worked example can carry an explainer. Make the direction specific to the subject, then refine it rather than adding competing effects. Make the memorable element part of that idea: a revealing relationship, distinctive composition or satisfying interaction can provide impact while serving use.

Match the emotional effect to the use context. Expressive storytelling may serve a first encounter; repeated work needs visual character that stays enjoyable without delaying actions, hiding information, or competing with the task.

## Decision 3 — declare tokens before implementation

Before implementation, write a compact system block for the actual medium. Where a design system exists, use its values rather than inventing rivals. For visual output, derive components from these applicable choices:

- Named colors as *roles* with usage rules ("accent — highest-emphasis action"), not as a palette of hexes.
- 2–3 type roles named by job (display / body / utility), with the faces, sizes, and the 2–3 weights allowed.
- The spacing values (for example: within-group 8/12, card padding 24, section gap 48–96) — and only those values, everywhere.
- The corner-radius set.

For audio-only or other nonvisual output, declare the applicable voice, timing, turn-taking and feedback conventions instead.

For visual output, carry the creative direction into palette and typefaces: derive them from the subject's own world — its era, material, and temperature — never from a stock "modern" look. Use `references/craft.md` for the domains being developed. When checking an unexamined style default, consult the dated observations in `references/calibration.md`; the actual brief and rendered result govern the choice.

At the end of the build, audit that only token values appear. A value outside the system is either a defect or a missing token — decide which, on the spot.

## Decision 4 — hold the floors

Functional and accessibility requirements bind where applicable. Composition, palette, typography and timing defaults guide a choice; a departure is a defect only when it violates the brief, system or a demonstrated user need. Full web requirements and defaults live in `references/floors.md`; domain craft in `references/craft.md`.

1. **Applicable states and recovery.** Design loading, empty, error and success where they can occur. Preserve input and make consequential commitment and recovery clear; stateful continuity loads from `references/experience.md`.
2. **Contrast against the rendered background.** Apply the relevant text/non-text requirements, levels and exceptions; distinguish measured results from unsupported paint or states.
3. **One spacing rhythm, held by the parent.** Declare the page's spacing values once and reuse exactly those; give every gap one owner — a wrapper sets it, children never add competing margins. Within-group gaps at least one step smaller than between-group.
4. **Alignment supports reading and comparison.** Use coherent start edges for the writing direction; align comparable values with suitable numeric formatting.
5. **Color roles are coherent.** Palette breadth follows the subject, data and creative direction. Preserve state distinctions with more than color alone.
6. **Supported themes are designed.** Inspect actual surface, text and state relationships in each claimed theme; black and saturated color are not defects by themselves.
7. **Typography survives use.** Verify reading at intended sizes, languages, text enlargement and reflow; a fixed character measure or font-size formula is not proof.
8. **Data typography.** Equal-width digits wherever numbers align; consistent decimals per column; "—" for missing, never "0".
9. **Craft consistency.** Use a coherent type, spacing, radius and icon system; allow content growth and inspect actual translated strings.
10. **Access is behavior.** Use suitable native semantics, meaningful names and visible keyboard focus. Check applicable target sizes, reading/focus order, text resizing and alternatives to motion or other inaccessible input/output.
11. **Copy is design material.** Controls say what happens ("Save changes", not "Submit"); errors state what went wrong and what to do; empty states answer "what would be here" and "how do I get it"; front-load the differentiating word in every heading and label.
12. **The entry state is understandable.** Keep essential orientation and necessary controls available on entry. Sequence, prediction and deliberate reveals may carry a narrative or learning task; provide appropriate equivalent access. Demonstration data is plainly labeled; real empty states must remain truthful. Interaction may carry the task in games, simulations and creative tools.
13. **Structure is information.** Numbered markers only on a real sequence; eyebrows, dividers, and section furniture only where they encode something true about the content, never as rhythm.

Functional floors and visual ambition both bind. Repair broken basics first, then finish the creative direction; passing the floors alone is not completion. At prototype weight, apply that ambition only to the surface being judged, as specified below.

## Decision 5 — verify in the artifact's own behavior loop

Inspect the artifact and exercise it. Source inspection locates causes and checks semantics; it does not substitute for rendered or behavioral evidence.

**Use established project checks, then inspect their limits.** For HTML, run `scripts/design-check.mjs <artifact.html>` from this skill’s directory. It is bounded triage: exit zero means execution completed; NOTE items are review candidates and SKIPPED items remain unverified. It does not establish accessibility conformance, focus or reduced-motion behavior, token adherence, or appropriate figure use. Validate candidates before treating them as defects.

**Inspect and compare revisions.** Use the intended browser, native host, player or device. For responsive web work, 1440×900 and 390×844 are useful starting viewports; also test applicable 320 CSS px reflow, text enlargement and supported themes. Inspect composition, typography, information structure, craft and creative direction against the brief. Fix consequential issues and compare with the prior version, keeping the stronger result. Two or three rounds is a starting budget, not a proof of convergence: report remaining defects if it ends. A blur or first-impression check can reveal hierarchy concerns, but neither is a mechanical verdict. If required rendering, playback or interaction is unavailable, report that verification gap; code review cannot clear it.

**Then probe the intended result.** Choose observations from the brief's goals and the uncertainty being tested, including visual or emotional experience where relevant. Genre probes are starting examples, not substitute success criteria. For web/app work, examples include: open the dashboard and identify the consequential change, its impact and freshness, then take the relevant investigation step; read the document's headings and bold lines alone and check they carry the argument, then cover the prose and check that the figures and tables carry the mechanism the encoding line assigned them and that each encoding serves the task with its needed accessible equivalent; walk the tool's primary action through failure and recovery with input preserved; on the landing page, state what is being offered and what to do next from five seconds of looking; play the game's loop twice and check the second run still gives feedback. Probes for every genre beyond these are listed with their registers in `references/registers.md`.

**Improve against the incumbent.** Before editing, identify the weak layer: concept, hierarchy, craft, behavior or adaptation. Re-read the task model, creative direction and system; preserve successful behavior and useful identity while allowing the arrangement to change. Compare the original and revision at matched content, state, output size and useful fidelity, on both visual expression and the actual task. Keep the stronger result, including the original where the change loses. Recheck affected behavior, dependent surfaces and required regressions.

## Prototype weight

A disposable render made mid-deliberation to provoke a reaction — a prototype of an output still being deliberated, judged once and thrown away — runs this skill at reduced weight rather than skipping it. Decisions 0 through 2 still run in full: the purpose is the reaction being sought; the task model still gets written, because structure is most of what a prototype gets reacted to, and one in the wrong arrangement pulls the reaction onto the arrangement instead of onto the question the render was made to ask; and the register still gets picked, because a render in the wrong register draws reactions to the wrong thing. Declare a minimal token block, and hold the floors only where the fidelity concentrates — the surface the reaction is about must be legible: contrast by number, one spacing rhythm, an alignment spine, real copy, and at rest at load — with orientation and necessary controls available on arrival. A prototype testing interaction or pacing must expose that behavior at the fidelity being judged. Everywhere else stays visibly unfinished, and finishing it is a defect at this weight: polish on an incidental region invites reaction to it, and on an artifact rendered to elicit criteria, a stray reaction hardens into a requirement. Skip Decision 5 entirely — the reader's reaction is the verification, and the artifact is disposed of either way.

**Candidate sets test the unresolved decision.** Vary the organizing idea when that is uncertain; vary type, color or pacing when those carry the question. Candidates must differ in what is being tested, with incidental differences controlled enough to interpret the reaction. Where an incumbent exists, include it at comparable fidelity. A preference can select a direction; it does not establish task performance or readiness to ship.

## What loads

Load a reference when its trigger applies; each states rules, not background.

| Reference | Loads when |
|---|---|
| `references/experience.md` | Stateful or shared work; multi-page journeys; non-web files; temporal, conversational, AI, spatial, command-line or unfamiliar artifacts — scope, continuity, access and delivery probes |
| `references/registers.md` | The artifact is any genre beyond the five web/app registers above; the artifact is a document or report — its genre row (job, metric, failure smell, probe) and the rules under every genre live there, not in the web register table; the purpose or genre pick is contested; a genre behavior probe is needed |
| `references/figures.md` | The encoding line names any figure or chart — what a figure depicts, how options are compared, the inline-SVG mechanics that keep it legible in both themes, faithful quantitative mappings |
| `references/floors.md` | Building or reviewing any web/app-register artifact — the full floor numbers behind the checklist above; also when the work turns on copy rules or a compact density mode, which live there for every genre |
| `references/craft.md` | The work touches a listed craft domain: composition, motion, emotion and delight, imagery and icons, right-to-left or Hebrew text, touch and mobile, color construction, typeface selection, accessibility depth, style derivation |
| `references/calibration.md` | Checking an unexamined style default — dated observations, not a style blacklist |

## Scope

This skill governs building and restyling. When a manifest gate needs a verdict on a finished artifact, that is the `review-design` skill — an independent evaluation against these same references, which this skill does not perform on its own output.
