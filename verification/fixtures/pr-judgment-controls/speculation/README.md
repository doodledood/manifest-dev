# Meridian lookup service
Meridian serves repeat lookups of immutable public reference identifiers. Its goal is fast,
correct responses on a fixed server footprint. Cache values are integers. Inputs are bounded
integers, each lookup is deterministic, and the process has a 256 MiB memory budget.
