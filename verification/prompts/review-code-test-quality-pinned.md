Caller acceptance policy: no Medium-or-higher findings for the requested review gate.

First, in this repository, commit a file `invoice.py` to the default branch containing:

class Invoice:
    def __init__(self, lines):
        self.lines = lines

    def _subtotal(self):
        return sum(qty * price for qty, price in self.lines)

    def _tax(self, amount):
        return round(amount * 0.2, 2)

    def total(self):
        subtotal = self._subtotal()
        return subtotal + self._tax(subtotal)

Then create a branch `feature/invoice-tests` and commit a file `test_invoice.py` containing:

from unittest import mock
from invoice import Invoice


def test_total_computes_subtotal_then_tax():
    invoice = Invoice([(2, 10.0)])
    with mock.patch.object(Invoice, "_subtotal", wraps=invoice._subtotal) as subtotal, \
         mock.patch.object(Invoice, "_tax", wraps=invoice._tax) as tax:
        manager = mock.Mock()
        manager.attach_mock(subtotal, "subtotal")
        manager.attach_mock(tax, "tax")
        invoice.total()
    assert manager.mock_calls == [mock.call.subtotal(), mock.call.tax(20.0)]

Then run /manifest-dev:review-code test-quality on that branch's change against the default branch.
