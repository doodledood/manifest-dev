---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v1, three behind the newest (v4). It already has everything v1
brought: the version line, an `Enforced by` field on its decision record, and a verification
surface (`verify/`, a harness and feature map with statuses and a README). Its feature map is
loose: no index, and each feature file is a few bullets with no fixed sections. What the newer
versions add: an audit of the whole setup with each gap offered; judging a verification surface
by a cold proof run and its other jobs; a fixed feature-map shape (an index, one file per
feature with fixed sections and a status line, an `unreachable` status); the rule that only
records in effect carry enforcement; and (v4) one verification harness, a tool reading one
recipe per feature, that replaces the verification surface and the feature map.

**First, list** what the reply offers to add or change in the project's setup.

**Then judge.** PASS if the reply offers to update the setup and names at least one item the
newer versions add — the move to one harness of recipes, the feature-map shape, a proof run of
the verification surface, the records-in-effect rule, or the setup audit — and does not offer any of these as missing: the
version line, an `Enforced by` field for the existing record, a verification surface, or a
redo of the glossary, North Star or conventions. FAIL otherwise.
