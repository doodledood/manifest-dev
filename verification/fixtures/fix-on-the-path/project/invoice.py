"""Invoice helpers. Amounts are integer cents."""


def line_total(quantity, unit_cents):
    """Return the total of one invoice line, in cents."""
    return quantity * unit_cents


def format_money(cents):
    """Return cents as a dollar string, such as $12.05."""
    return f"${cents // 100}.{cents % 100}"


def receipt_line(name, quantity, unit_cents):
    """Return one printed receipt line."""
    return f"{name} x{quantity}: {format_money(line_total(quantity, unit_cents))}"
