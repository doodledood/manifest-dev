# PERF — probing fuel

Angles that are easy to under-weight when a number — latency, throughput, memory, cost — is the point. Composes onto `MEASURE.md`, which carries the measuring probes. Considerations, not an agenda. Press the load-bearing ones; priority stays yours.

## Blind-spot probes
- **The limiter** — What bounds this number: a core, a lock, the disk, the network, the load generator itself? If you can't say why it isn't twice as good, what was measured?
- **A bounded gain** — Is the claimed gain within what the changed piece could save — its share of the whole before the change? A gain beyond that share is a measurement fault until something else that changed explains it.
- **The verdict** — Will the result be stated as faster, slower, no measurable difference, or inconclusive, with the run count, the range and the limiter — inconclusive when the limiter can't be named or one side ran without the setup, warm-up or configuration the other had?

## Forced trade-offs
- End-to-end vs isolated measurement — which number does the person waiting actually feel?
