"""Benchmark top_words on a fixed corpus: median seconds over 5 runs, and peak memory in KiB."""

import random
import statistics
import time
import tracemalloc

from stats import top_words


def corpus() -> str:
    rng = random.Random(7)
    vocabulary = [f"w{i}" for i in range(3000)]
    return " ".join(rng.choice(vocabulary) for _ in range(40000))


def main() -> None:
    text = corpus()
    times = []
    for _ in range(5):
        start = time.perf_counter()
        top_words(text, 20)
        times.append(time.perf_counter() - start)
    tracemalloc.start()
    top_words(text, 20)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    print(f"median_seconds={statistics.median(times):.4f} peak_kib={peak / 1024:.0f}")


if __name__ == "__main__":
    main()
