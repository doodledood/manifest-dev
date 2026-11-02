---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/write-goal
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# write-goal

Writes one standalone goal of at most 4,000 characters from a Manifest, a figure-out read, a Ticket, a handoff, a plain request or several of them, for pasting into a goal field with no file behind it. Before it writes, it tests that the sources settle the outcome, a done check, the limits and where the work stops; it asks a gap that is one clear question directly, and hands a gap that needs investigation to figure-out. Without a Manifest among the sources, its cold reader also reviews the goal as a contract: conditions that cannot all hold, and work that passes every check while missing the outcome.

## How a user reaches it

- `/write-goal <Manifest, read, Ticket, handoff or request>`.
- Phrases its description matches: "turn this into a goal", "write a goal for this", "paste into the goal field".
- No other skill calls or offers it.

## Scenarios

### convert
Run: `scripts/drive-skill.sh write-goal verification/prompts/write-goal-convert.md --tools`
Proves: one goal block in the reply. At most 4,000 characters; every gate's threshold survives; nothing new is invented. The run wrote the goal without starting figure-out or asking a question.
Check: read

### fresh-review
Run: `scripts/drive-skill.sh write-goal verification/prompts/write-goal-fresh-review.md --tools`
Proves: on a 28-gate Manifest with one amendment that removes a gate, whose pass conditions come close to 4,000 characters, the goal block is at most 4,000 characters and keeps every pass condition. That includes the 64 MB peak-memory bound stated only in a gate's why, the 366-day range, the ten-per-hour rate limit, the exact JSON keys and their order, the 100,000-row page with its `Link` header, the p95 under 800 ms over 200 requests, the 404 without the `usage_export` flag, the `review-code` and `review-writing` checks by name, and the stop at a ready pull request with nothing merged or deployed. Nothing asks for the removed CSV export: no CSV gate, and no Initial Approach "then add CSV". A line excluding CSV, as the amendment says, is fine. The profiling, test-first and 40-line steps are not stated as requirements, and the Initial Approach's route and `usage_daily` table, where the goal mentions them, read as a plan rather than a requirement. The goal names no gate ID or Manifest. The goal came back from a fresh review, or the note under the fence says the review was self-graded. The run wrote the goal without starting figure-out or asking a question.
Check: read

### from-read
Run: `scripts/drive-skill.sh write-goal verification/prompts/write-goal-from-read.md --tools`
Proves: one goal block of at most 4,000 characters. The read's check survives with its specifics: `--json` printing an array with exactly the keys `id`, `title`, `created` in that order, `created` as ISO 8601 UTC, `[]` for an empty notebook, the plain output unchanged against `tests/fixtures/three-notes/expected.txt`, `pytest tests/test_list_json.py` and `make test` passing, and the stop at a ready pull request with nothing merged or released. The `--format` option is stated as excluded. Nothing the read leaves out is required: no `--pretty` flag, no JSON Lines, no streaming, no requirement drawn from the evidence or the overturn condition. The goal names no read, figure-out, log or other document. The run wrote the goal without starting figure-out or asking a question.
Check: read

### sharp-gap
Run: `scripts/drive-skill.sh write-goal verification/prompts/write-goal-sharp-gap.md --tools`
Proves: the reply asks one question: whether the work stops at a ready pull request or merges it. The transcript shows figure-out was not started, and the reply holds no goal block.
Check: read

### fills-gaps
Run: `scripts/drive-skill.sh write-goal verification/prompts/write-goal-fills-gaps.md --tools`
Proves: the request settles the outcome but not how to tell the signup flow is less confusing, and nothing in the scratch project settles it. The transcript shows figure-out started on that gap (its skill loaded or its log written), and the reply holds no goal block. A done check put to the user as a question or a recommended option counts as asked; a done check stated as settled, or one inside a goal block, fails.
Check: read

### weak-check
Run: `scripts/drive-skill.sh write-goal verification/prompts/write-goal-weak-check.md --tools`
Proves: the read's only done check, `make test` passing, already passes on the code that loads the whole table, so it cannot tell streaming from not streaming. The reply holds no goal block and asks how streaming will be checked, directly or through figure-out. A check put to the user as a question or a recommended option counts as asked; a goal block, or a memory bound or test stated as settled that the read does not give, fails.
Check: read

## Gotchas

- A goal that refers back to a source file, a read or a log is the defect it exists to avoid.
- `sharp-gap`, `fills-gaps` and `weak-check` end on a question, because a drive is one headless prompt; what they show is that the skill held the goal back and chose the right way to fill the gap.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set.
