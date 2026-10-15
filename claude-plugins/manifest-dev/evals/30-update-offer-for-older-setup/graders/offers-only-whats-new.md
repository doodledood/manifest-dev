---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project was set up by an older version: it has a glossary, a North Star, ADR
conventions and a project-surfaces section, but the section records no surfaces version and
the project has no way to check its work.

**First, list** what the reply offers to add or change in the project's setup, and how it
describes the way the project would check its work.

**Then judge:** PASS if all of these hold:
- the reply offers to update the setup, naming items the newer setup adds — a version line, an
  `Enforced by` field for decision records, or a verification harness (one command, such as
  `scripts/verify`, with a recipe per thing it checks);
- where it offers a way to check the project's work, that is the harness — never a
  verification-surface document, a feature map (one entry per feature under `docs/features/` or
  `verify/features/`) or reader-task files kept beside or instead of it, the shapes earlier
  versions shipped and the newest replaced;
- it does not offer to redo setup the project already has (re-creating the glossary, North Star,
  or conventions from scratch). Offering to install a surface the project lacks, such as a
  conventions file it does not have, is an update item, not a redo.

FAIL otherwise.
