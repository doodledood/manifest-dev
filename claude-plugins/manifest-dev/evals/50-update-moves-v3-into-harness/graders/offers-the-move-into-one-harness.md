---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project records surfaces version v3, one behind the newest (v4). It has everything v1 to v3
brought: the version line, an `Enforced by` field on its decision record, the records-in-effect
rule, a test suite, a feature map (`docs/features/`, three entries, one verified with evidence and
one carrying a project-specific *Club notes* section), a reader-task list
(`docs/reader-tasks/TASKS.md`, two tasks, one verified with evidence) and context-file bullets for
the verification surface, the feature map and the reader tasks. v4 replaces those pieces with one
verification harness: a command-line tool reading one recipe per feature or document task.

**First, list** what the reply offers to add, change or remove.

**Then judge.** PASS only if all of these hold:

- It offers moving the feature map and the reader tasks into one harness of recipes — one per
  feature-map entry and one per reader task — rather than adding a harness beside them.
- It says the existing content carries over: at least one of the entries' drive steps, the
  *Club notes* section, or the existing evidence.
- It offers replacing the context file's verification bullets with a single one.
- It does not offer, as missing, anything v1 to v3 already gave: the version line, an `Enforced
  by` field, the records-in-effect rule, the feature map's fixed shape, the v3 feature-map bullet
  wording, or a redo of the glossary, North Star or conventions.

FAIL otherwise.
