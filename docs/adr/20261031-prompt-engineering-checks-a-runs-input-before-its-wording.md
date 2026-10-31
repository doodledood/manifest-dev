# ADR: prompt-engineering checks a failing run's input before its wording, and ranks after-the-fact correction second

## Status
Accepted

## Area
Prompt architecture

## Decided by
The user

## Context

The `prompt-engineering` skill decided whether a prompt line exists, where it sits and how it is worded. When a run gave bad output, both of its improvement paths went to the prompt's own lines: *Updating* asked for the gap a line closes, and `references/metaprompting.md` asked a model "which lines of the prompt are causing which observed behaviors", then for "small, explicit edits". Its pre-flight checked for a missing goal, a capability gap and a typo, never for the input. Its deployment blocks in `references/system-prompts.md` offer review passes and self-checks with no order relative to anything else.

In practice the usual cause of bad output from a capable model is the input it was fed — the prompt and the dynamic data filled into it or read by it — with a piece missing, two pieces conflicting, a piece wrong or out of date, or what matters buried in noise. A wording edit or an added correction leaves that input as it was, so the next run meets the same fault. The repository's own prompt-tuning loop (`claude-plugins/manifest-dev/evals/README.md` → *Hill-climbing a prompt against a suite*) showed the same gap: its analyzer received only judged outputs, so it could not see what a failing run had read, and one recorded climb spent two wording rounds that moved nothing before concluding that what was left to try lay outside the line being reworded.

## Decision

The guide states one rule, in its own `SKILL.md` section *What the run has in front of it*: a run's result is bounded by what it has in front of it — the prompt plus everything fed into it, including inputs filled into a template, files it reads, retrieved material, tool output, conversation history, and what a handed-off agent receives. When a run underperforms, read what it actually had before changing wording, and check for four faults: missing, conflicting, wrong or stale, and noise. Fix the input first; wording edits and after-the-fact corrections — review passes, self-checks, rules added after a failure — come after it. Completeness is measured against the task, so the rule works with the guide's load discipline rather than against it. When the input is already complete, consistent and clean, the instructions are where to look; when the model lacks a capability no input supplies, the architecture is.

*Updating* sends a change that follows a bad result through that section first. `metaprompting.md` carries what each failing run was fed in its traces, sorts each failure by whether the fed material or the prompt's own text caused it before attributing it to prompt lines, fixes a fed-material fault at its source, and keeps its surgical prompt revision for faults in the prompt's own text. The eval hill-climb loop keeps transcripts and reads what the failing train runs had before it chooses a round's change, pointing at the guide's section; a fault in an eval case or its scaffold is a case defect fixed outside the climb, never a round's change, so the climb cannot tune the instrument to the skill.

`system-prompts.md` is unchanged: it loads after `SKILL.md`, whose rule already ranks its correction blocks second, and a second statement there would drift from the first.

## Alternatives Considered

- **Keep wording edits as the first lever.** Rejected: it treats every failure as an instruction failure, so input faults survive each revision and the prompt accretes rules that compensate for them.
- **Lead with after-the-fact correction** — verification passes, self-checks, review loops. Rejected as the first lever: a correction catches an instance of the fault downstream and leaves its cause in place. It stays available second, and where an irreversible step needs a check of its own.
- **Read "context" as the prompt text only.** Rejected: the guide's load and provenance rules already cover the prompt text, and the faults that most often break a run sit in dynamic input the template never shows.

## Consequences

### Positive
- A failing run is diagnosed from what it actually had, so a fix lands where the fault is and the prompt stops gaining rules that cover for bad input.
- The rule lives in one section; `metaprompting.md`, the eval README and `review-prompt` (which loads the guide's principles) reach it by pointer.
- The hill-climb loop can now see input faults and is guarded against fixing them by editing the cases it measures with.

### Negative
- Reading a run's input costs a trace or a transcript the author may not keep; where none exists the diagnosis starts by getting one.
- The rule's claim that input is the usual cause rests on practice, not on a measurement in this repository; the `diagnose-input` scenario is written but has not been driven.

## Enforced by
partly — `verification/recipes/prompt-engineering.md` scenario `diagnose-input` (ask-first) checks that the guide traces an input-caused failure to its input and fixes what the run is fed; `review-prompt` applies the guide's principles; the rest stays judgment.

## Source
- Related: See also [20260817-prompt-lines-earn-their-place-by-provenance](20260817-prompt-lines-earn-their-place-by-provenance.md)
