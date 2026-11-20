"""Money helpers. Every amount is a whole number of cents, as an int."""


def line_total(quantity, unit_cents):
    """Return the total of one line, in cents."""
    return quantity * unit_cents


def apply_discount(cents, percent):
    """Return cents after a percent discount, rounded down to a whole cent."""
    return cents * (100 - percent) // 100
