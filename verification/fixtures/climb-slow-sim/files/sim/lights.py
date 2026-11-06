"""Traffic lights on a fixed cycle."""


def is_red(time: float, cycle: float, index: int) -> bool:
    phase = (time + index * cycle / 2) % (2 * cycle)
    return phase >= cycle
