# ADR: Harden figure-out truth-seeking via inline general-case rigor; defer the independent verification pass

## Status
Accepted

## Context

figure-out can converge prematurely — declare "I unraveled it" when it stopped at the first coherent story. The scariest failure is the **never-considered cause**: a hypothesis no participant ever generated, so no amount of checking surfaces it. This is worst in `--autonomous` mode, where the human — figure-out's real adversary in interactive use — is gone and the belief register becomes self-graded.

A companion ADR establishes that figure-out should not gain verifier fan-out (it buys process trust, not artifact trust). The open question was *how* to raise figure-out's truth-seeking rigor for **all** uses — general investigations, coding investigations (root-cause and design), and research-style investigations — without bloating the skill or adding interactive friction.

Honest bound carried through the analysis: no process catches the never-considered cause with certainty. Inline rigor raises the probability; only an independent (fresh-context) generator escapes self-grading, and that costs machinery.

## Decision

Strengthen figure-out's investigation process **inline, in the spine, mode-general** — applying to interactive and autonomous, and to coding/research/general alike — with a strict replace-before-add discipline:

1. **Live rival set** (replace the existing "don't stop at the first coherent explanation" line): treat the set of rival explanations/answers as live, not fixed at the outset. When a finding opens or forecloses a region, *regenerate* rivals — don't merely re-weight the ones already held. Commit only once new evidence stops moving the set (this clause is also the convergence terminator, so it cannot spin). Phrased investigation-general so "rivals" reads as causes for a diagnosis and as candidate designs for a decision; kept distinct from BUG.md's "one symptom, several causes."
2. **Outside view / reference class** (one new line): before locking the read, ask what this *class* of problem usually turns out to be — base rates pull in branches the inside view skipped.
3. **Source-rigor awareness** (conditional, not spine weight): external sources lie (fabricated citations, circular sourcing, AI-content pollution). Fires only when an investigation leans on external sources, held to a tight ~two-line bar — otherwise it belongs in `deep-research`, not figure-out.

**Defer** (logged as direction, not built now): the independent unanchored fresh-context pass at autonomous convergence — the residual catcher that self-critique provably cannot reach — and the non-convergence→`/define` router.

## Alternatives Considered

- **Independent unanchored pass now (blind re-derivation at autonomous convergence)**: spawn a fresh-context agent that re-derives from the evidence without seeing the conclusion, then compare reads — Deferred: it is the only thing that escapes self-grading, but adds machinery; chose simplicity for now.
- **Multi-frame fan-out / full re-investigation**: several diverse-frame re-derivers plus new evidence gathering — Rejected for figure-out: becomes a research engine / `deep-research` / `/do`, the exact convergence this project avoids.
- **Same-context "register critic" self-critique**: have the same context attack its own read — Rejected as the primary mechanism: it shares the converged frame and hits the self-rationalization floor.
- **Add competing-hypotheses + inversion + outside-view as three new lines**: import the research disciplines verbatim — Rejected as bloat: inversion and up-front enumeration are largely already in the spine; net honest change is one replace + one add.

## Consequences

### Positive
- Better convergence across all figure-out uses — coding root-cause and design, research, and general — from a minimal footprint (~one replaced line + one added line + a conditional note).
- The live-rival-set's commit clause doubles as a convergence terminator, preventing endless re-enumeration.
- Replace-before-add keeps the skill lean and avoids accretion.

### Negative
- The autonomous self-grading hole is only *partially* closed; the never-considered cause is made less likely, not impossible. Closing the residual requires the deferred independent pass.

## Source
- Related: See also 20260606-figure-out-process-trust-vs-define-do-artifact-trust; the deferred independent pass was later un-deferred by 20260611-figure-out-evidence-ledger-and-independent-rederivation
