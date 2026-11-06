"""Quick check: one still frame of the grid preset at 30 s, checked for spacing and positions."""

from sim.presets import PRESETS
from sim.vehicle import CAR_LENGTH
from sim.world import World


def main() -> None:
    preset = PRESETS["grid"]
    world = World(preset, seed=1)
    for _ in range(30 * 30):
        world.step()
    problems = 0
    lanes: dict[int, list[float]] = {}
    for lane, x in world.frame():
        if not 0 <= x < preset.road_length or not 0 <= lane < preset.lanes:
            problems += 1
        lanes.setdefault(lane, []).append(x)
    for xs in lanes.values():
        xs.sort()
        for a, b in zip(xs, xs[1:]):
            if b - a < CAR_LENGTH:
                problems += 1
        if len(xs) > 1 and xs[0] + preset.road_length - xs[-1] < CAR_LENGTH:
            problems += 1
    print(f"quick_check={'PASS' if problems == 0 else 'FAIL'} problems={problems}")


if __name__ == "__main__":
    main()
