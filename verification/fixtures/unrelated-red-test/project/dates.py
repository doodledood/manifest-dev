"""Date helpers for the publishing calendar."""

from datetime import date


def days_between(start, end):
    """Return the number of days from start to end, counting both days."""
    return (end - start).days
