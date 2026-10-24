---
kind: suite
covers: scripts/evals, claude-plugins/manifest-dev/evals, tests/test_eval_cases.py, tests/test_eval_contract.py, tests/test_eval_outcomes.py, tests/test_eval_shared_graders.py, tests/test_figure_out_coverage.py, tests/eval_result_fixtures.py, tests/native_eval_fixture.py, tests/test_score_rounds.py, tests/test_extract_outputs.py, tests/test_drive_scripts.py
---
# Eval tooling and fixtures

Free checks for the Claude Code measurement path. Behavioral model quality still needs the
separate ask-first eval recipes. Native preflight uses a zero-dollar ceiling and disables
scaffolds; it launches no agent or judge. Run with the repository virtual environment active.

## How a user reaches it

- `claude-plugins/manifest-dev/evals/READINESS.md` gives preflight, validation, extraction and comparison commands.

## Scenarios

### regression
Run: `python3 -m pytest tests/test_eval_cases.py tests/test_eval_shared_graders.py tests/test_figure_out_coverage.py tests/test_eval_contract.py tests/test_eval_outcomes.py tests/test_score_rounds.py tests/test_extract_outputs.py tests/test_drive_scripts.py -q`
Proves: invalid or incomplete results fail, native normalization matches an independent fixture, extraction keeps run/source identity, protected final files reject any writer, scaffolds execute and case documentation stays synchronized.
Workload: varies

### figure-out-preflight
Run: `scripts/evals/run_eval.sh --preflight tooling-figure-out evals/results/tooling/figure-out.json --tag figure-out --ablation with-without --judge-model sonnet --scaffold --max-cost-usd 205`
Proves: the selected both-arm figure-out instrument parses natively and its regexes compile before any paid launch; inventory prints the workload.
Workload: varies

### guard-preflight
Run: `scripts/evals/run_eval.sh --preflight tooling-guards evals/results/tooling/guards.json --tag figure-out-plugin-only --ablation none --judge-model sonnet --scaffold --max-cost-usd 15`
Proves: the plugin-only guard instrument is valid without model calls.
Workload: varies

### define-preflight
Run: `scripts/evals/run_eval.sh --preflight tooling-define evals/results/tooling/define.json --tag define --ablation with-without --judge-model sonnet --scaffold --max-cost-usd 65`
Proves: every selected define case and its artifact selectors load before spending.
Workload: varies
