---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

this is the function that prices every order in our shop. checkout calls it and so does the monthly invoice export that finance sends to the accountants, about 3k orders a day. there are no tests for it. the guy who wrote it left last year.

```python
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_HALF_UP

TAX_RATES = {"US": Decimal("0.08"), "CA": Decimal("0.13"), "DE": Decimal("0.19")}
CENT = Decimal("0.01")

def compute_total(order, customer):
    if customer.type == "partner":
        return order.subtotal
    subtotal = Decimal("0")
    for line in order.lines:
        price = line.unit_price * line.qty
        if line.qty >= 10:
            price = price * Decimal("0.95")
        subtotal += price
    if customer.type == "wholesale":
        subtotal = subtotal * Decimal("0.90")
    fee = Decimal("0")
    if subtotal < Decimal("50"):
        fee = Decimal("4.99")
    # per finance, do not change
    subtotal = subtotal.quantize(CENT, rounding=ROUND_HALF_DOWN)
    rate = TAX_RATES.get(customer.country, Decimal("0"))
    tax = (subtotal * rate).quantize(CENT, rounding=ROUND_HALF_UP)
    return subtotal + tax + fee
```

make it cleaner, split it into smaller functions, the rounding thing looks like a bug since everything else we have rounds half-up, fix that too. figure out how we should do this so we can hand it to /define next. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
