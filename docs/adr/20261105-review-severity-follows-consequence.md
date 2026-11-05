# ADR: Review severity follows consequence, with presentation-only Lows below the bar

## Status
Accepted

## Area
Code review

## Decided by
The user, for the severity definitions and Low policy; an agent implements the wording and consumer updates under that ruling. Merging remains with the maintainer.

## Context
Issue #419 describes repeated Low findings in cosmetic display code. Each repair made a stronger claim, and subsequent reviews found a rarer input that broke it. The existing defect-finder threshold blocked every Low, while several dimension examples defined Low by rarity or a workaround. Thus a presentation defect could keep completion blocked like a correctness or safety failure.

This concerns the North Star's purpose: people can trust delegated progress while retaining their decisions. A finite review scope alone cannot make an unbounded space of newly introduced cosmetic edge cases finite.

## Decision
Severity follows the consequence, independently of confidence and trigger frequency:

- Critical retains its existing release-blocking meaning.
- High covers correctness, safety, a broken promise or wrong behavior.
- Medium covers a clear product or quality gap a careful reviewer would insist on fixing before shipping.
- Low covers presentation, polish or taste that does not change the underlying promise.

Every review-code dimension uses no Medium-or-higher findings as its PASS threshold. The dimension roles still decide what each review owns and which advisory gates are eligible for omission; they no longer define different severity thresholds. Dimension examples apply the shared ladder without overriding it. A rare substantive failure is High or Critical by consequence, not Low because it is rare.

Presentation-only Lows follow the existing finite-batch rule: apply useful findings from the first review in a batch, dismiss the rest with reasons, and leave new cosmetic nits on repairs. This is a default all users receive, with the existing user and project rule channels as overrides. An explicit binding presentation requirement remains binding.

A correctness or safety finding received as Low still blocks. Reviewers and consolidation assess its evidence and correct its grade before filtering; the incoming label never discharges the defect. All High and Medium findings remain blocking. A missing-evidence blocker stays a blocker. No new severity category or configuration surface is introduced.

The shared owner is review-code, with calling task data and PR consolidation kept consistent. Writing and design anchors use the same consequence boundary, so presentation-only style findings cannot re-enter as blocking grades. review-prompt retains confidence as its reporting filter separately from severity, and keeps duplication as a Low example without asking for style or minor-wording findings.

## Alternatives Considered
- **Keep every defect-finder Low blocking:** leaves cosmetic finding space unbounded and gives frequency-based labels authority over consequence.
- **Drop every incoming Low label:** could silence substantive correctness, safety or remediation obligations from older or miscalibrated reviewers.
- **Add a second severity or impact taxonomy:** creates another classification to maintain when the existing ladder can express the distinction.
- **Add a retry cap or let an executor lower a gate:** a count cannot establish correctness, and the binding contract remains the owner's.

## Consequences

### Positive
- Cosmetic repairs cannot keep completion blocked merely because a defect-finder reported them.
- Correctness and safety remain blocking even under rare triggers or old Low labels.
- One shared bar and consistent callers replace contradictory role-based thresholds.

### Negative
- Severity grades change for existing findings previously classified by rarity.
- Consequence and whether presentation is part of an explicit promise still require judgment.
- New below-bar polish found on repairs is intentionally left alone.

## Enforced by
partly — `tests/test_review_convergence.py` checks the shared ladder, task thresholds, dimension contradictions and consolidation guard in source and Codex copies. `verification/recipes/review-code.md` → *rare-correctness* and `verification/recipes/do.md` → *promise-convergence* exercise the decisions. Real native GPT-6.1 Sol/xhigh sessions ran one pair each. The rare pagination defect was Low before and High after, and remained blocking in both. The resumed /do case passed on both sides: it fixed the real fee defect and left Unicode-spacing polish alone. That case shows no measured convergence uplift; source locks and the after-run establish the stated policy and its exercised behavior, not a general convergence rate. The documentation review control returned PASS with Low-only polish findings. A later after-run exposed a pre-existing contradictory scope rule: it recognized the paging loss but excluded it as intent mismatch. The owning rule now retains traced mechanical failures, including broken bounds, and implementation choices cannot waive an accepted promise. The corrected-scope rerun reported the loss as High and FAIL. This intermediate failure is retained as evidence rather than hidden by the earlier successful run.

## Source
- The owner's severity and Low-policy ruling in the work request for [Issue 419](https://github.com/doodledood/manifest-dev/issues/419).
- Amends 20260811-a-review-dimension-may-take-a-defect-as-input and 20260926-defect-remediation-requires-justified-prevention: replaces their no-Low threshold and Low consolidation exception; their remediation obligations remain.
- Related: 20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges, whose finite first-review batching and continued-review rule remain.
