"""Realism review: every preset, several seeds, ten simulated minutes each, scored 0-100.

A viewer sees motion, so the score reads the motion: sudden changes in deceleration (jerk),
harsh braking, cars that snap from moving to stopped, collisions, cars that jump sideways in a single
frame, and traffic that barely moves; a run in which any car drives on past the end of a lane that
ends instead of merging scores 0. It also reports each preset's 99th-percentile frame time
against the 20 ms budget: a percentile rather than the single worst frame, since one stall from a
busy machine says nothing about the simulation.
"""

import statistics
import time

from sim.presets import PRESETS
from sim.vehicle import CAR_LENGTH

JUMP = 0.5  # metres sideways in one frame that a viewer sees as a jump
from sim.world import DT, World

SECONDS = 600
SEEDS = (1, 2, 3)


def score_run(preset_name: str, seed: int) -> tuple[float, float]:
    preset = PRESETS[preset_name]
    world = World(preset, seed)
    prev_v = [car.v for car in world.cars]
    prev_a = [0.0] * len(world.cars)
    prev_y = [car.y for car in world.cars]
    prev_x = [car.x for car in world.cars]
    harsh = jerky = snaps = crashes = teleports = overruns = samples = 0
    distance = 0.0
    frame_times: list[float] = []
    merge = preset.merge_at
    for _ in range(int(SECONDS / DT)):
        start = time.perf_counter()
        world.step()
        frame_times.append(time.perf_counter() - start)
        lanes: dict[int, list[float]] = {}
        for i, car in enumerate(world.cars):
            a = (car.v - prev_v[i]) / DT
            if a < -6.0:
                harsh += 1
            if abs(a - prev_a[i]) / DT > 15.0:
                jerky += 1
            if prev_v[i] > 3.0 and car.v == 0.0:
                snaps += 1
            if abs(car.y - prev_y[i]) > JUMP:
                teleports += 1
            if merge is not None and car.lane == 1 and prev_x[i] < merge <= car.x:
                overruns += 1
            distance += car.v * DT
            prev_v[i], prev_a[i], prev_y[i], prev_x[i] = car.v, a, car.y, car.x
            lanes.setdefault(car.lane, []).append(car.x)
            samples += 1
        for xs in lanes.values():
            xs.sort()
            crashes += sum(1 for p, q in zip(xs, xs[1:]) if q - p < CAR_LENGTH * 0.5)
            if len(xs) > 1 and xs[0] + preset.road_length - xs[-1] < CAR_LENGTH * 0.5:
                crashes += 1
    rate = samples / 1000
    penalty = (harsh + jerky + 20 * snaps + 50 * crashes + 200 * teleports) / rate
    mean_speed = distance / (samples * DT)
    flow = min(1.0, mean_speed / 4.0)
    p99_frame = statistics.quantiles(frame_times, n=100)[98]
    # A car that drives on past the end of its lane is not traffic at all, so the run scores 0.
    realism = 0.0 if overruns else 100.0 * flow / (1.0 + penalty / 25.0)
    return realism, p99_frame * 1000


def main() -> None:
    overall = []
    for name in PRESETS:
        scores, frames = zip(*(score_run(name, seed) for seed in SEEDS))
        overall.append(statistics.mean(scores))
        print(
            f"{name}: realism={statistics.mean(scores):.1f} "
            f"(seeds {' '.join(f'{s:.1f}' for s in scores)}) p99_frame_ms={max(frames):.1f}"
        )
    print(f"overall_realism={statistics.mean(overall):.1f}")


if __name__ == "__main__":
    main()
