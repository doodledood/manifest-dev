import unittest

from inventory import low_stock


class LowStockTest(unittest.TestCase):
    def test_reports_items_below_threshold(self):
        items = [
            {"name": "tea", "qty": 1},
            {"name": "jam", "qty": 9},
            {"name": "bread", "qty": 2},
        ]
        self.assertEqual(set(low_stock(items, 3)), {"tea", "bread"})


if __name__ == "__main__":
    unittest.main()
