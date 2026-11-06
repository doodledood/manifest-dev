"""The world: cars on lanes of a ring road, lights and merges."""

import random

from sim.lights import is_red
from sim.presets import Preset
from sim.vehicle import CAR_LENGTH, Car, follow

DT = 1 / 30


class World:
    def __init__(self, preset: Preset, seed: int = 0) -> None:
        self.preset = preset
        self.time = 0.0
        rng = random.Random(seed)
        self.cars: list[Car] = []
        for lane in range(preset.lanes):
            spacing = preset.road_length / preset.cars_per_lane
            for i in range(preset.cars_per_lane):
                jitter = rng.uniform(-0.2, 0.2) * spacing
                self.cars.append(Car(x=(i * spacing + jitter) % preset.road_length, lane=lane))

    def _ahead(self, car: Car, lane_cars: list[Car]) -> tuple[float, float]:
        length = self.preset.road_length
        best_gap, best_speed = length, car.v
        for other in lane_cars:
            if other is car:
                continue
            gap = (other.x - car.x) % length - CAR_LENGTH
            if 0 <= gap < best_gap:
                best_gap, best_speed = gap, other.v
        for index, line in enumerate(self.preset.lights):
            if is_red(self.time, self.preset.light_cycle, index):
                gap = (line - car.x) % length
                if gap < best_gap:
                    best_gap, best_speed = gap, 0.0
        return best_gap, best_speed

    def step(self) -> None:
        by_lane: dict[int, list[Car]] = {}
        for car in self.cars:
            by_lane.setdefault(car.lane, []).append(car)
        for car in self.cars:
            gap, lead_speed = self._ahead(car, by_lane[car.lane])
            follow(car, gap, lead_speed, DT)
            car.x %= self.preset.road_length
        merge = self.preset.merge_at
        if merge is not None:
            for car in self.cars:
                if car.lane == 1 and abs(car.x - merge) < 5:
                    car.lane = 0  # moves across in one frame
        self.time += DT

    def frame(self) -> list[tuple[int, float]]:
        """What a viewer sees this frame: each car's lane and position."""
        return [(car.lane, car.x) for car in self.cars]
