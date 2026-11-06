"""The team's benchmark for slugify: one timed run on a shared CI machine, printed in ms.

The shared machine's load swings widely, which this script simulates so the drive is repeatable
offline: each run is scaled by a random factor between 0.3 and 3.
"""

import random
import time

from slugify import slugify


def main() -> None:
    titles = [f"Release notes for version {i}: what's new & fixed!" for i in range(20000)]
    start = time.perf_counter()
    for title in titles:
        slugify(title)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"ms={elapsed * random.uniform(0.3, 3.0):.1f}")


if __name__ == "__main__":
    main()
