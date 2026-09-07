---
name: just-define
description: 'Goal-based Manifest builder. Encodes shared understanding into a verifiable Manifest — Deliverables, Acceptance Criteria, Global Invariants — deciding for itself how to interview. Use when the user asks to just define it, spec it lean, or make a manifest with minimal process.'
argument-hint: '[task] [<manifest-path> to amend]'
user-invocable: true
---

Encode the conversation's shared understanding as a Manifest at
`~/.manifest-dev/manifests/manifest-<ts>.md` (create the dir); how you interview
is yours. No shared understanding in the transcript → invoke
just-figure-out first. A manifest path in the arguments means
amend: targeted changes only, IDs stable, no renumbering.

An amendment from `just-do` is unattended: self-answer within the caller's
delegation, ask no questions, and wait for no approval. Validate a delegated
Appetite revision before applying it: the broader work serves the requested
outcome, its benefit justifies the added complexity and maintenance, it has not
already been done as excess, and it crosses no explicit exclusion or binding
requirement. Preserve those requirements unless user steering explicitly changes
them. A request outside that delegation returns an evidenced blocker without
changing the Manifest. Record material autonomous decisions as `(auto)` items
with matching `ASM-*` entries naming the rationale and impact if wrong.

The Manifest is the acceptance contract — what the user accepts as "I'd ship
the outcome of executing this" — and /do or /just-do executes it later with
none of this conversation's context, so everything binding lives in the gate
texts themselves. That gives a floor that isn't ceremony:

- Follow the schema in this skill's own `references/SCHEMA.md` exactly — it is
  what the executor parses.
- Every Acceptance Criterion and Global Invariant is one text — title, body,
  optional why — stating what done means, the evidence to inspect, and the
  threshold between PASS and FAIL, precise enough that two evaluations read the
  same thing.
- Every gate declares "Judgment gate." or "Deterministic gate." — never
  inferred; an executor handed an undeclared kind is broken by it.
- Anything whose violation would be unsafe or irreversible becomes a Global
  Invariant — never Process Guidance, never dropped for resisting verification.
- Encode every explicit Out of bounds exclusion once as a Global Invariant;
  anticipated omissions that may change belong in the advisory plan.
- Every manifest carries the ceiling invariant from the schema, verbatim — the
  one bound on the other side.
- A criterion nothing can check is sharpened or dropped with a recorded
  assumption; only gates bind.

Before finishing, give a plain-language digest — the pain, the plan, what gets
built, the guardrails — and wait for a yes unless the caller is /just-auto or
an amendment. Then emit the handoff (`<manifest-path>` is the absolute path you
wrote):

```text
Manifest complete: <manifest-path>

To execute: /just-do <manifest-path>
For unattended execution, invoke /just-do <manifest-path> as the execution entrypoint. /just-do reads the manifest and owns the manifest-completion contract: it sets that completion contract when the active harness exposes a goal-setting or continuation capability, or prints the manual copy-paste contract when not. just-define does not set a separate /just-do goal.
```
