---
name: hillclimb
description: 'Improve an existing artifact round after round toward a goal — a page, a prompt, a document, code whose speed matters, a simulation — keeping a change only when it measures better, until rounds bring no confirmed gain. Runs figure-out, define and do; quick by default, thorough when asked or when the stakes call for it. Use when the user asks to hill-climb, optimize, keep improving or make something as good as it can be for its goal, or to continue an earlier climb.'
argument-hint: '<target> [goal and measure] [--autonomous]'
user-invocable: true
---

Hill-climb the target the arguments name toward the goal they state, in the requester's words,
with any measure or results from real use they bring. With no target given or inferable, halt with
usage.

This command holds no loop of its own: it is the same request made to figure-out, define and do,
whose task files for climbs say what a climb owes. Tell each that this is a hill-climb on the
target, and pass the request as given. A climb continuing an earlier one names that climb's
Manifest or record, found through the execution logs that name this target or the record the
requester points to.

- **Attended:** invoke `figure-out` with the request, then `define`, with the requester taking part.
- **With `--autonomous`:** invoke `figure-out --autonomous` where shared understanding is missing,
  then `define --autonomous`. Nobody is asked from start to end.

Do not set or print a continuation goal during understanding or definition, and tell figure-out
that it runs chained under this command, which continues from its Read as a checkpoint: /do owns
the completion backstop, and automatic continuation begins at execution.

When `define` reports the Manifest path, invoke `do` with that exact path in the same turn, unless
the requester asked to stop at the plan. No path → stop and report. An attended climb asks at the
end whether to push, unless the requester already said.
