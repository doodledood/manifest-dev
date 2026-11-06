"""City presets: ring roads with lights, and a merge."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    name: str
    road_length: float  # metres, a ring
    lanes: int
    cars_per_lane: int
    lights: tuple[float, ...] = ()  # stop-line positions
    light_cycle: float = 30.0  # seconds green, then the same red
    merge_at: float | None = None  # position where lane 1 ends and merges into lane 0


PRESETS = {
    "grid": Preset("grid", 1200.0, 2, 18, lights=(200.0, 500.0, 800.0, 1100.0)),
    "ring": Preset("ring", 900.0, 1, 30),
    "highway_merge": Preset("highway_merge", 2000.0, 2, 25, merge_at=1500.0),
    "rush_hour": Preset("rush_hour", 1500.0, 3, 40, lights=(300.0, 750.0, 1200.0), light_cycle=20.0),
}
