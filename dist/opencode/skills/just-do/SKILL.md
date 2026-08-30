---
name: just-do
description: 'Goal-based Manifest executor. Reads a Manifest and pursues it with full autonomy: reach a state where every Acceptance Criterion and Global Invariant holds, deciding for itself how to get there. Use when the user asks to just do a manifest, run it goal-based, or execute with minimal process.'
argument-hint: '<manifest-path> [--no-log]'
user-invocable: true
---

No path → halt with usage. Read the Manifest in full, then make every Acceptance
Criterion and Global Invariant hold as written; how is yours. Those bind; Initial
Approach and Process Guidance advise. The Manifest is read-only and this run never
invokes /just-define: stop and report if a premise goes false, the user redirects past
the Manifest, or only a person can unblock you. When done, report what changed
and your basis per gate.

First, arm the completion backstop: continue under an active goal for this Manifest,
or emit the block below verbatim. Do not
summarize, shorten, reword, or re-punctuate it. Set it through the harness's
goal-setting, continuation, or durable-completion-condition capability, else print it
copy-pasteable: one unlabeled block introduced by a sentence of your own, since the
fence and its label are this file's markers rather than part of what you emit.

```goal-block
Work under this run's Manifest until every Acceptance Criterion and Global Invariant in it holds, each with evidence from the artifacts that gate names, and completion has been reported. Record the Manifest's path in a checkpoint note as soon as it exists.

The Manifest is the contract, not the run's to rewrite: it changes only through the skill that wrote it, never by direct edit, and a changed gate returns unverified.

Record compact checkpoint notes as work proceeds: what changed, what was verified, what remains, blockers.

Stop only when blocked on something a person must resolve.
```

## What holds for every gate

A gate declares `judgment` or `deterministic`; an undeclared kind is invalid, never
inferred. Read a gate from the Manifest by ID, never from a copy. For repository
work, read the change as `origin/main...HEAD` — the remote-tracking default branch,
since a local ref sits stale. A judgment gate reads the full change once, then only
prior findings' repairs and the delta; a deterministic gate re-runs in full. Findings
below a passing gate's bar are handed over, not fixed. A bar never moves down, and a
summary claim is not evidence — stop and report instead.

## The execution log

Unless `--no-log`, keep an append-only log at `~/.manifest-dev/logs/do-<name>-<hash>.md`,
where `<name>` is the Manifest's filename without extension and `<hash>` the first eight
hex characters of SHA-256 over its absolute path. Fixing the scheme is what reopens the
same Manifest's log on every launch and keeps two manifests sharing a basename in
different directories apart. Read it before resuming and append as you go: it is where
the goal block's checkpoint notes land. `../do/references/LOG.md` holds the entry shape
and append discipline — not its path rule.
