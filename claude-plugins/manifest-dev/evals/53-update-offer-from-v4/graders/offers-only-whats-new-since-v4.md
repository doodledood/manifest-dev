---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v4, one behind the newest (v5). It already has everything v1
to v4 brought: the version line, an `Enforced by` field on its decision record, the
records-in-effect rule, and one verification harness (`scripts/verify`, `verification/harness.md`,
three recipes with evidence, and the v4 verification bullet). The harness has no control
commands: the overdue page is started by `scripts/serve.sh` on fixed port 8000 and stopped by
`scripts/stop.sh`. The `full-suite` recipe is marked ask-first only because it takes fifteen
minutes. What v5 adds: control commands declared in `harness.md` with a per-run identity in place
of the fixed port, failure logs in evidence, time lines on durations, one summary per scenario,
`verify affected`, the ask-first mark narrowed to cost, and the bullet's new wording.

**First, list** what the reply offers to add, change or remove in the project's setup.

**Then judge.** PASS only if all of these hold:

- It offers to update the setup to v5, naming at least two of: control commands for the overdue
  page (or replacing the fixed port with a per-run one), removing the run-time-only ask-first mark
  from `full-suite`, the updated tool, and the bullet's new wording.
- It does not offer, as missing, anything v1 to v4 already gave: the version line, an `Enforced
  by` field, the records-in-effect rule, a verification harness or `scripts/verify` as something
  new, moving a feature map or reader tasks into recipes, or a redo of the glossary, North Star or
  conventions.

FAIL otherwise.
