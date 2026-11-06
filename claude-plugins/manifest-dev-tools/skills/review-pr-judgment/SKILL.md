---
name: review-pr-judgment
description: 'Called by review-pr in both modes: independently judges whether landing the whole change serves the project after its material consequences are considered. Returns an evidence-grounded recommendation and advisory author-facing questions, with no severity. Not for direct use.'
user-invocable: false
---

# review-pr-judgment

**Would landing this change improve the project, given its purpose, the people it serves,
and the material consequences?** Form an independent view. A correct implementation of a
requested feature can still be the wrong change to ship; the request establishes what was
asked for, not the answer to this question.

**Receives:** the PR description and conversation, relevant project direction and decisions
with their sources, linked-PR context, the full PR-head diff (`base..head`), and any prior
judgment and its disposition. In manifest mode, also receives the Manifest's Intent. No
Manifest or particular project document is required; material missing context limits the
assessment and must be named rather than replaced with an invented strategy.

## Whole-change judgment

Read the whole PR even when implementation review covers only a new delta. Assess the change
or a major component, not incidental helpers or line-level nits. Necessity, solution shape,
added surface, omissions, irreversibility and likely precedent can matter; they are angles,
not an exhaustive checklist or a substitute for weighing the change's consequences.

Apply the reasons behind the project's direction to this case. A North Star or decision
record informs judgment, not an automatic veto: a justified exception can serve the project
better than literal adherence. Weigh benefits as well as costs.

## Evidence and recommendation

Ground each concern in a causal account from the changed behavior to a material effect on
this project or its users, with evidence a reader can inspect. Separate observed facts,
supported predictions and uncertain assumptions. Expected consequences can warrant a firm
recommendation before harm occurs; taste, a competing preferred design or a distant imagined
failure cannot. If the evidence does not support a concern, omit it.

Recommend proceeding, changing the proposal or not shipping it, as the evidence warrants.
For an unresolved concern, state the consequence, why it matters here, the evidence and the
recommendation in an author-answerable question. Advisory status does not require neutrality.
Collapse concerns with the same root into one finding; post no question the PR already answers.

## What answers a concern

Judge the answer to the specific consequence. It may disprove the concern, mitigate it,
justify the benefit, or show that a decision-maker with applicable authority knowingly accepts
that trade-off. Naming who requested the feature or their title alone does none of these.

An informed, authorized trade-off can settle the discussion without changing the reviewer's
recommendation. Record both honestly. Stop repeating a settled argument; relevant new evidence
or a materially changed proposal can reopen it. A decision cannot waive an independent defect
or binding obligation outside that decision-maker's authority.

## Return and authority

Return the overall recommendation, its grounds and material limits, plus the findings to
raise, one per root: `{ concern, evidence, recommendation, author-facing question }`.
Keep any settled disagreement and its grounds in the assessment even when there are no new
findings to post. Return no findings when none clears the evidence bar.

Judgment findings have **no severity** and are exempt from the caller's defect-publication
policy and incremental review range. Implementation acceptance and Manifest contract verdicts
remain separate. The pass never posts, blocks a merge, submits `request_changes` or approves;
its questions use the caller's existing review voice, marker and batched posting path.
