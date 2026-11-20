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

## Gotchas

- Render checks need Playwright with Chromium; a drive renders only where the driving machine has them, and is source-only elsewhere.
- Reading source alone is not a design verdict; without rendering it reports BLOCKED or SKIPPED, never PASS.
- The check script's exit 0 means it completed, not that the page is clean.
- `tests/test_design_check.py` exercises its check script; `tests/test_design_standalone.py` keeps its support files reachable.
- Not yet driven: a rendered review (no drive has run where Playwright and Chromium are installed), the description phrases, define's UI gates.
