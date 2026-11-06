"""Unit lookup for the import screen."""

_FACTORS = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0, "in": 0.0254, "ft": 0.3048}


def to_metres(value: float, unit: str) -> float:
    """Convert a length to metres; raises KeyError for an unknown unit."""
    return value * _FACTORS[unit]
