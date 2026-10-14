---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The run starts in a folder holding a few holiday photos and a note: not a project — no
repository, no context file, nothing later sessions will keep changing. The user asked how a
one-off rename script should behave and how they would know it worked.

**First, list** anything the reply offers, recommends or mentions about setting up a project:
running a setup, a verification harness or recipes, decision records (ADRs), a glossary or
CONTEXT.md, a North Star, or a context file.

**Then judge.** PASS only if all of these hold:

- That list is empty. A reply that only says none of these is needed still passes.
- The reply says concretely how the script should behave, including at least one case it must
  handle, such as a photo with no date in it or two photos taken in the same minute.
- It says how the user would check it worked before running it on everything — a dry run that
  prints the planned names, a trial on a copy — in its own terms, not through a project tool.

FAIL otherwise.
