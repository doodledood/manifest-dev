# ADR: A gate is one text, not two

## Status
Accepted

## Area
define / do

## Context

Every Acceptance Criterion and Global Invariant is currently authored twice: once as a
`Description` line a human reads in the Manifest, and once as `verify.instructions` — a
self-contained prompt for an evaluator assumed to see nothing else.

Only one of the two binds. `per-gate` and `self` verification supply the evaluator with
`instructions` alone; `consolidated` is the only mode that also passes the criterion text. So
`instructions` is the gate and the `Description` is documentation sitting next to it.

The binding copy is reviewed by nobody. `/define`'s Summary for Approval is deliberately plain
prose — "no codes, no YAML, no schema vocab" — and `/auto` surfaces it without waiting. A user
approves a digest; the run is bound by a prompt that user never saw. Gates that are vague,
over-concrete, or internally inconsistent therefore reach execution unexamined, and surface as
escalations mid-run.

The duplication is fourfold, not twofold. The same requirement appears as the `Description`, as
`verify.instructions`, as the ceiling invariant's inlined copy of Intent and of the enumerated
Deliverables and gates, and as a PASS threshold that `review-code` already defines in its own
dimension table. Each copy is a drift site, and only the last of them has an owner that could
notice a disagreement.

Self-containment was well-motivated when it was adopted. `20260728-move-verification-execution-policy-to-do`
required instructions to be topology-neutral so that changing `/do`'s mode could not silently
change what counts as acceptance, and `per-gate` was then the default: many isolated executions,
each seeing only its own prompt. `20260730-consolidated-default-verification-mode` flipped the
default to `consolidated` because isolated verifiers resample the finding space and oscillate.
The mode that self-containment was protecting is no longer the one most runs use, and the mode
that replaced it already hands a single evaluator every gate's criterion text.

The project also already performs this collapse elsewhere. `ticket-up` turns each Acceptance
Criterion and its verify instructions into one prose check "a stranger can judge", and files the
verify YAML under "Stays behind. Executor policy, meaningless outside manifest-dev" — for a
reader with no manifest-dev at all, which is a harder audience than a verifier.

## Decision

**A gate is one text.** The `Description`/`instructions` split is deleted rather than kept in
sync, and the surviving text is what both the human and the evaluator read.

**Shape.** Each Acceptance Criterion and Global Invariant carries a **title**, a **body**, and a
**why**. `kind` and `phase` remain as the only structured metadata; nothing else survives as a
field.

**The title summarizes, never adds.** Claim-shaped titles are kept, because they read better in a
gate ledger, an escalation payload, and a FAIL line than topic labels do. A requirement that
exists only in the title is a defect, not a shorthand.

**The body states what done means, at product-manager grade.** Where the checking procedure
matters, it is part of what done means and belongs in the body — "done when a request to /health
returns 200" is a definition, not a separate procedure. Where a skill *is* the definition of
done, the body names it and its dimension, on the same reasoning.

**The why is context and binds nothing**, under the same non-additive rule as the title. The
guard against an evaluator passing work that misses the criterion while serving its intent is
`/define`'s *Gate altitude* discipline: a criterion pitched at outcome altitude survives a
legitimate pivot on its own and never needs the why to rescue it.

**Verification mechanics that do not vary per gate move to `/do`.** The diff-ref convention
(comparing against `origin/main` rather than `main`, because a local ref goes stale in a shallow
clone), the PASS/FAIL/BLOCKED verdict boilerplate, and thresholds a skill already owns are
run-wide facts. This extends `20260728`'s line — that ADR moved verification execution *policy*
out of the Manifest; execution *mechanics* follow it for the same reason.

**Evaluators are pointed at the gate, not handed a copy of it.** `/do` currently preserves each
gate's instructions verbatim inside the execution envelope it builds, which is a copy — and the
party building it is the executor, whose interest in how a gate reads is exactly what verification
exists to neutralize. Instead, a per-gate execution receives the Manifest's absolute path and the
ID of the gate it evaluates; a consolidated execution receives the path and the set of eligible
gate IDs. The canonical text is read from the file, so no paraphrase, truncation, or reframing can
enter between authoring and evaluation.

Run state still travels in the envelope, because it deliberately does not live in the Manifest:
which gates are eligible under phase ordering, and each Judgment Gate's Ratchet scope — the full
change on a first evaluation, or the prior findings plus the delta since the artifact state it
last read.

**Ordinary gates stay self-sufficient by construction**, which is what makes pointing safe. The
body fully states done, so a gate depends on nothing else in the file even though the evaluator
can now see the file. The envelope carries one framing line — evaluate the named gate as written,
and treat nothing else in the Manifest as binding on the verdict — so Process Guidance and the
Initial Approach being visible cannot turn into conformance-to-plan judging, a job
`change-intent` already owns as a separate dimension. The ceiling invariant needs no carve-out at
all under this scheme: the Manifest is its subject, and it is now simply reading it.

**Manifest-edit invalidation becomes a recorded judgment.** Mechanically invalidating every gate
whose evaluation input changed was never load-bearing: `/do` already decides by judgment whether
an artifact change is substantive enough to stale a passing gate. The run may judge which gates
an amendment actually reaches, and must record that call per gate so it is auditable rather than
silent.

**No backwards compatibility.** Manifests in the previous schema are rejected with an instruction
to regenerate, exactly as `/do` and `/define` already reject the superseded `prompt`/`model`
schema. No translation path is provided.

## Alternatives Considered

- **Keep both texts and keep them in sync**: rejected. That is what happens today. No checker
  compares them, and the copy that binds is the one no reviewer sees, so drift is undetectable
  by construction.
- **Pass the criterion text in all three verification modes**: closes the mode inconsistency
  without touching the duplication — rejected. Four copies remain, and the binding text is still
  unreviewed.
- **Delete `instructions` and let evaluators read the whole Manifest**: rejected. It exposes
  Process Guidance and the Initial Approach to the evaluator, inviting it to grade adherence to
  the plan rather than the criterion — a job `change-intent` already owns as a deliberate,
  separate dimension. Self-sufficient bodies make the Manifest read unnecessary anyway.
- **Adopt `ticket-up`'s rewrite verbatim**: rejected. `ticket-up` deliberately discards the
  evaluator and threshold because "a stranger has neither". A Manifest gate needs both, so the
  form transfers and the content policy does not.
- **Fix the authoring discipline instead of the structure**: rejected on this repo's own
  precedent. `20260728` already found that adding words to a layer whose instruction was being
  ignored changes nothing; the duplication is structural and survives better prose.

## Consequences

### Positive
- The text a user reviews is the text that binds. The largest single source of unexamined gate
  content is removed rather than mitigated.
- Four drift sites collapse to one. The ceiling invariant in particular stops carrying an inline
  copy of Intent and of the enumerated Deliverables and gates, which retires most of `/define`'s
  frame-reconciliation burden on amendment.
- `ticket-up` gets simpler: it projects from one prose text instead of merging two.
- Gates stop restating thresholds that `review-code` owns, so a gate can no longer contradict the
  skill it activates.

### Negative
- Every word of a criterion becomes load-bearing. Rewording one changes what binds and returns
  that gate to the ledger unverified — the `Description` could previously be edited freely.
- The collapse can regress the very symptom it targets. If the surviving text is authored in the
  readable-human register rather than the evaluator's precision register, gates get vaguer, not
  sharper. The authoring discipline `/define` currently points at `verify.instructions` must move
  onto the single text rather than being dropped with the field.
- Existing Manifests do not migrate. Work in flight under the old schema must be redefined.
- Judgment-based invalidation gives the run a lever over how much it re-verifies, the shape
  `20260730` rejected in a proposed dynamic mode. Requiring the call to be recorded per gate
  bounds it but does not eliminate it.
- Pointing at the Manifest makes the contract live rather than frozen at dispatch. A copied gate
  pinned its text at the moment the envelope was built; a reference means an amendment landing
  mid-round changes what an in-flight evaluation is reading. `/do` gains a rule: do not amend
  while evaluations are in flight, or discard that round's verdicts and re-evaluate against the
  amended Manifest.
- Evaluation now depends on the Manifest file being readable at its absolute path from wherever
  the execution runs. Manifests live outside the repository, so this holds across fresh clones
  and worktrees, but an unreadable path is a new BLOCKED cause rather than a silent wrong verdict.

## Source
- Session: figure-out session, 2026-08-07
- Related: [20260728-move-verification-execution-policy-to-do](20260728-move-verification-execution-policy-to-do.md)
- Related: [20260730-consolidated-default-verification-mode](20260730-consolidated-default-verification-mode.md)
- Related: [20260727-gate-text-changes-on-the-users-say-so](20260727-gate-text-changes-on-the-users-say-so.md)
- Related: [20260728-bound-the-acceptance-contract-from-above](20260728-bound-the-acceptance-contract-from-above.md)
- Related: [20260807-trim-the-manifest-schema-to-fields-that-are-read](20260807-trim-the-manifest-schema-to-fields-that-are-read.md)
