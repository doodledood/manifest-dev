---
kind: eval
covers: claude-plugins/manifest-dev/skills/define, claude-plugins/manifest-dev/evals/define
ask-first: a full suite runs many agent sessions with and without the plugin, which uses a lot of model quota
---
# define behavior suite

Measures `/define`'s uplift over the no-plugin baseline, case by case. Case statuses, the judge
model, the baseline and the noise live in `claude-plugins/manifest-dev/evals/define/README.md`;
this recipe starts the suite and does not redefine them.

## How a user reaches it

- `claude-plugins/manifest-dev/evals/define/README.md`; `scripts/evals/run_eval.sh` starts every
  run, locally or in a cloud session, as `claude-plugins/manifest-dev/evals/README.md` → *Running
  a suite* says.

## Scenarios

### with-without
Run: `scripts/evals/run_eval.sh --wait define-with-without evals/results/define-with-without/aggregate-result.json --tag define --ablation with-without --judge-model sonnet --scaffold --max-cost-usd 65`
Proves: the suite ran both arms; the Δ it reports, read against the suite README's noise, is the measurement, and the README records it.
Check: read

## Gotchas

- Read `claude-plugins/manifest-dev/evals/README.md` on noise before trusting a Δ from this suite.
- `--scaffold` is required, and `run_eval.sh` always passes `--allow-tools Write Edit Bash Agent`, as for the figure-out suite.
- `--max-cost-usd` stops new scheduling; up to eight in-flight trials can finish above it. A cut-short result exits 2 and is rejected by the scorer.
- On macOS each eval child may raise a keychain dialog; run suites in a cloud session where you can.
