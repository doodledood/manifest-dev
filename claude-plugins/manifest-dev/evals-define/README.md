# define contract evals

These cases exercise contract authoring from settled understanding. They are separate from
`evals/`, whose measured baseline covers figure-out. Run from this plugin directory:

```bash
claude plugin eval . --eval-dir evals-define --ablation with-without --judge-model sonnet --allow-tools Write --runs 3 --no-publish
```

Cases 01 and 02 supply adversarial draft Manifests: overlapping unbounded visual/subjective
acceptance and incompatible cold-access budgets. Case 03 is a straightforward export with
all material choices settled: it protects ordinary autonomy and useful ambition from a
policy that always asks for a smaller scope. Every case preserves the user's actual outcomes;
no grader rewards shorter Manifests, fewer gates, or a fixed retry/coverage count.

The scored grader enumerates the obligations before judging the final proposed contract or
owner decision. The saved contract is requested verbatim after the digest because `last_message`
graders cannot infer file contents from a summary or path. Use `--keep-temp` when
auditing a pilot so the emitted contract can be compared to the saved artifact. Skill firing is display-only, never uplift.
A proposal awaiting the owner can pass the adversarial cases; fabricated owner agreement
cannot. Files belong in the sandbox working directory, not the installed skill or user home.

Freeze prompts and graders before comparing source revisions. For a before/after comparison,
copy this same suite into an isolated checkout of the baseline revision and use identical
model, judge and run settings. Read outputs and decompose scores by arm; a small pilot is
behavioral evidence on these cases, not an estimate of general improvement. These cases have
no established noise floor or held-out validation set. The existing figure-out suite's
noise estimates do not transfer automatically. `tests/` and `sync_dist.py --check` establish
structural properties and distribution parity only, never behavioral improvement.

## Initial observability pilot — 2026-10-04

The initial input requested a proposed contract in the final reply but did not explicitly
request the saved gate bodies. Both with-plugin arms returned digests and file paths. The
three-case, one-run pilot finished without execution errors, but its scored outputs omit
the saved contract: latest main scored 0/1/0 and the patch 1/0/0 (visual/budgets/export).
The corresponding no-plugin scores were 1/0/1 and 1/1/1. These scores are retained as an
inconclusive instrument pilot, not prompt uplift or proof of regression. A fresh reviewer
also found that the budget failure's final reply satisfies its stated rubric on its face,
so judge reliability remains unestablished.

The input now requests verbatim gate bodies. Graders were not relaxed. This input change
invalidates comparison with the initial scores; both revisions must be rerun on the updated
inputs. Artifact visibility and judge agreement must be checked before trusting any score.

## Corrected artifact-observable pilot — 2026-10-04

CLI 2.1.289, opus case model, sonnet judge, `--runs 1 --ablation with-without
--allow-tools Write --no-publish --keep-temp`. Same corrected inputs and unchanged graders
in both revisions; baseline `e957e914`, patch production prompt `dd9f8dc8` (the subsequent
fixture correction is `1087d921`). Both reports are complete with no execution errors.

| Case | Main with | Main without | Patch with | Patch without |
|---|---:|---:|---:|---:|
| Overlapping evidence | 0 | 1 | 1 | 1 |
| Conflicting budgets | 1 | 1 | 1 | 1 |
| Straightforward export | 1 | 1 | 1 | 1 |

The six with-plugin final replies contain their saved Manifest text verbatim, checked against
preserved sandbox artifacts. The patch's visual contract retains a universal visual obligation,
a finite shared evidence plan with limits, and pending curator decisions with a disagreement
boundary. Its budget contract keeps every frame lossless, no server and the memory ceiling,
with proposed timings awaiting owner decision. Its ordinary export finishes unattended.

This is one paired pilot: with-plugin 2/3 → 3/3, while both controls passed 3/3. It establishes
one observed positive case and a regression floor on these inputs, not general effectiveness,
reliable uplift, or a measured noise floor. One control export judgment split 2–1; all other
scored votes were unanimous. The initial pilot's grading disagreement remains reason to audit
outputs, not to equate vote agreement with validity. These cases were authored for this change,
so there is no held-out validation or unseen-task result. Full local reports and traces are
operator evidence, not committed run outputs or published reports.
