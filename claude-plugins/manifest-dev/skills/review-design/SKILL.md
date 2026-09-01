---
name: review-design
description: 'Review a user-visible artifact against design standards — a page, dashboard, tool, document, report, deck, infographic, poster, form, email, game, or explorable. Renders the artifact (BLOCKED when it cannot), runs machine checks, exercises its states and behavior, and reports graded findings with the fix. Use when checking design quality, evaluating a design gate in a manifest run, reviewing an interface before shipping, or asking whether a visual artifact holds up.'
user-invocable: true
---

# review-design — evaluate a user-visible artifact

Report where an artifact departs from the design standard that governs its genre. Review only: you find and explain, the author decides and edits. You never repair the artifact, and when this skill is activated on work you produced, hand the evaluation to a fresh context instead — an author re-reading their own build re-reads their intentions.

## Input

`$ARGUMENTS` carries what to review — a file path, a directory, a URL, or a running app plus how to reach it. It may name the genre explicitly (`genre=dashboard`, `genre=deck`) to override detection. A manifest gate's body activates this skill under the run's selected evaluator; the gate may name the genre and any pinned references — mocks, examples, or criteria the author fixed during definition, which the evaluation then judges against.

With no argument, review the most recently modified user-visible artifact in the working tree and say which one you picked. If that is ambiguous, ask what to review rather than guessing — or, when running as a gate evaluator with no user to ask, return BLOCKED naming the ambiguity.

## Rendered evidence or BLOCKED

A verdict formed from reading markup, styles, or components alone is not a design evaluation. Render the artifact — open it in a browser, screenshot every surface the review covers at the desktop and narrow-mobile viewports the loaded design standards pin, in both themes where it claims both — and exercise it: click the primary actions, submit the form wrong, trigger the empty and error states its data produces, resize it. When the artifact cannot be rendered or executed with what you have, the verdict is **BLOCKED**, naming exactly what would unblock it (a build step, a data fixture, a browser), never a silent fall-back to code inspection. Reading the code is for locating a defect's cause after the render shows it, and for the checks only code can show (token discipline, semantic markup).

## Standards

The standards this skill judges against live with the `design` skill, so the two cannot drift apart:

- `../design/SKILL.md` — the six decisions, the task-model block the layout must trace to, the register tables, the compressed floor checklist.
- `../design/references/registers.md` — genres beyond web/app, their success metrics, failure smells, and per-genre behavior probes.
- `../design/references/floors.md` — the full floor numbers, density rules, and banned rationales.
- `../design/references/craft.md` — per-domain craft checklists; load the domains the artifact touches.
- `../design/references/calibration.md` — the dated list of currently-overused looks.

Load `../design/SKILL.md` plus whichever references the artifact's genre and touched domains call for, under that file's own loading table. These paths are where the files sit when the whole plugin is installed; where they are absent — a single-skill install, or a host that lays skills out differently — search for them by name before giving up, and where they genuinely cannot be found, say so and report only the findings you can support without them rather than reviewing against remembered rules.

## Procedure

1. **Name the genre and register** you are judging against, in one line, before any finding — a finding graded under the wrong register is noise the author should ignore. An explicit `genre=` argument wins; otherwise detect from the artifact's job, and where detection is genuinely balanced, say so and ask — with no user to ask, judge under the closer register and name the call in the report.
2. **Name the loop the artifact serves**, in one line, before judging anything: the person at it, the sequence they repeat, and what has to be on screen at the same time for each step of that sequence to happen without them holding a value in their head. Take it from whatever the activation supplied — a task model the author wrote, a pinned reference, the gate body — and otherwise derive it from the artifact's own job, the way a labeling tool's loop is *read the item → judge it → answer → next*. Where the job is genuinely unreadable from the artifact and nothing supplied it, say so and judge everything else; never invent a loop and then convict the artifact against it.
3. **Run the machine checks**: `node ../design/scripts/design-check.mjs <artifact.html>` (path relative to this skill's directory) for any HTML artifact. Its findings enter the report like any other, and its passing proves only the mechanical layer — it licenses nothing about task fit, register fit, or hierarchy.
4. **Render and exercise** per the section above. Run the loop from step 2 yourself, twice, and watch what each pass costs. For the genre's behavior probe, use the one listed with its register in the loaded standards.
5. **Judge the renders** against the loaded standards, in this order: task fit — whether the arrangement lets that loop run, with what the loop needs together visible together, the repeated action reachable without hunting, and the sequence's order matching the reading order; register fit; functional floors (states, error paths, recovery); composition and hierarchy, including the blur test as the standards specify it; craft consistency (spacing rhythm, alignment spine, palette discipline, type); copy; where the artifact claims distinctiveness, whether its signature element derives from the subject or from the overused-looks list.

Task fit comes first because it is the one dimension whose repair restructures the artifact: every finding below it is graded against an arrangement that may not survive. It is judged against the artifact's job, never against the arrangement you would have chosen — an unfamiliar layout that runs the loop cleanly is not a finding.

## Grading

- **CRITICAL** — the artifact fails its genre's job: the form loses input on error, the deck's argument cannot be restated, content is unreachable or unreadable, the repeated loop cannot be completed at all.
- **HIGH** — a floor violation the audience will hit in normal use: a missing empty or error state, failed contrast on body text, a broken narrow-viewport layout, or an arrangement that breaks the loop's co-visibility so every pass costs a scroll away from what is being acted on or a value carried in the head.
- **MEDIUM** — a rule violation a careful audience member would notice: register mismatch in a region, spacing rhythm broken, mixed alignment, off-token values, misleading copy on a control.
- **LOW** — polish: optical alignment, a duration slightly off the motion table, a wordier-than-needed label.

The threshold, unless the activating gate states its own: **no MEDIUM-or-higher findings** to PASS.

## Reporting

Report each finding with:

- the severity and the rule area
- where it is — the element, screen, and state, with the screenshot or machine-check line that shows it
- what the standard requires, and why this instance fails it
- the concrete fix — the changed value or rule where one line is enough, the shape of the change where it isn't

Order findings by severity, then by position. A clean artifact is a real result: say so plainly, name the genre, register, and references you applied, and stop. Never pad a report with marginal findings to look thorough. When the artifact has many instances of one pattern, report the pattern once with two or three examples and a count. Where a rule's application is a genuine judgment call, say that in the finding instead of grading it as a defect.

## Scope, and what this is not

This skill evaluates finished or in-progress artifacts on request or under a manifest gate. Building and restyling belong to the `design` skill; applying fixes after the report is a separate request and ordinary editing. It does not review prose style — a document's writing quality is the `review-writing` skill; this skill judges the same document's layout, hierarchy, typography, and reading structure.
