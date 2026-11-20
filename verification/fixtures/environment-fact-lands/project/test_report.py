import unittest

from report import all_items, connect


class ReportTest(unittest.TestCase):
    def test_all_items_sorted_by_name(self):
        names = [name for name, _ in all_items(connect())]
        self.assertEqual(names, sorted(names))


if __name__ == "__main__":
    unittest.main()
