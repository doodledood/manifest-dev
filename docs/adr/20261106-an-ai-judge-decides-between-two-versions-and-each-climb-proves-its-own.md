# ADR: An AI judge in a hill-climb decides between two versions, and each climb builds and proves its own

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user ruled five things: the judge decides between A and B with the goal, the people and their moment in front of it; it sees no example versions; it serves any kind of artifact; its form stays flexible, with the research as nudges and probes for each task; and no judge is built in and no study of judges ships. The user also chose to turn the research's guards into probes that are off until a climb's own proof shows they are needed. The agent drafted the proof, voting and teaching practices below from the research note `docs/research/hillclimb-ai-judges-20261106.md`.

## Context
Some goals have no number. Does a page serve the people arriving at it? Does a document answer its reader? Do a prompt's outputs read the way the task needs? For goals like these, the measure is a model's judgment.

A model's judgment is noisy and biased in known ways, all reported in `docs/research/hillclimb-ai-judges-20261106.md`:
- **Position.** Verdicts flip when the two versions swap places, most often on close pairs.
- **Self-preference.** Some judges favour their own model's outputs.
- **Spurious features.** Pairwise verdicts are swayed by length, assertiveness and flattery, the very features a climb tends to produce.
- **Missed drops.** Judges miss a quality drop inside a version they otherwise prefer in more than half of targeted perturbations.
- **Reward hacking.** A loop that optimizes against a judge finds what the judge rewards but the goal does not, and the exploits transfer across model families.

Context and structure help: assessing each version against the goal before deciding the pair, committing to criteria first, evidence before the verdict, and grounding the people in their own words. How large each failure is depends on the model, the artifact and the goal, and changes with each model generation. A study shipped with the plugin would measure one model on one set of artifacts and age with them.

## Decision
- **The judge decides between two versions.** Each comparison ends with a verdict: which version better serves the stated goal for the stated people in their moment, or a tie. Before the verdict, the judge may assess each version alone in the form the task calls for: criteria met or missed, a score per criterion, or none. `define/tasks/references/AI_JUDGE.md` gives the research as nudges for choosing the form.
- **It sees no example version.** Neither a target to imitate nor a past pair as a worked example: an example pulls every candidate toward itself. A requester's reasons reach the judge only as criteria.
- **No judge is built in, and no study of judges ships.** Each climb crafts its judge for its goal and people, and proves it before round 1 on the model the climb runs. A quick climb checks only that a degraded version loses, and decides each comparison by one judgment run in both orders, a split counting as a tie. A thorough climb also checks that a pair about the size of the gains sought is told apart, the gain sought recorded and the pair built from one known change of that size, and that identical versions tie, one copy labeled the newer, and records order flips and run-to-run noise. A judge that fails its proof stops the climb before round 1.
- **The research's guards are off by default.** Hiding which version is newer and who made it, checking protected parts inside each comparison, a fresh judge per vote, judging both orders in a thorough climb's votes, and several rendered states of a page are probes. A climb's proof turns each on where it shows the failure that guard prevents, and the requester can ask for any of them. Protected parts are checked on every kept version regardless, outside the judge.
- **Votes stop at a clear lead or a cap, after a minimum.** In a thorough climb, from the recorded noise and the cost of a vote, the proof sets a minimum number of votes, the lead that counts as clear, and a cap; votes run to the minimum, so an early lucky lead cannot end a comparison, then continue until the lead is reached or the cap. A result short of clear is a tie that keeps the current best. A new leader is confirmed on fresh votes.
- **What teaches the judge follows the kind of goal.** A thorough climb offers calibration to the requester's picks for their own taste or for a climb they will repeat: the reasons behind some picks become criteria, and the rest are held out and checked once against a bar set before checking. A climb toward a behavior proves its judge on the requester's past results from real use where they exist, and otherwise calls the judge's ranking a prediction. An unattended climb uses only what the request holds and says so.
- **The proposer sees outcomes and criteria, never the judge's words.** Where the host can run the judge in a separate context it does; where it cannot, the report says so.

## Alternatives Considered
- **No scores at all.** Not chosen: a score per criterion before the verdict suits some tasks, and the research does not favour one form for every task. The verdict stays between versions, because a comparison is a question the judge can answer where an absolute score drifts across calls.
- **A built-in judge, measured once on pairs with known winners before it ships.** Not chosen: it would measure one model on one set of artifacts, age with each model generation, and add machinery every climb carries. A per-climb proof on the climb's own model checks the judge where it is used.
- **Every guard on by default.** Not chosen: each guard multiplies the cost of every comparison, and the proof shows which failures this model and task actually have.
- **Example or reference versions as anchors.** Not chosen: the climb then moves toward resembling the example instead of serving the goal.

## Consequences

### Positive
- Any climb can use a judge on the day it is needed, proven on the model it runs.
- Each guard earns its cost by a failure the proof saw.
- A judge's brief is kept in the climb's record, so a re-run reuses it.

### Negative
- A quick climb's single check can pass a judge that a thorough proof would reject; the quick climb's report says what it did not check.
- A judge without results from real use cannot know what people will actually do, so a climb toward a behavior ends with a prediction until a test on real use runs.

## Enforced by
`tests/test_hillclimb.py` (`test_the_judge_decides_between_versions_sees_no_examples_and_keeps_guards_off`) fails when the judge reference drops the verdict between versions, the ban on examples, the per-climb proof or the guards' off default. Whether a judge fits its task stays judgment, read in the `hillclimb` recipe's judged scenarios.

## Revisit when
Climbs' final checks or later results from real use overturn their judges' winners more often than they confirm them; read in the climbs' reports and execution logs.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Research: `docs/research/hillclimb-ai-judges-20261106.md`.
- Related: 20261106-a-climb-designs-its-measure-and-search-for-its-task, 20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record, 20260901-design-skill-pair-distills-research-eval-deferred
