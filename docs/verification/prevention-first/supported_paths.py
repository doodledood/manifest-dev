import unittest

import owner
from additional import additional_order
from callers import batch, web


class SupportedPaths(unittest.TestCase):
    def test_invalid_never_changes_shipments(self):
        for call in (owner.send, web, batch, additional_order):
            for quantity in (-1, 0):
                with self.subTest(call=call.__name__, quantity=quantity):
                    owner.sent.clear()
                    with self.assertRaises(ValueError):
                        call(quantity)
                    self.assertEqual(owner.sent, [])

    def test_valid_shipments_still_work(self):
        for call in (owner.send, web, batch, additional_order):
            with self.subTest(call=call.__name__):
                owner.sent.clear()
                self.assertEqual(call(2), 2)
                self.assertEqual(owner.sent, [2])


if __name__ == "__main__":
    unittest.main()
