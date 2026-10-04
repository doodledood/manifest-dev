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
owner decision. The full contract is requested in the final message because `last_message`
graders cannot infer file contents from a path. Skill firing is display-only, never uplift.
A proposal awaiting the owner can pass the adversarial cases; fabricated owner agreement
cannot. Files belong in the sandbox working directory, not the installed skill or user home.

Freeze prompts and graders before comparing source revisions. For a before/after comparison,
copy this same suite into an isolated checkout of the baseline revision and use identical
model, judge and run settings. Read outputs and decompose scores by arm; a small pilot is
behavioral evidence on these cases, not an estimate of general improvement. These cases have
no established noise floor or held-out validation set. The existing figure-out suite's
noise estimates do not transfer automatically. `tests/` and `sync_dist.py --check` establish
structural properties and distribution parity only, never behavioral improvement.
