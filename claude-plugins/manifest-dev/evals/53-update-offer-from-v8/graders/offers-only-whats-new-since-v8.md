---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v8, one behind the newest (v9). It already has everything v1
to v8 brought: the version line, an `Enforced by` field on its decision records, the
records-in-effect rule, one verification harness (`scripts/verify`, `verification/harness.md`
with `start`, `logs` and `stop` control commands on a per-run identity, two feature recipes), a
`project-checks` recipe running its tests and linter, the verification bullet, each time line as a
`Line:` field in its recipe, no committed evidence, a North Star in six sections (*Purpose*,
*Goal*, *Principles*, *How we know*, *What this rests on*, *Open*) with a *Strategy choices in
force* list, the `Strategy` area in its ADR conventions, and its newsletter channel already in a
`Strategy` decision record. Its *Purpose* opens with a barrier (clubs losing track of loans), its
*Goal* lists features, and its *How we know* counts how often those features are used, with no
measure of the end they serve. What v9 adds: a *Purpose* that opens with the end the person is
after, found by asking the owner, with the barrier kept as one thing in its way; a *Goal* and
measures tested against that end, the end getting a measure of its own; a `Revisit when` signpost
on decision records that the strategy list shows; a note in the ADR conventions that a record
whose decision sits outside the *Purpose* says so in its context; and a check that rebuilds the
ADR index and the strategy list.

**First, list** what the reply offers to add, change or remove in the project's setup.

**Then judge.** PASS only if all of these hold:

- It offers to update the setup to v9, naming the change to the *Purpose* (opening with the end,
  or asking the owner for the end, rather than with the barrier) and at least one of: the
  `Revisit when` signpost or the strategy list showing it; the outside-Purpose note in the ADR
  conventions; or the check that rebuilds the index and the list.
- It leaves the *Purpose*, *Goal* and measure changes for the user to rule on rather than
  presenting them as done or as something it will write without asking, and it does not state a
  `Revisit when` condition for the newsletter record as settled without the user giving one.
- It does not offer, as missing, anything v1 to v8 already gave: the version line, an `Enforced
  by` field, the records-in-effect rule, a verification harness or `scripts/verify` as something
  new, control commands or a per-run identity, a recipe for the tests or the linter, moving time
  lines into recipes, removing committed evidence, reshaping the North Star into the six sections,
  the `Strategy` area, or moving the newsletter channel out of the North Star.

FAIL otherwise.
