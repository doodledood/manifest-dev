# ADR: Review severity follows consequence, with optional nits of any kind below the bar

## Status
Accepted

## Area
Code review

## Decided by
The user, for the severity definitions and Low policy; an agent implements the wording and consumer updates under that ruling. Merging remains with the maintainer.

## Context
Issue #419 describes repeated Low findings in cosmetic display code. Each repair made a stronger claim, and subsequent reviews found a rarer input that broke it. The existing defect-finder threshold blocked every Low, while several dimension examples defined Low by rarity or a workaround. Thus a presentation defect could keep completion blocked like a correctness or safety failure.

This concerns the North Star's purpose: people can trust delegated progress while retaining their decisions. A finite review scope alone cannot make an unbounded space of newly introduced nits finite. Naming, structure and other optional improvements have the same convergence problem as presentation polish.

## Decision
Severity follows the consequence, independently of confidence and trigger frequency:

- Critical retains its existing release-blocking meaning.
- High covers correctness, safety, a broken promise or wrong behavior.
- Medium covers a clear product or quality gap a careful reviewer would insist on fixing before shipping.
- Low is optional polish or a nit of any kind: style, naming, structure, or otherwise.

Every review-code dimension uses no Medium-or-higher findings as its PASS threshold. The dimension roles still decide what each review owns and which advisory gates are eligible for omission; they no longer define different severity thresholds. Dimension examples apply the shared ladder without overriding it. A rare substantive failure is High or Critical by consequence, not Low because it is rare.

All such Lows follow the existing finite-batch rule: apply useful findings from the first review in a batch, dismiss the rest with reasons, and leave new Lows on repair reviews. This is a default all users receive, with the existing user and project rule channels as overrides. An explicit binding requirement remains binding, including one about style, naming or structure.

A correctness or safety failure or broken binding promise received as Low still blocks. Reviewers and consolidation assess its evidence and correct its grade before filtering; the incoming label never discharges the defect. All Critical, High and Medium findings remain blocking. A missing-evidence blocker stays a blocker. No new severity category or configuration surface is introduced. Related repairs remain tracked by their underlying accepted promise under 20261105-repairs-track-the-accepted-promise.

The shared owner is review-code, with calling task data and PR consolidation kept consistent. Writing and design anchors use the same consequence boundary, so optional nits cannot re-enter as blocking grades merely because they concern structure or another nonvisual area. review-prompt retains confidence as its reporting filter separately from severity, and keeps duplication as a Low example without asking for style or minor-wording findings.

The shared report format owns the `Location: file:line` requirement. Dimension instructions do not restate it; their mechanism tracing, evidence, trigger and fix requirements remain. Concrete `Location` fields in worked findings remain as examples of that shared format, not additional requirements.

## Alternatives Considered
- **Keep every defect-finder Low blocking:** leaves cosmetic finding space unbounded and gives frequency-based labels authority over consequence.
- **Limit below-bar Lows to presentation:** leaves optional naming, structural and other nits able to prolong repair loops for the same reason.
- **Drop every incoming Low label:** could silence substantive correctness, safety or remediation obligations from older or miscalibrated reviewers.
- **Add a second severity or impact taxonomy:** creates another classification to maintain when the existing ladder can express the distinction.
- **Add a retry cap or let an executor lower a gate:** a count cannot establish correctness, and the binding contract remains the owner's.

## Consequences

### Positive
- Optional polish and nits of any kind cannot keep completion blocked merely because a defect-finder reported them.
- Correctness and safety remain blocking even under rare triggers or old Low labels.
- One shared bar and consistent callers replace contradictory role-based thresholds.

### Negative
- Severity grades change for existing findings previously classified by rarity.
- Consequence, optionality and whether a preference is part of an explicit binding promise still require judgment.
- New below-bar polish found on repairs is intentionally left alone.

## Enforced by
partly — `tests/test_review_convergence.py` checks the shared ladder, task thresholds, dimension contradictions and consolidation guard in source and Codex copies. `verification/recipes/review-code.md` → *rare-correctness* and `verification/recipes/do.md` → *promise-convergence* exercise the decisions. Real native GPT-6.1 Sol/xhigh sessions ran one pair each. The rare pagination defect was Low before and High after, and remained blocking in both. The resumed /do case passed on both sides: it fixed the real fee defect and left Unicode-spacing polish alone. That case shows no measured convergence uplift; source locks and the after-run establish the stated policy and its exercised behavior, not a general convergence rate. The documentation review control returned PASS with Low-only polish findings. A later after-run exposed a pre-existing contradictory scope rule: it recognized the paging loss but excluded it as intent mismatch. The owning rule now retains traced mechanical failures, including broken bounds, and implementation choices cannot waive an accepted promise. The corrected-scope rerun reported the loss as High and FAIL. This intermediate failure is retained as evidence rather than hidden by the earlier successful run.

The broader any-nit policy also has one native before/after pair at baseline 36baccea for each extended fixture, using GPT-6.1 Sol/xhigh. In `review-pr consolidation`, both arms filtered optional naming and structural nits, retained a binding identifier-contract failure received as Low and regraded it High, and preserved the missing-evidence blocker. In `do promise-convergence`, both arms left the new naming and helper-extraction nits unapplied, repaired only the fee expression, and retained the Manifest, check and label bytes. The after-run explicitly grouped the repeated spacing repairs by their accepted promise and regraded the fee defect High. These are conformance observations, not measured uplift; the do judgments were self-reviewed inside each isolated session. Documentation calibration also follows the shared bar: missing docs alone cannot establish Medium, uncertainty alone is not a finding, and the shared report format owns Location.

## Source
- The owner's severity and Low-policy ruling in the work request for [Issue 419](https://github.com/doodledood/manifest-dev/issues/419).
- Amends 20260728-bound-the-acceptance-contract-from-above, 20260811-a-review-dimension-may-take-a-defect-as-input and 20260926-defect-remediation-requires-justified-prevention: replaces their no-Low threshold and Low consolidation exception; their trigger and substantive remediation obligations remain.
- Related: 20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges, whose finite first-review batching and continued-review rule remain.
