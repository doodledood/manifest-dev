# Order export

The export is a projection of an order, not a new identifier scheme. Keep the identifier
as the original string, including leading zeroes. Keep line items in input order. Include
only the public identifier, item SKUs, and total; private notes stay out. The total is the
sum of quantity times unit price. An order with no lines has a total of zero.
