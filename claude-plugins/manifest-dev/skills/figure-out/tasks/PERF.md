# PERF — probing fuel

Angles that are easy to under-weight when a number — latency, throughput, memory, cost — is the point. Considerations, not an agenda. Press the load-bearing ones; priority stays yours.

## Blind-spot probes
- **The limiter** — What bounds this number: a core, a lock, the disk, the network, the load generator itself? If you can't say why it isn't twice as good, what was measured?
- **Noise floor** — How large is the run-to-run variation, and is the difference bigger than it?
- **A fair comparison** — Were both sides tuned, run alternately, on the same inputs?
- **The harness first** — Can the measuring harness tell a known-slow case from a known-fast one before it is trusted, and is it frozen before the attempts start?
- **Unlike scenarios** — Does any ratio compare two different scenarios?

## Forced trade-offs
- End-to-end vs isolated measurement — which number does the person waiting actually feel?
