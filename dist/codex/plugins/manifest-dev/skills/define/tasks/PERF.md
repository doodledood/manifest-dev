# PERF Task Guidance

Work whose point is a number — latency, throughput, memory, cost — or that claims to move one.
Composes onto `MEASURE.md`, and onto `CODING.md` when code changes.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Verdict | The result is stated as faster, slower, no measurable difference, or inconclusive, with the run count, the range, and what limits the number; inconclusive when the limiter cannot be named or a side ran untuned |

Encode the verdict as a judgment gate whose body names the measurement the change is judged by
and the evidence the verdict cites.

## Defaults

*Domain best practices for this task type.*

- **Name the limiter** — Ask "why not double?": name the resource or code path that bounds the number, from a profile or counters taken during a run, not from reading code
- **Bound the gain by the changed piece's share** — A change can save at most the share of the whole that the changed piece took before it; treat a claimed gain beyond that share as a measurement fault until something else that changed explains it
