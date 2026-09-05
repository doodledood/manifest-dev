---
name: just-auto
description: 'Goal-based autonomous chain: figures out the task, encodes a Manifest, and pursues it end-to-end with full autonomy and minimal process. Use when the user asks to just build it, just auto it, run end-to-end goal-based, or go from idea to done without approval gates.'
argument-hint: '<task>'
user-invocable: true
---

Run the flow for the task given or inferable from the conversation; with
neither, halt with usage.

Where shared understanding is missing, invoke just-figure-out with the task and
`--autonomous`; invoke just-define; invoke just-do with the exact Manifest path
just-define reports. No path → stop and report.

Do not set or print a continuation goal during understanding or definition.
/just-do owns the completion backstop. Automatic continuation begins at execution;
an interrupted earlier phase must be restarted by the caller.
