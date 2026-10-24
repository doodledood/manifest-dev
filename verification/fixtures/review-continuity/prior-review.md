# Prior change-intent review

The first full review assessed `order_export.py` against `contract.md`.

- F1: The export includes internal `private_note` data. The contract excludes that field.
- F2: The total omits the last line. A one-line order therefore returns zero instead of its line price.

Verdict: FAIL. Neither repair has been verified.
