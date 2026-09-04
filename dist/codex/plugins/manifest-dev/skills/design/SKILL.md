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

## Decision 0 — name the purpose

State the primary user outcome and any secondary outcome that must survive. These are examples, not exclusive categories:

| Purpose | Optimize for | What changes |
|---|---|---|
| Comprehension | Minimal reading effort | One idea per chunk, verdict first, labels beside the thing they label |
| Retention | Successful recall later | Questions before answers, spaced re-exposure — difficulty in the *task*, never in legibility |
| Persuasion | Fluency and credibility | Maximal polish, zero errors, short words, verifiable claims |
| Action | Successful, informed completion | Clear next action, necessary choices and recovery |
| Creation, exploration, communication or play | The brief’s actual outcome | Tools and feedback that support the activity; no forced single call to action |

Difficulty belongs in the task, never in the surface: a retention artifact asks the reader to predict before revealing, on a maximally legible page. Hard-to-read styling teaches nothing and costs trust.

## Decision 1 — model the task before any layout

Purpose names what the artifact optimizes for. It does not name what the person at it actually *does*, and the doing is what structure has to follow. Write the model down before any layout — five lines, kept beside the token block and treated the same way:

- **Who** — the person at the artifact, what they know, and relevant access, language, device and input conditions.
- **The loop** — the one sequence they repeat, in verbs: *read the task → judge it → answer three questions → next*. Name the main sequence and any consequential entry, return, recovery or exit path. Frequency shapes efficiency; consequence can make a rare path structurally important.
- **Co-visible** — for each step of the loop, what has to be on screen *at the same time* for that step to happen without the person holding something in their head. This is the line that decides the arrangement: make information needed together available without avoidable memory work. On nonvisual surfaces, preserve equivalent context; on constrained displays, adapt the arrangement without losing the relationship.
- **Rate** — how often the loop runs and how long one pass takes. A loop run three hundred times a day earns keyboard paths and a dense arrangement that a once-a-quarter form must not spend on.
- **Encoding** — for each claim the reader must take in, whether prose, a table, or a figure carries it. One test decides: a figure earns its place when a cold reader would otherwise have to assemble a mechanism from prose — where data flows, which parts talk, what changes between two options, what state something moves through; a table when the claim compares several things on the same attributes; and if a sentence says it faster, write the sentence. Avoid needless repetition of the same explanation; retain labels, complementary prose, captions and accessible equivalents needed to convey the meaning. What a figure shows and how it is drawn load from `references/figures.md`.

For stateful, shared, multi-page, non-web, temporal, conversational, spatial or unfamiliar artifacts, load `references/experience.md` before settling the model. Name the final delivery format and use its platform guidance; a web preview cannot establish native-file behavior.

The layout traces to this block. Before writing markup, take each region and name the line of the model that put it there; a region tracing to nothing is decoration or a missing model line, and which one it is gets decided on the spot — the same call as a value outside the token system. A claim the encoding line assigned to a figure that arrives as a paragraph is the same defect from the other side. A layout that breaks a co-visibility pair is wrong however well it is made, and what gets revised on new evidence about the work is the model line, never the layout that traced to it.

**When the brief does not carry the loop, ask — once, and narrowly.** Most briefs name an artifact and no work: *a page for labeling tasks* says nothing about whether the labeler judges one long document or fifty short strings. Ask for the loop and its co-visibility in one bounded question — two or three specifics, with the structural choice each answer would settle stated beside it, so the answer is cheap to give and visibly worth giving. Never open an interview, and never ask what the brief already settles. Where there is nobody to ask — an unattended run, an evaluation, a render made mid-deliberation — write the model down as an assumption, mark it as assumed, and build on it; the model is never left unstated, because an unstated model is the habit layout wearing the work's name.

## Decision 2 — choose the register and creative direction

A **register** sets the density, typography, and ornament that suit the artifact's use. It shapes how creative ambition is expressed: an everyday tool can impress through composition and information design while keeping repeated actions direct.

First look for what already exists — a project tokens file, a component library, a house style — and hold the precedence: the user's words, then the project's existing system, then this skill's own choices. Develop the direction within those constraints. The web/app starting registers below supply defaults, not universal numerical floors. Task fit, applicable standards, the brief and the existing system govern departures:

| Register | Density | Type | Decoration | Non-negotiables |
|---|---|---|---|---|
| Dashboard / analytics | Task-appropriate density; verify data-text legibility and enlargement | Aligned digits throughout; labels small and quiet | Minimal: hairline borders, muted neutrals, color only for state and data series | Summary before detail; numeric columns right-aligned |
| Document / report | Reading order and useful comparisons govern columns | Readable measure and hierarchy; test the actual language and output size | Nearly none: no cards around paragraphs, no icon bullets | Reading order is the layout; answer first, evidence beneath |
| Tool / app | Matched to repeated work | Existing type system; controls sized for the supported input | Functional: visible affordances, predictable placement | All states designed; one primary action per view |
| Landing / marketing | Message-led | Expressive display type with readable supporting copy | Deliberate: one accent, one repeated call to action | The offer and next action are clear on arrival |
| Game / playful | Custom | Art direction owns the page | Full-bleed, motion welcome | Feedback rules still hold; reduced-motion still respected |

The Decoration column budgets ornament — borders, shadows, backgrounds, mood imagery. It never counts a figure or table the task model's encoding line put there: those are information, sized to the claim they carry, and a document register's "nearly none" leaves every one of them standing.

For any other genre — a deck, an infographic, a poster, a data story, a form or checkout, a print-shaped document, an email, an explorable — load `references/registers.md` before proceeding: each has its own job, success metric, and failure smell, and applying a web register to it is the same defect as putting the marketing look on a dashboard.

Two rules that ride with the pick:

- **Hybrid briefs compose; they never average.** Real briefs blend genres (a dashboard with a marketing header). Choose one governing register per *region* by that region's job, plus one page-level treatment read that arbitrates conflicts — never a blend of two registers' values, which produces mush.
- **Commit to a creative direction.** Use the purpose, audience, and task model to choose what will make this artifact compelling and memorable. Carry that idea through composition, typography, imagery, and interaction where they serve it. An elegant decision chart can carry a serious report; a vivid worked example can carry an explainer. Make the direction specific to the subject, then refine it rather than adding competing effects.

Match the emotional effect to the use context. Expressive storytelling may serve a first encounter; repeated work needs visual character that stays enjoyable without delaying actions, hiding information, or competing with the task.

## Decision 3 — declare tokens before implementation

Before implementation, write a compact system block for the actual medium. Where a design system exists, use its values rather than inventing rivals. For visual output, derive components from these applicable choices:

- Named colors as *roles* with usage rules ("accent — highest-emphasis action"), not as a palette of hexes.
- 2–3 type roles named by job (display / body / utility), with the faces, sizes, and the 2–3 weights allowed.
- The spacing values (for example: within-group 8/12, card padding 24, section gap 48–96) — and only those values, everywhere.
- The corner-radius set.

For audio-only or other nonvisual output, declare the applicable voice, timing, turn-taking and feedback conventions instead.

For visual output, carry the creative direction into palette and typefaces: derive them from the subject's own world — its era, material, and temperature — never from a stock "modern" look. Construction procedures (color ramps, typeface derivation) are in `references/craft.md`; before styling, also load `references/calibration.md` and write a short Don'ts list for this artifact from it — the currently overused looks to avoid where the choice is otherwise free.

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
12. **The entry state is understandable.** Keep essential orientation and narrative available without forced reveals. Demonstration data is plainly labeled; real empty states must remain truthful. Interaction may carry the task in games, simulations and creative tools.
13. **Structure is information.** Numbered markers only on a real sequence; eyebrows, dividers, and section furniture only where they encode something true about the content, never as rhythm.

Functional floors and visual ambition both bind. Repair broken basics first, then finish the creative direction; passing the floors alone is not completion. At prototype weight, apply that ambition only to the surface being judged, as specified below.

## Decision 5 — verify in the artifact's own behavior loop

Inspect the artifact and exercise it. Source inspection locates causes and checks semantics; it does not substitute for rendered or behavioral evidence.

**Use established project checks, then inspect their limits.** For HTML, run `scripts/design-check.mjs <artifact.html>` from this skill’s directory. It is bounded triage: exit zero means execution completed; NOTE items are review candidates and SKIPPED items remain unverified. It does not establish accessibility conformance, focus or reduced-motion behavior, token adherence, or appropriate figure use. Validate candidates before treating them as defects.

**Inspect and compare revisions.** Use the intended browser, native host, player or device. For responsive web work, 1440×900 and 390×844 are useful starting viewports; also test applicable 320 CSS px reflow, text enlargement and supported themes. Inspect composition, typography, information structure, craft and creative direction against the brief. Fix consequential issues and compare with the prior version, keeping the stronger result. Two or three rounds is a starting budget, not a proof of convergence: report remaining defects if it ends. A blur or first-impression check can reveal hierarchy concerns, but neither is a mechanical verdict. If required rendering, playback or interaction is unavailable, report that verification gap; code review cannot clear it.

**Then the genre's own behavior probe.** Every genre is measured in a behavior loop a screenshot cannot see. For the web/app registers, the probes are these: open the dashboard and time how fast the one deviant number is found; read the document's headings and bold lines alone and check they carry the argument, then cover the prose and check that the figures and tables carry the mechanism the encoding line assigned them and that each encoding serves the task with its needed accessible equivalent; walk the tool's primary action through failure and recovery with input preserved; on the landing page, state what is being offered and what to do next from five seconds of looking; play the game's loop twice and check the second run still gives feedback. Probes for every genre beyond these are listed with their registers in `references/registers.md`.

**Preserve the design through edits.** Before editing, re-read the task model, creative direction and system. After editing, check the affected behavior and dependent surfaces; keep any broader regression checks the project requires.

## Prototype weight

A disposable render made mid-deliberation to provoke a reaction — a prototype of an output still being deliberated, judged once and thrown away — runs this skill at reduced weight rather than skipping it. Decisions 0 through 2 still run in full: the purpose is the reaction being sought; the task model still gets written, because structure is most of what a prototype gets reacted to, and one in the wrong arrangement pulls the reaction onto the arrangement instead of onto the question the render was made to ask; and the register still gets picked, because a render in the wrong register draws reactions to the wrong thing. Declare a minimal token block, and hold the floors only where the fidelity concentrates — the surface the reaction is about must be legible: contrast by number, one spacing rhythm, an alignment spine, real copy, and at rest at load — with orientation and necessary controls available on arrival. A prototype testing interaction or pacing must expose that behavior at the fidelity being judged. Everywhere else stays visibly unfinished, and finishing it is a defect at this weight: polish on an incidental region invites reaction to it, and on an artifact rendered to elicit criteria, a stray reaction hardens into a requirement. Skip Decision 5 entirely — the reader's reaction is the verification, and the artifact is disposed of either way.

Two further rules govern a *set* of candidates rendered for one reaction. **When the reaction sought is the direction rather than its execution, the judged surface is the signature element** — the one designed move a direction is recognised by — so every candidate carries one, derived as Decision 3 requires, and the candidates differ *in signature*. A set varying only palette and typeface holds the judged surface constant across all of them, which probes the wrong axis: it draws "fine" from every reader whatever the directions were worth, and the round ends knowing nothing. **Where an incumbent design already exists, it is rendered as the control in the same set**, at the same fidelity as the candidates. Without it a reader rates the candidates against each other and the round ends in a preference; with it the reader is choosing what ships, and the round ends in a decision.

## What loads

Load a reference when its trigger applies; each states rules, not background.

| Reference | Loads when |
|---|---|
| `references/experience.md` | Stateful or shared work; multi-page journeys; non-web files; temporal, conversational, AI, spatial, command-line or unfamiliar artifacts — scope, continuity, access and delivery probes |
| `references/registers.md` | The artifact is any genre beyond the five web/app registers above; the artifact is a document or report — its genre row (job, metric, failure smell, probe) and the rules under every genre live there, not in the web register table; the purpose or genre pick is contested; a genre behavior probe is needed |
| `references/figures.md` | The encoding line names any figure or chart — what a figure depicts, how options are compared, the inline-SVG mechanics that keep it legible in both themes, charts to one scale |
| `references/floors.md` | Building or reviewing any web/app-register artifact — the full floor numbers behind the checklist above; also when the work turns on copy rules or a compact density mode, which live there for every genre |
| `references/craft.md` | The work touches a listed craft domain: composition, motion, emotion and delight, imagery and icons, right-to-left or Hebrew text, touch and mobile, color construction, typeface selection, accessibility depth, style derivation |
| `references/calibration.md` | Writing the token block or making any style choice the brief leaves free — the dated list of currently-overused looks |

## Scope

This skill governs building and restyling. When a manifest gate needs a verdict on a finished artifact, that is the `review-design` skill — an independent evaluation against these same references, which this skill does not perform on its own output.
