"""One car and how it follows the car ahead."""

from dataclasses import dataclass

MAX_SPEED = 14.0  # m/s
ACCEL = 1.5  # m/s^2
COMFORT_DECEL = 2.0  # m/s^2
MIN_GAP = 2.0  # m
HEADWAY = 1.5  # s
CAR_LENGTH = 4.5  # m


@dataclass
class Car:
    x: float
    lane: int
    v: float = 0.0
    a: float = 0.0


def follow(car: Car, gap: float, lead_speed: float, dt: float) -> None:
    """Advance one car one frame given the free gap to whatever is ahead."""
    desired_gap = MIN_GAP + car.v * HEADWAY
    if gap < desired_gap:
        # Too close: stop dead this frame.
        car.v = min(car.v, lead_speed) if gap > MIN_GAP else 0.0
        car.a = 0.0
    else:
        car.a = ACCEL * (1 - (car.v / MAX_SPEED) ** 4)
        car.v = min(MAX_SPEED, car.v + car.a * dt)
    car.x += car.v * dt
