First, in this repository, commit to the default branch a file `pricing.py` containing:

def unit_price(total, count):
    """Return the price of one unit."""
    return total / count


def apply_discount(price, percent):
    """Return price after a percent discount (0-100)."""
    return price - price * percent / 100

Then create a branch `feature/discount-cap` and change only `apply_discount` there so that it
caps `percent` at 100 before applying it, and commit.

Then run /manifest-dev:review-code code-bugs on that branch's change against the default branch,
and ask it for the Pre-existing list.
