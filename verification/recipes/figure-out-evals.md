---
kind: eval
covers: claude-plugins/manifest-dev/skills/figure-out, claude-plugins/manifest-dev/evals
ask-first: a full suite runs many agent sessions with and without the plugin, which uses a lot of model quota
---
# figure-out behavior suite

Measures whether `figure-out` delivers the discipline its own prompt states, as uplift: every case
runs with the plugin and without it, and the headline number is Δ, not the pass rate. Case
statuses — unmeasured, measured with a date, or stale — and the baseline, the held-out split and
the run-to-run noise live in `claude-plugins/manifest-dev/evals/README.md`; this recipe starts the
suite and does not redefine them.

## How a user reaches it

- `claude-plugins/manifest-dev/evals/README.md` → *Scope and statuses*, *Cases*, *Running a
  suite* and *Recording a baseline*; `scripts/evals/run_eval.sh` starts every run, locally or in
  a cloud session.
- `claude-plugins/manifest-dev/evals/README.md` → *Hill-climbing a prompt against a suite*, with
  the scripts under `scripts/evals/`.

## Scenarios

### with-without
Run: `scripts/evals/run_eval.sh --wait figure-out-with-without evals/results/figure-out-with-without/aggregate-result.json --tag figure-out --ablation with-without --judge-model sonnet --scaffold --max-cost-usd 205`
Proves: the suite ran both arms; the Δ it reports, read against the noise section of the suite README, is the measurement, and the README's results section records it.
Check: read
Workload: varies

### plugin-only
Run: `scripts/evals/run_eval.sh --wait figure-out-plugin-only evals/results/figure-out-plugin-only/aggregate-result.json --tag figure-out-plugin-only --ablation none --judge-model sonnet --scaffold --max-cost-usd 15`
Proves: the cases that test behavior existing only with the plugin pass on the plugin arm.
Check: read
Workload: varies

## Gotchas

- Read the suite README's noise section before using a Δ to justify a prompt change; saturated non-guards are retirement candidates after repeated evidence; meaningful negative guards stay.
- `--scaffold` is required, and `run_eval.sh` always passes `--allow-tools Write Edit Bash Agent`; without them file graders fail in both arms and scaffolded cases run against an empty directory.
- Judge with `sonnet` at one run per arm, as the suite README says, and read a result as its *Reading a result at this depth* says; numbers judged by different models do not compare.
- `--max-cost-usd` stops new scheduling; up to eight in-flight trials can finish above it. A cut-short result exits 2 and is rejected by the scorer.
- On macOS each eval child may raise a keychain dialog; run suites in a cloud session where you can.
- `tests/test_eval_cases.py` fails when a case directory and the README's case table disagree.
