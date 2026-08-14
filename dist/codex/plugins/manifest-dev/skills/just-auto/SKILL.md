---
name: just-auto
description: 'Goal-based autonomous chain: figures out the task, encodes a
Manifest, and pursues it end-to-end with full autonomy and minimal process.
Use when the user asks to just build it, just auto it, run end-to-end
goal-based, or go from idea to done without approval gates.'
argument-hint: '<task>'
user-invocable: true
---

Run the full flow for the given task — stated as an argument or inferable
from the conversation; with neither, halt with usage.

Before starting, arm the completion backstop. If an active goal's completion
condition already covers this task's outcome, continue under it. Otherwise,
if the harness provides a goal-setting, continuation, or
durable-completion-condition capability, set this goal, with `<task>`
replaced by a one-line statement of the task: "For the task <task>: shared
understanding is reached — where figure-out runs, a full-anatomy
Read checkpoint is completed before define runs: every load-bearing branch
pressed, independent re-derivation run or explicitly unavailable, the rival
set no longer moving; a missing or weak Read checkpoint is a defect to repair
before define, not a terminal failure after gates pass — a Manifest is written from it, every Acceptance Criterion and Global
Invariant in that Manifest holds with evidence from the artifacts they name,
and completion has been reported. The Manifest, once written, is canonical
and read-only. Record compact checkpoint notes as work proceeds — what
changed, what was verified, what remains, blockers. Record the Manifest's path in a checkpoint note as soon as it is
written. Stop only when blocked on something a person must resolve." If it
provides none, print that goal in
copy-pasteable form for the user's own continuation mechanism and proceed.

Then: if the conversation lacks shared understanding of the task, first
invoke the manifest-dev:figure-out skill with the task and `--autonomous`.
Invoke the manifest-dev:define skill with `--autonomous`. Invoke the
manifest-dev:just-do skill with the
Manifest path define reports, noting that the chain goal already owns the
completion backstop, so just-do continues under it rather than arming its
own. If define reports no Manifest path, stop and report.
