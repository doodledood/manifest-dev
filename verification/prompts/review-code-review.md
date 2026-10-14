First, in this repository, create a branch `feature/discount` and commit a file `discount.py` containing:

def apply_discount(price, percent):
    """Return price after a percent discount (0-100)."""
    return price - price * percent

Then run /manifest-dev:review-code code-bugs on that branch's change against the default branch.
