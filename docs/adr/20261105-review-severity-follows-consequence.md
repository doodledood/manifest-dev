# ADR: Severity classifies consequence; callers own acceptance and handling

## Status
Accepted

## Area
Code review

## Decided by
The user, for the severity definitions and reviewer/caller boundary. An agent implements that ruling. Merging remains with the maintainer.

## Context
Issue #419 describes repeated Low findings in display code. Repair prose strengthened the promise, while later reviews found rarer cases that broke it. Frequency-based grades and a universal every-Low gate confused consequence with the decision to require a repair. Naming, structure and other nits can cause the same loop.

The North Star calls for trusted delegated progress with retained human decisions. Review classification and caller acceptance are different decisions: the grade describes the finding, while the Manifest or another caller chooses what to address.

## Decision
Reviewers classify findings by consequence, independently of confidence and frequency:

- Critical covers data loss, corruption, security breach or complete failure for all users without a workaround.
- High covers correctness, safety, a broken promise or wrong behavior.
- Medium covers a clear product or quality gap a careful reviewer would insist on fixing before shipping, with its concrete cost.
- Low is polish or a nit of any kind: style, naming, structure, or otherwise.

The Manifest or another caller owns acceptance and handling policy: which severities and categories to address, which fail a gate, which to publish, and how repairs are batched. Requiring a Low does not change its severity. The same Low may pass a caller's Medium+ gate and fail another caller's Low-inclusive gate. The reviewer reports classifications without a verdict when no gate is requested. A requested verdict with no recoverable caller policy is BLOCKED or asks for that policy, rather than inventing a threshold.

No Medium-or-higher findings remains a usual gate only where chosen by the caller. The define task defaults choose that bar and encode the chosen policy into the Manifest's gate body. Review-code owns the ladder, not acceptance. Writing/design reviewers follow the same boundary. Review-pr chooses its usual Medium+ fleet and publication policies in no-manifest mode, honors explicit caller changes including Low, and passes the chosen policies to consolidation. Manifest mode follows the accepted Manifest. Consolidation imposes no independent Low cutoff.

A correctness or safety failure or broken binding promise received as Low is regraded from evidence before applying caller policy; rarity never turns wrong behavior into polish. An explicit artifact promise can concern style, naming or structure. Classification and filtering do not waive a binding criterion, and a missing-evidence blocker remains a blocker. No new severity category is introduced.

The do executor applies the accepted Manifest's policy. Its existing finite-batch rule handles findings below the chosen gate: batch useful first-review fixes, dismiss the rest with reasons, and leave new below-gate findings on repair reviews. A caller that includes Low in its gate still owes those findings. Related repairs stay tracked by their underlying accepted promise under 20261105-repairs-track-the-accepted-promise; repair prose cannot strengthen or waive that promise.

The shared report format owns Location: file:line. Dimension instructions retain mechanism tracing, evidence, trigger and fix requirements, with concrete Location fields in worked examples illustrating the shared format. Review-prompt keeps confidence separate from severity and retains duplication as a Low example without adding style-like examples to its reporting scope.

## Alternatives Considered
- **Make the decision to fix part of Low's meaning:** prevents callers from requiring a Low without distorting its grade.
- **Let reviewers impose a universal Medium+ gate:** hides caller policy in the classifier and can silently change an accepted contract.
- **Keep every defect-finder Low blocking:** lets a grade dictate repair policy and leaves the nit space unbounded.
- **Drop every incoming Low label:** can suppress substantive failures from miscalibrated reviewers.
- **Add another taxonomy or a retry cap:** adds machinery without resolving classification ownership or proving an owed promise.

## Consequences

### Positive
- A finding's severity stays stable across callers with different acceptance policies.
- Accepted gates state their bar instead of inheriting a changing reviewer threshold.
- The usual caller-selected Medium+ gate can converge while preserving real correctness and safety findings.
- Callers can deliberately require polish and nits without reclassifying them.

### Negative
- A caller requesting a verdict must supply or recover its acceptance policy.
- Consequence and the accepted source of a promise still require judgment.
- The do policy deliberately leaves new below-gate findings on repairs; that policy is separate from severity.

## Enforced by
partly — tests/test_review_convergence.py checks the ladder, caller-owned policy, explicit gate encoding, regrading and repair handoffs in source and Codex mirrors. The caller-policy scenario in verification/recipes/review-code.md exercises one Low under different caller gates and a classification-only request. The rare-correctness, promise-convergence and PR consolidation scenarios cover substantive failures and finite repair scope. Prior native runs regraded paging loss and retained the real fee defect while leaving nits under the chosen gates. Both promise-convergence arms passed, so they establish conformance rather than measured uplift. An earlier paging run exposed a scope exclusion and incorrectly passed; correcting that rule restored High/FAIL, with the failed run retained as evidence. Runtime judgments remain separate from source locks, and single-session do judgments are disclosed as self-reviewed.

The caller-policy case ran through actual GPT-6.1 Sol/xhigh general agents before (plugins at ff488c24) and after this correction. Both arms kept one Low while returning PASS under the caller's Medium+ gate, FAIL under its Low-inclusive gate, and no verdict for the classification-only turn. The old arm still described the grade through handling language; the corrected arm described consequence only. Both arms already honored the explicit policy overrides, so this is conformance evidence rather than measured uplift. The expanded PR consolidation control retained a Low under an explicit Low-inclusive policy, retained/regraded the real contract defect under the usual caller policy, and preserved the missing-evidence blocker. The do control retained its contract/check/label bytes and repaired only the fee expression under its explicitly chosen Medium+ gates.

## Source
- The owner's severity/caller-policy correction for [PR 420](https://github.com/doodledood/manifest-dev/pull/420), covering [Issue 419](https://github.com/doodledood/manifest-dev/issues/419).
- Amends 20260728-bound-the-acceptance-contract-from-above, 20260811-a-review-dimension-may-take-a-defect-as-input and 20260926-defect-remediation-requires-justified-prevention: classification is separate from caller-selected acceptance and handling; substantive remediation obligations remain.
- Related: 20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges and 20261105-repairs-track-the-accepted-promise.
