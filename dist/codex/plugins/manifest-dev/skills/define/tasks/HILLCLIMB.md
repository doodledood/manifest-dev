# HILLCLIMB Task Guidance

Work that improves an existing artifact round after round toward a goal — a page, a prompt, a
document, code whose speed matters, a simulation — keeping a change only on a confirmed gain,
until rounds bring no confirmed gain. Composes onto `MEASURE.md` and onto the artifact's own task
file, whose gates become floors every kept version holds.

A climb is **quick** by default and **thorough** when the requester asks or the stakes show: a
long or unattended run, a worse result that is costly once the artifact is in use — judged by what
it is for, not by how easily its commits revert — or objectives that pull against each other.
Running unattended does not by itself make a climb thorough. The Manifest's Initial Approach opens
with one line saying which and why, how rounds try changes, and how the climb measures. A thorough
climb settles with an attended requester what counts as better and what must not change; a quick
one asks only what it cannot infer.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Measure shown good | Before round 1 the measure — a number, a suite, results from real use, or an AI judge comparing two versions — is shown to serve the goal and is then held fixed until the final comparison. An AI judge is shown no example version to imitate, and before use it prefers the original over a version made clearly worse. A thorough climb also shows the measure separates a gap about the size of the gain sought and guards each way it could rise while the goal is not served; its AI judge also ties identical versions and keeps its verdict when the two swap places. A measure that cannot be shown good stops the climb before round 1, saying what failed and what would fix it. A change to the measure or to the priority among objectives starts a new climb; results from real use replacing an offline measure continue the same one |
| Confirmed gains | A version replaces the current best only on a gain beyond the measure's noise, confirmed on fresh measurement, with every other objective no worse than the original beyond its noise. A gain far larger than expected is checked for a fault in the measure or the version before it is kept. A cheap stand-in for a slow measure screens versions only after it catches a known-worse version under each condition people meet the artifact in; the full measure confirms what it passes |
| Protected parts | What the requester names, and by default the artifact's facts, figures, prices, required text, tested behavior and public interface, survive in every kept version |
| Stop rule | Rounds draw on the record of every attempt so far and continue until two rounds in a row bring no confirmed gain in a thorough climb, one in a quick climb, or a limit the requester set is reached. The last round before stopping includes a bold attempt. A re-run continues the earlier record and proposes nothing it rejected |
| Final comparison | The final version beats the original on fresh measurement before a judge that took no part in the rounds — for a number or suite, cases no round saw. When nothing beats the original, the climb keeps it and says it held against everything tried |
| No win by misleading | No kept version gains by misleading or manipulating the people served — fake scarcity, hidden costs, shaming those who decline. The requester's request, rules or context file can relax it |
| Report | Says quick or thorough and why, what was kept against what it beat on each objective, why the climb stopped, what taught any judge, and which defaults the requester changed. Claims no gain beyond what was measured; an offline gain in a behavior only real use shows, such as sign-ups, is a prediction |

Encode each as a judgment gate over the climb's record. Drop *No win by misleading* when no people
act on the artifact.

## Defaults

*Domain best practices for this task type.*

- **Try changes the way the cost of measuring allows** — When measuring is cheap, each round tries three candidates, at least one bold; when it is costly, each round makes one change aimed at a diagnosed cause
- **One primary, the rest guards** — With several objectives, a gain is claimed on one; the others may not get worse against the original. Never invent weights
- **A behavior goal climbs offline first** — A behavior of the people served, such as sign-ups, is climbed on what can be checked offline plus a judge's prediction, and ends with the leading versions ready for a test on real use; start no such test unless the requester asks
- **Extra judge guards stay off until needed** — Hiding which version is newer, a fresh judge for each vote, and both orders in every vote are turned on only where the judge's proof shows the failure each prevents, or the requester asks
- **Keep the record findable** — The record of every attempt lives in the execution log, or in a project file the requester names; a climb pointed to an earlier record continues that file. The Manifest names where
- **Push only when asked** — Push or open a pull request only when the requester asks, in the request, their rules or their context file; the climb's Manifest carries no pull-request gate otherwise
- **Every number here is a default** — The requester's words replace any of them, and the report names each one changed
