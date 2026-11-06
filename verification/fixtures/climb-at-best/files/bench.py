"""Benchmark to_metres: median nanoseconds per call over 7 runs of 200,000 calls."""

import statistics
import time

from units import to_metres


def main() -> None:
    units = ["mm", "cm", "m", "km", "in", "ft"] * 33334
    runs = []
    for _ in range(7):
        start = time.perf_counter_ns()
        for unit in units:
            to_metres(3.0, unit)
        runs.append((time.perf_counter_ns() - start) / len(units))
    print(f"median_ns_per_call={statistics.median(runs):.1f} min={min(runs):.1f} max={max(runs):.1f}")


if __name__ == "__main__":
    main()
