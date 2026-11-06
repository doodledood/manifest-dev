---
name: hillclimb
description: 'Improve an existing artifact round after round toward a goal — a page, a prompt, a document, code whose speed matters, a simulation — keeping a change only when it measures better, until rounds stop paying. Runs figure-out, define and do; quick by default, thorough when asked or when the stakes call for it. Use when the user asks to hill-climb, optimize, keep improving or make something as good as it can be for its goal, or to continue an earlier climb.'
argument-hint: '<target> [measure] [--autonomous]'
user-invocable: true
---

Climb the target the arguments name: a file, a folder, a page, a prompt, a component. With no
target given or inferable from the conversation, halt with usage. The rest of the arguments say
the goal and, if the requester has one, the measure, in their own words; results from a test on
real use, such as an earlier A/B test, may come with them.

This command holds no loop of its own. figure-out, define and do run the climb, and their task
files for climbs and measured comparisons say how: what counts as better, how rounds try changes,
when a gain is confirmed, and when to stop. Pass every handoff the request as given, the
requester's words on the goal and the measure, and these limits:

- **The assignment** is to improve the target toward the goal, inside what the climb protects.
  It does not authorize a push, a pull request, publishing, or a test that puts versions before
  real people, unless the requester asks for it in the request, their rules or their context file.
- **Quick or thorough.** A climb is quick unless the requester asks for a thorough one or the
  request shows what is at stake: a long run, such as many rounds or one that keeps running
  unattended under a scheduler or coordinator; a wrong result that is costly or hard to undo; or
  objectives that pull against each other. `--autonomous` alone does not make a climb thorough.
  Pass your reading on; defining may revise it as it learns the artifact.

**Without `--autonomous`:**

- A **thorough** climb: invoke `figure-out` with the climb request, then `define`, with the
  requester taking part — they settle what counts as better, whether the measure reflects the
  goal, how objectives trade off, and what must not change.
- A **quick** climb: ask the requester only when the goal cannot be inferred from the request and
  the target, then invoke `define` with `--autonomous`.

**With `--autonomous`:** invoke `figure-out` with `--autonomous` where shared understanding is
missing, then `define` with `--autonomous`. Nobody is asked from start to end.

The request to climb is the request to run it: when `define` reports the Manifest path, invoke
`do` with that exact path in the same turn, unless the requester asked to stop at the plan. No
path → stop and report. Before the first round, tell the requester the Manifest's opening line:
quick or thorough and why, how rounds try changes, and how the climb measures. They change any
of it in plain words; a change goes to `define` as an amendment.

When `do` finishes, an attended climb asks whether to push the result, unless the requester
already said. An autonomous climb with no instruction to push keeps its commits local and says so.

**A re-run** on a target already climbed continues that climb: `define` finds its Manifest and
execution log, and any results from real use the requester supplied become the climb's measure.
