---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v2, three behind the newest (v5). It already has everything v1 and
v2 brought: the version line, an `Enforced by` field on its decision record, a verification surface
(`tests/`), the rule that only records in effect carry enforcement, and a feature map
(`docs/features/`) in the fixed shape with an index and a status per entry. Its project-surfaces
section names the feature map but in v2's words, which do not say where the map's commands live or
that a change to a feature updates and drives its entry. The newer versions add only that wording (v3) and one verification
harness, a tool reading one recipe per feature, that replaces the feature map, the verification
surface and their bullets (v4). v5 then adds control commands, time lines and failure logs to that harness; offering them with
the harness is fine.

**First, list** what the reply offers to add or change in the project's setup.

An update goes straight to the newest version: v4 replaces the feature-map bullet, so offering
v3's wording for it is offering a shape the project would only have to move out of again.

**Then judge.** PASS only if all of these hold:

- It offers to update the setup, and offers the move of the feature map and `tests/` surface into
  one harness of recipes.
- It does not offer v3's feature-map bullet wording, or keeping the feature map beside the
  harness.
- It does not offer as missing what the project has: the version line, an `Enforced by` field,
  the records-in-effect rule, or a redo of the glossary, North Star or conventions.

FAIL otherwise.
