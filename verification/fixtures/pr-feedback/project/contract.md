# Order export contract

`export_order(order)` returns the order identifier unchanged, the sum of quantity times unit
price for every line, and the line SKUs in input order. Identifiers are strings.
Internal `private_note` values are excluded. No tax or currency conversion is part of this export.

The requested change is this export behavior. Naming and equivalent expression choices are
ordinary implementation choices; there is no prescribed helper count or naming scheme.
