# MEASURE — probing fuel

Angles that are easy to under-weight whenever a measured comparison decides something: a number, a suite's pass rate, or a verdict between two versions. `PERF.md` and `HILLCLIMB.md` compose onto it. Considerations, not an agenda. Press the load-bearing ones; priority stays yours.

## Blind-spot probes
- **The measure first** — Can the measure tell a known-worse case from a known-better one before it is trusted, and is it frozen, with its inputs and setup, before the attempts start?
- **Noise floor** — How large is the run-to-run variation, and is the difference bigger than it? If not, it is no measurable difference.
- **A fair comparison** — Were both sides tuned, run alternately, on the same inputs?
- **Unlike scenarios** — Does any ratio compare two different scenarios?
- **A floor on attempts** — Is the number of runs fixed before the result is read, so an early lucky win can't end the comparison?
