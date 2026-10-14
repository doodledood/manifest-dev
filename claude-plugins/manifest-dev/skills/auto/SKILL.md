---
name: auto
description: 'End-to-end autonomous execution: figure-out → define → do, chained without manual approval gates. Use when you want to define and execute without intervention during planning, when the user asks for autonomous or end-to-end work, or asks to go from idea to done without approval gates.'
argument-hint: '<task>'
user-invocable: true
---

Run the flow for the task given or inferable from the conversation; with
neither, halt with usage.

Where shared understanding is missing, invoke figure-out with the task and
`--autonomous`; invoke define with `--autonomous`; invoke do with the exact
Manifest path define reports. No path → stop and report.

figure-out and define each end by stopping and leaving the next step to their
caller. You are that caller: figure-out's read and define's handoff are
checkpoints that return control to this flow, so invoke the next step in the
same turn rather than ending it or offering the step to the user. The run ends when do finishes or escalates, or
when define reports no path.

The chain runs the same with or without a project — a chat with no workspace, a home or
scratch folder. Each skill it invokes decides which project surfaces apply there.

Do not set or print a continuation goal during understanding or definition.
/do owns the completion backstop. Automatic continuation begins at execution;
an interrupted earlier phase must be restarted by the caller.
