# MEASURE Task Guidance

Work that keeps or claims a result because it measured better: a number, a suite's pass rate, or
a verdict between two versions. `PERF.md` and `HILLCLIMB.md` compose onto it.

## Defaults

*Domain best practices for this task type.*

- **Prove the measure, then freeze it** — Before trusting a measure, show it can tell a known-worse case from a known-better one; then freeze it, with its inputs and setup, before the attempts start
- **Respect the noise floor** — A gap smaller than the run-to-run variation is no measurable difference; measure the variation before claiming one
- **Compare like with like** — Tune both sides, run them alternately on the same inputs, count errors and work done alongside the result, and compare a number only with the same scenario measured the same way
- **Set a floor on attempts** — Fix how many runs a comparison takes before reading its result, so an early lucky win cannot end it
