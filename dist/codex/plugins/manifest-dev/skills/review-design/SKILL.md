---
name: review-design
description: 'Review digital artifacts against the user’s task, creative direction, functional and accessibility requirements, and actual delivery medium. Inspect renders, native files, playback or interaction as appropriate; exercise relevant failure and recovery paths and report evidence-backed findings. Use for design review or a manifest gate. Building and restyling belong to design.'
user-invocable: true
---

# review-design — evaluate a user-visible artifact

Report where an artifact departs from the design standard that governs its genre, including its purpose-led visual ambition. Review only: you find and explain, the author decides and edits. You never repair the artifact, and when this skill is activated on work you produced, hand the evaluation to a fresh context instead — an author re-reading their own build re-reads their intentions.

## Input

`$ARGUMENTS` carries what to review — a file path, a directory, a URL, or a running app plus how to reach it. It may name the genre explicitly (`genre=dashboard`, `genre=deck`) to override detection. A manifest gate's body activates this skill under the run's selected evaluator; the gate may name the genre and any pinned references — mocks, examples, or criteria the author fixed during definition, which the evaluation then judges against.

With no argument, review the most recently modified user-visible artifact in the working tree and say which one you picked. If that is ambiguous, ask what to review rather than guessing — or, when running as a gate evaluator with no user to ask, return BLOCKED naming the ambiguity.

## Rendered evidence or BLOCKED

A verdict from source inspection alone is not a complete design evaluation. Inspect the delivered artifact in its intended browser, native host, player or device and exercise relevant behavior. Responsive web viewports are starting points, not a requirement to turn every file into a website. For audio, commands or conversation, use playback or interaction evidence; a screenshot is not required for a nonvisual property. Check supported themes, inputs, access and relevant states. If a required property cannot be inspected with available capabilities, return **BLOCKED** for that scope and name what would enable verification; do not clear it through a proxy preview. Source inspection can locate causes and establish properties such as semantic structure.

## Standards

The standards this skill judges against live with the `design` skill, so the two cannot drift apart:

- `../design/SKILL.md` — the six decisions, the task-model block the layout must trace to, the register tables, the compressed floor checklist.
- `../design/references/experience.md` — medium, journey, continuity, consequence and final-delivery probes.
- `../design/references/registers.md` — genres beyond web/app, their success metrics, failure smells, and per-genre behavior probes.
- `../design/references/floors.md` — the full floor numbers, density rules, and banned rationales.
- `../design/references/craft.md` — per-domain craft checklists; load the domains the artifact touches.
- `../design/references/calibration.md` — dated style observations, not a blacklist.
- `../design/references/figures.md` — what a figure depicts, how options are compared, the inline-SVG mechanics, faithful quantitative mappings.

Load `../design/SKILL.md` plus whichever references the artifact's genre and touched domains call for, under that file's own loading table. These paths are where the files sit when the whole plugin is installed; where they are absent — a single-skill install, or a host that lays skills out differently — search for them by name before giving up, and where they genuinely cannot be found, say so and report only the findings you can support without them rather than reviewing against remembered rules.

## Procedure

1. **Name the genre and register** you are judging against, in one line, before any finding — a finding graded under the wrong register is noise the author should ignore. An explicit `genre=` argument wins; otherwise detect from the artifact's job, and where detection is genuinely balanced, say so and ask — with no user to ask, judge under the closer register and name the call in the report.
2. **Name the loop the artifact serves**, in one line, before judging anything: the person at it, the sequence they repeat, and what has to be on screen at the same time for each step of that sequence to happen without them holding a value in their head. Take it from whatever the activation supplied — a task model the author wrote, a pinned reference, the gate body — and otherwise derive it from the artifact's own job, the way a labeling tool's loop is *read the item → judge it → answer → next*. Where the job is genuinely unreadable from the artifact and nothing supplied it, say so and judge everything else; never invent a loop and then convict the artifact against it.
3. **Run applicable checks.** Use established project tooling and, for HTML, `node ../design/scripts/design-check.mjs <artifact.html>`. Exit zero means completed, not clean. Validate measured candidates and NOTE items against the actual artifact and applicable exceptions before grading; SKIPPED properties remain unverified. Neither selector presence nor a heuristic count establishes a requirement violation or pass.
4. **Render and exercise** per the section above. Run the loop from step 2 yourself, twice, and watch what each pass costs. For the genre's behavior probe, use the one listed with its register in the loaded standards.
5. **For improvements, compare with the incumbent** under matched content, state, output size and useful fidelity. Use the builder’s edit contract in `../design/SKILL.md`; identify gains and losses in the actual task and visual expression. If the original is unavailable, state that limit rather than claim superiority.
6. **Judge the renders** against the loaded standards, in this order: task fit — whether the arrangement lets that loop run, with what the loop needs together visible together, the repeated action reachable without hunting, and the sequence's order matching the reading order, and whether the chosen representation serves the information or experience under the shared encoding guidance in `../design/references/figures.md`; register fit; functional floors (states, error paths, recovery); composition and hierarchy, using appropriate visual probes as judgment aids; craft consistency (spacing rhythm, alignment spine, palette discipline, type); copy; visual impact and creative direction — whether the composition, typography, color, imagery, material, interaction and motion make the artifact compelling in a way that serves its purpose and subject. Apply this to every genre, within the user's requirements and existing design system; mechanical correctness alone does not establish finished design. Inspect the relevant experience beyond its strongest frame, including active use, endings and return. Distinguish a judgment about a coherent, memorable idea from a measured claim about audience recall or preference.

Task fit comes first because it is the one dimension whose repair restructures the artifact: every finding below it is graded against an arrangement that may not survive. It is judged against the artifact's job, never against the arrangement you would have chosen — an unfamiliar layout that runs the loop cleanly is not a finding.

A deviation from a numerical or stylistic default is not itself a finding. Name the applicable requirement or the observed task consequence; standards retain their levels and exceptions. Preference cannot cancel a critical functional or access failure.

A finding about visual ambition must point to what the render leaves unresolved — for example, an interchangeable composition that gives the subject no visual expression, or a treatment whose competing effects obscure its central idea — and describe a concrete improvement within the brief. Familiar patterns, restrained styling, and required design-system components are not defects. Judge how well the chosen direction is realized, not whether you would have picked another style.

## Grading

- **CRITICAL** — the artifact fails its genre's job: the form loses input on error, the deck's argument cannot be restated, content is unreachable or unreadable, the repeated loop cannot be completed at all.
- **HIGH** — a floor violation the audience will hit in normal use: a missing empty or error state, failed contrast on body text, a broken narrow-viewport layout, or an arrangement that breaks the loop's co-visibility so every pass costs a scroll away from what is being acted on or a value carried in the head, or a misleading or unsuitable representation that materially obscures information the task needs.
- **MEDIUM** — a supported defect a careful audience member would notice, rather than a different valid style choice: register mismatch in a region, an unresolved creative direction supported by the rendered evidence above, spacing rhythm broken, mixed alignment, off-token values, misleading copy on a control.
- **LOW** — a supported polish issue: awkward optical alignment, unnecessarily distracting timing or a wordier-than-needed label.

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
