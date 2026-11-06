# HILLCLIMB Task Guidance

Work that improves an existing artifact round after round toward a goal: each round tries
changes, measures them, and keeps one only on a confirmed gain, until rounds stop paying. The
artifact can be anything — a page, a prompt, a document, code whose speed matters, a simulation.
Composes onto `MEASURE.md` and onto the artifact's own task file (`UI.md`, `PROMPTING.md`,
`WRITING.md`, `PERF.md`, `CODING.md` …), whose gates become floors every kept version holds.

Words used below: a **climb** is the whole run; a **round** tries one or more **attempts**, each
a **candidate** version; the **current best** is the version every attempt starts from or is
compared to; the **record** lists every attempt and its result; the **spread** is how much the
measure varies between runs on the same version; the **primary** is the one objective a gain is
claimed on; a **guard** is any other objective, which may not get worse against the original by
more than its **margin** — by default no confirmed loss beyond the spread.

## Quick or thorough

A climb is **quick** by default: it infers the goal and the people served, checks its measure
once, and stops at the first round with no confirmed gain. It is **thorough** when the requester
asks, or when the session sees what is at stake: a long run (many rounds, or one that keeps
running unattended under a scheduler or coordinator), a wrong result that is costly or hard to
undo, or objectives that pull against each other. Running unattended does not by itself make a
climb thorough. The Manifest's Initial Approach opens with one line stating which it is and why,
how rounds try changes, and how the climb measures; the requester changes any of it in plain
words. The Outcome owes the best version the stop rule and the final comparison accept, or the
original kept with the evidence that nothing tried beat it — so a climb that finds no gain still
finishes.

While defining, a thorough climb settles with an attended requester what counts as better,
whether the measure reflects the goal, how objectives trade off, and what must not change; for a
goal of their own taste, or a climb they will repeat, it also takes the picks that teach and check
the judge, with the bar for the held-out picks set before checking. A quick climb asks only when
it cannot infer the goal, or for a few picks when the goal is the requester's taste.

## Choosing the measure

Name the kind of goal, since it decides what can measure it:

- **A number** — speed, size, cost, a suite's pass rate: measure it directly.
- **A behavior of the people served** — sign-ups, clicks, retention: only real use measures it.
  Offline, check what can be checked — whether a fresh visitor, played by an agent as the stated
  person, understands the offer and completes the key task, plus guards such as speed — and let
  a judge predict the rest. Any offline gain in the behavior is a prediction.
- **How well the artifact serves its people** — clarity, usefulness: an AI judge built for that
  goal and those people.
- **The requester's own taste** — an AI judge taught by their picks. A quick attended climb asks
  for a few picks with a reason each; an unattended one teaches it from the request alone and
  says so.

When no number, suite or test on real use captures the goal, an AI judge comes first: a thorough
climb lays out the measures that could serve, a quick climb takes the judge and names the
alternatives in its report. Human judgment is the measure only when the requester chooses it.
A judged climb builds, proves and votes its judge as `references/AI_JUDGE.md` beside this file
says; the gates that rest on it cite that file by its full path so the executor can read it.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Measure shown good | Before round 1 the measure is shown good for this goal and frozen with its inputs and setup until the final comparison. Thorough: each way it could rise while the goal is not served is named and guarded by a counter-measure, a guard or a protected part; a clearly worse version cannot win; a pair whose gap is about the size of the gains sought is told apart; the gain sought is recorded, the requester's or inferred and labeled so, and the pair is the original against a version with one known change of about that size; the run-to-run spread is recorded; for a number or suite, held-out cases or checks are set aside and recorded, and no round sees them. Quick: one check — a clearly worse version loses — with the spread from measuring the original twice, or from one judgment run in both orders, a split counting as a tie. A measure the requester names gets the same checks, and a mismatch with the goal is raised (attended thorough) or stated in the first lines and report (otherwise). A measure that cannot be shown good stops the climb before round 1 with what failed and what would fix it. A change to the measure or to the priority among objectives starts a new climb with its own record. The one exception is a behavior climb's hand-over to results from real use: the record marks the switch, and versions kept on the offline measure count as candidates until those results confirm them |
| Protected parts | Before round 1 the record lists what must not change: what the requester names, plus by default the artifact's facts, figures, prices, legal and required text and promises; for code, its tested behavior and public interface; and the floors of the artifact's own task-file gates, such as `review-design`'s standards for a page. Every kept version keeps them |
| Confirmed gains | A candidate replaces the current best only on a gain beyond the measure's spread, confirmed on fresh measurement; with several objectives, a confirmed gain on the primary with every guard within its margin of the original |
| Staged measure | When the full measure is slow, a cheap check screens attempts only after it has caught a known-worse version under each condition the record names as one people meet the artifact in — each class of input, setting, device or presentation, such as motion against a still, under which the cheap check could see something different. One that misses under a condition is extended or that condition goes to the full measure. Passing attempts build a pending batch on the current best that becomes the current best only once the full measure confirms it; a failed batch is traced to the change that caused it before going on. The stop rule counts full-measure confirmations. The report names each condition the cheap check does not cover |
| Stop rule | Rounds continue, each drawing on the full record, until the stop rule holds — by default two rounds in a row with no confirmed gain in a thorough climb, one in a quick climb — or a limit the requester set is reached; a behavior climb then ends with its leading versions ready for a test on real use. The round that would meet the stop rule includes a bold attempt; with one change per round, that change is the bold one. A re-run proposes nothing the record already rejected, and with nothing new to try stops before proposing |
| Final comparison | The final version beats the original head to head, on fresh measurement, before a judge independent of the loop: for a number or suite, a fresh measurement plus checks the climb did not optimize against, such as held-out cases, or in a quick climb that set none aside, a report line saying nothing independent checked it; for an AI judge, one that took no part in the rounds, with its brief fixed before round 1 — from another model family where the host offers one in a thorough climb, a fresh judge in both orders in a quick one; for the requester's own choices, their blind head-to-head plus such a judge where one can be shown good, or the report says nothing independent checked it. A staged climb compares on the full measure; several objectives are shown one by one against the original. When nothing beats the original, the climb keeps it and says it held against everything tried |
| No win by misleading | By default no kept version gains by misleading or manipulating the people served — fake scarcity, hidden costs, shaming those who decline; truthful urgency or a real cost stated plainly is fine. The requester's request, rules or context file can relax it |
| Report | Says whether the climb ran quick or thorough, how it tried changes and how it measured; lists each kept version beside the version it beat with the measured difference on each objective; says why it stopped and, where nothing beat the original, the smallest difference the measure could detect; says what taught any judge, which defaults the requester changed and what an unattended climb inferred about the goal and its people; for a quick climb, what it did not check and what a thorough climb would add; names the evidence from real use that would test the result; claims no gain beyond what was measured, calling an offline gain in a behavior a prediction |

Encode each as a judgment gate over the climb's record, which holds what those gates are judged
on. Before round 1: the measure's proof, the spread, the frozen setup, the conditions a staged
measure covers, the protected parts, any held-out set and any judge's brief. Per attempt: its
commit or other id, the version it started from, whether it was bold, the result on each
objective with its spread, any confirming measurement, and the protected-part check. Drop *Staged measure* when the full
measure is cheap, and *No win by misleading* when no people act on the artifact.

## Defaults

*Domain best practices for this task type.*

- **Try changes the way the cost of measuring allows** — When measuring is cheap, each round tries three candidates, at least one departing boldly from the current best, and more when it is cheaper still. When it is slow, each round makes one change aimed at a cause diagnosed from the raw evidence: where the gap to the goal is largest, and what produces it. On an artifact too large to vary whole, change the part whose gap matters most, change coupled parts together, hold the rest as guards, and measure the whole
- **Learn from what lost, not only that it lost** — Before proposing, read the raw evidence of each loss: outputs, traces, renders, the criteria a judge found met or missed. The work proposing changes sees which of a judge's criteria each version met or missed, not the judge's own words, wherever the host can keep the two apart, and proposes nothing the record already rejected
- **Search past the nearest peak** — Attempts differ from each other and from everything the record holds. A bold attempt may start from a runner-up rather than the current best. When greedy rounds stall, keep a few different runners-up as starting points. Drop an attempt clearly losing early, before its full measurement; the floor on attempts governs declaring a win, not dropping a clear loser
- **One primary, the rest guards** — With several objectives, one is primary, every other is a guard whose margin is by default no confirmed loss beyond the recorded spread against the original, and what no measure covers is protected. Never invent weights. Alternatives, each when it fits: a few finalists the requester chooses among by comparing whole versions (attended, no primary); improvement over the original on every objective with the final pick by its worst one (unattended, no primary); a weighted sum normalized to the original, only when the requester states exchange rates over the real ranges; floors that veto; a level past which an objective is enough and becomes a guard; reducing the objectives when there are more than three or four
- **A behavior goal climbs offline first** — Climb on what can be checked plus a judge's prediction, and end with the leading versions ready for a test on real use. Start no such test unless the requester asks. A later run reads its results as the measure and continues the record
- **Size a test on real use before proposing one** — From how many people the artifact reaches and its current rate, state the smallest gain the test could detect and how long it would run; where only large gains are detectable, prefer versions bold enough to reach them, and read results with a test that allows looking before the end. Never show such a test good by putting a deliberately worse version before real people
- **Keep the record bounded and findable** — One line per attempt: what changed, the result on each objective, kept or why not. Past 50 lines, append one summary line per older round, which readers take in place of that round's losing attempts; kept versions, confirmations and what was recorded before round 1 are read in full. The record lives in the climb's execution log, or in a file in the project the requester names, which lets a re-run on another machine find it; the Manifest names where. A re-run finds it for this target, plus the pull request description where the work was pushed and any results from real use the requester supplies
- **Push only when asked** — Push or open a pull request only when the requester asks, in the request, their rules or their context file, even where the project's `origin` is on GitHub; the climb's Manifest carries no pull-request gate otherwise. An attended climb asks at its end; an unattended one keeps its commits local and says so
- **Every number here is a default** — The requester's words replace any of them, and the report names each one changed
