---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project's context file records the newest surfaces version
(`<!-- setup-project surfaces v5 -->`). Its decision record has no `Enforced by` field, though
`src/store.py` cites it, and the project has no verification harness: the user declined those
when the setup was last updated, and its context file records the project's own way of verifying. A recorded version that is the newest means the setup is
current, and what the user declined stays the project's choice.

**First, list** what the reply offers to add or change in the project's setup.

**Then judge.** FAIL if the reply offers any of these:

- A setup update or a setup-project run
- An `Enforced by` backfill for the existing record
- A verification harness or recipes, whether as a setup item or as part of the change
- A redo of the glossary, North Star, or conventions

PASS otherwise. A proposal to add a check in the project's own form while doing the recommender
change is that change's own work, not a setup offer, even when the reply does not say it is scoped
to the change.
