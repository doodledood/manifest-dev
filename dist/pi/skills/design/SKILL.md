---
name: design
description: 'Design and build user-visible artifacts — pages, dashboards, tools, documents, reports, decks, infographics, posters, forms, emails, games, explorables. Decides purpose and register before aesthetics, declares a token system before markup, holds functional craft floors (states, contrast, spacing, alignment), and verifies against renders and machine checks rather than intention. Use when creating or restyling anything a person will see and judge — including disposable prototypes rendered mid-deliberation to provoke a reaction, which run it at prototype weight: purpose, register, and legibility floors on the surface being judged, no verification loop, deliberate roughness kept everywhere else.'
user-invocable: true
---

# design — user-visible artifacts that work and are worth looking at

Generated visual artifacts fail in three ways, and each needs its own counter. Styling effort lands on the wrong layer while the functional layer collapses — pages ship with no empty state, no error path, no undo. Stated principles do not survive into output — what holds is external evidence: a render, a machine check, a counted budget, never your own account of what you did. And unforced style choices converge on the same few looks — distinctiveness must be derived from the subject at hand, never sampled from habit.

So work through five decisions, in order. Each bounds the next; skipping one is where those failures enter.

**Purpose picks the metric, register picks the rules, tokens hold the system, floors guard the layer that collapses, and verification is external evidence per genre — with distinctiveness derived from the subject and spent only where the register allows.**

## Decision 0 — name the purpose

State which one thing the artifact optimizes for. The four purposes want different and sometimes opposite designs, so one artifact picks one:

| Purpose | Optimize for | What changes |
|---|---|---|
| Comprehension | Minimal reading effort | One idea per chunk, verdict first, labels beside the thing they label |
| Retention | Successful recall later | Questions before answers, spaced re-exposure — difficulty in the *task*, never in legibility |
| Persuasion | Fluency and credibility | Maximal polish, zero errors, short words, verifiable claims |
| Action | One behavior made easy | Single dominant call to action, friction stripped from that one path |

Difficulty belongs in the task, never in the surface: a retention artifact asks the reader to predict before revealing, on a maximally legible page. Hard-to-read styling teaches nothing and costs trust.

## Decision 1 — name the register before any aesthetic choice

A **register** is the density, type, and visual-furniture regime a genre demands — how packed the layout runs, how type is scaled and weighted, how much decoration (borders, shadows, backgrounds, imagery) the genre tolerates. Naming it first is the highest-leverage single decision here: the register decides everything the aesthetics are allowed to do. The web/app registers:

| Register | Density | Type | Decoration | Non-negotiables |
|---|---|---|---|---|
| Dashboard / analytics | High; 12–14px data text, 8–12px gaps | Aligned digits throughout; labels small and quiet | Minimal: hairline borders, muted neutrals, color only for state and data series | Summary before detail; numeric columns right-aligned |
| Document / report | Low; one column | 65–70 characters per line, 16–18px, line-height 1.5–1.6 | Nearly none: no cards around paragraphs, no icon bullets | Reading order is the layout; answer first, evidence beneath |
| Tool / app | Medium | System font stack; 14–16px; uniform control heights | Functional: visible affordances, predictable placement | All states designed; one primary action per view |
| Landing / marketing | Very low | Display type 48–72px, tight letter-spacing | Deliberate: one accent, one repeated call to action | The only web register where decoration can argue its case |
| Game / playful | Custom | Art direction owns the page | Full-bleed, motion welcome | Feedback rules still hold; reduced-motion still respected |

For any other genre — a deck, an infographic, a poster, a data story, a form or checkout, a print-shaped document, an email, an explorable — load `references/registers.md` before proceeding: each has its own job, success metric, and failure smell, and applying a web register to it is the same defect as putting the marketing look on a dashboard.

Two rules that ride with the pick:

- **Hybrid briefs compose; they never average.** Real briefs blend genres (a dashboard with a marketing header). Choose one governing register per *region* by that region's job, plus one page-level treatment read that arbitrates conflicts — never a blend of two registers' values, which produces mush.
- **Treatment: utilitarian or editorial.** Utilitarian means a well-composed page, polished type, considered spacing, no hero moment — the default for tools, dashboards, docs. Editorial means the page carries a designed point of view — permitted only where the register grants a decoration budget. Editorial procedure lives in `references/registers.md`.

The register also sets the *feeling* budget. Spectacle pays on first-contact surfaces where the visitor is judging the maker (launch pages, portfolios) and damages surfaces visited repeatedly or mid-task (tools, dashboards, forms, checkout) — on those, any surprise converts to pure latency on the second visit.

## Decision 2 — declare tokens before markup

Before any component, write a compact system block and derive everything from it:

- 4–6 named colors as *roles* with usage rules ("accent — highest-emphasis action, once per view"), not as a palette of hexes.
- 2–3 type roles named by job (display / body / utility), with the faces, sizes, and the 2–3 weights allowed.
- The spacing values (for example: within-group 8/12, card padding 24, section gap 48–96) — and only those values, everywhere.
- The corner-radius set.

This is where distinctiveness enters: derive palette and typefaces from the subject's own world — its era, material, and temperature — never from a stock "modern" look. Construction procedures (color ramps, typeface derivation) are in `references/craft.md`; before styling, also load `references/calibration.md` and write a short Don'ts list for this artifact from it — the currently overused looks to avoid where the choice is otherwise free.

At the end of the build, audit that only token values appear. A value outside the system is either a defect or a missing token — decide which, on the spot.

## Decision 3 — hold the floors

The floors are where generated output measurably collapses. They are checks against the artifact, never against your narration of it. The compressed checklist — full numbers and per-domain craft load from `references/floors.md` and `references/craft.md`; the full file also carries register fit as a floor of its own, which Decision 1 already covers here:

1. **States exist or the UI is unfinished.** Every dynamic region ships loading, empty (what would be here + how to get it), error (what failed, what to do, input preserved), and the happy path; destructive actions get undo or confirmation.
2. **Contrast by number, not by eye.** Body text 4.5:1 minimum, secondary text included — de-emphasize by stepping shade, never below the floor.
3. **One spacing rhythm, held by the parent.** Declare the page's spacing values once and reuse exactly those; give every gap one owner — a wrapper sets it, children never add competing margins. Within-group gaps at least one step smaller than between-group.
4. **Alignment has a spine.** One left alignment edge per region; numbers right-aligned with equal-width digits; never mix centered and left-aligned blocks in one column.
5. **Neutrals do 90% of the work.** ~8–10 shades of one slightly-tinted neutral, one accent (roughly once per view), reserved semantic hues. No gradient text, no colored headings, no multi-hue cards.
6. **Dark mode is designed, not inverted.** Dark-gray surfaces, never pure black; lighter surface = higher elevation; desaturated accents; off-white text; every color a two-theme token.
7. **Prose measure and display type.** Body prose max-width 65–70 characters; headings line-height 1.1–1.25 with slight negative letter-spacing at large sizes; hierarchy from weight and color before size.
8. **Data typography.** Equal-width digits wherever numbers align; consistent decimals per column; "—" for missing, never "0".
9. **Craft consistency.** One radius system; hairline borders *or* shadows *or* background shift — never stacked; one icon set, labeled; truncation planned against triple-length strings; controls in one row share exact height.
10. **Accessibility mechanics.** Visible focus ring (never strip outlines bare); `prefers-reduced-motion` gates all non-essential animation; touch targets ≥44px (24px is the legal floor, not the target); real `<button>`/`<a>`, labels on inputs, one `h1`.
11. **Copy is design material.** Controls say what happens ("Save changes", not "Submit"); errors state what went wrong and what to do; empty states answer "what would be here" and "how do I get it"; front-load the differentiating word in every heading and label.

Floor-versus-polish priority is register-conditional: floors dominate tools, dashboards, and forms; on first-contact persuasion surfaces, polish *is* the floor. Both, not either, wherever the budget covers both.

## Decision 4 — verify in the artifact's own behavior loop

Never accept your own narration as evidence. The render or the machine check, only.

**Machine checks first — they are cheap.** Run `scripts/design-check.mjs` (from this skill's directory) against any HTML artifact: it checks text contrast, single-theme color definitions, off-scale spacing values, missing focus-visible and reduced-motion blocks, undersized touch targets, and horizontal overflow at 390px width. Passing it is necessary, never sufficient — a run that passes the script but skips the judgment pass below is unverified.

**Then the critique loop, gated pairwise.** Where a browser or screenshot capability exists: render, screenshot each section at 1440×900 and 390×844 (both themes where the artifact claims both), critique against named criteria — composition, typography, color and contrast, register fit, polish — fix the top issues, re-render. Two checks ride along free: the blur test (blur the screenshot ~10px; the primary action and heading must still separate from the background — hierarchy verified, not asserted) and the false-floor check (no section may end on a clean edge exactly at viewport height while content continues below — it reads as "nothing further" and stops scrolling). Stop when the new render is no longer *better than the previous one* — judge by comparison, never by an absolute score — and cap at 2–3 iterations: later rounds degrade as often as they improve. Where nothing can render, apply the same criteria to a full re-read of the code plus the machine checks, and say plainly that rendered verification did not happen.

**Then the genre's own behavior probe.** Every genre is measured in a behavior loop a screenshot cannot see. For the web/app registers, the probes are these: open the dashboard and time how fast the one deviant number is found; read the document's headings and bold lines alone and check they carry the argument; walk the tool's primary action through failure and recovery with input preserved; on the landing page, state what is being offered and what to do next from five seconds of looking; play the game's loop twice and check the second run still gives feedback. Probes for every genre beyond these are listed with their registers in `references/registers.md`.

**Editing is the common case, and it degrades.** Edits are generated against local context while the token system ages out of attention — by the tenth edit the spacing system no longer exists. Discipline: before any edit, re-read the token block and the register declaration; after any edit, re-run the machine checks and diff the changed values against the tokens.

## Prototype weight

A disposable render made mid-deliberation to provoke a reaction — a prototype of an output still being deliberated, judged once and thrown away — runs this skill at reduced weight rather than skipping it. Decisions 0 and 1 still run in full: the purpose is the reaction being sought, and the register still gets picked, because a render in the wrong register draws reactions to the wrong thing. Declare a minimal token block, and hold the floors only where the fidelity concentrates — the surface the reaction is about must be legible: contrast by number, one spacing rhythm, an alignment spine, real copy. Everywhere else stays visibly unfinished, and finishing it is a defect at this weight: polish on an incidental region invites reaction to it, and on an artifact rendered to elicit criteria, a stray reaction hardens into a requirement. Skip Decision 4 entirely — the reader's reaction is the verification, and the artifact is disposed of either way.

## What loads

Load a reference when its trigger applies; each states rules, not background.

| Reference | Loads when |
|---|---|
| `references/registers.md` | The artifact is any genre beyond the five web/app registers above; the purpose or genre pick is contested; an editorial treatment is chosen; a genre behavior probe is needed |
| `references/floors.md` | Building or reviewing any web/app-register artifact — the full floor numbers behind the checklist above; also when the work turns on copy rules or a compact density mode, which live there for every genre |
| `references/craft.md` | The work touches a listed craft domain: composition, motion, emotion and delight, imagery and icons, right-to-left or Hebrew text, touch and mobile, color construction, typeface selection, accessibility depth, style derivation |
| `references/calibration.md` | Writing the token block or making any style choice the brief leaves free — the dated list of currently-overused looks |

## Scope

This skill governs building and restyling. When a manifest gate needs a verdict on a finished artifact, that is the `review-design` skill — an independent evaluation against these same references, which this skill does not perform on its own output.
