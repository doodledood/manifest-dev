---
name: just-auto
description: 'Goal-based autonomous chain: figures out the task, encodes a Manifest, and pursues it end-to-end with full autonomy and minimal process. Use when the user asks to just build it, just auto it, run end-to-end goal-based, or go from idea to done without approval gates.'
argument-hint: '<task>'
user-invocable: true
---

Run the full flow for the given task — stated as an argument or inferable
from the conversation; with neither, halt with usage.

Before starting, arm the completion backstop. If an active goal's completion
condition already covers this task's outcome, continue under it. Otherwise
emit the blocks below verbatim. `<manifest-path>` stays literal — the chain
prefix defines it as the path define reports. Do not summarize, shorten, reword,
or re-punctuate them. Set it through the harness's
goal-setting, continuation, or durable-completion-condition capability where
one exists; print it in copy-pasteable form for the user's own continuation
mechanism where none does. Emit the chain prefix first, then the goal block,
and proceed either way.

```chain-prefix
Reach shared understanding of the task, then write a Manifest from it. Where figure-out runs, complete a full-anatomy Read checkpoint before /define: every load-bearing branch pressed; Evidence Ledger explicit; assumptions separated from verified and inferred claims; independent re-derivation run or explicitly unavailable; rival set no longer moving; confidence, evidence, and overturn conditions stated. For diagnosis-shaped work, the Read checkpoint is not complete if it only localizes where the symptom concentrates: name the concrete mechanism — the variable, difference, or sequence that produces the symptom, including why this case differs when the question is comparative — or earn an underdetermined Read by naming the surviving explanations and showing which feasible probes that could distinguish them were run, what they showed, or why they were blocked. Treat a missing or weak Read checkpoint as a phase defect to repair before /define, not a post-hoc terminal failure after /do has fresh all-gate PASS evidence. Record the Manifest's path in a checkpoint note as soon as define reports it; <manifest-path> below is that path. Stop if the run stalls — consecutive turns moving neither the work nor its verification.
```

```goal-block
Work under the Manifest at <manifest-path> until every Acceptance Criterion and Global Invariant in it holds, each with evidence from the artifacts that gate names, and completion has been reported.

The Manifest is the contract, not the run's to rewrite: it changes only through /define, never by direct edit, and a changed gate returns unverified.

Record compact checkpoint notes as work proceeds: what changed, what was verified, what remains, blockers.

Stop only when blocked on something a person must resolve.
```

Then: if the conversation lacks shared understanding of the task, first
invoke the manifest-dev:figure-out skill with the task and `--autonomous`.
Invoke the manifest-dev:define skill with `--autonomous`. Invoke the
manifest-dev:just-do skill with the
Manifest path define reports, noting that the chain goal already owns the
completion backstop, so just-do continues under it rather than arming its
own. If define reports no Manifest path, stop and report.
