"""The team's benchmark for slugify: one timed run on a shared CI machine, printed in ms.

The shared machine stalls a run at random, which this script simulates so the drive is
repeatable offline: each timed run includes a stall of 20 to 200 ms, and slugify itself handles
only a handful of titles, so its own cost is a fraction of a millisecond of what is printed.
"""

import random
import time

from slugify import slugify


def main() -> None:
    titles = [f"Release notes for version {i}: what's new & fixed!" for i in range(50)]
    start = time.perf_counter()
    time.sleep(random.uniform(0.02, 0.2))
    for title in titles:
        slugify(title)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"ms={elapsed:.1f}")


if __name__ == "__main__":
    main()
