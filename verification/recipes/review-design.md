---
kind: skill
covers: claude-plugins/manifest-dev/skills/review-design
ask-first: starts a fresh agent per scenario, which uses model quota
dry-run: honored
---
# review-design

Reviews a digital artifact as delivered — rendered, played or opened in its real medium — against the user's task and direction, and reports evidence-backed graded findings.

## How a user reaches it

- `/review-design [artifact] [genre=…]`. Without a named artifact it reviews the most recent one the user can see; `genre=` wins, otherwise the genre is inferred and disclosed.
- Phrases its description matches: "design review", "is this page accessible".
- define's UI gates (run under `/do`).
- On HTML it runs `claude-plugins/manifest-dev/skills/review-design/scripts/design-check.mjs` (see design-instruments).
- Grades run CRITICAL to LOW; PASS by default at no MEDIUM or above.
- In a project whose context file points to principles skills, it follows those pointers and holds the work to the principles: a principle outranks the shipped standards both ways, and an unchosen departure is reported with the principle quoted. The skill states no rule for this; the `principles` scenario shows the behavior.

## Scenarios

### review
Run: `scripts/drive-skill.sh review-design verification/prompts/review-design-review.md`
Proves: a report with findings tied to rendered evidence, or BLOCKED naming the evidence it could not get. The artifact is unchanged.
Check: read

### project-rule-critical
Run: `scripts/drive-skill.sh review-design verification/prompts/review-design-project-rule-critical.md`
Proves: with a rule whose result is a critical access failure (a fixed palette at 1.92:1 contrast), the failure is still reported, naming the rule.
Check: read

### project-rule
Run: `scripts/drive-skill.sh review-design verification/prompts/review-design-project-rule.md`
Proves: with a context file holding a rule a standard would flag (a fixed-width layout) and a page following it, the overridden checks raise no finding and the report names the rule; rendered properties are BLOCKED where no browser runs.
Check: read

### principles
Run: `scripts/drive-skill.sh review-design verification/prompts/review-design-principles.md --scaffold verification/scaffolds/principles-design-review`
Proves: review-design, run alone, in a project whose context file points in its own words to `kiosk-principles`. Graders: (1) the run read that skill; (2) no finding asks for colour, imagery or more visual character, and the report names the black-on-white principle it applied; (3) a finding quotes the list-count principle for the list of 14 loans with no count, with the yield not shown: 14 rows do not fit the 768-pixel screen, and the page's own comment claiming the list fits is not taken as evidence; (4) the gate verdict fails on that finding. A BLOCKED result for the list count is not a pass. PASS when all four hold.
Check: read

### explained
Run: `scripts/drive-skill.sh review-design verification/prompts/review-design-explained.md --scaffold verification/scaffolds/review-explained-page`
Proves: review-design, run alone, in a project with no principles skill, on a tracking page whose five earlier findings — each saying that people would not understand something — were each answered with an added explaining sentence: a sentence whose job is to say what something on the page is or how to use it. The findings and how each was answered are supplied. Graders: (1) the run rendered the page — its session record shows the page check reporting render samples, or a screenshot it took — and the report is not BLOCKED; (2) the report names the added sentences as a cost to the person and does not accept them as the fix for the findings they answered; (3) each of the five sentences says something a label, a mark, an order or a position on the page could carry, and for each the fix the report proposes names such a form and proposes no further sentence — one by one, or as a pattern fix that moves each sentence's content onto the thing it explains. PASS when all three hold. The result counts only for a run whose session record shows it read `review-design` from the snapshot it was handed and no principles skill from outside the scratch project; any other run is a harness fault, driven again.
Check: read

### explained-retested
Run: `scripts/drive-skill.sh review-design verification/prompts/review-design-explained-retested.md --scaffold verification/scaffolds/review-explained-retested`
Proves: the `explained` case built to make accepting the sentences more tempting: each of the five is short, and the supplied record ends with a re-test in which six customers read the page through on a tablet at a counter, then said correctly what each element meant, and which counts the five findings as closed. The graders, the PASS condition and the rule for which runs count are those of `explained`, unchanged. The re-test shows the sentences are understood when read through; it does not show the same for a person who glances at the page on a phone while doing something else, which is the use the project's context file names. How the graders read a report from this case: a report that grants what the re-test shows does not fail (2) for that; one that counts the findings closed, or offers the label and mark forms only as optional, does. For (3), keeping, trimming or moving one of the five sentences is not a form; words set on the element itself — a step's name, a word before a time, a button's visible name, a day heading — are.
Check: read

### reading
Run: `scripts/drive-skill.sh review-design verification/prompts/review-design-reading.md --scaffold verification/scaffolds/review-reading-page`
Proves: review-design, run alone, in a project with no principles skill, on a guide page its reader came to read, which holds a term first met there, glossed in one short line beside it, and an action that cannot be undone after seven days, with its consequence stated before the button. Graders: (1) the run rendered the page — its session record shows the page check reporting render samples, or a screenshot it took — and the report is not BLOCKED; (2) no finding in the report asks to cut or shorten the guide's text for being text, the gloss, or the consequence statement. A finding about how that text is set — its size, measure, contrast or order — does not fail (2). PASS when both hold. The result counts only for a run whose session record shows it read `review-design` from the snapshot it was handed and no principles skill from outside the scratch project; any other run is a harness fault, driven again. The scenario guards against a review that counts every sentence as a cost, so a pass from a review that counts none settles nothing by itself.
Check: read

## Gotchas

- Render checks need Playwright with Chromium; a drive renders only where the driving machine has them, and is source-only elsewhere.
- The `explained`, `explained-retested` and `reading` scaffolds stop unless `DESIGN_TOOLS_PLAYWRIGHT` names a `playwright` or `playwright-core` module directory, which they link into the scratch project's `node_modules` so the page check run there renders; the browser is the Chromium that Playwright bundles. A source-only report cannot pass any of the three, so they refuse to start one.
- Reading source alone is not a design verdict; without rendering it reports BLOCKED or SKIPPED, never PASS.
- The check script's exit 0 means it completed, not that the page is clean.
- `tests/test_design_check.py` exercises its check script; `tests/test_design_standalone.py` keeps its support files reachable.
- Not yet driven: the description phrases, define's UI gates.
