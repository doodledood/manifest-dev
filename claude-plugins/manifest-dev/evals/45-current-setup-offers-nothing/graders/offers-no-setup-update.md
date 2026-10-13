---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project's context file records the newest surfaces version
(`<!-- setup-project surfaces v1 -->`). Its decision record has no `Enforced by` field, though
`src/store.py` cites it, and the project has no verification surface: the user declined those
when the setup was last updated. A recorded version that is the newest means the setup is
current, and what the user declined stays the project's choice.

**First, list** what the reply offers to add or change in the project's setup.

**Then judge:** PASS if the reply treats the setup as current and does not offer a setup update,
a setup-project run, an `Enforced by` backfill for the existing record, a project-wide
verification surface installed as a setup item, or a redo of the glossary, North Star or
conventions. Proposing to build checks or a verification surface scoped to the recommender
change, as part of that change's work, is not a setup offer. FAIL if the reply offers any of the
setup items above.
