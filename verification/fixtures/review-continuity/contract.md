# Order export contract

`export_order(order)` returns the order identifier unchanged, the total price of all lines,
and the line SKUs in input order. An identifier is a string and can have leading zeros.
Each line has `sku`, `quantity`, and `unit_price`. An empty order has a total of zero.
Internal `private_note` values must never enter the export.
