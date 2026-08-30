---
name: just-auto
description: 'Goal-based autonomous chain: figures out the task, encodes a Manifest, and pursues it end-to-end with full autonomy and minimal process. Use when the user asks to just build it, just auto it, run end-to-end goal-based, or go from idea to done without approval gates.'
argument-hint: '<task>'
user-invocable: true
---

Run the flow for the task given or inferable from the conversation; with
neither, halt with usage.

First, arm the completion backstop: continue under an active goal covering
this outcome, or emit both blocks below verbatim, chain prefix first. Do not
summarize, shorten, reword, or re-punctuate them. Set them through the
harness's goal-setting, continuation, or durable-completion-condition
capability, else print them copy-pasteable. Emit the chain prefix, then the
goal block, as one contract: one unlabeled block introduced by a sentence of
your own, since the fences and their labels are this file's markers rather than part of what you emit. Proceed either way.

```chain-prefix
Reach shared understanding of the task, then write a Manifest from it. Where an investigation phase runs, complete a full-anatomy Read checkpoint before the Manifest is written: every load-bearing branch pressed; Evidence Ledger explicit; assumptions separated from verified and inferred claims; independent re-derivation run or explicitly unavailable; rival set no longer moving; confidence, evidence, and overturn conditions stated. For diagnosis-shaped work, the Read checkpoint is not complete if it only localizes where the symptom concentrates: name the concrete mechanism — the variable, difference, or sequence that produces the symptom, including why this case differs when the question is comparative — or earn an underdetermined Read by naming the surviving explanations and showing which feasible probes that could distinguish them were run, what they showed, or why they were blocked. Treat a missing or weak Read checkpoint as a phase defect to repair before the Manifest is written, not a post-hoc terminal failure after execution has fresh all-gate PASS evidence. Stop if the run stalls — consecutive turns moving neither the work nor its verification.
```

```goal-block
Work under this run's Manifest until every Acceptance Criterion and Global Invariant in it holds, each with evidence from the artifacts that gate names, and completion has been reported. Record the Manifest's path in a checkpoint note as soon as it exists.

The Manifest is the contract, not the run's to rewrite: it changes only through the skill that wrote it, never by direct edit, and a changed gate returns unverified.

Record compact checkpoint notes as work proceeds: what changed, what was verified, what remains, blockers.

Stop only when blocked on something a person must resolve.
```

Then: where shared understanding is missing, invoke just-figure-out
with the task and `--autonomous`; invoke just-define; invoke
just-do with the Manifest path just-define reports; the chain goal
already owns the backstop, so just-do continues under it. No path → stop and
report.
