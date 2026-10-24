# Preparing a trustworthy baseline

The 2026-10-24 revision repairs the measurement instrument for Claude Code. It has not measured
current skill uplift or judge agreement. The skill prompts are unchanged; changed cases and
rubrics need a fresh baseline, and old reports without a launch contract cannot be compared by
the repaired tools.

## Preflight before spending

Run `scripts/setup.sh` once for Python dependencies and Node tooling. The signed-in Claude command-line interface (CLI)
must be on `PATH`. From the repository root:

```bash
scripts/evals/run_eval.sh --preflight preview-figure-out evals/results/next/figure-out.json \
  --tag figure-out --ablation with-without --judge-model sonnet --scaffold --max-cost-usd 205
scripts/evals/run_eval.sh --preflight preview-guards evals/results/next/guards.json \
  --tag figure-out-plugin-only --ablation none --judge-model sonnet --scaffold --max-cost-usd 15
scripts/evals/run_eval.sh --preflight preview-define evals/results/next/define.json \
  --tag define --ablation with-without --judge-model sonnet --scaffold --max-cost-usd 65
```

Preflight uses the native parser with a zero-dollar ceiling and scaffolding disabled. It launches
no agent, judge, or scaffold. It also compiles regexes in Node, since the CLI defers regex
compilation until grading. The printed inventory comes from selected files, not a maintained
count. For an inventory without invoking Claude, use:

```bash
.venv/bin/python scripts/evals/eval_contract.py inventory claude-plugins/manifest-dev -- \
  --tag define --ablation with-without --judge-model sonnet --scaffold
```

Preflight leaves its instrument in the run directory and does not reserve the requested result
path. To start an authorized paid run, replace `--preflight` with `--wait` or omit it for a
detached run. The wrapper repeats preflight and freezes the actual selected instrument beside
the result as `*.instrument.json`. Reusing an existing result path is refused. Keep the result
and sidecar together. The run copy, native log, and exit code live outside the checkout under
`~/.local/state/manifest-dev-evals/`.

The sidecar records case, fixture, prompt, and rubric hashes, normalized grader definitions, planned
repetitions, CLI version, arguments, and exposed model identifiers. Claude Code 2.1.306 reports
supplied model identifiers without independently resolved model IDs. Alias equality alone cannot
prove that an underlying model stayed fixed across days; use fixed IDs through `--model` and
`--judge-model` when available. The contract labels unavailable details explicitly.
The skill-source hash is separate so a hill-climb can change the skill while holding the
instrument fixed. The inventory supports this repository's prose cases with optional scaffold
context; it refuses YAML (YAML Ain’t Markup Language) cases without a prompt file, or mixed execution/grader definitions before a paid launch.

The example budgets are scheduling ceilings, not spending guarantees. With eight concurrent
trials, work already in flight can finish above the ceiling. Historical cost per trial is an
estimate from a different instrument. Inventory reports projected three-vote large language model (LLM) judging under
CLI 2.1.306; missing artifacts and interrupted runs can use fewer votes. Check pilot costs before
committing the full budget. A partial, errored, or incomplete result is never a quality score.

## Read and compare results

Freeze `train_ids` and `test_ids` in `_state.json` before inspecting outputs. Use full case names
from the README tables. The established held-out sets remain; `d27` is the new explicit-target
witness for `d25`. Assign other unmeasured cases before their first measurement.

```bash
.venv/bin/python scripts/evals/eval_contract.py validate path/to/result.json
.venv/bin/python scripts/evals/score_rounds.py --state path/to/_state.json \
  v0=path/to/v0 v1=path/to/v1
.venv/bin/python scripts/evals/extract_outputs.py path/to/result.json \
  --state path/to/_state.json --grader binding-lives-in-gates \
  --cases d01-layer-cut --out path/to/new-analysis-directory
```

The scorer requires every case selected by the frozen split, or an explicit `--cases` subset.
It rejects missing cases, graders, repetitions, judge votes, errored trials, and changed
instruments. Different planned repetition counts are allowed; accidental missing repetitions
are not. Every result in a selected directory is validated, including its control arm. Schema
and skill-invocation diagnostics are excluded from quality even in plugin-only runs, where the
native CLI includes them in its raw score. Do not use that raw aggregate as a comparable score.

Extraction selects one named grader's evidence and records its source and run identity. It
accepts training cases only and requires a fresh destination. Missing evidence fails; it never
substitutes a different grader's evidence or recovers HTML (HyperText Markup Language) report rows by position. A missing requested
output artifact is a legitimate behavioral FAIL when the native error names that exact case and
path. Unreadable files, other grader errors, absent evidence for extraction, and truncated runs
remain invalid measurements.

## What the evidence can establish

| Native selector | Visible evidence | Boundary |
|---|---|---|
| `focus: {source: file, path: ...}` | Final contents of that file | Includes modified scaffold files; a missing required artifact fails |
| `focus: trace` on LLM graders | First and last 12 messages | Cannot establish absence or successful action in an unseen middle |
| `target: trace` on regex graders | Complete serialized trace | Establishes only the literal pattern checked |
| `tool_used` / `tool_order` | Actual calls and matching inputs | Tool use alone does not establish a useful result |
| `files` / `file_exists` | Newly created paths relative to the work directory | No file contents, modified paths, or deleted paths |
| Generated `state-*` checks | Exact final fixture contents plus allowed new paths | Any tool's persistent edits are covered; transient edits, modes, and files outside the work directory are not |

Cases 18 and 62 require visible action evidence as well as an actual tool call. An action outside
the LLM trace excerpt may fail for insufficient evidence; inspect that failure before tuning the
skill. Case 62 separately judges whether the visible handoff carries both prices and the retained
owner boundary. This is semantic evidence from the excerpt, not complete visibility of every delegation.
Case 46 checks references to the two seeded log filenames across the full trace and checks the
answer for contamination; it does not establish that no home-directory listing occurred.
Cases 67/68 measure research planning, not completed source retrieval. Interactive cases use
quoted history in a single turn. Define's fresh-context review remains a separate paid drive.
These limits should bound claims, not become unobserved PASS assumptions.

## Audit dispositions

The current case and classification tables remain the complete inventory. Every case was read;
unchanged cases retain their stated purpose pending fresh measurement. The repairs below resolve
the confirmed defects without changing the skill being measured.

| Surface | Resolution |
|---|---|
| Native schema and launch | Replace seven invalid file focuses (one retired with d19); native zero-cost parse plus JavaScript regex compilation precedes spending |
| Scoring and extraction | Freeze launch contracts; reject missing/mismatched evidence; exclude diagnostics; remove unsafe HTML recovery |
| 08, 23, 24, 84 | Grade actual decision/glossary contents; reserve known architecture decision record (ADR) output paths; check restatus and index; preserve old decision bodies; protect attribution and reject other new ADRs in 24 |
| 10, 11, 14, 15, 16 | Invoke the autonomous mode that their graders already required |
| 13 | Treat propagation as a hypothesis; require a discriminating check instead of unsupported causal certainty |
| 17, 18, 25, 27, 28, 52, d16, d17 | Replace selective tool/file guards with generated final-state checks; seed a real preference file for Taste cases |
| 18, 62 | Require actual experiment/delegation evidence; expose Agent in 62 and preserve the owner's third-price/contact/submission limits in the handoff |
| 21, 22, 34 | Require an exercisable verification path, distinct design options or a load-bearing unknown, and stale-result handling |
| 31 | Consolidate its separate Enforced-by verdict into 23's existing ADR transaction, saving two agent trials |
| 46, 85 | Replace unsupported whole-trace absence claims with full-trace literal checks or final-answer judgments and state their limits |
| 56, 60 | Accept the cheapest adequate order/protocol check rather than requiring a named exhaustive method |
| 65, 66 | Remove answer cues; give each PRODUCT probe its own verdict on the same generated trajectory |
| 77, 80 | Require benchmark sensitivity, frozen setup, and repetition discipline; distinguish unattended design choices from actual user approval |
| Shared define graders | Compare explicit original requirements, including total omissions; reject invented unreachable targets and impossible gates hidden behind BLOCKED or a named check |
| Ceiling diagnostic | Generate the complete whitespace-normalized canonical invariant; deletion and changed-body mutants fail |
| d05, d06, d07, d09, d10 | Permit an honest blocker without a spec; preserve owner constraints, full subjective anchors, the no-problem stop, amendment frame, and explicit absolutes |
| d19 | Retire the execution/code-review duty from this spec suite; the ADR states that its review-code behavior check remains to be added |
| d20, d21 | Use real CLI behavior and meaningful baseline checks; permit verification-first and justified small designs in d20; reproduce the actual renewal duplicate in d21 |
| d25, d27 | Unknown agent-chosen targets stay advisory; add an explicit user target as the held-out mirror; fix the separate drive's stale oracle |

Keep the positive/negative mirrors (04/05, 08/17, 27/28, 37/39, 40/42, 63/64 and the define
negative guards). Cases 20/29 and d02/d03 are retirement candidates after repeated fresh evidence,
not deletions justified by old scores. Case 30 covers an update offer, not full setup migration;
53 covers the one-version boundary. Current hole-search calibration and unseen transfer cases
remain future measurement work, not a claim that this instrument proves generalization.

## Calibration and free verification

`tests/test_eval_contract.py` uses a literal native-derived serialization fixture independent of
the inventory. Regression tests reject incomplete reports and extraction mixups. Fixture tests
execute d20/d21 and break their baseline behavior to show the checks can fail. Final-state tests
use a Python writer to bypass Write/Edit guards and mutate every protected fixture file.
`sync_graders.py --check` detects stale snapshots and canonical-ceiling copies.

[Judge calibration examples](judge-calibration.json) retain small expected PASS/FAIL examples for
the shared semantics and repaired requirements. They are review fixtures, not measured judge
agreement. Before a paid hill-climb, give the chosen judge only each grader and its `evidence` field, keeping `expected` and `reason`
separate for comparison. Inspect
both false passes and false failures, then inspect generated failing traces. Do not change the
skill and its measuring rubric in the same comparison. A static test cannot certify an LLM judge.

Run the free `eval-tooling` and `property-suite` recipes. Paid baseline, generated-trace judge
calibration, and hill-climbing are explicitly deferred. No present result supports an uplift or
cost-saving claim beyond the removed redundant agent trials.
