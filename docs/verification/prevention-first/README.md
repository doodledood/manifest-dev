# Prevention-first policy verification

These checks exercise the September 2026 policy change for
[issue 336](https://github.com/doodledood/manifest-dev/issues/336). They support
specific behavior claims, not a measured reduction in general defect rates.

## Paired review checks

The baseline is commit `a295c9b6acc8d70f302dbf59968911565c5a8263`. The candidate
is the policy introduced with this report. Eleven fixtures were frozen before
running either arm. Separate agent contexts loaded the baseline or candidate
`review-code` skill and each case's dimension reference, inspected identical Git
diffs and task context, executed direct runtime probes where applicable, and
returned verdicts with findings. They did not see the other arm's results.

Each arm evaluated all eleven cases in one context. Two supplemental cases were
added after inspecting those results and evaluated in fresh contexts. They are
not a preregistered held-out set. Agents inherited the session's model defaults;
there was one sample per arm, no model comparison, and no repeated-run estimate
of variance. The JSON files preserve the evaluator outputs.

| Case | Situation | Baseline | Candidate |
|---|---|---|---|
| 01 | Current callers guarded; supported owner permissive | FAIL | FAIL |
| 02 | Optional shared helper; supported bypass remains | FAIL | FAIL |
| 03 | Guard at sole owning operation | PASS | PASS |
| 04 | Same guard adds lines; maintainability review | PASS | PASS |
| 05 | Similar credit operation has different valid semantics | PASS | PASS |
| 06 | Explicit frozen-owner boundary permits containment | PASS | PASS |
| 07 | Initial plan excludes an active sibling without authority | FAIL | FAIL |
| 08 | Later unrelated documentation-only delta | PASS | PASS |
| 09 | Known supported failure plus unavailable plugin region | FAIL | FAIL |
| 10 | Required owner enforcement conflicts with edit permission | PASS | BLOCKED |
| 11 | Ordinary feature adds another manual recording obligation | PASS | FAIL |
| 12 | Author explicitly excuses permissive owner by initial plan | PASS | FAIL |
| 13 | Visible owner protected; required external coverage unknown | BLOCKED | BLOCKED |

The baseline already found the supported owner bypass in cases 01 and 02. Those
cases establish no uplift. Case 12 isolates the baseline's acceptance of a stated
scope excuse. Case 10 distinguishes permitted containment from an impossible
binding outcome. Case 11 exercises the general default without a reported bug;
the candidate reports High under the existing maintainability calibration.

Case 04's supplied context says three added lines; the diff adds two. Both arms
noticed the discrepancy. The fixed inputs were retained. Case 06 states that
regression checks exist, but the fixture does not contain them; the candidate
records that limitation and probes both entry points directly.

The supplemental candidate identified an ambiguity between failing unsupported
closure and blocking on missing evidence. The final policy clarifies that FAIL
requires a demonstrated gap; unsupported closure remains unresolved evidence.
A subsequent prompt review passed that clarification. The paired outputs predate
it and are preserved unchanged; no post-clarification paired rerun is claimed.

## Integrated repair and consolidation

The case 01 finding led to enforcement at `owner.send` before state mutation and
removal of the duplicated caller guards. An additional ordinary caller then
called `send` without validation. Two behavioral tests cover four supported paths:
invalid -1 and 0 must raise without changing shipment state, and positive 2 must
still ship. All tests pass with the repaired owner. The same checks fail against
the permissive owner. This demonstrates protection at the owning runtime boundary,
not a type-level guarantee or protection for unrelated input classes.

An independent review inspected the original-to-repaired range, ran the checks,
and returned PASS for defect-class. Activating the holistic consolidation policy
on the original finding and repair evidence returned no comment: the finding was
resolved by the code. Two separate synthetic routing exercises retained an
unresolved Low defect-class obligation under a premise question and kept a
BLOCKED verdict with no findings from becoming a clean result or approval offer.
The latter exposed a caller bug, which was corrected and rechecked.

These were local policy exercises. No GitHub posting, remote review loop, or
end-to-end autonomous remediation loop was tested. The coordinating agent applied
the repair; the reviewer independently verified it.

## General-purpose authoring

A separate candidate-only context loaded `define`, its schema and relevant task
profiles, and `do`. It produced acceptance text and artifacts for three requests:

- **Reusable onboarding:** replace repeated common setup in engineer and analyst
  guides and add support onboarding, within a Markdown-only scope. The result
  puts installation and token requirements in one shared Markdown file, linked
  by all three roles. Its acceptance requires one edit for a common requirement.
- **One-off meeting note:** record a date, room, decision topic, and attendee count.
  The result is a two-sentence note, with no reusable template or automation.
- **Ordinary feature with sound structure:** add gamma to a transformation registry
  whose existing dispatcher already records successful results. The result adds
  one registry entry and test text; it leaves the dispatcher unchanged.

[Artifact excerpts](general-authoring.md) preserve the outputs. These are text-only
exercises, not changes to a real target application. The onboarding facts were
supplied, so no installation or credential operation was tested. The dispatcher
implementation and recording interface were unavailable, so no runtime or
recording-order claim is established for that feature. There was no baseline arm
for these authoring exercises.

## Reproduce the fixtures and runtime checks

From the repository root, choose an output directory that does not exist:

```sh
python3 docs/verification/prevention-first/fixtures.py /tmp/prevention-fixtures
python3 docs/verification/prevention-first/integrated_check.py /tmp/prevention-fixtures
```

The fixture builder creates eleven tiny Git repositories, `cases.json`, and
`supplemental-cases.json`. Cases 12 and 13 reuse code from cases 01 and 03 with
different task context. Commit identities can differ between reproductions;
comparison of all eleven original and regenerated base/head trees and task
contexts found them identical.

To repeat policy review, provide each arm only its policy tree and the same
case metadata, ask it to inspect each exact base/head range with the named
dimension and context, and save its verdict, findings, and rationale. For the
baseline, obtain `claude-plugins` from the pinned commit. Keep arm contexts
separate. The helper scripts do not invoke or score a language model.

The integrated checker copies the same behavioral tests into a temporary
application directory, uses unguarded callers in both runs, and selects the
permissive or protected owner. Expected exit codes are 1 and 0 respectively.
The checked-in test source is an application fixture, not a repository test.

## Repository checks

The repository suite passed with 115 tests and 12 existing Playwright-dependent
skips. Ruff, Black, mypy, distribution consistency, and whitespace checks passed.
The three verification scripts also pass Ruff and Black. Prompt, change-intent,
scope, and documentation review were performed separately from these mechanical
checks. None of these static checks measures policy effectiveness.
