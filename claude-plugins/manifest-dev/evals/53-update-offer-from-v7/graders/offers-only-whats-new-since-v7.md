---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v7, one behind the newest (v8). It already has everything v1
to v7 brought: the version line, an `Enforced by` field on its decision record, the
records-in-effect rule, one verification harness (`scripts/verify`, `verification/harness.md`
with `start`, `logs` and `stop` control commands on a per-run identity, two feature recipes), a
`project-checks` recipe running its tests and linter, the v6 verification bullet, each time line
as a `Line:` field in its recipe, and no committed evidence. Its North Star is in the older form:
a *Who it's for* section, a *How they arrive* section that names a chosen channel (the library
network's newsletter, one release note a month, no website), and a *Never* entry. What v8 adds:
the North Star reshaped into the newer sections, holding only what decisions are judged against,
with a chosen option such as that channel moved to a decision record, on the owner's ruling; the
`Strategy` area reserved in the project's ADR conventions; and the North Star line of the context
file reworded.

**First, list** what the reply offers to add, change or remove in the project's setup.

**Then judge.** PASS only if all of these hold:

- It offers to update the setup to v8, naming the North Star reshape, and at least one of: the
  `Strategy` area in the ADR conventions, and the reworded North Star line in the context file.
- Where it says what happens to the newsletter channel, it moves it to a decision record or out of
  the North Star, rather than keeping it as a position; and it leaves the reshape for the user to
  rule on rather than presenting it as done or as something it will write without asking.
- It does not offer, as missing, anything v1 to v7 already gave: the version line, an `Enforced
  by` field, the records-in-effect rule, a verification harness or `scripts/verify` as something
  new, control commands or a per-run identity, a recipe for the tests or the linter, moving time
  lines into recipes, or removing committed evidence.

FAIL otherwise.
