# PERF — probing fuel

Angles that are easy to under-weight when a number — latency, throughput, memory, cost — is the point. Considerations, not an agenda. Press the load-bearing ones; priority stays yours.

## Blind-spot probes
- **The limiter** — What bounds this number: a core, a lock, the disk, the network, the load generator itself? If you can't say why it isn't twice as good, what was measured?
- **Noise floor** — How large is the run-to-run variation, and is the difference bigger than it? If not, it is no measurable difference.
- **A fair comparison** — Were both sides tuned, run alternately, on the same inputs?
- **The harness first** — Can the measuring harness tell a known-slow case from a known-fast one before it is trusted, is it frozen before the attempts start, and is there a floor on attempts so an early lucky win can't end the run?
- **Unlike scenarios** — Does any ratio compare two different scenarios?
- **The verdict** — Will the result be stated as faster, slower, no measurable difference, or inconclusive, with the run count, the range and the limiter — inconclusive when the limiter can't be named or a side ran untuned?

## Forced trade-offs
- End-to-end vs isolated measurement — which number does the person waiting actually feel?
