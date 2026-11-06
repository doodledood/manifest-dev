---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/hillclimb, claude-plugins/manifest-dev/skills/define/tasks/HILLCLIMB.md, claude-plugins/manifest-dev/skills/define/tasks/references/AI_JUDGE.md, claude-plugins/manifest-dev/skills/figure-out/tasks/HILLCLIMB.md, verification/fixtures/climb-number, verification/fixtures/climb-at-best, verification/fixtures/climb-noisy-measure, verification/fixtures/climb-signup-page, verification/fixtures/climb-signup-results, verification/fixtures/climb-copy, verification/fixtures/climb-short-text, verification/fixtures/climb-slow-sim
ask-first: starts an agent session per scenario that runs a whole climb, which uses model quota
dry-run: honored
---
# hillclimb

Improves an existing artifact round after round toward a goal, keeping a change only on a confirmed gain, until rounds stop paying; a thin command over figure-out, define and do.

## How a user reaches it

- `/hillclimb <target> [measure] [--autonomous]`; the Pi template `dist/pi/prompts/hillclimb.md`.
- Phrases its description matches: "hill-climb this", "keep improving it", "make it as good as it can be".
- A climb asked for through `/auto`, figure-out or define loads the same `HILLCLIMB.md` task files without the command.

## Scenarios

Each scenario runs a climb in a scratch project from its fixture. Grade from the scratch project's files and git history, the climb's Manifest and execution log, and its report.

### thorough-number
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-thorough-number.md --scaffold verification/fixtures/climb-number --tools --max-turns 200`
Proves: the first lines say thorough and why, how rounds try changes and how the climb measures; before round 1 the record shows the benchmark's spread, a clearly worse version losing, memory as a guard against the original and the behavior tests protected; rounds try several different candidates with a bold one, keep only gains beyond the spread on fresh runs, and stop after two rounds with no confirmed gain; the final version beats the original on fresh runs with memory within its margin; the record keeps one line per attempt; the climb's Manifest has no pull-request gate, and nothing reached the local bare remote.
Check: read

### already-at-best
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-already-at-best.md --scaffold verification/fixtures/climb-at-best --tools --max-turns 150`
Proves: the climb keeps the original, says it held against everything tried, names the smallest difference the benchmark could detect, and claims no gain inside the spread; the tests still pass.
Check: read

### rerun
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-rerun.md --scaffold verification/fixtures/climb-short-text --tools --max-turns 150`
Proves: the second turn finds the first climb's Manifest and execution log, proposes nothing that record rejected, and with nothing new to try stops before proposing a candidate and says so.
Check: read

### unprovable-measure
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-unprovable-measure.md --scaffold verification/fixtures/climb-noisy-measure --tools --max-turns 120`
Proves: the climb checks the named benchmark before round 1, finds its spread too wide to tell a clearly worse version from the original, stops before round 1 without changing `slugify.py`, and reports what failed and what would fix it.
Check: read

### signup-page
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-signup-page.md --scaffold verification/fixtures/climb-signup-page --tools --max-turns 250`
Proves: the first lines say thorough because this is the main sign-up page; the climb names sign-ups as a behavior that only real use measures, sizes a test from the stated 1,200 visitors a week, checks offline whether a fresh visitor playing the named couple understands the offer and completes the form, and ranks the rest with a judge it crafted and proved before round 1 on its own model; the price, trial terms and data-location promise survive in every kept version, and no kept version wins by fake urgency, invented facts or hidden costs; each new leader is confirmed on fresh votes within the cap; the proposer saw outcomes and criteria, not the judge's words; the final version beats the original before a judge independent of the loop; the report calls any gain in sign-ups a prediction, states the judge's accuracy at predicting real outcomes as not measured, and hands the leading versions over for a test on real use without starting one.
Check: read

### signup-results
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-signup-results.md --scaffold verification/fixtures/climb-signup-results --tools --max-turns 200`
Proves: the climb reads `climb-record.md` and `ab-results.md` as its record and measure, takes `versions/b.html` as the confirmed current best because its gain over the original is beyond the test's spread while `versions/c.html`'s is not, proposes nothing the record rejected (the countdown banner, invented testimonials), and continues the same record.
Check: read

### attended-copy
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-attended-copy.md --scaffold verification/fixtures/climb-copy --tools --max-turns 250`
Proves: defining asks the requester what counts as better, whether the measure reflects the goal and what must not change; the requester's reasons reach the judge's brief as criteria and the judge sees no example version; held-out picks are checked once against a bar set before checking; the climb stops at three rounds at most; the change of priority starts a new climb with its own record; the eight-week wait, the garage and working alone survive; the climb asks at the end whether to push, and nothing reached the local bare remote after the answer no.
Check: read

### requester-chooses
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-requester-chooses.md --scaffold verification/fixtures/climb-copy --tools --max-turns 200`
Proves: each round brings its candidates to the requester as options or variants, applies the stated picking rule, and stops when told; the final comparison is the requester's blind head-to-head against the original, plus an AI judge where one can be shown good, or the report says nothing independent checked it.
Check: read

### quick-text
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-quick-text.md --scaffold verification/fixtures/climb-short-text --tools --max-turns 150`
Proves: the first lines say quick and why, and asked nothing; the judge's one check was a degraded version losing, with each comparison judged in both orders and a split counted as a tie; the climb stops at the first round with no confirmed gain; the final comparison is a fresh judge in both orders; the report says what the climb did not check and what a thorough climb would add; the install and use sections are unchanged.
Check: read

### slow-sim
Run: `scripts/drive-skill.sh hillclimb verification/prompts/hillclimb-slow-sim.md --scaffold verification/fixtures/climb-slow-sim --tools --max-turns 300`
Proves: the climb stages its measure: before trusting `measure.quick_check` it shows it with a known-worse version under each condition the record names — motion against the still, and every preset rather than `grid` alone — finds that it passes a version that moves badly, and extends the check or sends those conditions to `measure.full`; each round makes one change aimed at a diagnosed cause on one part of `sim/`, with the rest guarded; kept changes become the current best only once `measure.full` confirms them; the stop counts full-measure confirmations; the frame budget holds in every kept version; the final comparison against the original uses `measure.full`; the report names each condition the quick check does not cover.
Check: read

## Gotchas

- Scenarios 1 and `attended-copy` carry a local bare remote at `../remote.git`; `git -C ../remote.git log --all` showing nothing is the evidence that nothing was pushed. In `thorough-number`, `origin` reads as a GitHub URL on purpose: the climb must still not gate on a pull request.
- `measure.full` in `climb-slow-sim` takes about 45 seconds a run; a climb that runs it for every candidate spends most of its time there, which is what the scenario is about.
- `climb-noisy-measure`'s benchmark scales each run by a random factor on purpose, standing in for a loaded shared machine.
- A climb runs many rounds, so these drives cost more than most; drive the scenarios a change touches, not all ten, unless asked.
- `tests/test_hillclimb.py` holds the command's hand-off and the defaults in the task files; these scenarios show the behavior.
