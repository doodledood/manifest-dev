---
name: auto
description: 'End-to-end autonomous execution: figure-out → define → do, chained without manual approval gates. Use when you want to define and execute without intervention during planning, when the user asks for autonomous or end-to-end work, or asks to tend or babysit a PR.'
argument-hint: '[task] [--babysit <pr-url>] [--verification per-gate|consolidated|self] [--verifier-model <model>]'
user-invocable: true
---

Chain `manifest-dev:figure-out --autonomous` (when the transcript lacks shared understanding) → `manifest-dev:define --autonomous` → `manifest-dev:do` on a single task. The `--autonomous` flag on figure-out makes the model self-answer with recommended answers instead of waiting on the user (see `figure-out/references/autonomous.md`). Surface define's Summary for Approval for visibility, then treat it as approved and proceed to /do.

**Task text** comes from `$ARGUMENTS`; if empty, infer from conversation context (summarize the discussed task into a concrete description). Fresh session with no context and no args → halt: `No task description provided and no conversation context to infer from. Usage: /auto <task description> | /auto --babysit <pr-url>`.

**Verification policy.** Parse only top-level option uses of `--verification` and `--verifier-model` as `/auto` flags; quoted or topic mentions remain task text. Omitted `--verification` means `per-gate`. After resolving that default, load the matching sibling `/do` reference under `../do/references/` and apply its policy validation before `/define`; the reference, not `/auto`, owns mode-specific model support and evidence provenance. Remove parsed flags from the task before `/define`, and forward them only to `/do`. Never write either option into the Manifest. Use the reference's required evidence/provenance wording when recording each gate's provenance in the ledger.

**Babysit mode** (`--babysit <pr-url>`) skips fresh synthesis. Invoke `manifest-dev:define` with `--babysit <pr-url> --autonomous`, then /do with the parsed verification options. PR-lifecycle platform auto-detects from PR URL host (`github.com` → github composition); non-github host → halt. Multi-repo manifest produced by /define → single /do invocation navigates all repos.

**Failure handling.** /define returns no manifest path → stop, report. /do escalates (BLOCKED criterion or other blocker) → surface the escalation verbatim to the user with the action it requests.

**Unattended launch.** At the start of a standalone run, before chaining, establish a durable full-chain goal-setting backstop. Its completion contract spans the whole chain, so continuation does not stop after the first phase. The terminal success condition is outcome-gated: the Manifest is written, `/do` reports `/done`, and every Acceptance Criterion and Global Invariant has fresh PASS evidence under the selected verification mode in a manifest gate ledger. `/auto` owns this backstop as the chain entrypoint: `figure-out --autonomous` suppresses its standalone Read-level backstop because this parent carries the Read bar as a phase checkpoint before `/define`, `/define` only emits the manifest handoff, and `/do` operates under the existing full-chain contract instead of setting or printing a narrower manifest-only goal. Emit the blocks below verbatim. Do not summarize, shorten, reword, or re-punctuate them. Set it through the harness's goal-setting, continuation, or durable-completion-condition capability where one exists; print it in copy-pasteable form for the user's own continuation mechanism where none does. Emit the chain prefix, then the goal block, then the gate-ledger clause, as one contract: one unlabeled block introduced by a sentence of your own, since the fences and their labels are this file's markers rather than part of what you emit.

```chain-prefix
Reach shared understanding of the task, then write a Manifest from it. Where an investigation phase runs, complete a full-anatomy Read checkpoint before the Manifest is written: every load-bearing branch pressed; Evidence Ledger explicit; assumptions separated from verified and inferred claims; independent re-derivation run or explicitly unavailable; rival set no longer moving; confidence, evidence, and overturn conditions stated. For diagnosis-shaped work, the Read checkpoint is not complete if it only localizes where the symptom concentrates: name the concrete mechanism — the variable, difference, or sequence that produces the symptom, including why this case differs when the question is comparative — or earn an underdetermined Read by naming the surviving explanations and showing which feasible probes that could distinguish them were run, what they showed, or why they were blocked. Treat a missing or weak Read checkpoint as a phase defect to repair before the Manifest is written, not a post-hoc terminal failure after execution has fresh all-gate PASS evidence. Stop if the run stalls — consecutive turns moving neither the work nor its verification.
```

```goal-block
Work under this run's Manifest until every Acceptance Criterion and Global Invariant in it holds, each with evidence from the artifacts that gate names, and completion has been reported. Record the Manifest's path in a checkpoint note as soon as it exists.

The Manifest is the contract, not the run's to rewrite: it changes only through the skill that wrote it, never by direct edit, and a changed gate returns unverified.

Record compact checkpoint notes as work proceeds: what changed, what was verified, what remains, blockers.

Stop only when blocked on something a person must resolve.
```

```gate-ledger-clause
Maintain a gate ledger covering every Acceptance Criterion and Global Invariant: gate id, gate-text source, selected verification mode, evaluator provenance, explicit or inherited verifier model, latest verdict, evidence, and freshness relative to the last relevant change to its subject. Completion requires every listed gate to have fresh PASS evidence under the selected verification mode. Unverified, FAIL, stale, BLOCKED/actionable, or escalation-pending gates are non-terminal. A substantive change to a gate's subject after a PASS marks it stale until re-evaluated, while re-reading, re-examining, and cosmetic or no-op edits do not. Never accept unevidenced self-attestation, "looks done", or a summary claim in place of the selected mode's required evidence.
```
