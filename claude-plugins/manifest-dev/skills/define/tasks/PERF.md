# PERF Task Guidance

Work whose point is a number — latency, throughput, memory, cost — or that claims to move one.
Composes onto `CODING.md` when code changes.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Verdict | The result is stated as faster, slower, no measurable difference, or inconclusive, with the run count, the range, and what limits the number; inconclusive when the limiter cannot be named or a side ran untuned |

Encode the verdict as a judgment gate whose body names the measurement the change is judged by
and the evidence the verdict cites.

## Defaults

*Domain best practices for this task type.*

- **Name the limiter** — Ask "why not double?": name the resource or code path that bounds the number, from a profile or counters taken during a run, not from reading code
- **Respect the noise floor** — A gap smaller than the run-to-run variation is no measurable difference; measure the variation before claiming one
- **Compare fairly** — Tune both sides, run them alternately on the same inputs, and count errors and work done alongside time
- **Prove the harness, then freeze it** — Show the measuring harness can tell a known-slow case from a known-fast one before trusting it, freeze it before the attempts start, and set a floor on attempts so an early lucky win cannot end the run
- **No ratio across unlike scenarios** — Compare a number only with the same scenario measured the same way
