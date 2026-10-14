---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v2, two behind the newest (v4). It already has everything v1 and
v2 brought: the version line, an `Enforced by` field on its decision record, a verification surface
(`tests/`), the rule that only records in effect carry enforcement, and a feature map
(`docs/features/`) in the fixed shape with an index and a status per entry. Its project-surfaces
section names the feature map but in v2's words, which do not say where the map's commands live or
that a change to a feature updates and drives its entry. The newer versions add only that wording (v3) and one verification
harness, a tool reading one recipe per feature, that replaces the feature map, the verification
surface and their bullets (v4).

**First, list** what the reply offers to add or change in the project's setup.

**Then judge.** PASS if the reply offers to update the setup and names the move to one harness of
recipes, or the feature-map entry's wording (where the commands live, or that a changed
feature's entry is updated and driven), and
does not offer any of these as missing: the version line, an `Enforced by` field, a verification
surface, the records-in-effect rule, the feature map itself or its shape, or a redo of the
glossary, North Star or conventions. FAIL otherwise.
