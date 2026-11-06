"""Realism review: every preset, several seeds, ten simulated minutes each, scored 0-100.

A viewer sees motion, so the score reads the motion: sudden changes in deceleration (jerk),
harsh braking, cars that snap from moving to stopped, collisions, and lane changes that happen in
a single frame, and traffic that barely moves. It also reports the worst frame time per preset against the 20 ms budget.
"""

import statistics
import time

from sim.presets import PRESETS
from sim.vehicle import CAR_LENGTH
from sim.world import DT, World

SECONDS = 600
SEEDS = (1, 2, 3)


def score_run(preset_name: str, seed: int) -> tuple[float, float]:
    preset = PRESETS[preset_name]
    world = World(preset, seed)
    prev_v = [car.v for car in world.cars]
    prev_a = [0.0] * len(world.cars)
    prev_lane = [car.lane for car in world.cars]
    harsh = jerky = snaps = crashes = teleports = samples = 0
    distance = 0.0
    worst_frame = 0.0
    for _ in range(int(SECONDS / DT)):
        start = time.perf_counter()
        world.step()
        worst_frame = max(worst_frame, time.perf_counter() - start)
        lanes: dict[int, list[float]] = {}
        for i, car in enumerate(world.cars):
            a = (car.v - prev_v[i]) / DT
            if a < -6.0:
                harsh += 1
            if abs(a - prev_a[i]) / DT > 15.0:
                jerky += 1
            if prev_v[i] > 3.0 and car.v == 0.0:
                snaps += 1
            if car.lane != prev_lane[i]:
                teleports += 1
            distance += car.v * DT
            prev_v[i], prev_a[i], prev_lane[i] = car.v, a, car.lane
            lanes.setdefault(car.lane, []).append(car.x)
            samples += 1
        for xs in lanes.values():
            xs.sort()
            crashes += sum(1 for p, q in zip(xs, xs[1:]) if q - p < CAR_LENGTH * 0.5)
    rate = samples / 1000
    penalty = (harsh + jerky + 20 * snaps + 50 * crashes + 200 * teleports) / rate
    mean_speed = distance / (samples * DT)
    flow = min(1.0, mean_speed / 4.0)
    return 100.0 * flow / (1.0 + penalty / 25.0), worst_frame * 1000


def main() -> None:
    overall = []
    for name in PRESETS:
        scores, frames = zip(*(score_run(name, seed) for seed in SEEDS))
        overall.append(statistics.mean(scores))
        print(
            f"{name}: realism={statistics.mean(scores):.1f} "
            f"(seeds {' '.join(f'{s:.1f}' for s in scores)}) worst_frame_ms={max(frames):.1f}"
        )
    print(f"overall_realism={statistics.mean(overall):.1f}")


if __name__ == "__main__":
    main()
