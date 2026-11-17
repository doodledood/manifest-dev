"""Stock report for a small shop's shelf list."""


def low_stock(items, threshold):
    """Names of items whose quantity is below the threshold, sorted by name."""
    return sorted(item["name"] for item in items if item["qty"] < threshold)
