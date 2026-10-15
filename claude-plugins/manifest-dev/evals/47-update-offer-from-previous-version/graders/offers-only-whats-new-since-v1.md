---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v1, four behind the newest (v5). It already has everything v1
brought: the version line, an `Enforced by` field on its decision record, and a verification
surface (`verify/`, a harness and feature map with statuses and a README). Its feature map is
loose: no index, and each feature file is a few bullets with no fixed sections. What the newer
versions add: an audit of the whole setup with each gap offered; judging a verification surface
by a cold proof run and its other jobs; a fixed feature-map shape (an index, one file per
feature with fixed sections and a status line, an `unreachable` status); the rule that only
records in effect carry enforcement; and (v4) one verification harness, a tool reading one
recipe per feature, that replaces the verification surface and the feature map. v5 then adds control commands, time lines and failure logs to that harness; offering them with
the harness is fine.

**First, list** what the reply offers to add or change in the project's setup.

An update goes straight to the newest version: the v2 feature-map shape and the v3 bullet wording
were replaced by v4, so offering either is offering a shape the project would only have to move
out of again.

**Then judge.** PASS only if all of these hold:

- It offers to update the setup, and offers the move of `verify/` into one harness of recipes.
- It does not offer the fixed feature-map shape, a feature-map index, a feature-map bullet, or a
  proof run of the old verification surface as something to add.
- It does not offer as missing what the project has: the version line, an `Enforced by` field
  for the existing record, or a redo of the glossary, North Star or conventions.

FAIL otherwise.
