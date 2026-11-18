---
name: evaluation-principles
description: 'Evaluation principles for manifest-dev: how its maintainer wants measurements — behavior drives, eval suites, design-instrument experiments and hill-climbs — designed, run and read, and why. Use before planning, running, reading or reviewing an evaluation, or a choice between versions on a measured result, in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Settle a prompt change on one run per arm and accept the noise: each touched case once on the skills before the change and once after, adding runs only where that pair does not settle it — a must-catch case passes or fails on both arms, or a verdict is borderline — every run is a paid model session and more runs get expensive, while one pair is good enough once its noise is accepted. Yields when the decision would be costly to reverse and rests on one borderline pair, or when the maintainer asks for a fuller measurement.
- What would change the decision is written down before the first run whose result could change it, where its date shows it came first — the measure, the pass rule, how many runs, and when to stop or add more — a bar fixed after seeing the numbers approves whatever came out, and adding runs until a result looks right finds what was hoped for. Yields for runs that only calibrate the measure — its spread, or whether it can fail — which decide nothing.
- A measure is first shown to flag an example already known to be worse, or made worse on purpose, and that run is shown with the result — a measure no one has seen fail may be incapable of failing. Yields when no worse example exists or can be made; then the result is reported as a proxy, and no keep-or-discard decision rests on it alone.
- A claim about what one change did rests on arms that differ in that change alone — when two things change at once, nobody can tell which one moved the number. Yields when only the combination will ship; then the combination is judged and nothing is claimed for its parts.
- A comparison runs on inputs, load and configuration resembling what the thing will meet in use, and a baseline is built only from runs made under matching conditions — otherwise the gap reflects the data rather than the change. Yields when nothing comparable exists yet; then the result is named a proxy.
- A score counts only what the candidate itself produced: the run's actual behavior, rather than its label or configuration, shows that the new path executed with nothing standing in for it, and failures of the harness are tallied separately from failures of the candidate, with both reported — a score a fallback helped produce says nothing about the candidate, and a harness crash charged to it blames it for nothing it did. Yields for parts that match on every arm and are too few to sway the decision.
- Before anyone acts on a number that moved, the items behind the movement are read and sorted by cause, and that sorting is shown with the decision — an improvement may be incidental, and a drop may be exactly what a deliberate change intended. Yields when no reading of the items could change the decision.
- What a change is for sets its bar: a bet on quality has to show an improvement, a simplification only has to avoid getting worse, and a narrow fix has to reach its targets without losing elsewhere — a bar sized for improvements turns down every change whose value lies somewhere else. Yields to a safety floor, which holds whatever a change is for.
- Quality, cost and time are counted over everything one task sets off, not over one call or step — the people waiting and the budget paying feel the total. Yields when the work is diagnosing a single step.
- Nothing is tuned on the data that scores it: a set held back from tuning, named in the result, judges it — a score on data that shaped the change measures recall, not improvement. Yields when no data can be held back yet; then the score is reported as in-sample.
- Each run keeps its raw outputs and its exact settings, so its result can be scored again under a new rule — a result that cannot be scored again cannot be checked or reused. Yields where the outputs hold personal data the project may not keep; then only what it may keep is stored.

Before calling evaluation work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
