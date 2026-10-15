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

- `claude-plugins/manifest-dev/evals/define/README.md`; on macOS, `scripts/evals/run_eval.sh` runs
  the same command in the eval container.

## Scenarios

### with-without
Run: `cd claude-plugins/manifest-dev && claude plugin eval . --tag define --ablation with-without --judge-model opus --allow-tools Write Bash --scaffold -j 8`
Proves: the suite ran both arms; the Δ it reports, read against the suite README's noise, is the measurement, and the README records it.
Check: read
Workload: varies

## Gotchas

- Read `claude-plugins/manifest-dev/evals/README.md` on noise before trusting a Δ from this suite.
- `--allow-tools Write Bash` and `--scaffold` are required, as for the figure-out suite.
- On macOS run it inside the container (`scripts/evals/run_eval.sh`).
